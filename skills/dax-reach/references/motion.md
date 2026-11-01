---
type: "Playbook"
title: "Purposeful Motion"
description: "Make relationships and state changes legible without hiding content or harming accessibility."
sources: [{"id":"impeccable-motion","resource":"https://github.com/pbakaus/impeccable/blob/4f956490f0056ae1ff5ea80372cf56e83c001d3c/skill/reference/animate.md"}]
reviewed_on: "2026-11-01"
---

# Purposeful Motion

Modified adaptation of Impeccable's animate workflow under Apache-2.0; see [licensing](LICENSE.txt). Engine-specific commands are replaced with the host's available tools.

State what the animation explains: a transformation, sequence, relationship, feedback, or change of state. Plan one focal sequence where justified, with quiet supporting motion. Specify the starting state, trigger, key frames, final state, replay/interruption behavior, and reduced-motion alternative. The intended outcome must still be understandable as a static composition.

Choose timing by distance and importance. Start with brief feedback and slightly longer transitions, then verify perceived responsiveness; timing ranges are design starting points, not universal standards. Use the existing CSS, Web Animations API, or motion library. Avoid introducing a new runtime for an effect the project already supports.

Prefer transforms and opacity for routine movement. Bound expensive masks, filters, shadows, or canvas effects to the focal region and measure actual performance. Avoid repeated layout reads/writes and broad permanent will-change hints. Clean up observers, listeners, and timers; stop nonessential loops offscreen and in hidden tabs.

Keep important text, links, and CTAs visible before scripts run. Scroll effects should clarify the content relationship, preserve ordinary scrolling, and have a fallback. On reduced motion, remove large spatial travel and parallax while preserving a legible final state and useful feedback. Provide appropriate pause/control behavior for ongoing automatic motion.

Verify initial load, partial scroll, fast scroll, reverse scroll, resize, repeated activation, interrupted transitions, touch, keyboard, and reduced motion. Inspect target devices or state the emulation limits. Record frame timing or performance evidence when available; never claim smooth 60 fps from a still screenshot.
