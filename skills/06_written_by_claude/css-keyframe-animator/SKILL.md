---
name: css-keyframe-animator
description: Generate and validate CSS @keyframes animations — checking that every keyframe selector is well-formed, every animated property is actually animatable, and timing/easing choices match the intended motion feel. Use whenever the user asks for a CSS/HTML animation (hover effects, loading spinners, entrance transitions, micro-interactions) rather than a JS animation library.
---

# CSS Keyframe Animator

## Purpose
Hand-written CSS animations often break silently: animating a non-animatable property (like `display`), a typo'd percentage selector, or an easing curve that doesn't match the requested feel (e.g. "snappy" using `ease-in-out` instead of a sharp cubic-bezier). This skill validates the animation before shipping it.

## When to use
- User wants a pure CSS animation: hover states, loading spinners, entrance/exit transitions, attention-grabbers (pulse, shake, bounce).
- Lightweight micro-interactions where pulling in a JS animation library (GSAP, Framer Motion, anime.js — see those skills) would be overkill.

## Not for
- Complex sequenced/orchestrated timelines with dozens of steps — hand off to `gsap-scrolltrigger` or `motion-framer`.
- SVG path morphing — that needs JS (anime.js, GSAP) or SMIL, not plain CSS keyframes.

## Workflow

1. **Pick the motion vocabulary that matches intent.** Map feeling → easing:
   - "snappy / punchy" → `cubic-bezier(0.4, 0, 0.2, 1)` or steeper
   - "smooth / gentle" → `ease-in-out` or `cubic-bezier(0.65, 0, 0.35, 1)`
   - "bouncy / playful" → `cubic-bezier(0.68, -0.55, 0.265, 1.55)` (overshoot)
   - "mechanical / robotic" → `linear` or `steps(n)`

2. **Write the animation**, animating only compositor-friendly properties when possible (`transform`, `opacity`) for smooth 60fps performance — avoid animating `width`, `height`, `top`, `left`, `margin` when a `transform: translate/scale` will do the same job without triggering layout.

3. **Validate it** with the bundled checker before presenting it:
   ```bash
   python3 scripts/validate_keyframes.py path/to/styles.css
   ```
   This flags: non-animatable properties, missing `0%`/`100%` (or `from`/`to`) endpoints, keyframe percentages out of 0–100 range, and duplicate percentage selectors that silently override each other.

4. Fix anything flagged, then present the final CSS along with a one-line note on which properties are compositor-friendly (cheap) vs. layout-triggering (expensive), so the user knows the performance trade-off if they modify it later.

## Notes
- Always include `prefers-reduced-motion` handling for anything beyond a subtle fade/opacity change:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .thing { animation: none; }
  }
  ```
- Respect this even if not asked — accessibility for motion-sensitive users isn't optional.
