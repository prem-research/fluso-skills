#!/usr/bin/env node
import { existsSync, statSync } from "node:fs";
import { basename, resolve } from "node:path";
import { spawnSync } from "node:child_process";

function usage() {
  console.error(`Usage: node validate-render.mjs <video-file> [options]

Options:
  --expect-duration <seconds>
  --duration-tolerance <seconds>  default: 1
  --expect-width <pixels>
  --expect-height <pixels>
  --expect-fps <fps>
  --fps-tolerance <fps>           default: 0.5
  --require-audio
  --min-size <bytes>              default: 1024
`);
}

function parseArgs(argv) {
  const args = { file: null, requireAudio: false, minSize: 1024, durationTolerance: 1, fpsTolerance: 0.5 };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!args.file && !arg.startsWith("--")) {
      args.file = arg;
      continue;
    }
    if (arg === "--require-audio") {
      args.requireAudio = true;
      continue;
    }
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for ${arg}`);
    i += 1;
    if (arg === "--expect-duration") args.expectDuration = Number(value);
    else if (arg === "--duration-tolerance") args.durationTolerance = Number(value);
    else if (arg === "--expect-width") args.expectWidth = Number(value);
    else if (arg === "--expect-height") args.expectHeight = Number(value);
    else if (arg === "--expect-fps") args.expectFps = Number(value);
    else if (arg === "--fps-tolerance") args.fpsTolerance = Number(value);
    else if (arg === "--min-size") args.minSize = Number(value);
    else throw new Error(`Unknown option: ${arg}`);
  }
  if (!args.file) throw new Error("Missing video file");
  return args;
}

function which(command) {
  const result = spawnSync("bash", ["-lc", `command -v ${command}`], { encoding: "utf8" });
  return result.status === 0 ? result.stdout.trim() : null;
}

function parseRatio(value) {
  if (!value || typeof value !== "string") return null;
  const [left, right] = value.split("/").map(Number);
  if (!Number.isFinite(left)) return null;
  if (!Number.isFinite(right) || right === 0) return left;
  return left / right;
}

function probeWithFfprobe(file) {
  const ffprobe = process.env.FFPROBE || which("ffprobe");
  if (!ffprobe) return null;
  const result = spawnSync(ffprobe, [
    "-v", "error",
    "-print_format", "json",
    "-show_format",
    "-show_streams",
    file,
  ], { encoding: "utf8" });
  if (result.status !== 0) {
    throw new Error(`ffprobe failed: ${(result.stderr || result.stdout).trim()}`);
  }
  const data = JSON.parse(result.stdout);
  const video = (data.streams || []).find((stream) => stream.codec_type === "video");
  const audio = (data.streams || []).find((stream) => stream.codec_type === "audio");
  return {
    method: "ffprobe",
    duration: Number(data.format?.duration ?? video?.duration),
    width: Number(video?.width),
    height: Number(video?.height),
    fps: parseRatio(video?.avg_frame_rate || video?.r_frame_rate),
    hasAudio: Boolean(audio),
    videoCodec: video?.codec_name || null,
    audioCodec: audio?.codec_name || null,
  };
}

function probeWithFfmpeg(file) {
  const ffmpeg = process.env.FFMPEG || which("ffmpeg");
  if (!ffmpeg) throw new Error("Neither ffprobe nor ffmpeg was found on PATH");
  const result = spawnSync(ffmpeg, ["-hide_banner", "-i", file], { encoding: "utf8" });
  const output = `${result.stderr || ""}\n${result.stdout || ""}`;
  const durationMatch = output.match(/Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)/);
  const videoMatch = output.match(/Video:.*?(\d{2,5})x(\d{2,5}).*?(?:(\d+(?:\.\d+)?)\s*fps)?/);
  return {
    method: "ffmpeg",
    duration: durationMatch
      ? Number(durationMatch[1]) * 3600 + Number(durationMatch[2]) * 60 + Number(durationMatch[3])
      : null,
    width: videoMatch ? Number(videoMatch[1]) : null,
    height: videoMatch ? Number(videoMatch[2]) : null,
    fps: videoMatch?.[3] ? Number(videoMatch[3]) : null,
    hasAudio: /Audio:/i.test(output),
    videoCodec: null,
    audioCodec: null,
  };
}

function assertClose(failures, label, actual, expected, tolerance) {
  if (!Number.isFinite(expected)) return;
  if (!Number.isFinite(actual)) {
    failures.push(`${label} could not be determined`);
    return;
  }
  if (Math.abs(actual - expected) > tolerance) {
    failures.push(`${label} ${actual} does not match expected ${expected} (+/- ${tolerance})`);
  }
}

function assertEqual(failures, label, actual, expected) {
  if (!Number.isFinite(expected)) return;
  if (actual !== expected) failures.push(`${label} ${actual} does not match expected ${expected}`);
}

try {
  const args = parseArgs(process.argv);
  const file = resolve(args.file);
  if (!existsSync(file)) throw new Error(`Video file not found: ${file}`);
  const stat = statSync(file);
  const failures = [];
  if (!stat.isFile()) failures.push("path is not a file");
  if (stat.size < args.minSize) failures.push(`file is too small (${stat.size} bytes, expected at least ${args.minSize})`);

  const probe = probeWithFfprobe(file) || probeWithFfmpeg(file);
  assertClose(failures, "duration", probe.duration, args.expectDuration, args.durationTolerance);
  assertEqual(failures, "width", probe.width, args.expectWidth);
  assertEqual(failures, "height", probe.height, args.expectHeight);
  assertClose(failures, "fps", probe.fps, args.expectFps, args.fpsTolerance);
  if (args.requireAudio && !probe.hasAudio) failures.push("audio stream is required but missing");

  const summary = {
    file,
    name: basename(file),
    size_bytes: stat.size,
    ...probe,
    ok: failures.length === 0,
    failures,
  };
  console.log(JSON.stringify(summary, null, 2));
  process.exit(failures.length === 0 ? 0 : 1);
} catch (error) {
  usage();
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
