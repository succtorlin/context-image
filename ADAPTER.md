# Adapter — operational rules for `context-image`

Upstream ([`op7418/guizang-material-illustration`](https://github.com/op7418/guizang-material-illustration)) targets a Chinese-language workflow and an `imagegen` skill that does not exist in most installs. This file supplies the missing operational layer: a real image backend, English label limits measured against a real model, and a mandatory proofread step. Upstream rules govern everything not overridden here.

Sections 1 and 4 contain machine- and brand-specific values (a credential path, a palette). Treat those as worked examples and substitute your own.

---

## 1. Image backend routing (overrides SKILL.md step 8)

There is no `imagegen` skill on this machine. Use this ladder instead.

**Selection rule: labels render inside the image, so text fidelity decides the model.** GPT-Image and Gemini image models render embedded text reliably; FLUX historically garbles it. Never pick a backend on speed or cost when the illustration carries labels.

| Priority | Skill | Backend | Reach for it when |
|---|---|---|---|
| 1 | `baoyu-image-gen` | OpenAI / Google / DashScope, `scripts/main.ts` | Default. Explicit aspect-ratio flags and reference-image support — matches this skill's reference-gathering step directly. |
| 2 | `generate-image` | OpenRouter (Gemini 3.1 Flash Image, FLUX.2 Pro) | Fallback. **Select the Gemini image model, not FLUX**, whenever the illustration has labels. |
| 3 | `gemini-image` | Gemini via `config/secrets.md` | Image-to-image work: pass reference URLs ahead of the prompt text. |

### Chosen route: `baoyu-image-gen` on OpenAI (decided 2026-08-08)

Credential lives in `~/.baoyu-skills/.env` as `OPENAI_API_KEY` (skill-scoped, `chmod 600`, never in shell history or a repo). Load priority is `CLI args > EXTEND.md > env vars > ~/.baoyu-skills/.env`.

Invocation shape — **always pass the prompt as a file**, because this skill's prompts are long and structured, and `--prompt` mangles multi-line text:

```bash
SKILL_DIR=~/.claude/skills/baoyu-image-gen
npx -y bun $SKILL_DIR/scripts/main.ts \
  --promptfiles <prompt>.md \
  --image <name>.png \
  --provider openai \
  --ar 16:9 \
  --quality 2k
```

Flag rules for this skill:

- `--provider openai` **explicitly**, every time. Auto-selection defaults to Google when multiple keys exist; do not let a future Google key silently change the model mid-project.
- `--ref` (reference images, used by the reference-gathering step) requires a GPT Image model on OpenAI: add `--model gpt-image-1.5`.
- `--quality 2k` is the default and is correct for illustrations. Drop to `normal` only for throwaway previews.
- Aspect ratio by destination: `16:9` slides and landing bands · `4:3` docs and reports · `3:4` social cards · `1:1` avatars and icons.
- Generation is sequential by default. Keep it that way — parallel only on explicit request, since regeneration-on-QA-failure is the normal path here.

If the key is missing or the call fails auth, **stop at step 7 and deliver the prompt plan** — written prompts, labels, aspect ratio, style block — and say plainly that generation did not run. Never present an ungenerated plan as a finished deliverable.

> A Gemini key exists in `web-app/.env.local` for the ScheduleOpt app's text calls. It is a project secret scoped to that app. Do not copy it into a global skill config.

## 2. Label language (overrides SKILL.md "Text Rules")

Upstream mandates Chinese labels at 2–5 characters. Follow that **only when the deliverable is Chinese**. For English deliverables the equivalent density is:

- **1–3 words per label.** Two separate ceilings, measured on GPT Image (2026-08-08, four renders):
  - **Floating callouts** on quiet background: up to ~14 characters render cleanly. "Schedule data", "Metrics layer", "Provost view" were all correct every time.
  - **Text printed ON an object** (plate, badge, card, chip): **10 characters is the safe ceiling.** At 12 characters it fails. Measured: `Balance` (7) ✓, `Bottlenecks` (11) ✓, `Misalignment` (12) → rendered **"Misaiignment"**, the `l` silently substituted by `i`.
  - When a concept needs a longer word on an object, split it across two lines, abbreviate it, or move it to a floating callout.
- **Every render must be proofread under magnification** — the failure is silent and invisible at full size. This is a mandatory step, not advice: see §3.
- Prefer concrete nouns and verb phrases over abstract stage names: `Draft term` / `Review` / `Publish`, not `Input phase` / `Processing phase`.
- Sentence case for labels. Reserve ALL-CAPS for the mono eyebrow only (see §4).
- Keep explanatory sentences **outside** the image whenever a surrounding layout exists (card, slide, doc). Inside the image: labels on objects and flows, nothing more.
- Mixed-language decks: pick one language per image set. Never mix inside a single illustration.

Everything else in upstream's Text Rules still applies — no dense in-image legends, distinct label positions if the model struggles, short before clever.

## 3. Post-render proofread (overrides SKILL.md step 9 — MANDATORY)

Upstream step 9 says "inspect each image." That is not enough. **Baked-in text fails silently**: the model substitutes a letter, and at full size the word still looks right. Measured on this machine — a prompt demanding `Misalignment` rendered `Misaiignment`, and it passed a full-size eyeball check.

Never declare a render finished on a full-size look. Run this instead:

```bash
python3 ~/.claude/skills/context-image/scripts/proofread.py OUT.png
```

It slices the image into overlapping upscaled tiles and prints their paths. **Read every tile** and compare each label character-by-character against the exact strings the prompt specified. Useful flags:

- `--band 0.42 0.65` — restrict to one horizontal strip when you know where the text sits (cheapest; two tiles usually suffice)
- `--grid 3x2 --zoom 3` — finer slicing for small or dense lettering
- Default `--grid 2x2 --zoom 2` covers a whole 16:9 render in four tiles

**Check on every tile, in this order:**

1. **Spelling of every baked-in word**, letter by letter. Watch `l`↔`i`, `rn`↔`m`, doubled letters. Longest word first — that is where it breaks.
2. **Invented content.** Any number, percentage, unit, axis value, or caption the prompt did not explicitly ask for is a defect, regardless of how plausible it looks.
3. **Object count.** Ask for three instruments, count three. (The dark render silently produced two.)
4. **Numerals set in monospace** where the brand requires it.
5. **Clipping** — nothing cut at a frame edge.

Any failure is a **regeneration trigger**, never a ship-anyway. When regenerating for a text failure, shorten the offending word below the §2 on-object ceiling rather than repeating the same prompt and hoping — the same string tends to fail the same way.

Record the proofread outcome alongside the prompt and image per §5, so a later reader knows the render was actually verified rather than glanced at.

## 4. AristAI brand preset (overrides the default IKB blue in `references/visual-style.md`)

Use this whenever the illustration is for AristAI / ScheduleOpt — landing pages, decks, docs, provost-facing exports. It matches the shipped "instrument" design system, so generated art sits inside the product without a seam.

**Dark ground (default — matches the landing page and product shell):**
- Ground `#0b0b11` near-black · ink `#f5f2e9` warm off-white
- **Single accent: `#e0b84a` sodium gold**, highlight `#f5d889`
- Semantics, only with their meaning: success `#85c998` · warning `#F59E0B` · error `#F87171`

**Light ground (docs, print, provost exports):**
- Ground `#f5f3ec` warm parchment · ink `#201d15`
- **Single accent: `#c89d3c` gold**, deep `#6c5218`
- Semantics: success `#41785a` · warning `#c26b11` · error `#dc2626`

**Type pairing:** serif display for any headline set inside the image; **JetBrains Mono for all numerals, axis labels, units, and eyebrow text**; system sans for body. Numerals are always mono — this is a hard rule in the product and the illustrations must not contradict it.

**Discipline inherited from the product's design system:** one accent per image set. Gold carries emphasis; green/amber/red appear *only* when they encode success/warning/error. A gold-and-teal illustration is off-brand even if it looks good.

## 5. Output conventions

- Save images to the task folder alongside the prompt that made them, per upstream step 10.
- Working files for this repo go in the session scratchpad, not in `web-app/public/` — promote an asset into the repo only when it is actually being shipped, and compress it first (the product's perf gate is **≤ 30 KB per decorative asset**, see the `fantastic-ui` skill).
- Name files by content, not by index: `pathway-misalignment-cycle.webp`, not `image-3.png`.

## 6. Tracking upstream

This repo keeps the original as a remote so improvements can be pulled selectively:

```bash
git fetch upstream && git diff HEAD upstream/main -- references/
```

The `references/` directory is upstream's work and is the part worth re-syncing. `SKILL.md` carries local edits (name, description, the pointer above), so merge it by hand rather than taking theirs wholesale. If upstream renumbers the workflow steps, re-check the step references in §1 and §3.
