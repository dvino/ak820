"""Small Windows GUI for the shared installer; importing this module opens no USB."""
from __future__ import annotations

import contextlib
import queue
import threading
from datetime import datetime
from pathlib import Path

import ak820
from i18n import (LanguageSession, localize_output, localize_prompt,
                  needs_unlock_dialog, progress_text, text as tr)


def backup_destination(parent_dir, timestamp=None):
    """Return a unique new child directory, as required by the backup writer."""
    timestamp = timestamp or datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    return str(Path(parent_dir) / ('ak820-settings-' + timestamp))


def backup_args(session_dir, output_dir):
    """Build the read-only settings export command for the selected destination."""
    return ['backup', '--session', str(session_dir), '--output', str(output_dir)]


def restore_args(session_dir, backup_dir):
    """Build an explicit settings restore command for the selected backup."""
    return ['restore', '--session', str(session_dir), '--backup', str(backup_dir)]


def update_args(session_dir, backup_dir):
    """Build the protected OEM-session update command and its fresh-backup target."""
    return ['update', '--session', str(session_dir), '--backup-dir', str(backup_dir)]


def is_yes_confirmation(message):
    """Only the backend's explicit yes confirmation gets the highlighted word."""
    return message.endswith(('\nВведите yes (Enter — отмена): ', '\nType yes (Enter to cancel): '))


def build_yes_body(parent, message, language='ru'):
    import tkinter as tk
    from tkinter import ttk
    ttk.Label(parent, text=tr('yes_entry_label', language)).pack(anchor='w')
    ttk.Label(parent, text='yes', font=('', 20, 'bold')).pack(anchor='w', pady=(4, 6))
    entry = ttk.Entry(parent, width=35)
    entry.pack(fill='x', pady=(0, 12))
    ttk.Label(parent, text=message, wraplength=620, justify=tk.LEFT).pack(anchor='w')
    return entry


def ask_yes_confirmation(parent, message, language='ru'):
    import tkinter as tk
    from tkinter import simpledialog, ttk
    class Confirmation(simpledialog.Dialog):
        def body(self, master):
            self.entry = build_yes_body(master, message, language)
            return self.entry  # Dialog focuses the empty field; nothing is prefilled.

        def buttonbox(self):
            box = ttk.Frame(self)
            ttk.Button(box, text=tr('yes_confirm', language), command=self.ok).pack(side=tk.LEFT, padx=5, pady=5)
            ttk.Button(box, text=tr('cancel', language), command=self.cancel).pack(side=tk.LEFT, padx=5, pady=5)
            box.pack()
            self.bind('<Return>', self.ok)
            self.bind('<Escape>', self.cancel)

        def apply(self):
            self.result = self.entry.get()
    return Confirmation(parent, title=tr('yes_title', language)).result


class Controller:
    """One worker, queued messages, and explicit responses from the UI thread."""
    def __init__(self, runner=ak820.main, language=None):
        self.runner = runner
        self.language = LanguageSession(language)
        self.events = queue.Queue()
        self.busy = False
        self._answer = threading.Event()
        self._response = ''
        self.cancel_event = threading.Event()
        self.worker = None

    def progress(self, kind, message):
        self.events.put(('progress', (kind, message)))

    def set_language(self, language):
        self.language.language = language

    def cancel_wait(self):
        self.cancel_event.set()

    def write(self, text):
        if text:
            self.events.put(('output', localize_output(text, self.language.language)))
        return len(text)

    def flush(self):
        pass

    def prompt(self, message):
        self._answer.clear()
        self.events.put(('prompt', localize_prompt(message, self.language.language)))
        self._answer.wait()
        return self._response

    def respond(self, value):
        self._response = value
        self._answer.set()

    def start(self, args):
        if self.busy:
            return False
        self.busy = True
        self.cancel_event.clear()
        def work():
            status = 1
            try:
                with contextlib.redirect_stdout(self), contextlib.redirect_stderr(self):
                    status = self.runner(args, prompt=self.prompt, interactive=True,
                                         progress=self.progress, cancel_event=self.cancel_event)
            except BaseException as error:
                self.events.put(('output', '\n' + self.language.text('stopped_error', error=str(error)) + '\n'))
            finally:
                self.events.put(('finished', status))
        self.worker = threading.Thread(target=work, name='AK820 installer', daemon=False)
        self.worker.start()
        return True

    def finished(self):
        self.busy = False


def main(argv=None):
    import argparse
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog, ttk
    parser = argparse.ArgumentParser(description='AK820 standalone GUI; no automatic device access')
    parser.add_argument('--self-test', action='store_true', help='Create/update/destroy the GUI without USB access')
    parser.add_argument('--session', help='Preselect an OEM recovery session; does not start an action')
    parser.add_argument('--backup-dir', help='Preselect a parent folder for new settings backups; does not start an action')
    parser.add_argument('--restore-backup', help='Preselect a settings backup; does not start an action')
    args = parser.parse_args(argv)
    root = tk.Tk()
    controller = Controller()
    language = controller.language.language
    root.title(tr('title', language))
    root.geometry('900x740')
    if args.self_test:
        root.withdraw()
    title = ttk.Label(root, text=tr('title', language), font=('', 13, 'bold'))
    title.pack(anchor='w', padx=12, pady=(12, 6))
    instructions = tk.StringVar(value=tr('instructions', language))
    ttk.Label(root, textvariable=instructions, wraplength=860).pack(anchor='w', padx=12)
    logs_label = ttk.Label(root, text=tr('logs_path', language, path=ak820.RUNS), wraplength=860)
    logs_label.pack(anchor='w', padx=12, pady=6)
    buttons = ttk.Frame(root)
    buttons.pack(fill='x', padx=12, pady=6)
    controls = []
    state = tk.StringVar(value=tr('ready', language))
    current_stage = None
    current_stage_data = {}
    current_status = None
    unlock_dialog = None
    unlock_detail = None

    def refresh_stage():
        language_now = controller.language.language
        if current_stage is None:
            instructions.set(tr('instructions', language_now))
            if current_status is not None:
                state.set(tr('completed', language_now, code=current_status))
            else:
                state.set(tr('ready', language_now))
            return
        instruction, status = progress_text(current_stage, current_stage_data, language_now)
        instructions.set(instruction)
        state.set(status)
        if unlock_detail is not None and unlock_detail.winfo_exists():
            unlock_detail.configure(text=status)

    session_folder = tk.StringVar(value=args.session or '')
    output_parent = tk.StringVar(value=args.backup_dir or str(ak820.RUNS))
    restore_folder = tk.StringVar(value=args.restore_backup or '')

    def add_folder_row(parent, label_key, variable, choose_title_key, initialdir=None, save_parent=False):
        row = ttk.Frame(parent)
        row.pack(fill='x', padx=12, pady=3)
        label = ttk.Label(row, text=tr(label_key, language))
        label.pack(side='left')
        entry = ttk.Entry(row, textvariable=variable)
        entry.pack(side='left', fill='x', expand=True, padx=6)
        def choose():
            folder = filedialog.askdirectory(
                title=tr(choose_title_key, controller.language.language),
                initialdir=variable.get() or initialdir or str(ak820.RUNS))
            if folder:
                variable.set(folder)
        button = ttk.Button(row, text=tr('choose_folder', language), command=choose)
        button.pack(side='left')
        controls.extend((entry, button))
        return label, button

    session_label, session_button = add_folder_row(root, 'update_folder', session_folder,
                                                   'choose_session_title', str(ak820.RUNS))
    output_label, output_button = add_folder_row(root, 'backup_output', output_parent,
                                                  'choose_output_title', str(ak820.RUNS))
    restore_label, restore_button = add_folder_row(root, 'restore_backup', restore_folder,
                                                    'choose_backup_title', str(ak820.RUNS))
    scope_note = ttk.Label(root, text=tr('backup_scope', language), wraplength=860)
    scope_note.pack(anchor='w', padx=12, pady=(0, 4))

    reference_folder = tk.StringVar(value='')
    reference_label, reference_button = add_folder_row(root, 'oem_folder', reference_folder,
                                                         'choose_oem_title', str(ak820.RUNS))
    oem_note = ttk.Label(root, text=tr('oem_note', language), wraplength=860)
    oem_note.pack(anchor='w', padx=12)

    def start(command_args):
        nonlocal current_stage, current_stage_data, current_status
        if command_args[0] in ('prepare', 'install', 'recover', 'check-device', 'update-prepared') and reference_folder.get().strip():
            command_args = command_args + ['--reference-dir', reference_folder.get().strip()]
        if controller.start(command_args):
            current_stage = None
            current_stage_data = {}
            current_status = None
            instructions.set(tr('instructions', controller.language.language))
            state.set(tr('checking', controller.language.language))
            for button in controls:
                button.configure(state='disabled')
            return True
        return False

    def recover():
        folder = filedialog.askdirectory(title=tr('recover_title', controller.language.language))
        if folder:
            start(['recover', '--session', folder])

    def update_new():
        session = session_folder.get().strip()
        parent = output_parent.get().strip()
        if not session:
            session_button.invoke()
            session = session_folder.get().strip()
        if not parent:
            output_button.invoke()
            parent = output_parent.get().strip()
        if session and parent:
            target = backup_destination(parent)
            if start(update_args(session, target)):
                append_log(tr('update_backup_target', controller.language.language, path=target))

    def backup_settings():
        session = session_folder.get().strip()
        parent = output_parent.get().strip()
        if not session:
            session_button.invoke()
            session = session_folder.get().strip()
        if not parent:
            output_button.invoke()
            parent = output_parent.get().strip()
        if session and parent:
            target = backup_destination(parent)
            if start(backup_args(session, target)):
                append_log(tr('backup_target', controller.language.language, path=target))

    def restore_settings():
        session = session_folder.get().strip()
        folder = restore_folder.get().strip()
        if not session:
            session_button.invoke()
            session = session_folder.get().strip()
        if not folder:
            restore_button.invoke()
            folder = restore_folder.get().strip()
        if session and folder:
            start(restore_args(session, folder))

    def update_legacy():
        folder = filedialog.askdirectory(
            title=tr('choose_prepared_update_title', controller.language.language),
            initialdir=str(ak820.RUNS))
        if folder:
            start(['update-prepared', '--session', folder])

    primary = ttk.Button(buttons, text=tr('update', language), command=update_new)
    primary.pack(side='left', padx=(0, 6))
    controls.append(primary)
    backup_button = ttk.Button(buttons, text=tr('backup', language), command=backup_settings)
    backup_button.pack(side='left', padx=(0, 6))
    controls.append(backup_button)
    restore_settings_button = ttk.Button(buttons, text=tr('restore', language), command=restore_settings)
    restore_settings_button.pack(side='left', padx=(0, 6))
    controls.append(restore_settings_button)
    cancel_button = ttk.Button(buttons, text=tr('cancel_wait', language), command=controller.cancel_wait, state='disabled')
    cancel_button.pack(side='left')
    secondary = ttk.LabelFrame(root, text=tr('other_actions', language))
    secondary.pack(fill='x', padx=12, pady=4)
    other_buttons = []
    other_keys = ('verify_package', 'find_keyboard', 'backup_oem', 'install_oem', 'restore_oem', 'legacy_update')
    other_actions = (
        lambda: start(['verify']), lambda: start(['diagnose']), lambda: start(['prepare']),
        lambda: start(['install']), recover, update_legacy,
    )
    for index, (key, action) in enumerate(zip(other_keys, other_actions)):
        button = ttk.Button(secondary, text=tr(key, language), command=action)
        button.grid(row=index // 3, column=index % 3, sticky='w', padx=4, pady=4)
        controls.append(button)
        other_buttons.append(button)
    ttk.Label(root, textvariable=state).pack(anchor='w', padx=12, pady=4)
    language_button = ttk.Button(buttons, text=tr('language_button', language))
    language_button.pack(side='right')
    ui_labels = [title, session_label, output_label, restore_label, reference_label, oem_note, scope_note, secondary]
    ui_keys = ('title', 'update_folder', 'backup_output', 'restore_backup', 'oem_folder', 'oem_note', 'backup_scope', 'other_actions')

    def switch_language():
        new_language = controller.language.toggle()
        root.title(tr('title', new_language))
        for widget, key in zip(ui_labels, ui_keys):
            widget.configure(text=tr(key, new_language))
        instructions.set(tr('instructions', new_language))
        state.set(tr('ready', new_language))
        logs_label.configure(text=tr('logs_path', new_language, path=ak820.RUNS))
        for button in (session_button, output_button, restore_button, reference_button):
            button.configure(text=tr('choose_folder', new_language))
        primary.configure(text=tr('update', new_language))
        backup_button.configure(text=tr('backup', new_language))
        restore_settings_button.configure(text=tr('restore', new_language))
        cancel_button.configure(text=tr('cancel_wait', new_language))
        for button, key in zip(other_buttons, other_keys):
            button.configure(text=tr(key, new_language))
        language_button.configure(text=tr('language_button', new_language))
        refresh_stage()

    language_button.configure(command=switch_language)
    output = tk.Text(root, wrap='word', state='disabled')
    output.pack(fill='both', expand=True, padx=12, pady=(0, 12))

    def append_log(message):
        output.configure(state='normal')
        output.insert('end', message + '\n')
        output.see('end')
        output.configure(state='disabled')

    def open_unlock_dialog(stage, data):
        nonlocal unlock_dialog, unlock_detail
        is_restore = stage == 'restore_unlock_wait' or data.get('purpose') == 'restore'
        unlock_dialog = tk.Toplevel(root)
        unlock_dialog.title(tr('physical_unlock_title', controller.language.language))
        unlock_dialog.transient(root)
        unlock_dialog.resizable(False, False)
        ttk.Label(unlock_dialog,
                  text=tr('physical_unlock_restore' if is_restore else 'physical_unlock_update',
                          controller.language.language),
                  wraplength=500, justify='left').pack(anchor='w', padx=14, pady=(14, 8))
        digest = data.get('sha256')
        if digest:
            ttk.Label(unlock_dialog, text='SHA256: ' + str(digest), wraplength=500).pack(anchor='w', padx=14, pady=4)
        unlock_detail = ttk.Label(unlock_dialog, text='', wraplength=500)
        unlock_detail.pack(anchor='w', padx=14, pady=4)
        ttk.Button(unlock_dialog, text=tr('cancel_wait', controller.language.language),
                   command=controller.cancel_wait).pack(anchor='e', padx=14, pady=(8, 14))
        unlock_dialog.protocol('WM_DELETE_WINDOW', controller.cancel_wait)
        unlock_dialog.grab_set()
        refresh_stage()

    def close_unlock_dialog():
        nonlocal unlock_dialog, unlock_detail
        if unlock_dialog is not None:
            try:
                if unlock_dialog.winfo_exists():
                    unlock_dialog.grab_release()
                    unlock_dialog.destroy()
            except tk.TclError:
                pass
        unlock_dialog = None
        unlock_detail = None

    def poll():
        nonlocal current_stage, current_stage_data, current_status
        while True:
            try:
                kind, value = controller.events.get_nowait()
            except queue.Empty:
                break
            if kind == 'output':
                output.configure(state='normal')
                output.insert('end', value)
                output.see('end')
                output.configure(state='disabled')
            elif kind == 'prompt':
                value = localize_prompt(value, controller.language.language)
                if '[y/N]' in value:
                    answer = 'y' if messagebox.askyesno(tr('prepare_prompt_title', controller.language.language), value,
                        default=messagebox.NO, parent=root) else ''
                elif is_yes_confirmation(value):
                    answer = ask_yes_confirmation(root, value, controller.language.language)
                else:
                    answer = simpledialog.askstring(tr('confirm_write_title', controller.language.language),
                        tr('confirm_instruction', controller.language.language, message=value), parent=root)
                controller.respond(answer or '')
            elif kind == 'progress':
                old_stage, old_data = current_stage, current_stage_data
                old_unlock = needs_unlock_dialog(old_stage, old_data)
                current_stage, current_stage_data = value
                if not isinstance(current_stage_data, dict):
                    current_stage_data = {'message': current_stage_data}
                is_unlock = needs_unlock_dialog(current_stage, current_stage_data)
                unlock_changed = (old_stage, old_data.get('purpose') if isinstance(old_data, dict) else None) != (
                    current_stage, current_stage_data.get('purpose'))
                if old_unlock and (not is_unlock or unlock_changed):
                    close_unlock_dialog()
                refresh_stage()
                if is_unlock and unlock_dialog is None:
                    open_unlock_dialog(current_stage, current_stage_data)
                cancel_button.configure(state='normal' if current_stage in
                    ('unlock_wait', 'restore_unlock_wait', 'loader_wait', 'loader_detected') else 'disabled')
            elif kind == 'finished':
                close_unlock_dialog()
                controller.finished()
                cancel_button.configure(state='disabled')
                current_stage = None
                current_stage_data = {}
                current_status = value
                instructions.set(tr('instructions', controller.language.language))
                state.set(tr('completed', controller.language.language, code=value))
                for button in controls:
                    button.configure(state='normal')
        root.after(100, poll)

    def close():
        if controller.busy:
            messagebox.showinfo(tr('action_running_title', controller.language.language),
                tr('wait_for_completion', controller.language.language), parent=root)
        else:
            root.destroy()
    root.protocol('WM_DELETE_WINDOW', close)
    if args.self_test:
        dialog_body = ttk.Frame(root)
        entry = build_yes_body(dialog_body, 'GUI self-test without USB.\nSHA256: self-test', language)
        assert entry.get() == ''
        labels = [child.cget('text') for child in dialog_body.winfo_children() if isinstance(child, ttk.Label)]
        assert 'yes' in labels and tr('yes_entry_label', language) in labels
        assert update_args('session', 'backup') == ['update', '--session', 'session', '--backup-dir', 'backup']
        root.update_idletasks()
        root.update()
        root.destroy()
        return 0
    root.after(100, poll)
    root.mainloop()


if __name__ == '__main__':
    main()
