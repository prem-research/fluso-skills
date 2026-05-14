---
name: hyperframes
description: Create, edit, validate, preview, and render HTML-based videos with HyperFrames. Use when the user wants product videos, social clips, animated explainers, captions, overlays, transitions, data videos, website-to-video drafts, or any video made with HTML, CSS, and JavaScript.
labels:
  - Content
  - Marketing
---

# HyperFrames

HyperFrames turns HTML, CSS, and JavaScript into video. Use it when the user wants a renderable video project, not just a storyboard or script.

This skill follows the official HyperFrames skill guidance from `heygen-com/hyperframes/skills/hyperframes`, adapted for Fluso's workspace runtime. Keep the upstream authoring discipline, but keep the runtime loop bounded and fast.

The source of truth is a project folder with `index.html`, optional `compositions/`, and optional `assets/`. The fast dev loop is HyperFrames-native:

```bash
bash skills/hyperframes/scripts/setup-hyperframes-runtime.sh <project-dir>
source <printed-env-file>
hyperframes init <project-name> --non-interactive --example blank --skip-skills
hyperframes lint <project-dir>
hyperframes validate <project-dir>
timeout 90s hyperframes snapshot <project-dir> --frames 5
timeout 90s hyperframes inspect <project-dir> --samples 5
(cd <project-dir> && timeout 300s hyperframes render --quality draft --fps 24 --workers 1 --no-browser-gpu --output <file>.mp4)
node skills/hyperframes/scripts/validate-render.mjs <file>.mp4 --expect-duration <seconds> --expect-width <w> --expect-height <h> --expect-fps 24
```

This skill is allowed to prepare user-space runtime dependencies when needed. Do not block the workflow just because a dependency is not preinstalled. Try the user-space setup path first.

## Execution Contract

Use HyperFrames CLI as the default and preferred path for scaffolding, preview, snapshot, inspection, and rendering.

- Do not use Puppeteer, Playwright, Selenium, manual PNG frame capture, or custom renderers unless the user explicitly approves that fallback.
- If the user says "HyperFrames CLI only", treat that as a hard boundary. If the CLI cannot render, report the blocker and stop instead of switching tools.
- Never claim a video was rendered until the MP4/WebM exists and passes `validate-render.mjs` or equivalent `ffprobe` validation.
- Distinguish clearly between `project ready`, `preview available`, `draft rendered`, and `final rendered`.
- A video with no audio is a `silent draft` unless the user explicitly requested no audio.

## Recommended Fast Path

Start with the shortest HyperFrames-native path that can produce a reviewable result, then deepen quality after the draft is visible.

- For first drafts, prefer `1280x720`, `24fps`, `--quality draft`, and `--workers 1`.
- Prefer `--skip-skills` when scaffolding because this Fluso skill already provides the guidance.
- Prefer `snapshot --frames 5` before full render. If snapshot cannot launch the browser, render will likely fail too.
- Prefer `inspect --samples 5` for a first pass. Increase samples only after the draft render path is working.
- For a 30-60 second video, 4-6 clean scenes is usually enough. Add complexity when the brief needs it.
- Use final settings such as `1920x1080`, `30fps`, `--quality standard`, or `--quality high` after the draft has passed validation or when the user asks for final output.

## Runtime Exploration Budget

The goal is not to forbid exploration. The goal is to avoid spending most of the task on environment debugging before the video exists.

- First author the project and make it lint/validate clean. A previewable project is useful even if rendering later needs runtime work.
- If `snapshot`, `inspect`, or `render` hangs or Chrome/Chromium fails to launch, make at most 2 targeted attempts using the setup helper, `hyperframes browser ensure`, cache env vars, lower FPS, lower quality, or fewer workers.
- Avoid Debian package research, `apt`/`dpkg`, browser library symlink experiments, shared-library downloads, or manual Chrome patching inside Fluso unless the user explicitly asks for deep runtime debugging.
- If the native HyperFrames path is blocked, report the blocker and offer options: keep the previewable project, try a smaller/slower draft, spend more time on runtime setup, or use a custom rendering fallback.
- Treat linter warnings as repair targets when they affect render, layout, or visible quality. Do not spend long loops on non-blocking warnings after the video already validates and renders.

## Before Building

For open-ended requests, ask only for missing essentials:

- Purpose and audience
- Duration
- Format: `16:9`, `9:16`, or `1:1`
- Brand direction, colors, fonts, or reference assets
- Whether narration, captions, music, screenshots, or source footage are needed

For specific edits, read the existing HyperFrames files first and change only what was requested.

## Planning Before Code

Do not jump straight from a vague prompt to HTML. For new multi-scene videos, create a short internal plan first:

- Visual identity: use `design.md` or `DESIGN.md` when present. If missing, infer a compact mood, palette, type direction, and motion tone from the user request.
- Narrative arc: define what the viewer should understand by the end.
- Scene rhythm: name the pacing pattern, such as `hook-build-peak-breathe-cta` or `slow-build-BUILD-PEAK-resolve`.
- Beat direction: for each scene, describe the visual world, foreground/midground/background layers, and the motion verb for important elements.
- Transition plan: decide how each scene hands off to the next before writing timelines.

Build what the user asked for. Do not add extra scenes, audio, narration, or complex effects unless they clearly improve the requested video or the user asked for them.

## Upstream Quality References

This skill bundles upstream HyperFrames guidance for higher-quality output. Read selectively; do not load every file by default.

Always read these before a new multi-scene composition:

- `references/video-composition.md` for video-scale density, color, type, and frame composition.
- `references/beat-direction.md` for scene rhythm, beat direction, and transition planning.
- `references/typography.md` for font pairing, size, readability, and text treatment.
- `references/motion-principles.md` for GSAP motion quality and image/video movement.
- `references/transitions.md` plus `references/transitions/catalog.md` for scene handoffs.

Read these when relevant:

- `house-style.md`, `visual-styles.md`, and `palettes/*.md` when the user has not provided a visual identity.
- `references/prompt-expansion.md` for open-ended briefs that need a clearer creative direction before implementation.
- `references/techniques.md` for richer visual techniques such as SVG drawing, kinetic type, canvas, CSS 3D, or motion paths.
- `patterns.md` for title cards, picture-in-picture, slideshows, and common structure patterns.
- `data-in-motion.md` for stats, charts, KPIs, and infographic-style scenes.
- `references/captions.md`, `references/dynamic-techniques.md`, and `references/transcript-guide.md` when working with subtitles, transcripts, karaoke captions, or lyric-style timing.
- `references/audio-reactive.md` and `references/narration.md` when the brief includes music, voiceover, audio sync, or TTS.
- `references/css-patterns.md` for marker highlights, circles, burst lines, sketch effects, and animated emphasis.
- `references/design-picker.md` and `templates/design-picker.html` only when the user wants to visually choose a design direction.

## Runtime Setup

Use system tools when they already exist, but prefer user-space setup for missing tools. Fluso usually does not provide `sudo`, `apt`, Docker, or root-level installation, so treat those as unavailable unless the current runtime clearly supports them or the user explicitly asks for that investigation.

Run the bundled setup helper once per workspace/project. It prepares pinned user-space HyperFrames/FFmpeg tooling in a shared cache when possible and prints an environment file to source:

```bash
bash skills/hyperframes/scripts/setup-hyperframes-runtime.sh <project-dir>
source <printed-env-file>
```

The helper reuses existing system tools when available. It installs missing user-space packages under a shared versioned tool cache, not inside every generated video project. It does not install system packages or patch browser libraries.

For render-capable work, use the official HyperFrames browser manager before rendering:

```bash
HYPERFRAMES_ENSURE_BROWSER=1 bash skills/hyperframes/scripts/setup-hyperframes-runtime.sh <project-dir>
source <printed-env-file>
timeout 60s hyperframes doctor --json
```

Expected requirements for local rendering:

- Node.js 22 or newer and npm
- HyperFrames CLI
- Chrome or a HyperFrames-managed browser for preview/inspection/rendering
- FFmpeg for final MP4/WebM rendering
- FFprobe or `validate-render.mjs` fallback metadata parsing for output validation

If `doctor --json` reports missing Chrome/browser or FFmpeg after setup, continue authoring when useful, but clearly say final rendering is blocked by the remaining runtime issue.

Keep first-use expectations honest: installing HyperFrames packages and a browser can add hundreds of MB of cache and several minutes on a cold runtime.

## Authoring Rules

Every composition must follow these rules:

- Root composition includes `data-composition-id`, `data-start="0"`, `data-width`, and `data-height`.
- Timed visual clips include a unique `id`, `class="clip"`, `data-start`, `data-duration`, and `data-track-index`.
- Use `data-track-index` for timing lanes only. It does not control visual depth.
- Use CSS `z-index` for visual layering. `data-track-index` is timing/track metadata, not visual depth.
- Videos must be `muted playsinline`. If video audio is needed, add a separate `<audio>` element.
- GSAP timelines must be `paused: true` and registered on `window.__timelines["<composition-id>"]`.
- Avoid `Math.random()`, `Date.now()`, wall-clock timers, async timeline construction, and infinite repeats.
- Do not call `play()`, `pause()`, or manual seek on media. HyperFrames controls playback.
- Use `data-duration`, not `data-end`.
- Do not use a `<template>` wrapper for the standalone `index.html` root composition. Use templates only for sub-compositions.
- If pseudo-randomness is needed, use a seeded deterministic generator.
- Do not animate `visibility` or `display`. Animate visual properties such as opacity, transform, color, and blur.
- Avoid `repeat: -1`. Use a finite repeat count calculated from the composition duration.

## Layout Quality

Build the hero frame first, then animate into it.

- Position each scene at its most visible moment using static HTML/CSS first. Then use `gsap.from()` entrances to animate into those positions.
- Make the main scene container fill the canvas with `width: 100%`, `height: 100%`, `box-sizing: border-box`, and responsive padding.
- Prefer flex/grid layout for real content. Use absolute positioning mainly for decorative layers.
- Keep titles, captions, labels, and cards inside safe margins.
- Use video-scale typography: large readable headlines, clear body text, and enough contrast.
- Let text wrap naturally with `max-width`. Avoid forced `<br>` unless the line breaks are part of the visual design.
- If content is dynamic, use variables and fit text rather than hard-coding fragile sizes.

## Visual Quality

Video frames are not web pages. Do not make a sparse web layout and call it a video.

- Every scene needs background texture, midground content, and foreground accents.
- Use visible color presence. Muted is fine; flat or invisible is not.
- Scale up for video: headlines usually `64px+`, body text `28px+`, labels `18px+`.
- Add ambient motion to decorative elements. Static decor should be intentional.
- Use two or more focal points in rich scenes so the eye can travel.
- Anchor important content to zones and edges when useful. Avoid default centered stacks for every scene.
- Avoid full-screen linear gradients on dark backgrounds because they band badly in H.264. Prefer radial light, texture, grain, local glow, or structured panels.

## Scene Transitions

Multi-scene videos need deliberate transitions. A sequence of hard jumps usually feels unfinished.

- Use transitions between scenes unless the user explicitly asks for hard cuts or the edit is intentionally percussive.
- Give every scene entrance animations. Elements should not simply appear fully formed.
- Do not fade out every outgoing scene before the transition. Let the transition carry the handoff unless it is the final scene.
- For final scenes, a fade to black or fade out is acceptable.
- Match transition style to energy: CSS blur/whip/zoom for connective motion; shader transitions for hero reveals or major energy shifts.

## Workflow

1. Clarify the brief and choose the canvas size.
2. Decide audio status. If the user did not ask for narration/music, produce a `silent draft` and say that explicitly.
3. Prepare the runtime once and source the printed env file.
4. Scaffold a project with HyperFrames when possible:

   ```bash
   hyperframes init <project-name> --non-interactive --example blank --skip-skills
   ```

5. Write or edit the composition HTML, CSS, assets, and timeline.
6. Validate structure and browser smoke before rendering:

   ```bash
   hyperframes lint <project-dir>
   hyperframes validate <project-dir>
   timeout 90s hyperframes snapshot <project-dir> --frames 5
   timeout 90s hyperframes inspect <project-dir> --samples 5
   ```

7. Preview for the user when useful:

   ```bash
   (cd <project-dir> && hyperframes preview --port <free-port>)
   ```

8. Render a draft only after validation and snapshot succeed:

   ```bash
   (cd <project-dir> && timeout 300s hyperframes render --quality draft --fps 24 --workers 1 --no-browser-gpu --output draft.mp4)
   node skills/hyperframes/scripts/validate-render.mjs draft.mp4 --expect-duration <seconds> --expect-width <w> --expect-height <h> --expect-fps 24
   ```

Use `--quality standard`, `--quality high`, `30fps`, or `1920x1080` only for final output after the draft path has already worked.

## Advanced Quality Checks

For substantial new compositions, use the bundled quality scripts after `lint`, `validate`, and `inspect` pass:

```bash
node skills/hyperframes/scripts/animation-map.mjs <project-dir> --out <project-dir>/.hyperframes/anim-map
node skills/hyperframes/scripts/contrast-report.mjs <project-dir> --out <project-dir>/.hyperframes/contrast
```

If helper packages are missing, prefer the normal HyperFrames CLI checks first. Only allow script dependency bootstrap when the project already has HyperFrames tooling available and the extra report is worth the time.

Read the generated reports. Fix unexpected offscreen elements, collisions, invisible text, dead animation zones, and contrast warnings before calling the video production-ready.

## Variables and Editability

When the user may want to revise text, colors, or content later, expose the important inputs as HyperFrames variables:

- Declare variables on the root `<html>` with `data-composition-variables`.
- Read them once with `window.__hyperframes.getVariables()`.
- Provide sensible defaults so preview works without CLI overrides.
- Use `--strict-variables` for final validation when variable overrides are involved.

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
- If `doctor` still reports missing FFmpeg, FFprobe, Chrome, or browser setup after user-space setup, do not claim an MP4 was rendered.
- If HyperFrames browser setup or browser launch fails, keep the project previewable and report the browser/runtime blocker. Use a custom renderer only when the user chooses that fallback or the task explicitly prioritizes a rendered file over the native HyperFrames path.
- If `lint`, `validate`, or `inspect` fails, fix the HTML/CSS/timing before previewing as final.
- If assets are missing, use clearly named placeholders only when the user agrees or the placeholders are part of a draft.
- If rendering is slow or memory-heavy, reduce duration, resolution, FPS, worker count, or quality before retrying.
- If a render leaves a corrupt, tiny, wrong-duration, wrong-resolution, or partial output file, delete or quarantine it and report that no valid video was produced.

## Output Contract

When finished, report:

- Project directory
- Preview URL, if a preview server is running
- Rendered file path, only if render succeeded and validation passed
- Duration, resolution, FPS, file size, and audio status (`silent draft` or audio present)
- Validation commands run and their results
- Draft/final status
- Any unresolved blockers, especially missing FFmpeg, Chrome/browser, network access, or assets

Useful references:

- HyperFrames docs: https://hyperframes.heygen.com/introduction
- Quickstart: https://hyperframes.heygen.com/quickstart
- CLI reference: https://hyperframes.heygen.com/packages/cli
- Official upstream skill source: https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes
