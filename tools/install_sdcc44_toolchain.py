"""Install pinned official SDCC 4.4 locally for the production control build."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import shutil
import signal
import ssl
import subprocess
import sys
import tarfile
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://sourceforge.net/projects/sdcc/files/sdcc-linux-amd64/4.4.0/sdcc-4.4.0-amd64-unknown-linux2.5.tar.bz2/download'
DIRECT = 'https://downloads.sourceforge.net/project/sdcc/sdcc-linux-amd64/4.4.0/sdcc-4.4.0-amd64-unknown-linux2.5.tar.bz2'
PUBLISHED_SHA = '7cb4c96bd774f95e8032746e6808b59f3a8e2b3e7b4c72ac566bb67beeacff80'
TARGET = ROOT / 'toolchains/sdcc-4.4.0'
ARCHIVE_ROOT = 'sdcc-4.4.0'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trusted_url(url):
    parsed = urllib.parse.urlsplit(url)
    return parsed.scheme == 'https' and (parsed.hostname == 'sourceforge.net'
                                         or (parsed.hostname or '').endswith('.sourceforge.net'))


class HTTPSOnlySourceForge(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not trusted_url(newurl):
            raise ValueError('Redirect outside HTTPS SourceForge download infrastructure')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(destination):
    attempts = []
    opener = urllib.request.build_opener(HTTPSOnlySourceForge(),
                                        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    for url in (URL,DIRECT):
        try:
            with opener.open(url,timeout=45) as response:
                if not trusted_url(response.geturl()):
                    raise ValueError('Untrusted final download URL')
                digest = hashlib.sha256()
                size = 0
                with destination.open('wb') as target:
                    while True:
                        chunk = response.read(1024*1024)
                        if not chunk:
                            break
                        size += len(chunk)
                        if size > 128*1024*1024:
                            raise ValueError('Archive exceeds download limit')
                        target.write(chunk)
                        digest.update(chunk)
                if digest.hexdigest() != PUBLISHED_SHA:
                    raise ValueError('Archive does not match published SHA256')
                final = urllib.parse.urlsplit(response.geturl())
                return {'requested_url':url,'final_url_without_ephemeral_query':
                        urllib.parse.urlunsplit((final.scheme,final.netloc,final.path,'','')),
                        'bytes':size,'computed_sha256':digest.hexdigest(),
                        'publisher_sha256':PUBLISHED_SHA,'publisher_hash_matches':True,
                        'tls_certificate_verification':True,'earlier_attempts':attempts}
        except (OSError,ValueError) as exc:
            attempts.append({'url':url,'error':type(exc).__name__+': '+str(exc)})
    raise RuntimeError('Both official download routes failed: '+json.dumps(attempts))


def validate_members(archive):
    members = archive.getmembers()
    if len(members) > 100000:
        raise ValueError('Too many archive members')
    checked, names, links, total = [],set(),set(),0
    for item in members:
        path = PurePosixPath(item.name)
        if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != ARCHIVE_ROOT:
            raise ValueError('Archive member escapes expected sdcc root: '+item.name)
        relative = PurePosixPath(*path.parts[1:])
        if str(relative)=='.':
            if not item.isdir():raise ValueError('Root must be directory')
            continue
        key = str(relative)
        if key in names:raise ValueError('Duplicate archive member: '+key)
        names.add(key)
        if not (item.isfile() or item.isdir() or item.issym() or item.islnk()):
            raise ValueError('Special archive member rejected')
        target = None
        if item.issym():
            raw = PurePosixPath(item.linkname)
            if raw.is_absolute():raise ValueError('Absolute symlink rejected')
            target = posixpath.normpath(str(relative.parent/raw))
        elif item.islnk():
            raw = PurePosixPath(item.linkname)
            if raw.is_absolute() or '..' in raw.parts or not raw.parts or raw.parts[0]!=ARCHIVE_ROOT:
                raise ValueError('Unsafe hardlink target')
            target = str(PurePosixPath(*raw.parts[1:]))
        if target is not None:
            if target in ('.','..') or target.startswith('../'):
                raise ValueError('Link escapes root')
            links.add(key)
        if item.size < 0 or item.size > 128*1024*1024:
            raise ValueError('Invalid member size')
        total += item.size
        checked.append((item,relative,target))
    if total > 1024*1024*1024:raise ValueError('Uncompressed limit exceeded')
    for item,relative,target in checked:
        if any(str(parent) in links for parent in relative.parents):
            raise ValueError('Member would traverse archive symlink/hardlink')
        if target is not None and (target not in names or target in links):
            raise ValueError('Link target must be an existing non-link member')
    return checked,total


def command(args, cwd=None, env=None):
    proc = subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    result = {'args':args,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
    if proc.returncode:raise RuntimeError('Tool failed: '+json.dumps(result))
    return result


def linux_processes(directory, group=None):
    """Active processes in our run directory/group; zombies cannot continue IO."""
    root = Path(directory).resolve()
    rows = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit() or int(entry.name)==os.getpid():continue
        try:
            stat = (entry/'stat').read_text()
            fields = stat[stat.rfind(')')+2:].split()
            if fields[0]=='Z':continue
            pgid = int(fields[2])
            cwd = Path(os.readlink(entry/'cwd')).resolve()
            argv = (entry/'cmdline').read_bytes().split(b'\0')
            old_stage = (b'--linux-stage' in argv and any(
                value.endswith(b'/install_sdcc44_toolchain.py') for value in argv))
            if (group is not None and pgid==group) or cwd.is_relative_to(root) or old_stage:
                rows.append({'pid':int(entry.name),'pgid':pgid,'cwd':str(cwd)})
        except (FileNotFoundError,ProcessLookupError):pass
        except PermissionError as exc:
            raise RuntimeError('Cannot prove process quiescence: '+str(exc))
    return rows


def supervise_linux(args, directory, seconds=300, grace=10):
    """Linux timeout owns a dedicated group; supervisor also drains stray children."""
    directory = Path(directory).resolve()
    directory.mkdir(parents=True,exist_ok=True)
    wrapped = ['/usr/bin/timeout','--signal=TERM',f'--kill-after={grace}s',f'{seconds}s']+args
    started = time.monotonic()
    proc = subprocess.Popen(wrapped,cwd=directory,start_new_session=True,
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    error = None
    stdout = stderr = ''
    try:
        stdout,stderr = proc.communicate(timeout=seconds+grace+10)
    except subprocess.TimeoutExpired:
        error = 'Linux supervisor deadline expired'
    finally:
        # The group was created by this Popen. No foreign shell/bootstrap is run.
        try:os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        try:
            more_out,more_err = proc.communicate(timeout=5)
            if more_out:stdout=more_out
            if more_err:stderr=more_err
        except subprocess.TimeoutExpired:
            error = 'Cannot reap supervised Linux group'
    deadline = time.monotonic()+5
    active = linux_processes(directory,proc.pid)
    while active and time.monotonic()<deadline:
        time.sleep(0.1)
        active = linux_processes(directory,proc.pid)
    return {'command':wrapped,'returncode':proc.returncode,'stdout':stdout,'stderr':stderr,
            'elapsed_seconds':round(time.monotonic()-started,3),'owned_process_group':proc.pid,
            'post_cleanup_active_processes':active,'quiescent':not active,'error':error,
            'linux_timeout_seconds':seconds,'linux_kill_after_seconds':grace}


def host_quiescence(directory):
    """Independent read-only Linux query; never treats killing wsl.exe as cleanup."""
    query = command(['wsl','-d','Ubuntu','-u','root','--exec','python3',mounted(Path(__file__)),
                     '--linux-query','--output',mounted(Path(directory))])
    return json.loads(query['stdout'])


def linux_stage(archive_path, fixture_path, output):
    archive_path, fixture_path, output = Path(archive_path),Path(fixture_path),Path(output)
    if sha(archive_path)!=PUBLISHED_SHA:raise ValueError('Archive pin mismatch')
    parent = TARGET.parent
    parent.mkdir(parents=True,exist_ok=True)
    if parent.resolve()!=parent or TARGET.is_symlink():raise ValueError('Install root redirects through symlink')
    receipt = TARGET/'ak820-install-receipt.json'
    if TARGET.exists():
        if not receipt.is_file() or json.loads(receipt.read_text())['archive_sha256']!=PUBLISHED_SHA:
            raise ValueError('Existing target is not this pinned installation')
        extracted = json.loads(receipt.read_text())
    else:
        staging = parent/f'sdcc-4.4.0.staging-{time.time_ns()}'
        staging.mkdir()
        with tarfile.open(archive_path,'r:bz2') as archive:
            checked,total = validate_members(archive)  # All paths checked BEFORE first extraction.
            for item,relative,target in checked:
                if item.issym() or item.islnk():continue
                destination = staging/str(relative)
                if not destination.resolve().is_relative_to(staging.resolve()):
                    raise ValueError('Resolved extraction path escaped staging')
                if item.isdir():destination.mkdir(parents=True,exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True,exist_ok=True)
                    with archive.extractfile(item) as source,destination.open('xb') as dest:
                        shutil.copyfileobj(source,dest)
                    destination.chmod(0o755 if item.mode&0o111 else 0o644)
            for item,relative,target in checked:
                if not (item.issym() or item.islnk()):continue
                destination = staging/str(relative)
                destination.parent.mkdir(parents=True,exist_ok=True)
                if item.issym():destination.symlink_to(item.linkname)
                else:os.link(staging/target,destination)
        extracted = {'archive_sha256':PUBLISHED_SHA,'members':len(checked),'uncompressed_bytes':total,
                     'path_validation_before_extraction':True,'links_created_after_regular_files':True}
        (staging/'ak820-install-receipt.json').write_text(json.dumps(extracted,indent=2)+'\n')
        staging.rename(TARGET)
    system_sdcc = Path('/usr/bin/sdcc')
    old_hash = sha(system_sdcc) if system_sdcc.is_file() else None
    env = dict(os.environ,PATH=str(TARGET/'bin')+os.pathsep+os.environ.get('PATH',''))
    version = command([str(TARGET/'bin/sdcc'),'--version'],env=env)
    if '4.4.0' not in version['stdout']:raise ValueError('Wrong portable compiler version')
    output.mkdir(parents=True,exist_ok=True)
    smoke = command([str(TARGET/'bin/sdcc'),'-mmcs51','--model-large','--iram-size','0x0100',
                     '--xram-loc','0x0100','--xram-size','0x1f00','--code-size','0xf000',
                     str(fixture_path),'-o','probe.ihx'],cwd=output,env=env)
    system_version = command(['/usr/bin/sdcc','--version']) if old_hash is not None else None
    if old_hash is not None and sha(system_sdcc)!=old_hash:
        raise ValueError('System SDCC changed during local toolchain installation')
    return {'installed_directory':str(TARGET),'archive_validation':extracted,'portable_version':version,
            'system_sdcc_version':system_version,'system_sdcc_hash_unchanged':True,
            'system_sdcc_sha256':old_hash,
            'portable_binary_hashes':{name:sha(TARGET/'bin'/name) for name in ('sdcc','sdas8051','sdld','packihx')},
            'smoke_command':smoke,'fixture_sha256':sha(fixture_path),'fixture_executed':False,
            'smoke_artifacts':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in output.iterdir() if p.is_file()}}


def mounted(path):
    path = path.resolve()
    return '/mnt/'+path.drive[0].lower()+'/'+path.as_posix()[3:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--linux-stage',action='store_true')
    parser.add_argument('--linux-supervise',action='store_true')
    parser.add_argument('--linux-query',action='store_true')
    parser.add_argument('--archive');parser.add_argument('--fixture');parser.add_argument('--output');parser.add_argument('--result')
    args = parser.parse_args()
    if args.linux_query:
        active = linux_processes(args.output)
        print(json.dumps({'active':active,'quiescent':not active}))
        return
    if args.linux_supervise:
        result = supervise_linux(['python3',str(Path(__file__).resolve()),'--linux-stage',
            '--archive',args.archive,'--fixture',args.fixture,'--output',args.output,
            '--result',args.result],Path(args.result).parent)
        Path(args.result+'.lifecycle.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result))
        if result['returncode'] or not result['quiescent'] or result['error']:raise SystemExit(1)
        return
    if args.linux_stage:
        result = linux_stage(args.archive,args.fixture,args.output)
        Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
        return
    directory = ROOT/'work/sdcc44-install'/f'run-{time.time_ns()}'
    directory.mkdir(parents=True)
    metadata = {'release_url':'https://sourceforge.net/p/sdcc/news/2024/01/sdcc-440-released/',
                'publisher_hash_page':URL,'publisher_hash_is_digital_signature':False,
                'device_access':False,'foreign_qmk_build_executed':False,'global_path_modified':False,
                'installer_sha256':sha(Path(__file__))}
    try:
        metadata['preflight_quiescence'] = host_quiescence(ROOT/'work/sdcc44-install')
        if not metadata['preflight_quiescence']['quiescent']:
            raise RuntimeError('Previous installer stage still active; do not restart')
        archive = directory/'sdcc-4.4.0.tar.bz2'
        metadata['download'] = download(archive)
        result_path = directory/'linux-result.json'
        stage_args = ['wsl','-d','Ubuntu','-u','root','--exec','python3',mounted(Path(__file__)),
                    '--linux-supervise','--archive',mounted(archive),'--fixture',
                    mounted(ROOT/'tools/fixtures/sdcc_compile_probe.c'),'--output',mounted(directory/'smoke'),
                    '--result',mounted(result_path)]
        proc = subprocess.run(stage_args,capture_output=True,text=True,timeout=360)
        metadata['postflight_quiescence'] = host_quiescence(directory)
        if not metadata['postflight_quiescence']['quiescent']:
            raise RuntimeError('Linux installer still active; outcome not terminal, do not restart')
        stage = {'args':stage_args,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
        metadata['stage_lifecycle'] = json.loads(Path(str(result_path)+'.lifecycle.json').read_text('utf-8'))
        if proc.returncode:raise RuntimeError('Supervised Linux stage failed: '+json.dumps(stage))
        metadata.update(json.loads(result_path.read_text('utf-8')))
        metadata.update(passed=True,stage_process=stage)
    except Exception as exc:
        metadata.update(passed=False,error_type=type(exc).__name__,error=str(exc))
        try:metadata['postfailure_quiescence'] = host_quiescence(directory)
        except Exception as query_error:
            metadata['postfailure_quiescence'] = {'quiescent':None,'error':str(query_error)}
    report = ROOT/'host/runs/sdcc44-toolchain-checks.json'
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(metadata,indent=2)+'\n','utf-8')
    print(json.dumps({'passed':metadata['passed'],'directory':metadata.get('installed_directory'),
                      'error':metadata.get('error')}))
    if not metadata['passed']:raise SystemExit(1)


if __name__=='__main__':main()
