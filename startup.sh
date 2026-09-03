#!/bin/bash
set -Eeuo pipefail

cd "$(dirname "$0")"

# Do not clone/overwrite the project at runtime. The deployment image already
# contains the exact source that was built and deployed.
if [[ ! -f "main.py" ]]; then
    echo "ERROR: main.py was not found in the application directory." >&2
    exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ERROR: ffmpeg is required but was not found." >&2
    exit 1
fi

echo ">> STARTING MUSIC PLAYER USERBOT..."
exec python3 main.py
