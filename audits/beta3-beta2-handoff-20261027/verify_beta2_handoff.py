#!/usr/bin/env python3
"""Offline, fail-closed verification of public beta.2 -> delivered beta.3 handoff evidence."""
from __future__ import annotations
import argparse, hashlib, io, json, zipfile, sys
from pathlib import Path

PROFILES = ['main','game','mmo','typing','code','pointer','onehand','creative','shortcuts','multios']
EXPECTED = {'beta2_bundle':('8aa5176f657271f20834b35b4e80f79eb63ab7a6d3b5512478bf04a56031b1ce',2704055), 'beta2_matrix':('e646cb3cb58c50c55a184538b77674db92e0d54750b1a9734d1b092a6c20a08e',879783), 'beta3_outer':('14661efef8ce3577770327863a095168fbd0b6e392b083282c2672ba3d412a85',None)}
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok: raise ValueError(msg)
def readjson(b,label):
    try: return json.loads(b)
    except Exception as e: raise ValueError(f'{label}: invalid JSON: {e}')
def zipmap(blob,label):
    try: z=zipfile.ZipFile(io.BytesIO(blob))
    except Exception as e: raise ValueError(f'{label}: invalid ZIP: {e}')
    names=z.namelist(); need(len(names)==len(set(names)),f'{label}: duplicate ZIP paths')
    for n in names:
        if n.startswith('/') or '..' in Path(n).parts: raise ValueError(f'{label}: unsafe ZIP path {n}')
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True); ap.add_argument('--beta2-bundle',type=Path,required=True); ap.add_argument('--beta2-matrix',type=Path,required=True); ap.add_argument('--beta3-outer',type=Path,required=True); ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); repo=a.repo.resolve(); b2=zipmap(a.beta2_bundle.read_bytes(),'beta2 bundle'); matbytes=a.beta2_matrix.read_bytes(); matrix=readjson(matbytes,'beta2 matrix'); outerbytes=a.beta3_outer.read_bytes(); outer=zipmap(outerbytes,'beta3 outer')
    for label,path,blob in [('beta2_bundle',a.beta2_bundle,a.beta2_bundle.read_bytes()),('beta2_matrix',a.beta2_matrix,matbytes),('beta3_outer',a.beta3_outer,outerbytes)]:
        exp,size=EXPECTED[label]; need(sha(blob)==exp,f'{label} SHA256 mismatch'); need(size is None or len(blob)==size,f'{label} size mismatch')
    need('profiles' in matrix and matrix.get('catalog_version')==1,'beta2 matrix format missing')
    need({n.split('/')[1] for n in b2.namelist() if n.startswith('profiles/')}==set(PROFILES),'beta2 ZIP profile set mismatch')

    # Every ZIP payload file is listed by its profile manifest, with exact sizes and hashes.
    b2profiles={};
    for p in PROFILES:
        prefix=f'profiles/{p}/'; manifest=readjson(b2.read(prefix+'installer-release.json'),f'beta2 {p} manifest'); files=manifest.get('files'); need(isinstance(files,dict),f'{p}: missing file manifest')
        actual={n[len(prefix):] for n in b2.namelist() if n.startswith(prefix) and not n.endswith('/') and not n.endswith('installer-release.json') and not n.endswith('approved-release.json')}
        need(actual==set(files),f'{p}: manifest/file set differs')
        for rel,meta in files.items():
            data=b2.read(prefix+rel); need(len(data)==meta['size'] and sha(data)==meta['sha256'],f'{p}/{rel}: hash/size mismatch')
        manifest_bytes=b2.read(prefix+'installer-release.json'); approval=readjson(b2.read(prefix+'approved-release.json'),f'beta2 {p} approval')
        need(approval.get('manifest_sha256')==sha(manifest_bytes),f'{p}: beta2 approval does not bind manifest')
        ihx=b2.read(prefix+'firmware/application.ihx')
        mp=next(x for x in matrix['profiles'] if x['profile']==p); sid=mp['settings_identity']; identm=mp['identity']
        need(sha(ihx)==sid['ihx_sha256']==identm['ihx_sha256'],f'{p}: beta2 image identity mismatch')
        b2profiles[p]={'ihx':sha(ihx),'code':sid['code_sha256'],'manifest':sha(b2.read(prefix+'installer-release.json'))}

    # The outer delivery manifest must cover every other outer ZIP member exactly.
    delivery=readjson(outer.read('DELIVERY-MANIFEST.json'),'beta3 delivery manifest'); delivery_files=delivery.get('files',{})
    need(set(delivery_files)==set(outer.namelist())-{'DELIVERY-MANIFEST.json'},'beta3 outer manifest/member set differs')
    for n,meta in delivery_files.items():
        blob=outer.read(n); need(len(blob)==meta['size'] and sha(blob)==meta['sha256'],f'beta3 outer member {n}: hash/size mismatch')
    # Locate delivered Windows package and verify its packaged catalog and target firmware set.
    win='release/AK820-Windows.zip'; need(win in outer.namelist(),'delivered Windows ZIP missing'); wz=zipmap(outer.read(win),'beta3 Windows ZIP')
    catpath='AK820-Python/tools/installer/settings-catalog.json'; catalog=readjson(wz.read(catpath),'packaged beta3 catalog')
    local=json.loads((repo/'tools/installer/settings-catalog.json').read_text()); web=json.loads((repo/'web/firmware-matrix.json').read_text())
    need(catalog==local==web,'packaged catalog, repository catalog, and web matrix differ')
    need({x['profile'] for x in catalog['profiles']}==set(PROFILES) and len(catalog['profiles'])==10,'beta3 catalog target profile set mismatch')
    need(len(catalog['historical_profiles'])==20,'beta3 catalog historical descriptor inventory mismatch')
    b3zip=zipmap(outer.read('firmware/firmware-bundle.zip'),'beta3 firmware bundle')
    packing=json.loads((repo/'audits/beta3-direct-20261026/packing-preflight.json').read_text())
    packed={x['profile']:x for x in packing['profiles']}; transitions=json.loads((repo/'audits/beta3-direct-20261026/transition-preflight.json').read_text())['cases']
    fixture_doc=json.loads((repo/'audits/beta3-direct-20261026/beta2-input-fixtures.json').read_text())
    fixtures=fixture_doc['profiles']; fixture_by={x['profile']:x for x in fixtures}
    need(len(fixtures)==10 and set(fixture_by)==set(PROFILES),'beta2 fixture profile set mismatch')
    matrix_by={x['profile']:x for x in matrix['profiles']}
    historical={}
    for p in PROFILES:
        src=matrix_by[p]; fx=fixture_by[p]
        candidates=[x for x in catalog['historical_profiles'] if x['profile']==p and x['settings_identity']==src['settings_identity'] and x['identity']['ihx_sha256']==src['identity']['ihx_sha256']]
        need(len(candidates)==1,f'{p}: beta2 public matrix does not identify exactly one catalog historical descriptor')
        historical[p]=candidates[0]
        hist=historical[p]
        need(fx['ihx_sha256']==src['settings_identity']['ihx_sha256'] and fx['code_sha256']==src['settings_identity']['code_sha256'],f'{p}: preserved beta2 fixture identity/manifest differs from public input')
        need(fx['source_files_byte_unchanged'] and fx['archive_members_byte_equal'] and fx['validate_backup_passed'],f'{p}: beta2 retained fixture qualification incomplete')
    pre=[]
    for p in PROFILES:
        pref=f'profiles/{p}/'; manifest=readjson(b3zip.read(pref+'installer-release.json'),f'beta3 {p} manifest');
        actual={n[len(pref):] for n in b3zip.namelist() if n.startswith(pref) and not n.endswith('/') and not n.endswith('installer-release.json') and not n.endswith('approved-release.json')}
        need(actual==set(manifest.get('files',{})),f'beta3 {p}: manifest/file set differs')
        for rel,meta in manifest['files'].items():
            data=b3zip.read(pref+rel); need(len(data)==meta['size'] and sha(data)==meta['sha256'],f'beta3 {p}/{rel}: hash/size mismatch')
        ihx=sha(b3zip.read(pref+'firmware/application.ihx'))
        # Catalog and packing/final data both bind the delivered target image.
        cprof=next(x for x in catalog['profiles'] if x['profile']==p); ci=cprof.get('identity',{}); si=cprof.get('settings_identity',{})
        cihx=ci.get('ihx_sha256',si.get('ihx_sha256')); ccode=ci.get('settings_code_sha256',si.get('code_sha256'))
        need(ihx==cihx==packed[p]['build']['ihx_sha256'],f'{p}: delivered beta3 IHX identity mismatch')
        need(ccode==packed[p]['settings_code_sha256'],f'{p}: beta3 settings code identity mismatch')
        # Actual beta3 bundle and user Windows payload carry the same exact firmware image.
        wihx=f'AK820-Python/releases/beta3/{p}/firmware/application.ihx'; need(sha(wz.read(wihx))==ihx,f'{p}: Windows payload image differs')
        pre.append({'profile':p,'beta2_ihx_sha256':b2profiles[p]['ihx'],'beta2_settings_code_sha256':b2profiles[p]['code'],'beta3_ihx_sha256':ihx,'beta3_settings_code_sha256':ccode})
    need({n.split('/')[1] for n in b3zip.namelist() if n.startswith('profiles/')}==set(PROFILES),'beta3 firmware ZIP profile set mismatch')
    need(len(transitions)==330,'retained transition plan expected 330 rows')
    catalog_edges={(x['source'],x['target']) for x in catalog['settings_transitions']}
    expected_edges={(historical[sp]['settings_identity']['ihx_sha256'],next(x for x in catalog['profiles'] if x['profile']==tp)['identity']['ihx_sha256']) for sp in PROFILES for tp in PROFILES}
    need(len(catalog['settings_transitions'])==330 and expected_edges <= catalog_edges,'catalog is missing one or more beta2->beta3 settings transitions')
    selected=[c for c in transitions if c['source_case'].startswith('beta2-')]
    need(len(selected)==100,'expected exactly 100 beta2 transitions')
    rows=[]
    for sp in PROFILES:
      src=b2profiles[sp]
      for tp in PROFILES:
        candidates=[c for c in selected if c['source_case']==f'beta2-{sp}' and c['target_profile']==tp]
        need(len(candidates)==1,f'missing/duplicate transition {sp}->{tp}')
        c=candidates[0]; target=next(x for x in pre if x['profile']==tp)
        need(c['passed'] and c['offline_only'] and c['physical_device_commands']==0,f'{sp}->{tp}: retained plan not passed/offline')
        fx=fixture_by[sp]
        need(c['source']==src['ihx']==fx['ihx_sha256']==historical[sp]['settings_identity']['ihx_sha256'],f'{sp}->{tp}: source firmware identity mismatch')
        need(c['backup_manifest_sha256']==fx['manifest_sha256'],f'{sp}->{tp}: retained backup manifest does not bind public beta2 fixture')
        need(c['key_count']==fx['counts']['assignments'] and c['encoder_count']==fx['counts']['encoder_assignments'],f'{sp}->{tp}: retained transfer counts differ from beta2 fixture')
        need(c['combo_count']==matrix_by[sp]['capabilities']['dynamic_entries']['combos'],f'{sp}->{tp}: retained combo count differs from beta2 matrix')
        need(c['source_scope']==fx['scope'],f'{sp}->{tp}: retained source scope differs from beta2 fixture')
        need(src['code']==fx['code_sha256']==matrix_by[sp]['settings_identity']['code_sha256'],f'{sp}->{tp}: beta2 source CODE identity mismatch')
        need(c['target']==target['beta3_ihx_sha256'],f'{sp}->{tp}: target firmware identity mismatch')
        need((c['source'],c['target']) in catalog_edges,f'{sp}->{tp}: settings transition missing from beta3 catalog')
        semantics={'key_count':c['key_count'],'encoder_count':c['encoder_count'],'combo_count':c['combo_count'],'backup_manifest_sha256':c['backup_manifest_sha256'],'scope':c['source_scope']}
        rows.append({'source_profile':sp,'target_profile':tp,'source_ihx_sha256':src['ihx'],'source_settings_code_sha256':src['code'],'target_ihx_sha256':target['beta3_ihx_sha256'],'target_settings_code_sha256':target['beta3_settings_code_sha256'],'passed_retained_plan':True,'transfer_semantics':semantics})
    preserve=json.loads((repo/'audits/beta3-direct-20261026/preserved-profiles.json').read_text()); registry=repo/'qmk-8051-ak820/util/ak820_profiles.py'; registry_sha=sha(registry.read_bytes())
    need(preserve['source_sha256']=='485b8b40d4b78a80e568018ec7736700a11ea460739f4bc8f96a212ef1e056a2' and preserve['source_byte_unchanged'] and registry_sha==preserve['source_sha256'],'preserved profile composition evidence/registry bytes mismatch')
    need({x['profile'] for x in preserve['profiles']}==set(PROFILES) and len(preserve['profiles'])==10,'preserved composition profile set mismatch')
    result={'format':'ak820-beta2-beta3-handoff-check-1','status':'PASS','scope':'Authenticates public beta.2 inputs and delivered beta.3 images/catalog; rechecks retained offline transition plans. Does not freshly execute plan_restore and does not validate hardware or arbitrary settings.','evidence':{'beta2_bundle_sha256':sha(a.beta2_bundle.read_bytes()),'beta2_matrix_sha256':sha(matbytes),'beta3_outer_sha256':sha(outerbytes),'beta3_catalog_sha256':sha(wz.read(catpath)),'beta3_repo_catalog_sha256':sha((repo/'tools/installer/settings-catalog.json').read_bytes()),'beta3_web_matrix_sha256':sha((repo/'web/firmware-matrix.json').read_bytes()),'beta3_firmware_bundle_sha256':sha(outer.read('firmware/firmware-bundle.zip')),'transition_preflight_sha256':sha((repo/'audits/beta3-direct-20261026/transition-preflight.json').read_bytes()),'beta2_input_fixtures_sha256':sha((repo/'audits/beta3-direct-20261026/beta2-input-fixtures.json').read_bytes()),'packing_preflight_sha256':sha((repo/'audits/beta3-direct-20261026/packing-preflight.json').read_bytes()),'preserved_profiles_record_sha256':sha((repo/'audits/beta3-direct-20261026/preserved-profiles.json').read_bytes()),'preserved_registry_sha256':registry_sha,'beta2_historical_descriptors_verified':len(historical),'beta2_catalog_transition_edges_verified':len(expected_edges)},'profiles':pre,'pair_count':len(rows),'pairs':rows,'limitations':['No fresh plan_restore execution in this audit.','No keyboard connection, hardware validation, or settings write.','Curated beta.2 profile settings identities only; this is not universal compatibility for arbitrary settings backups.','Alpha compatibility remains outside this prioritized beta.2 handoff.']}
    result['execution']={'executable':sys.executable,'script':str(Path(__file__).resolve()),'argv':sys.argv,'cwd':str(Path.cwd().resolve())}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x',encoding='utf-8') as f: f.write(json.dumps(result,indent=2)+'\n')
    print(f"PASS: {len(rows)} beta2-to-beta3 pairs; wrote {a.output}")
if __name__=='__main__':
    try: main()
    except Exception as e: raise SystemExit(f'FAIL: {e}')
