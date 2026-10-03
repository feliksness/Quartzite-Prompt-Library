---
name: image-gen-prompt-engineer
description: Structure a detailed, unambiguous prompt for AI image-generation models (Midjourney, DALL-E, Stable Diffusion, Gemini/Imagen, Flux) using a consistent subject/composition/lighting/style formula, and check it against common failure patterns before it's used. Use whenever the user wants help writing or improving a prompt for an image generator, regardless of which specific tool or API they're using.
---

# Image Generation Prompt Engineer

## Purpose
Vague prompts ("a cool logo", "a nice landscape") produce generic, inconsistent output. This skill turns a loose idea into a structured prompt that specifies exactly what a generation model needs to be consistent and controllable — and checks the draft against known failure patterns (banned/ambiguous terms, missing aspect ratio, conflicting style cues) before handing it off.

## When to use
- User wants to generate an image via any AI image tool/API and needs prompt help.
- User has a prompt that isn't producing what they want and wants it debugged.
- Not for actually calling an image-generation API — that depends on which tool/MCP/connector is available; this skill only produces the prompt text (and, if useful, the parameter recommendations like aspect ratio/negative prompt).

## The 5-part formula
Every prompt should specify, in this order:
1. **Subject** — what/who, with concrete distinguishing detail (not just "a woman" — "a woman in her 60s with silver hair, weathered hands").
2. **Action/pose** — what's happening, not just a static noun.
3. **Setting/context** — where, when, environment.
4. **Composition** — camera angle, framing, shot type (close-up / wide shot / bird's-eye), rule-of-thirds placement.
5. **Style & lighting** — medium (photo/illustration/3D render), art movement or reference style, lighting quality (golden hour, studio softbox, harsh noon sun).

## Workflow

1. Ask (or infer from context) what the image is *for* — this determines aspect ratio and level of realism needed (a hero banner needs different composition than a square social post or an icon).

2. Draft the prompt following the 5-part formula above. Be concrete and visual — describe what a camera would see, not abstract concepts ("innovation," "synergy" don't render).

3. **Check the draft** against common failure patterns:
   ```bash
   python3 scripts/check_prompt.py "your prompt text here"
   ```
   This flags: conflicting style keywords (e.g. "photorealistic" + "cartoon" together), missing composition/framing info, overly abstract nouns with nothing visual to render, and vague quantity words ("some", "a few") that generation models handle inconsistently.

4. If targeting a specific platform, adapt syntax: Midjourney uses `--ar`, `--style`, `--no` (negative) flags; most others take a plain negative-prompt parameter instead of inline flags. Don't mix syntaxes.

5. For a character/subject that must stay visually consistent across multiple generations, write down the fixed descriptive details (exact clothing, features, palette) once and reuse that exact phrasing in every subsequent prompt rather than re-describing loosely each time.

## Notes
- Never fabricate a claim that a specific real, named public figure is depicted — keep subjects generic/fictional unless the user has explicit rights to generate a real person's likeness.
- If the platform in use is a connected tool (MCP/connector), the prompt built here is the input to that tool, not a replacement for it.
