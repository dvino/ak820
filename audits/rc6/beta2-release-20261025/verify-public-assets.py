#!/usr/bin/env python3
"""Fail-closed offline checks for downloaded AK820 v0.6.0-beta.2 assets.

This checks downloaded bytes and package closure. It does not validate provenance
signatures, run Windows binaries, or claim hardware behavior.
"""
import argparse, hashlib, json, os, posixpath, re, shutil, stat, subprocess, sys, tarfile, tempfile, zipfile
from pathlib import Path, PurePosixPath
from types import SimpleNamespace

PROFILES = ('main','game','mmo','typing','code','pointer','onehand','creative','shortcuts','multios')
ASSETS = (
 'AK820-Windows.zip','AK820-Windows.zip.sha256',
 'AK820-Linux-x86_64.tar.gz','AK820-Linux-x86_64.tar.gz.sha256',
 'firmware-bundle.zip','firmware-bundle.zip.sha256',
 'AK820-Beta2-Catalog.zip','AK820-Beta2-Catalog.zip.sha256',
 'firmware-matrix.json','capability-catalog.json','module-descriptions.json',
 'release-catalog.json','release-manifest.json','SHA256SUMS','INSTALL-en.md','INSTALL-ru.md')

def sha(b): return hashlib.sha256(b).hexdigest()
def fail(s): raise ValueError(s)
def json_bytes(b, label):
    try: return json.loads(b.decode('utf-8'))
    except Exception as e: fail(f'{label}: invalid JSON: {e}')
def safe_name(name):
    p=PurePosixPath(name)
    if p.is_absolute() or not p.parts or any(x in ('..','.') for x in p.parts) or '\\' in name or '\x00' in name:
        fail('unsafe archive path: '+repr(name))
    return p
def zip_map(path):
    with zipfile.ZipFile(path) as z:
        out={}
        for i in z.infolist():
            safe_name(i.filename.rstrip('/'))
            mode=(i.external_attr >> 16) & 0xffff
            if stat.S_ISLNK(mode): fail(f'archive symlink rejected: {i.filename}')
            if i.is_dir(): continue
            if i.filename in out: fail('duplicate ZIP member: '+i.filename)
            out[i.filename]=z.read(i)
        return out
def tar_map(path):
    with tarfile.open(path,'r:gz') as t:
        out={}
        for m in t.getmembers():
            safe_name(m.name.rstrip('/'))
            if m.isdir(): continue
            if not m.isfile(): fail('non-regular tar member: '+m.name)
            if m.name in out: fail('duplicate tar member: '+m.name)
            f=t.extractfile(m)
            if f is None: fail('unreadable tar member: '+m.name)
            out[m.name]=f.read()
        return out
def check_sidecar(root, name):
    data=(root/(name+'.sha256')).read_text(encoding='ascii').strip()
    m=re.fullmatch(r'([0-9a-fA-F]{64})\s+\*?'+re.escape(name),data)
    if not m: fail(f'{name}.sha256 malformed or names another file')
    if sha((root/name).read_bytes()) != m.group(1).lower(): fail(f'{name} sidecar mismatch')
def check_safe_extract(files, dest, modes=None):
    dest.mkdir(parents=True,exist_ok=False)
    root=dest.resolve()
    for name,data in files.items():
        p=safe_name(name); out=root.joinpath(*p.parts)
        out.parent.mkdir(parents=True,exist_ok=True)
        if not out.resolve().is_relative_to(root): fail('extraction escaped scratch directory')
        out.write_bytes(data)
        if modes and name in modes: out.chmod(modes[name] & 0o777)
def tar_modes(path):
    with tarfile.open(path,'r:gz') as t:
        return {m.name:m.mode for m in t.getmembers() if m.isfile()}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--assets',required=True,type=Path)
    ap.add_argument('--source-commit',required=True)
    ap.add_argument('--scratch-dir',type=Path,help='optional new empty directory for safe archive extraction')
    a=ap.parse_args(); root=a.assets.resolve()
    if not re.fullmatch(r'[0-9a-fA-F]{40}',a.source_commit): fail('--source-commit must be a full 40-hex commit')
    if not root.is_dir(): fail('assets directory is missing')
    missing=[n for n in ASSETS if not (root/n).is_file()]
    if missing: fail('required public assets missing: '+', '.join(missing))
    for n in ASSETS:
        p=root/n
        if p.is_symlink(): fail('asset symlink rejected: '+n)
    for n in ('AK820-Windows.zip','AK820-Linux-x86_64.tar.gz','firmware-bundle.zip','AK820-Beta2-Catalog.zip'):
        check_sidecar(root,n)
    catalogzip=zip_map(root/'AK820-Beta2-Catalog.zip')
    # The release manifest binds every catalog payload byte; it excludes itself and the zip checksum sidecar.
    rm=json_bytes((root/'release-manifest.json').read_bytes(),'release-manifest.json')
    if rm.get('format')!='ak820-beta-release-manifest-1' or rm.get('files') is None: fail('release manifest format/files mismatch')
    if set(rm['files']) != set(catalogzip)-{'release-manifest.json'}: fail('release manifest and catalog ZIP member sets differ')
    for n,meta in rm['files'].items():
        if not isinstance(meta,dict) or meta.get('sha256')!=sha(catalogzip[n]) or meta.get('size')!=len(catalogzip[n]): fail('release manifest hash/size mismatch: '+n)
    if rm.get('tag')!='v0.6.0-beta.2': fail('release manifest tag is not v0.6.0-beta.2')
    # The public checksum list covers catalog payload files and the catalog ZIP.
    sums=(root/'SHA256SUMS').read_text(encoding='ascii').splitlines(); parsed={}
    for line in sums:
        m=re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9._/-]+)',line)
        if not m: fail('malformed SHA256SUMS line')
        if m.group(2) in parsed: fail('duplicate SHA256SUMS name')
        parsed[m.group(2)]=m.group(1)
    expected={n:sha(b) for n,b in catalogzip.items()}; expected['AK820-Beta2-Catalog.zip']=sha((root/'AK820-Beta2-Catalog.zip').read_bytes())
    if parsed!=expected: fail('SHA256SUMS does not exactly cover catalog payload and ZIP')
    # Standalone files must be exact catalog copies.
    for n in ('firmware-matrix.json','capability-catalog.json','module-descriptions.json','release-catalog.json','release-manifest.json','INSTALL-en.md','INSTALL-ru.md'):
        if catalogzip.get(n)!=(root/n).read_bytes(): fail('standalone asset differs from catalog ZIP: '+n)
    rc=json_bytes((root/'release-catalog.json').read_bytes(),'release-catalog.json')
    if rc.get('tag')!='v0.6.0-beta.2' or rc.get('default_profile')!='main': fail('release catalog tag/default mismatch')
    if rc.get('installable_profiles')!=list(PROFILES) or rc.get('catalog_profiles')!=list(PROFILES): fail('release catalog must name exactly the ten required profiles, in order')
    if rc.get('hardware_validated') is not False or rc.get('flashing_authorized') is not False or rc.get('settings_writes_authorized') is not False: fail('release catalog overstates hardware or mutation authorization')
    for n,meta in rc.get('assets',{}).items():
        if n not in catalogzip or meta.get('sha256')!=sha(catalogzip[n]) or meta.get('size')!=len(catalogzip[n]): fail('release-catalog asset closure mismatch: '+n)
    if set(rc.get('assets',{})) != set(catalogzip)-{'release-catalog.json','release-manifest.json'}: fail('release-catalog asset list is not exact')
    # Profile catalog and bilingual guide closure are sourced from the current source checkout.
    repo=Path('/home/danil/ChatGPT/ak820-beta2-20261025')
    source_catalog=json_bytes((repo/'tools/installer/profile-catalog.json').read_bytes(),'source profile catalog')
    if source_catalog.get('default_profile')!='main' or [x.get('id') for x in source_catalog.get('profiles',[])]!=list(PROFILES): fail('current source profile catalog differs from required ten')
    if catalogzip.get('profile-catalog.json') != (repo/'tools/installer/profile-catalog.json').read_bytes(): fail('published profile catalog differs from source')
    # Resolve exact guide/image allowlist from the helper (expected 70 files in this checkout).
    sys.path.insert(0,str(repo/'tools'))
    import build_windows_installer
    guide_names=build_windows_installer.guide_files()
    if len(guide_names)!=70: fail(f'source guide closure count changed: {len(guide_names)}; inspect helper before proceeding')
    for n in guide_names:
        if n not in catalogzip or catalogzip[n] != (repo/n).read_bytes(): fail('public guide closure missing or source mismatch: '+n)
    # Check relative Markdown links across the complete published guide closure.
    for name in (x for x in guide_names if x.lower().endswith('.md')):
        text=catalogzip[name].decode('utf-8')
        for match in re.finditer(r'\[[^\]\n]*\]\(([^\s)]+)\)',text):
            target=match.group(1)
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith(('/', '#')): continue
            path=target.split('#',1)[0].split('?',1)[0]
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),path)) if path else name
            if resolved.startswith('../') or resolved not in catalogzip: fail(f'{name} relative link target absent from catalog: {target} -> {resolved}')
    # Firmware bundle payload is closed by its own sidecar and catalog manifest references.
    fb=zip_map(root/'firmware-bundle.zip')
    source_commit=a.source_commit.lower()
    # Bind approved host-file identities to the requested Git commit, not merely
    # to the possibly dirty working tree used to run this verifier.
    sys.path.insert(0,str(repo/'qmk-8051-ak820'/'util'))
    from ak820_release_manifest import HOST_FILES
    source_host_bytes={}
    for name in sorted(HOST_FILES):
        proc=subprocess.run(['git','-C',str(repo),'show',f'{source_commit}:{name}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if proc.returncode: fail(f'expected source commit lacks host file {name}')
        source_host_bytes[name]=proc.stdout
    tmp_root=Path(tempfile.mkdtemp(prefix='ak820-beta2-public-'))
    try:
        bundle_root=tmp_root/'firmware'
        check_safe_extract(fb,bundle_root)
        contexts=[]
        for profile in PROFILES:
            prefix=f'profiles/{profile}/'
            bundle=bundle_root/'profiles'/profile
            manifest=json_bytes((bundle/'installer-release.json').read_bytes(),profile+' installer-release.json')
            if manifest.get('format')!='ak820-installer-release-2' or manifest.get('release')!='rc6' or manifest.get('hardware_validated') is not False or manifest.get('install_modes')!=['permanent','trial']:
                fail('invalid/non-installable release manifest: '+profile)
            host=manifest.get('host_files')
            if not isinstance(host,dict) or set(host)!=set(HOST_FILES): fail('unexpected host-file set: '+profile)
            for name,data in source_host_bytes.items():
                expected={'size':len(data),'sha256':sha(data)}
                if host.get(name)!=expected: fail('approved host manifest is not bound to expected source commit: '+profile+'/'+name)
            approval=json_bytes((bundle/'approved-release.json').read_bytes(),profile+' approved-release.json')
            if approval!={'format':'ak820-installer-approval-1','release':'rc6','manifest_sha256':sha((bundle/'installer-release.json').read_bytes())}:
                fail('approved-release does not authorize exact manifest bytes: '+profile)
            report_file=bundle/'reviews/independent-review.md'
            if not report_file.is_file(): fail('missing independent review record: '+profile)
            import ak820_ci_authorization as authorization
            from ak820_release_manifest import read_review_record
            record=read_review_record(report_file.read_text(encoding='utf-8'))
            authorization.validate_bundle_authorization(bundle,manifest,record)
            # Catalog and distributable firmware bundle must carry identical bytes
            # for the whole profile tree, including approval and release manifests.
            prefix_catalog='profiles/'+profile+'/'
            catalog_profile={n[len(prefix_catalog):]:b for n,b in catalogzip.items() if n.startswith(prefix_catalog)}
            bundle_profile={n[len(prefix):]:b for n,b in fb.items() if n.startswith(prefix)}
            if catalog_profile!=bundle_profile: fail('catalog profile payload differs from firmware bundle: '+profile)
            contexts.append(SimpleNamespace(profile=profile,bundle=bundle,manifest=manifest))
        sys.path.insert(0,str(repo/'tools'))
        import build_beta_release_assets
        build_beta_release_assets.validate_profile_links(
            catalogzip,contexts,
            json_bytes(catalogzip['settings-catalog.json'],'settings-catalog.json'),
            json_bytes(catalogzip['capability-catalog.json'],'capability-catalog.json'),
            catalogzip['module-descriptions.json'])
    finally:
        shutil.rmtree(tmp_root,ignore_errors=True)
    for profile in PROFILES:
        prefix=f'profiles/{profile}/'
        members=[n for n in fb if n.startswith(prefix)]
        if not members: fail('firmware bundle lacks profile '+profile)
        att=[n for n in members if n.endswith('reports/build-attestation.json')]
        if len(att)!=1: fail('expected one build attestation for '+profile)
        av=json_bytes(fb[att[0]],att[0])
        if av.get('source_commit')!=a.source_commit: fail('source commit mismatch in '+profile+' attestation')
        manifest_path=prefix+'installer-release.json'; approval_path=prefix+'approved-release.json'
        if manifest_path not in fb or approval_path not in fb: fail('missing release/approval manifest for '+profile)
        manifest=json_bytes(fb[manifest_path],manifest_path)
        if not isinstance(manifest.get('files'),dict): fail('invalid installer manifest '+profile)
        for filename,desc in manifest['files'].items():
            name=prefix+filename
            if name not in fb or sha(fb[name])!=desc.get('sha256') or len(fb[name])!=desc.get('size'): fail('firmware bundle manifest closure mismatch: '+name)
    # Verify both native packages contain exactly identical approved manifest inputs per app/profile.
    win=zip_map(root/'AK820-Windows.zip'); lin=tar_map(root/'AK820-Linux-x86_64.tar.gz')
    for app in ('AK820','AK820-cli'):
        for profile in PROFILES:
            prefix=f'{app}/_internal/releases/beta2/{profile}/'
            rel='profiles/'+profile+'/'
            required=['installer-release.json','approved-release.json']
            man=json_bytes(fb[rel+'installer-release.json'],rel+'installer-release.json')
            required += list(man['files'])
            for name in required:
                expected=fb[rel+name]
                for label,tree,pkgprefix in (('Windows',win,f'AK820-Windows/{prefix}'),('Linux',lin,f'AK820-Linux-x86_64/{prefix}')):
                    key=pkgprefix+name
                    if tree.get(key)!=expected: fail(f'{label} {app} packaged input mismatch: {profile}/{name}')
    # Offline Linux-only CLI commands. `verify` is explicitly offline in the source CLI.
    if a.scratch_dir:
        scratch=a.scratch_dir.resolve()
        if scratch.exists(): fail('--scratch-dir must not already exist')
        check_safe_extract(lin,scratch/'linux',tar_modes(root/'AK820-Linux-x86_64.tar.gz'))
        cli=scratch/'linux/AK820-Linux-x86_64/AK820-cli/AK820-cli'
        if not cli.is_file() or not os.access(cli,os.X_OK): fail('extracted Linux CLI missing or not executable')
        subprocess.run([str(cli),'--help'],check=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
        subprocess.run([str(cli),'verify'],check=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
        for profile in PROFILES:
            # verify supports global profile option either before or after subcommand.
            subprocess.run([str(cli),'--profile',profile,'verify'],check=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    print('PASS: hashes, catalog closure, ten-profile bundle/manifests, both package trees, and guide closure')
    print('LIMIT: this does not authenticate publisher identity, run Windows, prove source provenance beyond embedded commit, qualify runtime/device behavior, or inspect package GUI behavior.')
    if not a.scratch_dir: print('SKIPPED: Linux CLI smoke; rerun with a new --scratch-dir to enable offline --help and verify per profile.')
if __name__=='__main__':
    try: main()
    except Exception as e:
        print('FAIL:',e,file=sys.stderr); sys.exit(1)
