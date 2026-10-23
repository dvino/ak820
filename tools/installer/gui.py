"""Small Windows GUI for the shared installer; importing this module opens no USB."""
from __future__ import annotations

import contextlib
import queue
import threading

import ak820
from i18n import (LanguageSession, hold_seconds_remaining, localize_output,
                  localize_prompt, text as tr)


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
    parser.add_argument('--session', help='Preselect a personal prepared update folder; does not start an action')
    args = parser.parse_args(argv)
    root = tk.Tk()
    controller = Controller()
    language = controller.language.language
    root.title(tr('title', language))
    root.geometry('900x650')
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

    def refresh_stage():
        language_now = controller.language.language
        if current_stage is None:
            instructions.set(tr('instructions', language_now))
            if current_status is not None:
                state.set(tr('completed', language_now, code=current_status))
            else:
                state.set(tr('ready', language_now))
            return
        if current_stage == 'unlock_wait':
            instructions.set(tr('prompt_update_unlock_hash', language_now,
                                 sha256=current_stage_data.get('sha256', '')))
            ticks = current_stage_data.get('counter', 0)
            seconds = hold_seconds_remaining(ticks)
            state.set(tr('hold_remaining', language_now, seconds=seconds))
        elif current_stage == 'loader_wait':
            instructions.set(tr('prompt_loader', language_now))
            state.set(tr('loader_wait', language_now))
        elif current_stage == 'loader_detected':
            instructions.set(tr('prompt_loader_detected', language_now))
            state.set(tr('prompt_loader_detected', language_now))
        elif current_stage == 'flashing':
            instructions.set(tr('prompt_flashing', language_now))
            state.set(tr('prompt_flashing', language_now))
        else:
            # Unknown event text may contain release, file, or device data.
            instructions.set(str(current_stage_data.get('message', current_stage)))
    session_folder = tk.StringVar(value=args.session or '')
    session_row = ttk.Frame(root)
    session_row.pack(fill='x', padx=12, pady=4)
    session_label = ttk.Label(session_row, text=tr('update_folder', language))
    session_label.pack(side='left')
    session_entry = ttk.Entry(session_row, textvariable=session_folder)
    session_entry.pack(side='left', fill='x', expand=True, padx=6)
    def choose_session():
        folder = filedialog.askdirectory(title=tr('choose_session_title', controller.language.language),
                                         initialdir=session_folder.get() or str(ak820.RUNS))
        if folder:
            session_folder.set(folder)
    session_button = ttk.Button(session_row, text=tr('choose_folder', language), command=choose_session)
    session_button.pack(side='left')
    controls.extend((session_entry, session_button))
    reference_folder = tk.StringVar(value='')
    reference_row = ttk.Frame(root)
    reference_row.pack(fill='x', padx=12, pady=4)
    reference_label = ttk.Label(reference_row, text=tr('oem_folder', language))
    reference_label.pack(side='left')
    reference_entry = ttk.Entry(reference_row, textvariable=reference_folder)
    reference_entry.pack(side='left', fill='x', expand=True, padx=6)
    def choose_references():
        folder = filedialog.askdirectory(title=tr('choose_oem_title', controller.language.language))
        if folder:
            reference_folder.set(folder)
    reference_button = ttk.Button(reference_row, text=tr('choose_folder', language), command=choose_references)
    reference_button.pack(side='left')
    controls.extend((reference_entry, reference_button))
    oem_note = ttk.Label(root, text=tr('oem_note', language), wraplength=860)
    oem_note.pack(anchor='w', padx=12)
    def start(args):
        nonlocal current_stage, current_stage_data, current_status
        if args[0] in ('prepare', 'install', 'recover', 'check-device', 'update-prepared') and reference_folder.get().strip():
            args = args + ['--reference-dir', reference_folder.get().strip()]
        if controller.start(args):
            current_stage = None
            current_stage_data = {}
            current_status = None
            instructions.set(tr('instructions', controller.language.language))
            state.set(tr('checking', controller.language.language))
            for button in controls:
                button.configure(state='disabled')
    def recover():
        folder = filedialog.askdirectory(title=tr('recover_title', controller.language.language))
        if folder:
            start(['recover', '--session', folder])
    def update_prepared():
        folder = session_folder.get().strip()
        if not folder:
            choose_session()
            folder = session_folder.get().strip()
        if folder:
            start(['update-prepared', '--session', folder])
    primary = ttk.Button(buttons, text=tr('update', language), command=update_prepared)
    primary.pack(side='left', padx=(0, 6))
    controls.append(primary)
    cancel_button = ttk.Button(buttons, text=tr('cancel_wait', language), command=controller.cancel_wait, state='disabled')
    cancel_button.pack(side='left')
    secondary = ttk.LabelFrame(root, text=tr('other_actions', language))
    secondary.pack(fill='x', padx=12, pady=4)
    other_buttons = []
    for index, (label, action) in enumerate((
        (tr('verify_package', language), lambda: start(['verify'])),
        (tr('find_keyboard', language), lambda: start(['diagnose'])),
        (tr('backup_oem', language), lambda: start(['prepare'])),
        (tr('install_oem', language), lambda: start(['install'])),
        (tr('restore_oem', language), recover),
    )):
        button = ttk.Button(secondary, text=label, command=action)
        button.grid(row=index // 3, column=index % 3, sticky='w', padx=4, pady=4)
        controls.append(button)
        other_buttons.append(button)
    ttk.Label(root, textvariable=state).pack(anchor='w', padx=12, pady=4)
    language_button = ttk.Button(buttons, text=tr('language_button', language))
    language_button.pack(side='right')
    ui_labels = [title, session_label, reference_label, oem_note, secondary]
    def switch_language():
        new_language = controller.language.toggle()
        root.title(tr('title', new_language))
        for widget, key in zip(ui_labels, ('title', 'update_folder', 'oem_folder', 'oem_note', 'other_actions')):
            widget.configure(text=tr(key, new_language))
        instructions.set(tr('instructions', new_language))
        state.set(tr('ready', new_language))
        logs_label.configure(text=tr('logs_path', new_language, path=ak820.RUNS))
        session_button.configure(text=tr('choose_folder', new_language))
        reference_button.configure(text=tr('choose_folder', new_language))
        primary.configure(text=tr('update', new_language))
        cancel_button.configure(text=tr('cancel_wait', new_language))
        for button, key in zip(other_buttons, ('verify_package', 'find_keyboard', 'backup_oem', 'install_oem', 'restore_oem')):
            button.configure(text=tr(key, new_language))
        language_button.configure(text=tr('language_button', new_language))
        refresh_stage()

    language_button.configure(command=switch_language)
    output = tk.Text(root, wrap='word', state='disabled')
    output.pack(fill='both', expand=True, padx=12, pady=(0, 12))
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
                current_stage, current_stage_data = value
                if not isinstance(current_stage_data, dict):
                    current_stage_data = {'message': current_stage_data}
                refresh_stage()
                stage = current_stage
                cancel_button.configure(state='normal' if stage in ('unlock_wait', 'loader_wait', 'loader_detected') else 'disabled')
            elif kind == 'finished':
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
        dialog_body.destroy()
        root.update_idletasks()
        root.update()
        root.destroy()
        return 0
    root.after(100, poll)
    root.mainloop()


if __name__ == '__main__':
    main()
