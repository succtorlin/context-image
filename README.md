# context-image

An agent skill that generates the **central explanatory image** — the one that carries the idea inside a doc, slide, card, or landing page. Labels are rendered *in* the illustration, then proofread under magnification before delivery.

> ## Credit
>
> This is an adaptation of **[op7418/guizang-material-illustration](https://github.com/op7418/guizang-material-illustration)** by 歸藏 (op7418). The methodology, the visual system, and everything in `references/` are that project's work. This fork adds an operational layer (see [What's different](#whats-different)) and nothing more.
>
> The upstream repository carries **no license file**. That means its author retains all rights by default. If you intend to use, redistribute, or build on this beyond personal use, seek permission from the original author first. Upstream is preserved as a git remote here so provenance stays traceable and improvements can be pulled back in.

---

## What it does

Three jobs, inherited from upstream:

- **Explanatory diagrams** — turn a concept, process, mechanism, or system relationship into a labeled illustration
- **Chart beautification** — extract the semantics from a chart screenshot or raw data (type, title, axes, units, values, conclusion) and redraw it, rather than reskinning the original
- **Reference-assisted illustration** — look up unfamiliar concepts, apparatus, or objects first so the structure isn't drawn wrong, then render in one consistent style

The house look is restrained Swiss-editorial composition, soft 3D material models, one accent color, no webfont dependencies or icon libraries.

## What's different

Four changes, all in service of making the skill actually runnable and verifiable outside its original Chinese-language context.

**1. A real image backend.** Upstream's step 8 calls an `imagegen` skill that most installs don't have. [`ADAPTER.md §1`](ADAPTER.md) replaces it with a priority ladder over commonly available generators, and states the selection rule that matters: since labels render inside the image, **text fidelity picks the model** — GPT Image and Gemini image models render embedded text reliably, FLUX garbles it. It also defines honest failure: with no backend configured, deliver the prompt plan and say so, rather than passing a plan off as a finished image.

**2. English label ceilings, measured not guessed.** Upstream mandates Chinese labels at 2–5 characters. `ADAPTER.md §2` establishes the English equivalent — and found that there are **two different ceilings**:

| Where the text sits | Safe ceiling | Evidence |
|---|---|---|
| Floating callout on quiet background | ~14 characters | `Schedule data`, `Metrics layer`, `Provost view` — correct in all four test renders |
| Printed **on an object** (plate, badge, chip) | **10 characters** | `Balance` (7) ✓ · `Bottlenecks` (11) ✓ · `Misalignment` (12) → rendered **`Misaiignment`** |

**3. A mandatory post-render proofread — the main addition.** Upstream step 9 says "inspect each image." That is precisely the instruction that lets defects through, because **baked-in text fails silently**: the model swaps one letter and the word still looks right at full size. `Misalignment` → `Misaiignment` passed a full-size eyeball check and was only caught under magnification.

So this fork ships [`scripts/proofread.py`](scripts/proofread.py):

```bash
python3 scripts/proofread.py OUT.png                      # 2x2 grid, 2x upscale
python3 scripts/proofread.py OUT.png --band 0.42 0.65     # one horizontal strip
python3 scripts/proofread.py OUT.png --grid 3x2 --zoom 3  # finer slicing
```

It slices a render into overlapping upscaled tiles so every label is large enough to proofread by eye. No OCR — stylized 3D lettering defeats OCR, and the agent already has vision; the job is purely to make text big enough to read reliably. `ADAPTER.md §3` turns this into an ordered checklist (spelling letter-by-letter longest-word-first, invented content, object count, monospace numerals, clipping) and rules that any failure is a regeneration trigger, never a ship-anyway.

**4. A worked brand preset.** `ADAPTER.md §4` replaces the default IKB blue with a full dual-ground palette (dark and light) as a concrete example of overriding the visual system for a product's own tokens. Substitute your own.

## Install

```bash
git clone <this-repo> ~/.claude/skills/context-image
```

Claude Code discovers skills in `~/.claude/skills/` automatically. Then ask for a diagram, an explanatory graphic, a chart cleanup, or a report figure — or invoke `/context-image` directly.

Before the first run, configure an image backend per `ADAPTER.md §1`. `scripts/proofread.py` needs Pillow:

```bash
python3 -m pip install --user Pillow
```

## Layout

```text
context-image/
├── SKILL.md              # workflow (upstream, with local name/description/pointer edits)
├── ADAPTER.md            # backend routing · label ceilings · proofread step · palette
├── scripts/
│   └── proofread.py      # post-render magnification for label QA
└── references/           # upstream: visual style, prompt patterns, chart rules,
                          #   routing, reference gathering, QA checklist
```

## Tracking upstream

```bash
git fetch upstream && git diff HEAD upstream/main -- references/
```

`references/` is upstream's work and is the part worth re-syncing. `SKILL.md` carries local edits, so merge it by hand.
