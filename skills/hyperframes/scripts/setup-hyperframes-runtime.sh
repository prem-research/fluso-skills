#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-.}"
TOOLS_DIR="${PROJECT_DIR%/}/.hyperframes-tools"
BIN_DIR="$TOOLS_DIR/bin"
NODE_MODULES_BIN="$TOOLS_DIR/node_modules/.bin"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required for HyperFrames but was not found on PATH." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required for HyperFrames but was not found on PATH." >&2
  exit 1
fi

mkdir -p "$BIN_DIR"

packages=()
SYSTEM_HYPERFRAMES=""
if command -v hyperframes >/dev/null 2>&1; then
  SYSTEM_HYPERFRAMES="$(command -v hyperframes)"
  ln -sf "$SYSTEM_HYPERFRAMES" "$BIN_DIR/hyperframes"
  echo "Using system hyperframes at $SYSTEM_HYPERFRAMES"
elif [ ! -x "$NODE_MODULES_BIN/hyperframes" ]; then
  packages+=("hyperframes@latest")
fi

SYSTEM_FFMPEG=""
if command -v ffmpeg >/dev/null 2>&1; then
  SYSTEM_FFMPEG="$(command -v ffmpeg)"
  ln -sf "$SYSTEM_FFMPEG" "$BIN_DIR/ffmpeg"
  echo "Using system ffmpeg at $SYSTEM_FFMPEG"
elif [ ! -d "$TOOLS_DIR/node_modules/ffmpeg-static" ]; then
  packages+=("ffmpeg-static@latest")
fi

if [ "${#packages[@]}" -gt 0 ]; then
  echo "Installing missing HyperFrames user-space packages into $TOOLS_DIR"
  npm install --prefix "$TOOLS_DIR" --no-audit --no-fund "${packages[@]}"
else
  echo "HyperFrames user-space packages already prepared in $TOOLS_DIR"
fi

FFMPEG_PATH="$(
  node - "$TOOLS_DIR" <<'NODE'
const toolsDir = process.argv[2];
process.chdir(toolsDir);
let ffmpegPath = null;
try {
  ffmpegPath = require("ffmpeg-static");
} catch {}
if (!ffmpegPath) process.exit(0);
console.log(ffmpegPath);
NODE
)"

if [ -n "$SYSTEM_FFMPEG" ]; then
  :
elif [ -n "$FFMPEG_PATH" ] && [ -f "$FFMPEG_PATH" ]; then
  chmod +x "$FFMPEG_PATH"
  ln -sf "$FFMPEG_PATH" "$BIN_DIR/ffmpeg"
  echo "Prepared user-space ffmpeg at $BIN_DIR/ffmpeg"
else
  echo "ffmpeg-static did not expose a usable binary. HyperFrames render may still need FFmpeg on PATH." >&2
fi

if [ -n "$SYSTEM_HYPERFRAMES" ]; then
  HYPERFRAMES_BIN="$BIN_DIR/hyperframes"
else
  HYPERFRAMES_BIN="$NODE_MODULES_BIN/hyperframes"
fi
if [ -x "$HYPERFRAMES_BIN" ]; then
  echo "HyperFrames CLI ready at $HYPERFRAMES_BIN"
  echo "Browser runtime is not installed by this helper. If browser launch fails, report the runtime blocker instead of installing system libraries."
else
  echo "HyperFrames CLI was not installed at $HYPERFRAMES_BIN" >&2
  exit 1
fi

cat <<EOF

User-space HyperFrames runtime is prepared.

Use this PATH before running HyperFrames commands in this project:

  export PATH="$BIN_DIR:$NODE_MODULES_BIN:\$PATH"

Then run:

  hyperframes --version
  hyperframes lint
  hyperframes inspect
  hyperframes preview
  hyperframes render --output final.mp4
EOF
