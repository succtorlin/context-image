<div align="center">

# context-image

**The one image that explains the idea.**

An agent skill for Claude Code that turns an article, a concept, a process, a screenshot, or a table of numbers into a labeled explanatory illustration — and then proofreads the labels under magnification before it lets you ship.

`/context-image` · diagrams · chart beautification · report figures · 配图 · 图解 · 图表美化

</div>

---

## Why this exists

Every doc, deck, and landing page has one image that carries the argument. Image models can draw it beautifully now — soft 3D material objects, clean Swiss editorial composition, labels printed right on the parts.

The catch: **baked-in text fails silently.** Ask for `Misalignment` and the model hands back `Misaiignment`. At full size the word looks fine. It passes a glance. It ships. Someone notices in the boardroom.

`context-image` treats the illustration as a deliverable with a QA gate, not a lucky render. It plans the image, picks a backend that can actually spell, generates, then slices the result into upscaled tiles and reads every label back character by character. Any mismatch is a regeneration, never a shrug.

## What you get

| You give it | It produces |
|---|---|
| A paragraph explaining a loop, pipeline, or system | A labeled 3D diagram in the right structure (cycle, pipeline, hub-and-spoke, before/after, layer stack) |
| A chart screenshot or a raw table | The same data redrawn in the house style — values kept exact, source styling discarded |
| A scientific mechanism, historical scene, or unfamiliar object | A reference-checked illustration that gets the structure right before it gets it pretty |
| A vague "make this section look better" | The one cognitive anchor worth illustrating, plus the prompt record so you can reproduce it |

The house look: off-white studio ground, black ink outlines, refined gray surfaces, **one** accent color per image set, no webfonts, no icon libraries, no gradient blobs, no fake app chrome.

## Quick start

```bash
git clone https://github.com/succtorlin/context-image ~/.claude/skills/context-image
python3 -m pip install --user Pillow
```

Claude Code discovers anything in `~/.claude/skills/` automatically. Then, in any session:

```text
/context-image  Draw the review loop from this section: draft → AI pass → human check → next round
```

```text
Turn this benchmark table into a report figure, 4:3, keep the exact numbers
```

```text
这段讲的是复利效应，帮我画一张带字的解释图
```

The skill routes the mode itself — you never have to say "cycle diagram" or "chart beautify". Before the first real run, point it at an image backend (see [Configure a backend](#configure-a-backend)).

## How a run works

1. **Read** the source and pick the 1–6 ideas that deserve an image. Not every paragraph gets one.
2. **Extract**, not inherit. For charts: type, title, values, axes, units, order, error bars. Nothing about the source's colors or fonts survives.
3. **Look it up** when the subject is visually specific — an apparatus, a species, a cultural artifact, a product — so the drawing is structurally right.
4. **Compress** each concept into a plain-language explanation and 3–5 short labels.
5. **Choose a structure**: cycle, pipeline, hub-and-spoke, before/after, layer stack, data-first scene, mechanism, or text scene.
6. **Write one prompt per image** with exact label strings, aspect ratio, safe margins, references, and the shared style block.
7. **Generate** through the configured backend.
8. **Proofread under magnification.** This step is mandatory, and it is the reason this fork exists.
9. **Record** prompt, output path, and proofread result in the task folder so the set is reproducible.

## The proofread step

```bash
python3 scripts/proofread.py OUT.png                      # 2x2 grid, 2x upscale
python3 scripts/proofread.py OUT.png --band 0.42 0.65     # one horizontal strip
python3 scripts/proofread.py OUT.png --grid 3x2 --zoom 3  # dense or small lettering
```

The script slices a render into overlapping, upscaled tiles and prints their paths. No OCR — stylized 3D lettering defeats it, and the agent already has vision. The job is purely to make every label big enough to read reliably.

The agent then walks a fixed checklist on every tile:

1. **Spelling**, letter by letter, longest word first. Watch `l`↔`i`, `rn`↔`m`, doubled letters.
2. **Invented content.** Any number, unit, or caption the prompt didn't ask for is a defect, however plausible.
3. **Object count.** Ask for three instruments, count three.
4. **Numerals in monospace** where the brand requires it.
5. **Clipping** at any frame edge.

When a label fails, the fix is to shorten it below the measured ceiling — not to rerun the same prompt and hope. The same string tends to fail the same way.

## Label ceilings (measured, not guessed)

Upstream mandates Chinese labels at 2–5 characters. For English we measured GPT Image across repeated renders and found **two different limits** depending on where the text sits:

| Where the text sits | Safe ceiling | Evidence |
|---|---|---|
| Floating callout on quiet background | ~14 characters | `Schedule data`, `Metrics layer`, `Provost view` — correct in every render |
| Printed **on an object** (plate, badge, chip) | **10 characters** | `Balance` (7) ✓ · `Bottlenecks` (11) ✓ · `Misalignment` (12) → `Misaiignment` |

Longer words go on two lines, get abbreviated, or move to a floating callout.

## Configure a backend

Labels render inside the image, so **text fidelity picks the model**. GPT Image and Gemini image models render embedded text reliably; FLUX historically garbles it. Never choose on speed or cost when the image carries labels.

[`ADAPTER.md §1`](ADAPTER.md) defines a priority ladder over commonly available image-generation skills and the exact invocation shape (prompt passed as a file, explicit provider flag, aspect ratio by destination). If no backend is configured, the skill stops after writing the prompt plan and says so plainly. It will never present an ungenerated plan as a finished image.

## Bring your own brand

The default accent is IKB blue `#002FA7`. [`ADAPTER.md §4`](ADAPTER.md) shows a complete override — dual light/dark grounds, a single accent, semantic colors reserved for their meaning, monospace numerals — as a worked example. Swap in your own tokens and every image in a set will sit inside your product without a seam.

## Layout

```text
context-image/
├── SKILL.md              # the workflow the agent follows
├── ADAPTER.md            # backend routing · label ceilings · proofread rules · brand preset
├── scripts/
│   └── proofread.py      # post-render magnification for label QA
├── assets/
│   └── prompt-template.md
└── references/           # visual style, prompt patterns, chart rules,
                          #   use-case routing, reference gathering, QA checklist
```

## Credit and license

This is an adaptation of **[op7418/guizang-material-illustration](https://github.com/op7418/guizang-material-illustration)** by 歸藏 (op7418). The methodology, the visual system, and everything under `references/` are that project's work. This fork adds the operational layer described above — a real backend, measured English label limits, and the mandatory proofread — and nothing more.

The upstream repository carries **no license file**, so its author retains all rights by default. If you intend to redistribute or build on this beyond personal use, seek permission from the original author first. Upstream is kept as a git remote so provenance stays traceable:

```bash
git fetch upstream && git diff HEAD upstream/main -- references/
```

`references/` is the part worth re-syncing. `SKILL.md` carries local edits, so merge it by hand.
