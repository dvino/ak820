"""Offline one-off updater sequencing and negative cases; no USB."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock,patch
import flash_reviewed_release_once as f


class OneOffTests(unittest.TestCase):
    def test_default_never_executes(self):
        with patch.object(f,'prepare') as prepare,patch.object(f,'execute') as execute:
            f.main(['--session','new','--source-rom','saved.bin','--reference-dir','private'])
            prepare.assert_called_once(); execute.assert_not_called()

    def test_explicit_execute_rejects_preparation_arguments(self):
        with patch.object(f,'execute') as execute:
            with self.assertRaises(ValueError): f.main(['--session','new','--execute','--source-rom','saved.bin'])
            execute.assert_not_called()

    def test_source_failure_rejects_before_settings_validation(self):
        with patch.object(f.p,'validate_nvm') as nvm:
            with self.assertRaises(ValueError): f.source_check(bytes(65536),bytes(f.p.APP_END-f.p.APP_START),bytes(65536))
            nvm.assert_not_called()

    def run_flash(self,failure=None):
        with tempfile.TemporaryDirectory() as directory,contextlib.ExitStack() as stack:
            folder=Path(directory); commands=[]
            device=Mock()
            def send(packet):
                if len(packet)==65 and packet[2:4]==bytes.fromhex('aa55'):
                    commands.append(packet[1])
                    if failure=='erase' and packet[1]==2: raise OSError('erase fault')
                return 65
            device.send_feature_report.side_effect=send
            device.get_feature_report.return_value=bytes(65)
            hid=Mock();hid.device.return_value=device
            image=bytes(f.p.APP_END-f.p.APP_START)
            validate=stack.enter_context(patch.object(f,'validate',return_value={'payload.bin':image}))
            if failure=='changed':validate.side_effect=[{'payload.bin':image},ValueError('changed')]
            stack.enter_context(patch.object(f.installer,'require_state',return_value={'path':b'loader'}))
            stack.enter_context(patch.object(f.transport,'loader_reply'))
            stack.enter_context(patch.object(f.time,'sleep'))
            error=None
            try:f.flash_once(folder,'identity',hid,{'path':b'loader'},image)
            except (ValueError,OSError) as caught:error=caught
            device.close.assert_called_once()
            return commands,error

    def test_exactly_one_loader_attempt(self):
        commands,error=self.run_flash()
        self.assertIsNone(error);self.assertEqual(commands,[1,2,3,4,5])

    def test_changed_session_never_erases(self):
        commands,error=self.run_flash('changed')
        self.assertIsInstance(error,ValueError);self.assertEqual(commands,[1])

    def test_erase_failure_never_retries_or_restarts(self):
        commands,error=self.run_flash('erase')
        self.assertIsInstance(error,OSError);self.assertEqual(commands,[1,2])

    def run_execute(self,failure=None):
        with tempfile.TemporaryDirectory() as directory,contextlib.ExitStack() as stack:
            folder=Path(directory);(folder/'oneoff.json').write_bytes(b'fixed session')
            rom=bytes(65536);image=bytes(f.p.APP_END-f.p.APP_START)
            files={'source-rom.bin':rom,'source-image.bin':image,'stock-full.bin':rom,'payload.bin':image}
            events=[]
            source=Mock();target=Mock()
            def source_rom(address,length):
                events.append('source-rom')
                return (bytes([1])+rom[1:]) if failure=='source-changed' and length==65536 else rom[address:address+length]
            source.rom.side_effect=source_rom
            target.rom.side_effect=lambda address,length:rom[address:address+length]
            source.vial_unlock_status.side_effect=[(0,0),(0,1),(1,0,0),(1,0)]
            source.vial_unlock_command.side_effect=lambda command:events.append('unlock-'+str(command))
            source.enter_vial_loader.side_effect=lambda:events.append('enter')
            if failure=='consent':source.vial_unlock_status.side_effect=[(0,0),(0,1),(0,0,0)]
            stack.enter_context(patch.object(f,'validate',return_value=files))
            stack.enter_context(patch.object(f,'source_check'))
            def status(app):
                if failure=='storage':raise ValueError('storage fault')
                return {}
            stack.enter_context(patch.object(f,'checked_status',side_effect=status))
            stack.enter_context(patch.object(f.installer,'hid_module',return_value=Mock()))
            stack.enter_context(patch.object(f.installer,'require_state',return_value={'path':b'app'}))
            stack.enter_context(patch.object(f.installer,'wait_state',side_effect=lambda hid,state,**kwargs:events.append(state) or {'path':state.encode()}))
            stack.enter_context(patch.object(f.transport,'Application',side_effect=[source,target]))
            stack.enter_context(patch.object(f,'flash_once',side_effect=lambda *args:events.append('flash')))
            stack.enter_context(patch.object(f.transport,'verify_live',side_effect=lambda *args:events.append('verify')))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            error=None
            try:f.execute(folder)
            except ValueError as caught:error=caught
            return events,error,(folder/'fresh-preflash-rom.bin').exists()

    def test_execute_backup_consent_one_flash_then_verify(self):
        events,error,backup=self.run_execute()
        self.assertIsNone(error);self.assertTrue(backup)
        self.assertEqual([e for e in events if e not in ('source-rom',)],['unlock-8','unlock-6','enter','LOADER','flash','VIAL_APP','verify'])

    def test_preflight_or_consent_failures_never_enter_or_flash(self):
        for failure in ('storage','source-changed','consent'):
            events,error,backup=self.run_execute(failure)
            self.assertIsNotNone(error)
            self.assertNotIn('enter',events);self.assertNotIn('flash',events)
            if failure!='storage':self.assertTrue(backup)


if __name__=='__main__':unittest.main()
