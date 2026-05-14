#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "${1:-.}" && pwd)"
HYPERFRAMES_VERSION="${HYPERFRAMES_VERSION:-0.6.6}"
FFMPEG_STATIC_VERSION="${FFMPEG_STATIC_VERSION:-5.3.0}"

if [ -n "${HYPERFRAMES_TOOLS_ROOT:-}" ]; then
  TOOLS_ROOT="${HYPERFRAMES_TOOLS_ROOT%/}"
elif [ -d "/fluso/user" ] && [ -w "/fluso/user" ]; then
  TOOLS_ROOT="/fluso/user/.runtime/tools/hyperframes"
elif [ -n "${HOME:-}" ] && [ -w "$HOME" ]; then
  TOOLS_ROOT="$HOME/.runtime/tools/hyperframes"
else
  TOOLS_ROOT="${PROJECT_DIR%/}/.hyperframes-tools"
fi

TOOLS_DIR="$TOOLS_ROOT/$HYPERFRAMES_VERSION"
BIN_DIR="$TOOLS_DIR/bin"
NODE_MODULES_BIN="$TOOLS_DIR/node_modules/.bin"
ENV_FILE="$TOOLS_DIR/env.sh"

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
  packages+=("hyperframes@$HYPERFRAMES_VERSION")
fi

SYSTEM_FFMPEG=""
if command -v ffmpeg >/dev/null 2>&1; then
  SYSTEM_FFMPEG="$(command -v ffmpeg)"
  ln -sf "$SYSTEM_FFMPEG" "$BIN_DIR/ffmpeg"
  echo "Using system ffmpeg at $SYSTEM_FFMPEG"
elif [ ! -d "$TOOLS_DIR/node_modules/ffmpeg-static" ]; then
  packages+=("ffmpeg-static@$FFMPEG_STATIC_VERSION")
fi

if command -v ffprobe >/dev/null 2>&1; then
  ln -sf "$(command -v ffprobe)" "$BIN_DIR/ffprobe"
  echo "Using system ffprobe at $(command -v ffprobe)"
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
else
  echo "HyperFrames CLI was not installed at $HYPERFRAMES_BIN" >&2
  exit 1
fi

if [ -d "/fluso/user" ] && [ -w "/fluso/user" ]; then
  RUNTIME_HOME="/fluso/user"
else
  RUNTIME_HOME="${HOME:-$PROJECT_DIR}"
fi
RUNTIME_CACHE="${XDG_CACHE_HOME:-$RUNTIME_HOME/.cache}"
mkdir -p "$RUNTIME_CACHE" "$RUNTIME_HOME/.config"

cat > "$ENV_FILE" <<EOF
export PATH="$BIN_DIR:$NODE_MODULES_BIN:\$PATH"
export HOME="$RUNTIME_HOME"
export XDG_CACHE_HOME="$RUNTIME_CACHE"
export PUPPETEER_CACHE_DIR="$RUNTIME_CACHE/puppeteer"
export HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_NO_TELEMETRY=1
EOF

if [ "${HYPERFRAMES_ENSURE_BROWSER:-0}" = "1" ]; then
  echo "Ensuring HyperFrames-managed browser with official CLI..."
  # This may download a browser. Keep it bounded and report blockers instead of patching system libraries.
  timeout "${HYPERFRAMES_BROWSER_TIMEOUT:-180s}" bash -c "source '$ENV_FILE' && '$HYPERFRAMES_BIN' browser ensure"
fi

cat <<EOF

User-space HyperFrames runtime is prepared.

Use this environment before running HyperFrames commands:

  source "$ENV_FILE"

Then run:

  hyperframes --version
  hyperframes doctor --json
  hyperframes lint "$PROJECT_DIR"
  hyperframes snapshot "$PROJECT_DIR" --frames 3
  (cd "$PROJECT_DIR" && hyperframes render --output final.mp4)

Browser runtime is prepared by HyperFrames itself with:

  HYPERFRAMES_ENSURE_BROWSER=1 bash skills/hyperframes/scripts/setup-hyperframes-runtime.sh "$PROJECT_DIR"

If browser launch still fails, report the runtime blocker instead of installing system libraries manually.
EOF
