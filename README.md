<div align="center">

# Context Image

### Turn complex ideas into images people understand.

**Labeled illustrations · Material-style diagrams · Mechanical cutaways · Chart visuals**

An agent skill for turning your notes, articles, screenshots, and data into explanatory visuals for documents, slides, and websites—with reference research, deliberate composition, and magnified label review built into the workflow.

[Get started](#get-started) · [Try a prompt](#try-a-prompt) · [Machine integration](#give-your-diagrams-a-mechanical-mind) · [How it works](#from-source-to-finished-visual)

</div>

---

## One image. A clearer idea.

A dense paragraph becomes a review loop. A confusing system becomes a layered diagram. A pump becomes a cutaway that shows where fluid enters, what moves it, and where it leaves.

**Context Image helps your agent decide what the picture needs to explain before it decides what the picture should look like.**

The result is a focused visual asset: short labels, purposeful arrows, tactile materials, and enough detail to make the mechanism understandable. Use it inside your existing deck, report, article, or landing page.

## What can you make?

| Start with | Create |
| --- | --- |
| Notes about a workflow | A cycle, pipeline, or hub-and-spoke diagram |
| A product or architecture explanation | A layer stack, concept breakdown, or before/after image |
| A table or chart screenshot | A restyled chart visual, with values, units, order, and error bars checked against the source |
| A machine or physical mechanism | A labeled cutaway, exploded assembly, or flow illustration |
| A scientific, historical, or cultural subject | A reference-informed illustration with clear evidence boundaries |
| A request for interactive machine behavior | An optional handoff to **Machine** for a code-rendered model or film |

**The visual language:** Swiss editorial composition, material-style 3D objects, restrained surfaces, soft lighting, and one intentional accent. Bring your own brand palette, choose light or dark, and keep the set consistent.

## Get started

Install the skill in your agent's global skill directory. Choose **one** command:

**Codex**

```bash
git clone https://github.com/succtorlin/context-image.git ~/.codex/skills/context-image
```

**Claude Code**

```bash
git clone https://github.com/succtorlin/context-image.git ~/.claude/skills/context-image
```

The magnified-review helper requires Python and Pillow. Install Pillow into your preferred Python environment:

```bash
python3 -m pip install Pillow
```

Then ask your agent:

```text
Use context-image to explain this workflow as a labeled 16:9 illustration:
Upload → Process → Review → Share.
Use a warm light background, one gold accent, and short English labels.
```

In Codex, you can invoke `$context-image`; in Claude Code, use `/context-image`. If the newly installed skill is not listed, start a fresh session.

**Image generation:** the skill prefers the host's built-in image tool when available. Otherwise, configure a supported backend using [ADAPTER.md](ADAPTER.md). Without a working backend, it delivers a prompt plan and explicitly reports that no image was generated.

## Try a prompt

### Explain a system

```text
Use context-image to turn these notes into one diagram for a presentation.
Show how an AI draft moves through human review and revision.
Use four short labels, generous margins, and a single blue accent.
```

### Reveal a mechanism

```text
Use context-image to explain a centrifugal pump with a labeled cutaway.
Show the inlet, impeller, casing, and outlet, with the flow direction visible.
Research the structure first. Keep it a static 4:3 teaching illustration.
```

### Show how the parts fit

```text
Use context-image to create an exploded view of a mechanical watch movement.
Keep parts aligned along their assembly axes and label only the key assemblies.
Use reference-grounded proportions and distinguish metal from glass.
```

### Make data readable

```text
Use context-image to restyle this chart for a report.
Keep every supplied value, unit, category, and error bar unchanged.
Use a restrained material style and check the result against the source table.
```

### Create in Chinese

```text
用 context-image 把这段内容画成一张带字解释图。
用 3–5 个简短标签，一张图讲清一个核心概念，适合放进汇报 PPT。
```

## Give your diagrams a mechanical mind

The new [Machine integration](references/machine-integration.md) brings physical construction principles into Context Image:

- **Parts that fit:** connected pipes, aligned shafts, seated bearings, and believable supports.
- **Cutaways that explain:** visible wall thickness and solid section faces.
- **Exploded views that retain structure:** components separate along plausible assembly axes.
- **Materials that read differently:** metal, rubber, glass, and painted surfaces have distinct treatments.
- **Flows with a source and destination:** vapor emerges from a nozzle; fluid follows a channel; heat effects carry meaning.

A request for a still image stays a still image. You do not need Machine installed to use the static illustration guidance.

For **interactive 3D, calculated behavior, or machine video**, install the separate [AirsupHQ/machine-skill](https://github.com/AirsupHQ/machine-skill):

```bash
# Codex
git clone https://github.com/AirsupHQ/machine-skill.git ~/.codex/skills/machine

# Claude Code: use ~/.claude/skills/machine as the destination instead.
```

Then try:

```text
Use context-image with Machine to build an interactive pump explainer.
Let me adjust the input, inspect the cutaway, and see the model's flow estimate.
Explain the equations and simplifications. Deliver HTML only.
```

Machine is an optional runtime dependency, not bundled code. Rendering requires the tools described in its documentation, including a suitable browser; recording also needs Node, Playwright/Chromium, and FFmpeg. Its HTML may load CDN dependencies. A convincing illustration is not a validated simulation, and a simplified simulation is not manufacturing-grade CAD, CFD, or FEA.

## From source to finished visual

```mermaid
flowchart LR
    A[Your source] --> B[Find the explanatory idea]
    B --> C[Research and structure]
    C --> D[Compose and generate]
    D --> E[Inspect and proofread]
    E --> F[Image and prompt record]
    E -->|Correction needed| D
```

1. **Understand:** select the concept worth illustrating and the intended audience.
2. **Ground:** gather references for visually specific subjects; extract chart data without inheriting the old styling.
3. **Compose:** choose a structure, one visual emphasis, and usually 3–5 short labels.
4. **Generate:** specify exact text, aspect ratio, safe margins, materials, and references.
5. **Review:** inspect the image, magnify labels, compare values, and correct defects.
6. **Deliver:** save the asset, prompt, sources, and review outcome in the task folder.

## Beautiful images still need proofreading

Image models can silently substitute a character. `Misalignment` can become `Misaiignment` while looking correct at a glance.

Context Image includes a helper that creates enlarged review tiles:

```bash
# Run from the installed skill directory, or use the script's full path.
python3 scripts/proofread.py OUT.png
python3 scripts/proofread.py OUT.png --band 0.42 0.65
python3 scripts/proofread.py OUT.png --grid 3x2 --zoom 3
```

**The script prepares the tiles; the agent reads them.** It is not an automatic spelling checker or a guarantee of correctness. The workflow checks exact label strings, invented numbers, object counts, clipping, and label targets before delivery.

English labels generally work best at **1–3 words**; Chinese labels at **2–5 characters**. The adapter records conservative length heuristics from a small set of earlier renders. Those are starting points, not universal model limits—every final image still needs inspection.

For data visuals, compare the final rendering against the original values and geometry. If exact plotting cannot be preserved by image generation, use a deterministic charting tool for the chart itself and keep generated illustration separate.

## Your brand, your format

Specify the label language, aspect ratio, destination, and brand colors in the request. The adapter includes a gold light/dark palette as a worked example; the underlying visual reference uses blue. Your explicit palette takes priority.

| Destination | Useful starting ratio |
| --- | --- |
| Slides and wide landing sections | 16:9 |
| Documents and report figures | 4:3 |
| Portrait social-card inserts | 3:4 |
| Square illustration slots | 1:1 |

Context Image creates the **visual inside the layout**. Continue using your slide or social-card skill for the surrounding typography, page structure, and presentation.

## What's in the skill?

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Main workflow and routing |
| [ADAPTER.md](ADAPTER.md) | Image backends, language guidance, proofreading, and brand examples |
| [machine-integration.md](references/machine-integration.md) | Physical illustration guidance and optional Machine handoff |
| [visual-style.md](references/visual-style.md) | The material illustration system |
| [prompt-patterns.md](references/prompt-patterns.md) | Reusable diagram structures |
| [chart-beautify.md](references/chart-beautify.md) | Chart extraction and preservation rules |
| [reference-gathering.md](references/reference-gathering.md) | Visual research guidance |
| [qa-checklist.md](references/qa-checklist.md) | Final review checklist |
| [proofread.py](scripts/proofread.py) | Magnified review tiles |

A typical task produces:

```text
local-tests/your-concept/
├── assets/
│   └── explanatory-image.png
└── PROMPTS.md
```

Optional interactive work adds task-local scene source and requested exports. Installed skill directories remain reusable instructions, not output folders.

## Credits and provenance

Context Image adapts [op7418/guizang-material-illustration](https://github.com/op7418/guizang-material-illustration) by 歸藏 (op7418). The original illustration methodology and base visual references come from that project.

This adaptation adds the operational adapter, English-label guidance, magnified review workflow, and the new Machine integration reference. Mechanical guidance is informed by [AirsupHQ/machine-skill](https://github.com/AirsupHQ/machine-skill); its runtime remains a separate installation.

This repository does not currently include a license file. Preserve attribution and check the respective upstream terms before redistribution; this README does not grant additional rights to upstream material.

---

<div align="center">

**Bring the idea. Give it a shape people can understand.**

</div>
