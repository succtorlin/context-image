# Machine-informed explanatory illustrations

Adapted from [AirsupHQ/machine-skill](https://github.com/AirsupHQ/machine-skill), locally installed as `machine`. This is a focused integration, not a vendored copy of its runtime. Read this reference for hardware and physical mechanisms only.

## Choose the output from the request

| Request | Route | Deliverable |
| --- | --- | --- |
| Explain a pump, engine, device, or mechanism in a slide/report | Context-image + physical guidance below | Generated labeled raster image and prompt |
| Show a cutaway, exploded assembly, or gas/heat/flow pattern | Same static route unless motion is requested | Image with accurate relationships and short callouts |
| Let me rotate it, adjust an input, or see calculated behavior | Read the installed Machine SKILL.md and relevant kit/example | Interactive HTML; film only if requested |
| Animate/film a machine operating | Machine workflow and recorder | Requested video and editable scene source |
| A metaphorical business process, chart, or humanities scene | Existing context-image workflow | Existing image deliverable |

Do not require a solver, full HTML app, film, failure scenario, or dozens of parts for a static image. Do not force an abstract process into a literal factory. If the user explicitly requests all Machine outputs, follow that scope.

## Physical specification before prompting

Capture only details needed to explain the idea:

- Recognizable silhouette and proportions, supported by references for a specific model. Record source URLs and distinguish measured dimensions, estimates, and unknowns.
- Essential visible parts, their materials, attachment points, and the part that causes the behavior. Prefer 3–5 visible callouts even when the geometry needs more parts.
- Where energy or material enters, the continuous path through the device, and where it leaves. Specify direction, source, and destination for each arrow or effect.
- The informative view: exterior, cutaway, exploded, or before/after. Pick one primary view rather than combining every mode.
- Any quantities: preserve supplied data exactly. Distinguish sourced specifications from model predictions. Never invent a performance number to make the image convincing.

## Translate Machine's craft into the established style

Keep context-image's approved palette, safe margins, editorial hierarchy, and short labels. Use Machine's physical detail where it teaches something:

- Closed solids and believable wall thickness; cut faces read as solid material, not hollow shells.
- Coaxial shafts and bearings, seated flanges, attached supports, and pipes connected to actual ports. No unexplained floating components or impossible intersections.
- Exploded parts move along plausible assembly axes; show their alignment. Detached parts are intentional only in an exploded view.
- Differentiate metal, rubber, glass, and painted surfaces through roughness and reflections. Do not replace the chosen editorial style with a mandatory photoreal product shot.
- Flow follows ducts, channels, or nozzles. Vapor begins at its source, expands downstream, and is occluded by solid parts. Separate cold gas/vapor from combustion flames; add shock diamonds only when the referenced flow regime supports them.
- Heat colors and flow colors explain a physical quantity when one is known. Decorative effects must not masquerade as computed evidence.
- Concept vehicles and speculative mechanisms must be identified as concept illustrations in the surrounding caption. A supplied concept render is visual reference, not proof of real engineering capability.

## Static prompt additions

Add a compact block to the existing prompt shell:

> Subject and explanatory claim: [object; one thing the viewer should understand].
> Reference-grounded structure: [silhouette, essential parts, relationships].
> View: [cut plane or explosion axis; what stays assembled].
> Materials: [part-to-material mapping consistent with the selected style].
> Flow/forces: [source → path → destination, direction, visual treatment].
> Exact labels: [3–5 strings and their target parts].
> Evidence boundary: [known facts, simplified geometry, conceptual elements; no invented metrics].

Continue using the image tool and magnified proofreading. Physical plausibility in an illustration does not constitute a validated simulation.

## Interactive and video handoff

Resolve `machine/SKILL.md` from the available skill catalog, or the sibling of this skill directory. Read its current instructions, the relevant example, kit, and solver references before writing code; do not reproduce guessed APIs here. If absent, continue the static route where it meets the request, or report the missing dependency for an explicitly interactive task.

For the context-image handoff, the user's requested deliverable overrides Machine's blanket HTML-plus-film default. Follow its relevant build and visual-review workflow for the selected output. Use task-local source files; never generate inside either installed skill directory.

For computed scenes, keep equations and constants explicit, drive motion and displayed predictions from the same model, identify simplifications, and compare the operating point against a relevant source with an appropriate tolerance. A generic 20% agreement threshold is not proof of accuracy for all mechanisms. Separate fixed sourced labels from computed readouts.

Check Node, browser/WebGL, Playwright, and (for video) ffmpeg before promising a render. The template uses CDN dependencies, so a single HTML file is not automatically offline-capable. Report actual dependency and test status. Respect reduced motion and provide a static fallback or descriptive caption for embedded explainers.

## Delivery checks

For static images: inspect silhouette, essential part count, contacts, cut faces, explosion alignment, flow direction, and label targets in addition to normal context-image QA. Inspect at final display size and proofread text under magnification. Regenerate defective imagery through the image tool.

For code-rendered outputs: inspect the actual exported still/video as well as the interactive scene; test the requested controls and relevant model behavior. Apply Machine's visual checks only to modes included in the deliverable.

Record sources, prompt or scene path, exact labels, final asset paths, approximations, and checks actually performed in the task folder. Do not call an image a simulation, a proposed prompt a generated asset, or an untested recorder a verified video.
