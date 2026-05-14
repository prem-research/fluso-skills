#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-.}"
TOOLS_DIR="${PROJECT_DIR%/}/.hyperframes-tools"
BIN_DIR="$TOOLS_DIR/bin"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required for HyperFrames but was not found on PATH." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required for HyperFrames but was not found on PATH." >&2
  exit 1
fi

mkdir -p "$BIN_DIR"

echo "Installing HyperFrames user-space runtime into $TOOLS_DIR"
npm install --prefix "$TOOLS_DIR" --no-audit --no-fund hyperframes@latest ffmpeg-static@latest

FFMPEG_PATH="$(
  node - "$TOOLS_DIR" <<'NODE'
const toolsDir = process.argv[2];
process.chdir(toolsDir);
const ffmpegPath = require("ffmpeg-static");
if (!ffmpegPath) process.exit(2);
console.log(ffmpegPath);
NODE
)"

if [ -n "$FFMPEG_PATH" ] && [ -f "$FFMPEG_PATH" ]; then
  chmod +x "$FFMPEG_PATH"
  ln -sf "$FFMPEG_PATH" "$BIN_DIR/ffmpeg"
  echo "Prepared user-space ffmpeg at $BIN_DIR/ffmpeg"
else
  echo "ffmpeg-static did not expose a usable binary. HyperFrames render may still need FFmpeg on PATH." >&2
fi

HYPERFRAMES_BIN="$TOOLS_DIR/node_modules/.bin/hyperframes"
if [ -x "$HYPERFRAMES_BIN" ]; then
  echo "Ensuring HyperFrames browser runtime when available"
  PATH="$BIN_DIR:$TOOLS_DIR/node_modules/.bin:$PATH" "$HYPERFRAMES_BIN" browser ensure || true
  echo
  echo "Runtime check:"
  PATH="$BIN_DIR:$TOOLS_DIR/node_modules/.bin:$PATH" "$HYPERFRAMES_BIN" doctor || true
else
  echo "HyperFrames CLI was not installed at $HYPERFRAMES_BIN" >&2
  exit 1
fi

cat <<EOF

User-space HyperFrames runtime is prepared.

Use this PATH before running HyperFrames commands in this project:

  export PATH="$BIN_DIR:$TOOLS_DIR/node_modules/.bin:\$PATH"

Then run:

  hyperframes doctor
  hyperframes lint
  hyperframes inspect
  hyperframes preview
  hyperframes render --output final.mp4
EOF
