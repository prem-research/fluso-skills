---
name: podcast-production
description: End-to-end podcast planning, scripting, audio generation, show notes, and publishing support. Use when the user asks to create, plan, script, produce, edit, or package a podcast episode or recurring podcast workflow.
labels:
  - Content
---

# Podcast Production

Use this skill to turn a podcast idea, transcript, outline, or source material into a production-ready episode package. Support planning, scripts, host notes, guest questions, synthesized audio drafts, show notes, titles, descriptions, chapters, and social snippets.

Prefer Fluso's existing audio capability for audio rendering. Do not install local TTS models, browser renderers, FFmpeg bundles, Torch, CUDA, or other heavy audio/video stacks unless the user explicitly asks for deeper production tooling.

## Core Workflow

1. **Clarify the episode goal.** Identify audience, format, tone, target duration, host/guest setup, and whether the user wants audio output now or only production materials.
2. **Create the production folder.** Save files under `podcasts/<episode-slug>/` inside the active project directory.
3. **Build the episode package.** Produce the relevant files:
   - `brief.md` — audience, goal, angle, tone, constraints, and open questions.
   - `outline.md` — segment-by-segment structure with approximate timing.
   - `script.md` — host-ready script or talking points.
   - `guest-questions.md` — if there is an interview guest.
   - `show-notes.md` — summary, links, credits, and listener takeaways.
   - `chapters.md` — timestamp-style chapters based on the planned timing.
   - `social-posts.md` — short launch copy for LinkedIn, X, newsletter, or community posts.
4. **Render audio when requested.** Use the `audio` tool with `action: "synthesize"` for clean voice drafts. Split long scripts into natural segments before synthesis, and save outputs with clear names such as `podcasts/<episode-slug>/audio/segment-01.wav` or `podcasts/<episode-slug>/audio/intro.wav`.
5. **Review and iterate.** Clearly separate `draft audio` from `final audio`. Ask for approval before presenting an episode as final.

## Audio Rules

- Use the `audio` tool only when audio service is available. If it is missing, keep the full script and production package ready, then report that audio rendering is blocked by unavailable TTS.
- Keep synthesized segments short enough to be reviewable and easy to regenerate. Prefer intro, segment bodies, ad breaks, and outro as separate files.
- Do not silently invent a voice identity. If the user does not specify voice/tone, use a neutral host voice in the script and let the configured audio service choose its default voice.
- For multi-speaker podcasts, generate separate labeled script sections first. Only synthesize after the user confirms the speaker plan.
- Save generated audio inside the episode folder so the Files sidebar can surface it with the rest of the package.

## Production Guidance

- Start with a strong hook in the first 20 seconds.
- Keep paragraphs short for spoken delivery. Rewrite dense text into natural speech before synthesis.
- Mark pauses, emphasis, and transitions in plain language, not complex SSML, unless the configured audio service supports it and the user asks for it.
- Use timestamps as planning estimates until real audio duration is known.
- For source-based episodes, preserve attribution and list sources in `show-notes.md`.
- For interview episodes, prioritize question flow: context, problem, story, evidence, practical advice, closing reflection.
- For solo episodes, prioritize narrative flow: hook, promise, context, main points, example, takeaway, call to action.

## Quality Check

Before finishing, verify:

- The episode has a clear listener promise.
- The script sounds natural when read aloud.
- Show notes are useful without exposing private planning notes.
- Audio files, if generated, exist at the paths reported to the user.
- Any missing audio capability, source material, or publishing requirement is called out plainly.
