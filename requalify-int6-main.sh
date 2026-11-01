#!/bin/sh
# Re-run canonical qualification for the already-built int6-main image.
# Fix vs first run: /tmp mounted exec (docker --tmpfs defaults to noexec, which
# broke every suite that compiles and executes a native test binary).
set -eu
cd /home/agent/work/ak820
B=/home/agent/work/ak820/qmk-8051-ak820/.build
exec docker run --rm --name ak820-int6-qualify --pull=never --network=none --read-only \
  --user "$(id -u):$(id -g)" --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 256 --memory 3g --cpus 2 \
  --tmpfs /tmp:rw,nosuid,nodev,exec,size=1024m \
  --mount type=bind,src=/home/agent/work/ak820,dst=/home/agent/work/ak820,readonly \
  --mount type=bind,src="$B",dst="$B" \
  --mount type=bind,src=/home/agent/ak820-profile-handoff-20261031/evidence/tmp/ak820-pointer-resume.phVRBT5t/tool-stage/sdcc-4.6.0,dst=/toolchain,readonly \
  --workdir /home/agent/work/ak820 \
  sha256:f611ccf71db2e2d1ad0bb6b40d0218748e41af009fd7eaf7762b41df719a5b9e \
  /usr/bin/env -i PATH=/opt/ak820/venv/bin:/usr/bin:/bin HOME=/tmp LC_ALL=C TZ=UTC \
  /bin/sh -c "/opt/ak820/venv/bin/python -s tools/configure_firmware.py qualify \
    --build-dir $B/int6-main --toolchain /toolchain"
