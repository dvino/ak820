#!/usr/bin/env python3
"""Run the optional production USB/indicator sources with host MMIO, offline."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    runs=[]
    for flags in ([],['--os-indicators'],['--os-indicators','--without-mouse'],['--os-indicators','--mac-pc']):
        p=subprocess.run([sys.executable,str(ROOT/'tests/ak820_usb/run.py'),*flags],text=True,capture_output=True)
        runs.append({'flags':flags,'pass':p.returncode==0,'stdout':p.stdout,'stderr':p.stderr})
    result={'level':'host production C with ASan/UBSan; no hardware validation','tests':runs,'pass':all(r['pass'] for r in runs)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['pass'] else 1)
if __name__=='__main__': main()
