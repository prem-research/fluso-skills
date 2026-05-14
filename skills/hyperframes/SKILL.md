---
name: hyperframes
description: Create, edit, validate, preview, and render HTML-based videos with HyperFrames. Use when the user wants product videos, social clips, animated explainers, captions, overlays, transitions, data videos, website-to-video drafts, or any video made with HTML, CSS, and JavaScript.
labels:
  - Content
  - Marketing
---

# HyperFrames

HyperFrames turns HTML, CSS, and JavaScript into video. Use it when the user wants a renderable video project, not just a storyboard or script.

The source of truth is a project folder with `index.html`, optional `compositions/`, and optional `assets/`. The normal dev loop is:

```bash
npx --yes hyperframes init <project-name> --non-interactive --example blank
npx --yes hyperframes lint
npx --yes hyperframes inspect
npx --yes hyperframes preview
npx --yes hyperframes render --output <file>.mp4
```

This skill is allowed to prepare user-space runtime dependencies when needed. Do not block the workflow just because a dependency is not preinstalled. Try the user-space setup path first.

## Before Building

For open-ended requests, ask only for missing essentials:

- Purpose and audience
- Duration
- Format: `16:9`, `9:16`, or `1:1`
- Brand direction, colors, fonts, or reference assets
- Whether narration, captions, music, screenshots, or source footage are needed

For specific edits, read the existing HyperFrames files first and change only what was requested.

## Runtime Setup

Use system tools when they already exist, but prefer user-space setup for missing tools. Never use `sudo`, `apt`, Docker setup, or root-level installation unless the user explicitly asks for it.

If HyperFrames, FFmpeg, or the browser runtime is missing, run the bundled setup helper from the installed skill folder:

```bash
bash skills/hyperframes/scripts/setup-hyperframes-runtime.sh <project-dir>
export PATH="<project-dir>/.hyperframes-tools/bin:<project-dir>/.hyperframes-tools/node_modules/.bin:$PATH"
```

The helper installs `hyperframes` and `ffmpeg-static` with npm under `<project-dir>/.hyperframes-tools`, then asks HyperFrames to prepare its managed browser runtime when available. This is intentionally user-space and project-local.

After setup, check the environment:

Run:

```bash
node --version
npm --version
hyperframes doctor
```

Expected requirements:

- Node.js 22 or newer
- npm or npx
- Chrome or a HyperFrames-managed browser for preview/inspection/rendering
- FFmpeg for final MP4/WebM rendering

If setup still cannot provide FFmpeg or Chrome, continue creating/editing the project when useful, but clearly say final rendering is blocked by the remaining runtime issue.

## Authoring Rules

Every composition must follow these rules:

- Root composition includes `data-composition-id`, `data-start="0"`, `data-width`, and `data-height`.
- Timed visual clips include a unique `id`, `class="clip"`, `data-start`, `data-duration`, and `data-track-index`.
- Use CSS `z-index` for visual layering. `data-track-index` is timing/track metadata, not visual depth.
- Videos must be `muted playsinline`. If video audio is needed, add a separate `<audio>` element.
- GSAP timelines must be `paused: true` and registered on `window.__timelines["<composition-id>"]`.
- Avoid `Math.random()`, `Date.now()`, wall-clock timers, async timeline construction, and infinite repeats.
- Do not call `play()`, `pause()`, or manual seek on media. HyperFrames controls playback.
- Use `data-duration`, not `data-end`.
- Do not use a `<template>` wrapper for the standalone `index.html` root composition. Use templates only for sub-compositions.

## Layout Quality

Build the hero frame first, then animate into it.

- Make the main scene container fill the canvas with `width: 100%`, `height: 100%`, `box-sizing: border-box`, and responsive padding.
- Prefer flex/grid layout for real content. Use absolute positioning mainly for decorative layers.
- Keep titles, captions, labels, and cards inside safe margins.
- Use video-scale typography: large readable headlines, clear body text, and enough contrast.
- Let text wrap naturally with `max-width`. Avoid forced `<br>` unless the line breaks are part of the visual design.
- If content is dynamic, use variables and fit text rather than hard-coding fragile sizes.

## Workflow

1. Clarify the brief and choose the canvas size.
2. Scaffold a project with HyperFrames when possible.
3. Write or edit the composition HTML, CSS, assets, and timeline.
4. Validate structure and layout:

   ```bash
   hyperframes lint
   hyperframes inspect --samples 15
   ```

5. Preview for the user:

   ```bash
   hyperframes preview --port <free-port>
   ```

6. Render only after validation is clean:

   ```bash
   hyperframes render --quality standard --output final.mp4
   ```

Use `--quality draft` for quick iteration and `--quality high` only for final output.

## Website-to-Video

When the user wants a video from a website:

1. Capture the user's goal, audience, duration, and format.
2. Inspect the website for brand, product visuals, and key claims.
3. Create a short script and scene plan before authoring.
4. Build the HyperFrames composition with the site's visual language, not a generic template.
5. Validate layout and render only after the user has reviewed the direction.

## Registry Blocks

Use HyperFrames registry blocks when they save real time:

```bash
hyperframes add data-chart
hyperframes add flash-through-white
hyperframes add instagram-follow
```

After adding a block or component, read the generated files and wire them into the composition deliberately. Do not paste snippets blindly.

## Failure Handling

- If HyperFrames packages cannot download, explain the network/package-manager blocker and keep the project files ready.
- If `doctor` still reports missing FFmpeg after user-space setup, do not claim an MP4 was rendered.
- If `lint` or `inspect` fails, fix the HTML/CSS/timing before previewing as final.
- If assets are missing, use clearly named placeholders only when the user agrees or the placeholders are part of a draft.
- If rendering is slow or memory-heavy, reduce duration, resolution, FPS, worker count, or quality before retrying.

## Output Contract

When finished, report:

- Project directory
- Preview URL, if a preview server is running
- Rendered file path, if render succeeded
- Validation commands run and the result
- Any unresolved blockers, especially missing FFmpeg, Chrome/browser, network access, or assets

Useful references:

- HyperFrames docs: https://hyperframes.heygen.com/introduction
- Quickstart: https://hyperframes.heygen.com/quickstart
- CLI reference: https://hyperframes.heygen.com/packages/cli
