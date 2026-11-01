#!/bin/sh
# Full ten-profile release CI inside the pinned build image (mirrors
# .github/workflows/firmware-catalog.yml): fresh exact builds + full offline
# qualification for every catalog profile, then stage the candidate catalog.
set -eu
cd /home/agent/work/ak820
B=/home/agent/work/ak820/qmk-8051-ak820/.build
exec docker run --rm --name ak820-beta5-ci --pull=never --network=none \
  --user "$(id -u):$(id -g)" --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 512 --memory 8g --cpus 6 \
  --tmpfs /tmp:rw,nosuid,nodev,exec,size=2048m \
  --mount type=bind,src=/home/agent/work/ak820,dst=/home/agent/work/ak820 \
  --mount type=bind,src=/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-pointer-resume.phVRBT5t/tool-stage/sdcc-4.6.0,dst=/toolchain,readonly \
  --workdir /home/agent/work/ak820 \
  sha256:f611ccf71db2e2d1ad0bb6b40d0218748e41af009fd7eaf7762b41df719a5b9e \
  /usr/bin/env -i PATH=/opt/ak820/venv/bin:/usr/bin:/bin HOME=/tmp LC_ALL=C TZ=UTC \
  /bin/sh -c "/opt/ak820/venv/bin/python -s tools/build_profile_catalog.py \
    --build-root qmk-8051-ak820/.build/beta5-ci \
    --output dist/beta5-ci \
    --toolchain /toolchain \
    --qmk-bin /opt/ak820/venv/bin/qmk \
    --python /opt/ak820/venv/bin/python"
