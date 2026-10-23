"""Builds docs/*.html from the content below. Run: python3 -I _course/build.py"""
import html, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs"

ORDER = [
    ("00-orientation", "Orientation: your printer, your workflow"),
    ("01-how-fdm-works", "How FDM printing really works"),
    ("02-file-formats", "File formats and conversion"),
    ("03-design-first-model", "Design your first model"),
    ("04-design-for-print", "Design for print"),
    ("05-edit-and-repair", "Edit, repair and remix models"),
    ("06-slicing", "Slicing in Bambu Studio"),
    ("07-x2d-and-materials", "The X2D, filaments and upkeep"),
    ("capstone", "Capstone: snap-fit box"),
    ("reference", "Reference and troubleshooting"),
]


def ex(n, title, task, hint, solution):
    return f"""<div class="exercise"><span class="tag">EXERCISE {n}</span><h3>{title}</h3><p>{task}</p>
<details class="hint"><summary>Hint</summary><div>{hint}</div></details>
<details class="solution"><summary>Show solution</summary><div>{solution}</div></details></div>"""


def quiz(items):
    qs = ""
    for q, opts, ans, why in items:
        b = "".join(f'<button type="button">{html.escape(o)}</button>' for o in opts)
        qs += f'<div class="q" data-answer="{ans}"><p>{q}</p><div class="opts">{b}</div><div class="why">{why}</div></div>'
    return f'<h2>Checkpoint quiz</h2><div class="quiz">{qs}<p class="score">Answer all questions. Pass mark: 70%.</p></div>'


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><tr>{h}</tr>{r}</table></div>'


def page(slug, kicker, h1, objectives, body, recap, with_mark=True):
    i = [s for s, _ in ORDER].index(slug)
    prev = ORDER[i - 1] if i else None
    nxt = ORDER[i + 1] if i + 1 < len(ORDER) else None
    nav = '<div class="nav">'
    nav += f'<a class="btn" href="{prev[0]}.html">← {prev[1]}</a>' if prev else '<a class="btn" href="index.html">← Course home</a>'
    nav += f'<a class="btn primary" href="{nxt[0]}.html">{nxt[1]} →</a>' if nxt else '<a class="btn primary" href="index.html">Course home</a>'
    nav += "</div>"
    obj = "".join(f"<li>{o}</li>" for o in objectives)
    rec = "".join(f"<li>{r}</li>" for r in recap)
    mark = '<p><button id="mark" class="primary" type="button">Mark module complete</button></p>' if with_mark else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{h1} · 3D Printing Bootcamp</title><link rel="stylesheet" href="assets/css/main.css"></head><body>
<header class="top"><a class="brand" href="index.html">3DP Bootcamp</a><div class="bar" role="progressbar" aria-label="Course progress"><i></i></div><button id="theme" type="button" aria-label="Toggle dark mode">◐</button></header>
<main><div class="kicker">{kicker}</div><h1>{h1}</h1>
<div class="objectives"><h3>By the end you can…</h3><ul>{obj}</ul></div>
{body}
<h2>You can now…</h2><ul>{rec}</ul>
{mark}
<h3>Your notes</h3><textarea class="notes" aria-label="Notes for this page" placeholder="Settings that worked, mistakes, ideas…"></textarea>
{nav}</main><script src="assets/js/main.js"></script></body></html>"""


P = {}

# ───────────────────────── 00 ORIENTATION ─────────────────────────
P["00-orientation"] = page(
    "00-orientation", "Module 0", "Orientation: your printer, your workflow",
    ["Describe the full idea-to-print workflow in six steps",
     "Name which application does which job",
     "State what is (and is not) confirmed about the X2D, and where to check the rest"],
    f"""
<h2>The one-sentence model</h2>
<p>A 3D print is a <strong>design</strong> turned into a <strong>mesh file</strong>, turned into <strong>toolpaths</strong> (G-code) by a slicer, then melted plastic laid down layer by layer. Every problem you will ever have lives in one of those three steps, and knowing which one is 80% of fixing it.</p>

<h2>Your printer</h2>
<p>You wrote “Pampolab XT2D”. This course assumes that means the <strong>Bambu Lab X2D</strong>, launched in April 2026. If your printer is a different model, modules 1–6 still apply to any FDM printer; only module 7 is X2D-specific.</p>
<p>Confirmed from launch coverage: a dual-nozzle toolhead with a mechanical nozzle-switching mechanism, an enclosed chamber heated up to 65&nbsp;°C, nozzles up to 300&nbsp;°C, about 256&nbsp;×&nbsp;256&nbsp;×&nbsp;256–260&nbsp;mm build volume with the main nozzle (less X travel and height when the second nozzle is involved), and the Bambu Studio + MakerWorld ecosystem. For anything else, such as exact profile names, AMS compatibility lists or maintenance intervals, read the official <strong>Bambu Lab Wiki</strong> for your printer. This course does not guess.</p>

<h2>The six-step workflow</h2>
{table(["Step","What happens","Typical app"],[
 ["1. Design","Create or find a model","Fusion, Tinkercad, FreeCAD, Onshape, MakerWorld"],
 ["2. Edit / repair","Fix errors, change dimensions, combine parts","Blender, Bambu Studio, your CAD app"],
 ["3. Export / convert","Save as STEP, 3MF or STL","Same app, or a script (module 2)"],
 ["4. Slice","Orient, add supports, pick material and quality","Bambu Studio"],
 ["5. Print","Send to the X2D, watch the first layer","Bambu Studio / Bambu Handy"],
 ["6. Measure + iterate","Check with calipers, change one thing","Calipers + your notes"],
])}
<div class="callout tip"><strong>Habit that makes you good fast:</strong> change <em>one</em> thing between prints, write it in your notes box, and measure the result with calipers. Skill in 3D printing is mostly disciplined iteration.</div>

<h2>Setup checklist</h2>
<ul><li>Bambu Studio installed and your printer bound to it.</li><li>A MakerWorld account (free) for downloading and remixing models.</li><li>One CAD app: <strong>Tinkercad</strong> (browser, easiest), <strong>Fusion</strong> (formerly Fusion 360; check Autodesk's current personal-use terms), <strong>Onshape</strong> or <strong>FreeCAD</strong>.</li><li><strong>Blender</strong> (free) for mesh editing.</li><li>Digital calipers (about 0.01 mm resolution). Essential.</li><li>A folder structure: <code>models/source</code> (CAD files), <code>models/export</code> (STL/3MF), <code>prints</code> (Bambu project files).</li></ul>

<h2>Exercises</h2>
{ex(1,"Make your tool map","Write down, for each of the six workflow steps, the exact app you'll use. Then create the three folders above.","Use the table above, but replace the examples with <em>your</em> choices.","Example: Design = Tinkercad first, Fusion later; Edit = Blender; Export = 3MF from CAD; Slice = Bambu Studio; Print = X2D; Measure = calipers. The point is that every step has one owner, so you never wonder where to fix a problem.")}
{ex(2,"Check your calipers","Close the calipers fully. Do they read 0.00? Measure a coin or a known object twice.","Zero them with the jaws closed and clean.","If the zero drifts, clean the jaws and replace the battery. Trustworthy measurement is the foundation of every tolerance in module 4.")}
{ex(3,"Find the real specs","Open the Bambu Lab Wiki page for your printer. Write down the build volume (single and dual nozzle), supported materials and the recommended nozzle maintenance.","Search for your exact model name on the wiki.","Whatever the wiki says overrides anything in this course. Paste the numbers in your notes box.")}
{quiz([
 ("Where do most print problems originate?",["Only the printer hardware","Design, slicing, or printing — and you must work out which","The filament colour"],1,"Splitting problems into design / slicing / print stages is the core diagnostic skill."),
 ("Which app is best for repairing or sculpting a downloaded mesh?",["Blender","Calipers","Tinkercad's export button"],0,"Blender is a mesh editor; parametric CAD apps are best for dimensioned parts."),
 ("What should you do between two test prints?",["Change several settings to save time","Change one thing and note the result","Nothing, reprint the same file"],1,"One variable at a time is the only way to learn what caused a change."),
 ("What should you trust for exact X2D numbers?",["This course","A forum post about a different printer","The official Bambu Lab Wiki"],2,"Specs and profiles change with firmware and software releases."),
])}
""",
    ["Describe the six-step workflow", "Choose one tool per step", "Know where to look up exact X2D facts"],
)

# ───────────────────────── 01 HOW FDM WORKS ─────────────────────────
P["01-how-fdm-works"] = page(
    "01-how-fdm-works", "Module 1", "How FDM printing really works",
    ["Explain layers, line width and why parts are weaker along Z",
     "Calculate layer counts and wall-loop counts",
     "Predict overhang, bridging and warping problems before printing"],
    f"""
<h2>Layers and lines</h2>
<p>FDM (fused deposition modelling) squeezes molten plastic through a nozzle and draws it in thin <strong>layers</strong>. With a standard <strong>0.4&nbsp;mm nozzle</strong> the extruded line is a bit wider than the hole — about 0.42–0.45&nbsp;mm — and the <strong>layer height</strong> is usually 0.08–0.28&nbsp;mm (0.20 is the everyday default). Thin layers give smooth curves and slow prints; thick layers give fast, rough prints.</p>
<pre><code>layers = model_height / layer_height
loops  = wall_thickness / line_width      (round to a whole number)</code></pre>

<h2>The big physical truths</h2>
<h3>1. Parts are weaker between layers</h3>
<p>Each layer bonds to the one below it by heat, which is weaker than the plastic running inside a single line. A part is strongest <em>along</em> the lines and weakest when pulled <em>across</em> layers (the Z axis). Orientation is a strength decision.</p>
<h3>2. Gravity wins on overhangs</h3>
<p>A layer needs something underneath it. Up to roughly 45° of lean from vertical, each layer is supported mostly by the previous one. Beyond that the underside gets rough and, near horizontal, needs <strong>support</strong>. Flat gaps crossed by a <strong>bridge</strong> sag more the longer they are.</p>
<h3>3. Plastic shrinks as it cools</h3>
<p>Large flat footprints in materials such as ABS or ASA can peel at the corners (<strong>warping</strong>). This is why the X2D's heated chamber matters (module 7), and why sharp, large base corners are risky.</p>
<h3>4. The first layer is squished on purpose</h3>
<p>That squish produces the <strong>elephant foot</strong>: a slight bulge at the bottom edge. Chamfer the bottom edge of precision parts (module 4).</p>

<h2>Worked example: a hook, two ways</h2>
<p>A wall hook has an arm that bends under load. Print it <strong>standing up</strong> and the layer lines cross the arm: it snaps along a layer. Print it <strong>lying flat</strong> and the layers run along the arm: it bends and holds. Same STL, same settings, very different part. The lying-flat version needs a flat face on the plate, so you may redesign the hook so one side is flat.</p>

<h2>Exercises</h2>
{ex(1,"Count the layers","A 48 mm tall part is printed at 0.16 mm, 0.20 mm and 0.28 mm layer height. How many layers each?","Divide height by layer height.","48/0.16 = 300 layers; 48/0.20 = 240 layers; 48/0.28 ≈ 171 layers. Going from 0.16 to 0.28 cuts layers by about 43%, which is roughly why print time drops, though walls, infill and travel also matter.")}
{ex(2,"How many wall loops?","You want about 2.0 mm walls with a 0.4 mm nozzle (line ≈ 0.42 mm). How many wall loops should the slicer use?","Divide 2.0 by 0.42.","2.0 / 0.42 ≈ 4.8, so use 4 loops (≈1.7 mm) or 5 loops (≈2.1 mm). Designing walls as multiples of the line width avoids gap-fill artefacts.")}
{ex(3,"Orient the part","A phone stand has a thin angled back plate that carries the phone's weight. Should the layers run along the plate's length or across its thickness? Describe how to place it on the build plate.","Where does the load try to pull layers apart?","Layers should run along the plate's length so the bending load is along the lines. Place the stand lying on its back or side so the long plate is parallel to the build plate. Never print it standing on its thin edge.")}
{quiz([
 ("A 0.4 mm nozzle produces a line about…",["0.1 mm wide","0.42–0.45 mm wide","1.2 mm wide"],1,"Lines are slightly wider than the nozzle because the plastic is squished against the layer below."),
 ("A printed part is weakest…",["Along the lines","Between layers (across Z)","Inside the nozzle"],1,"Inter-layer bonding is weaker than continuous extruded plastic."),
 ("Which overhang prints best without supports?",["80° from vertical","45° from vertical","Fully horizontal, 30 mm wide"],1,"45° is a widely used limit where each layer still sits mostly on the one below."),
 ("The 'elephant foot' is caused by…",["The first layers being squished and spreading outward","Too much cooling","A bent nozzle"],0,"Squish on the early layers bulges the bottom edge; a 0.4–0.6 mm chamfer hides it."),
 ("3 loops on a 0.42 mm line give a wall of about…",["0.4 mm","1.3 mm","5 mm"],1,"3 × 0.42 ≈ 1.26 mm."),
])}
""",
    ["Calculate layers and loops", "Choose an orientation for strength", "Spot overhang and warping risks"],
)

# ───────────────────────── 02 FILE FORMATS ─────────────────────────
P["02-file-formats"] = page(
    "02-file-formats", "Module 2", "File formats and conversion",
    ["Choose between STEP, STL, 3MF and OBJ for any situation",
     "Convert between mesh formats with a short script or an app",
     "Diagnose a wrong-size import (unit mismatch)"],
    f"""
<h2>Two families: solid models and meshes</h2>
<p><strong>Solid (B-rep) models</strong> store exact surfaces — a cylinder is a cylinder. <strong>Meshes</strong> store thousands of triangles approximating the surface. CAD programs work in solids; slicers work in meshes. Going solid → mesh is easy and safe. Going mesh → solid is lossy and often impossible, so <em>always keep your original CAD file</em>.</p>
{table(["Format","Type","Keeps","Use it for"],[
 ["<code>.step / .stp</code>","Solid","Exact geometry, editable in any CAD","Sharing a part someone else will edit"],
 ["<code>.stl</code>","Mesh","Triangles only. No units, colour or settings","Universal download format; fine for one-colour prints"],
 ["<code>.3mf</code>","Mesh + package","Units, multiple objects, colours, and slicer settings","Best format for Bambu Studio; Bambu's project files are 3MF"],
 ["<code>.obj</code>","Mesh","Triangles/polygons, colours and textures through an .mtl file","Scans and Blender workflows"],
 ["<code>.f3d / .blend / .FCStd</code>","Native","Everything that app knows","Your working source files"],
])}
<div class="callout warn"><strong>STL has no units.</strong> The slicer assumes millimetres. A model exported in inches arrives 25.4× too small. Always confirm size after import.</div>

<h2>Conversion paths that work</h2>
<ul><li>CAD → <strong>3MF</strong> or STL: use the app's export / “save as mesh” command. Pick a fine refinement setting so curves aren't visibly faceted.</li><li>STEP → slicer: Bambu Studio can import STEP directly and turns it into a mesh for you.</li><li>OBJ ↔ STL ↔ 3MF: any mesh app, or the script below.</li><li>Mesh → STEP: avoid. Use the mesh only as reference and rebuild it in CAD if you need dimensional edits.</li></ul>

<h2>Worked example: convert and sanity-check in Python</h2>
<p>This uses the <code>trimesh</code> library (<code>pip install trimesh numpy</code>).</p>
<pre><code>import trimesh

mesh = trimesh.load("part.obj", force="mesh")   # load as one mesh
print("size (x,y,z):", mesh.extents)             # compare with what you expect, in mm
print("watertight:", mesh.is_watertight)         # True = closed, printable solid
print("volume mm3:", mesh.volume if mesh.is_watertight else "n/a")

mesh.export("part.stl")                          # format chosen from the extension</code></pre>
<p>If a part you designed as 100 mm wide reports <code>3.94</code> in <code>extents</code>, it was exported in inches. Multiply by 25.4 — in the script with <code>mesh.apply_scale(25.4)</code> or in the slicer by scaling 2540%.</p>

<h2>Exercises</h2>
{ex(1,"Pick the format","Choose a format for each: (a) a bracket a friend will modify in their CAD; (b) a two-colour keychain you'll slice yourself; (c) a figurine you're uploading for people to print in one colour; (d) a coloured scan from your phone.","Ask: does anyone need to edit it? Does colour matter?","(a) STEP. (b) 3MF — keeps colours and objects. (c) STL (universal) or 3MF. (d) OBJ with its .mtl/texture, or 3MF.")}
{ex(2,"Diagnose the size","You export a 2-inch cube from CAD set to inches and import it into Bambu Studio. It appears 2 mm wide. Why, and what fixes it?","STL stores the number 2, not the unit.","The slicer reads 2 as 2 mm. Fix by exporting in millimetres (preferred) or by scaling the model by 25.4× (2540%) to get 50.8 mm.")}
{ex(3,"Run the check","Run the Python example on a downloaded STL (change the filename). Report extents and watertight status. If it isn't watertight, what does that predict?","A non-watertight mesh has holes in the surface.","A non-watertight mesh may slice with missing walls or odd gaps. Repair it in module 5 before printing.")}
{quiz([
 ("Which format can reliably go back into CAD for dimensional edits?",["STL","STEP","OBJ"],1,"STEP carries exact solid geometry; meshes do not."),
 ("STL files store…",["Units and colours","Only triangles — no units","Slicer settings"],1,"STL is triangles only; the slicer assumes millimetres."),
 ("Best format for Bambu Studio projects with colours and settings?",["3MF","STL","SVG"],0,"3MF is a package that stores objects, colours and settings."),
 ("A 100 mm part imports as 3.94 mm. Likely cause?",["Wrong nozzle","Exported in inches","Too little infill"],1,"100 mm ≈ 3.94 in; the slicer read 3.94 as millimetres."),
])}
""",
    ["Choose the right format for a job", "Convert meshes in an app or a script", "Fix unit-mismatch imports"],
)

# ───────────────────────── 03 FIRST MODEL ─────────────────────────
P["03-design-first-model"] = page(
    "03-design-first-model", "Module 3", "Design your first model",
    ["Explain sketch → extrude → modify as the CAD loop",
     "Use named parameters so a design can be resized in seconds",
     "Export a part for the slicer from Tinkercad or Fusion"],
    f"""
<h2>Choose your CAD app</h2>
{table(["App","Good for","Trade-off"],[
 ["Tinkercad (browser)","First prints in 20 minutes: combine shapes, subtract holes","Limited precision and parametrics"],
 ["Fusion (ex-Fusion 360)","Parametric parts, timeline history, assemblies","Check Autodesk's current personal-use licence terms"],
 ["Onshape","Browser CAD with versioning","Free plan is for public/non-commercial work"],
 ["FreeCAD","Open source, fully local","Steeper learning curve"],
])}
<p>The steps below use Fusion terminology, but the same loop exists in every CAD program.</p>

<h2>The CAD loop</h2>
<ol><li><strong>Sketch</strong> a 2D profile on a plane and add <strong>dimensions and constraints</strong> so it is fully defined.</li><li><strong>Extrude</strong> (or revolve) it into a solid; choose join, cut or new body.</li><li><strong>Modify</strong>: fillet/chamfer edges, shell, add holes.</li><li><strong>Parameters</strong>: name your key sizes (<code>width</code>, <code>wall</code>, <code>cable_d</code>) and use them in sketches so changing one number updates the model.</li></ol>

<h2>Worked example: parametric cable clip</h2>
<p>A clip that sticks to a desk edge and holds a 6 mm cable. Create these parameters first (Modify → Change Parameters → User Parameters):</p>
{table(["Name","Value","Meaning"],[["width","30 mm","Clip width"],["wall","2.4 mm","Wall thickness (≈ 6 loops at 0.42)"],["cable_d","6 mm","Cable diameter"],["clear","0.4 mm","Extra gap so the cable slides in"]])}
<ol>
<li>Sketch on the XY plane: a centre circle of diameter <code>cable_d + clear</code>.</li>
<li>Draw an outer circle of diameter <code>cable_d + clear + 2*wall</code>.</li>
<li>Extrude the ring <code>width</code>.</li>
<li>Sketch a slot on the top for the cable to snap in: a rectangle narrower than the cable (<code>cable_d*0.8</code>), cut through the ring.</li>
<li>Fillet the slot's edges 0.6 mm so the cable doesn't catch.</li>
<li>Add a flat base: sketch a rectangle under the ring, extrude to join. A flat base prints without supports.</li>
<li>Export: right-click the body in the browser → <em>Save as Mesh</em> → 3MF (or STL), millimetres, refinement “High”.</li>
</ol>
<p>Now change <code>cable_d</code> to 4 and watch everything update. That is parametric design.</p>
<div class="callout tip"><strong>Tinkercad version:</strong> drop a tube, set the hole size to the cable diameter + 0.4, add a box under it as a base, subtract a small box from the top as the slot, then Export → STL.</div>

<h2>Exercises</h2>
{ex(1,"Resize in one step","Change <code>cable_d</code> to 4 mm and <code>width</code> to 20 mm in your clip. What breaks?","If something breaks, a dimension was typed as a number instead of using a parameter.","Nothing should break. Anything that doesn't update still contains a hard-coded number; replace it with the parameter name.")}
{ex(2,"Add a mounting hole","Add a 3.4 mm hole through the base for an M3 screw, centred 6 mm from the edge. Make 3.4 a parameter called <code>m3_hole</code>.","Sketch on the top face of the base, circle, dimension, then extrude-cut through all.","3.4 mm gives clearance around an M3 screw (nominal 3.0) after the printer's slight shrinkage of holes. See module 4.")}
{ex(3,"Rebuild in Tinkercad","Make the same clip using only a tube, boxes and the Hole tool. Compare how long it took and what you couldn't set precisely.","Tinkercad dimensions are typed in the shape's handles.","Tinkercad is faster for one-offs, parametric CAD is faster for the second and third version. Both are valid; choose by how often you'll change the design.")}
{quiz([
 ("What makes a CAD model 'parametric'?",["It has many curves","Key dimensions are named values that drive the geometry","It is exported as STL"],1,"Parameters let you edit one number and rebuild the whole model."),
 ("Why design the clip with a flat base?",["It looks nicer","It prints without support and sticks to the plate","STL needs it"],1,"A flat face on the plate gives adhesion and removes the need for supports."),
 ("Which export is best for a one-colour print you'll slice immediately?",["3MF or STL in millimetres","Fusion's native .f3d","A screenshot"],0,"Slicers read mesh formats; the original CAD file stays your master."),
 ("You type 6 into a sketch dimension instead of using cable_d. Result?",["Nothing","That dimension won't follow later parameter changes","The file won't export"],1,"Hard-coded numbers don't update when the parameter changes."),
])}
""",
    ["Run the sketch-extrude-modify loop", "Use named parameters", "Export a mesh for the slicer"],
)

# ───────────────────────── 04 DESIGN FOR PRINT ─────────────────────────
P["04-design-for-print"] = page(
    "04-design-for-print", "Module 4", "Design for print",
    ["Apply minimum wall, overhang, bridge and clearance rules",
     "Size holes, screw bosses and fits correctly",
     "Choose orientation and split a model into printable pieces"],
    f"""
<h2>The core numbers (0.4 mm nozzle, PLA/PETG)</h2>
{table(["Feature","Rule of thumb","Why"],[
 ["Wall thickness","≥ 1.2 mm; ≥ 2.0 mm if it carries load","Multiples of line width (≈ 0.42 mm)"],
 ["Smallest feature","≥ 0.4 mm; text strokes ≥ 0.8 mm, relief ≥ 0.6 mm","Nozzle can't draw thinner"],
 ["Overhang","≤ 45° from vertical without support","Layers need something below"],
 ["Bridge","≤ ~25 mm clean, ~50 mm sags","Unsupported span sags"],
 ["Hole (clearance)","nominal + 0.2 to 0.4 mm","Holes print slightly small"],
 ["M3 screw clearance hole","3.2–3.4 mm","Fit around a 3.0 mm screw"],
 ["Sliding fit gap","0.3–0.4 mm loose, 0.2 mm snug","Under 0.1 mm parts fuse"],
 ["Press fit","pin + 0.05–0.15 mm; test first","Depends on printer and material"],
 ["Bottom edge","0.4–0.6 mm chamfer","Hides elephant foot"],
 ["Corners","Fillet inside corners ≥ 1 mm","Sharp corners concentrate stress"],
])}
<p>Heat-set inserts and self-tapping screws need specific hole sizes. Use the supplier's datasheet: for example, short M3 inserts commonly want a hole of about 4.0–4.2 mm, and a self-tapping M3 screw a pilot around 2.5 mm — but verify with a test coupon.</p>

<h2>Lab: design-for-print checker</h2>
<p>Move the sliders to see how a design choice scores. These thresholds match the table above.</p>
<div class="lab" id="dfp">
<label>Wall thickness (mm) <input id="wall" type="range" min="0.4" max="4" step="0.1" value="1.6"><output></output></label>
<label>Overhang lean from vertical (°) <input id="ang" type="range" min="0" max="90" step="1" value="40"><output></output></label>
<label>Hole diameter (mm) <input id="hole" type="range" min="1" max="12" step="0.1" value="3.4"><output></output></label>
<label>Bridge length (mm) <input id="bridge" type="range" min="0" max="100" step="1" value="20"><output></output></label>
<label>Moving-part gap (mm) <input id="gap" type="range" min="0" max="0.6" step="0.05" value="0.3"><output></output></label>
<div id="dfp-out" aria-live="polite"></div>
</div>
<noscript><p>Enable JavaScript for the checker; the table above has all the numbers.</p></noscript>

<h2>Orientation and splitting</h2>
<ul><li>Put the <strong>largest flat face</strong> on the plate: best adhesion, no support.</li><li>Run layers <strong>along</strong> the direction of load.</li><li>Put critical round holes <strong>vertical</strong> (axis along Z); horizontal holes print slightly oval and sag at the top. If horizontal is unavoidable, use a <strong>teardrop</strong> or diamond hole shape.</li><li><strong>Split</strong> complex parts into pieces that each print flat, then join with pins, screws or glue.</li><li>Add <strong>chamfers</strong> on lower edges instead of overhanging fillets.</li></ul>

<h2>Worked example: M3 screw boss</h2>
<p>You need a post that takes an M3 screw into a heat-set insert (4.2 mm hole from the datasheet). The post wall around the hole should be at least 2 mm: 4.2 + 2×2 = 8.2, so use an 8–9 mm post. Fillet its base 1 mm onto the floor so it doesn't snap off.</p>

<h2>Exercises</h2>
{ex(1,"Size three holes","Pick CAD diameters for: a 5 mm steel rod that must slide freely, a 3 mm screw passing through, and a 10 mm magnet that should press in.","Use nominal + clearance from the table; press fits need a test.","Rod: 5.3–5.4 mm. M3 screw: 3.3–3.4 mm. Magnet: start at 10.1 mm (+0.1), print a test piece, and adjust in 0.05 mm steps.")}
{ex(2,"Fix the design","A bracket has a shelf that leans 60° from vertical and a 0.8 mm wall. Propose two changes so it prints without supports and survives use.","One change handles the overhang, one the wall.","Chamfer the shelf underside to 45° (or add a triangular gusset). Thicken the wall to at least 1.2 mm — 2.0 mm if it carries load.")}
{ex(3,"Orient it","A hinge pin 5 mm in diameter and 30 mm long will be bent by a lever. Lying flat or standing? Why?","Which orientation puts layer lines along the length?","Lying flat: layers run along the pin so bending doesn't peel layers apart. Standing, it would snap at a layer line. Use a flat-bottomed profile or a tiny support if the round shape sags.")}
{quiz([
 ("Minimum wall for a load-bearing part?",["0.4 mm","1.2 mm","About 2 mm or more"],2,"Load-carrying walls should be several loops thick, ≥ 2 mm."),
 ("An M3 clearance hole in CAD should be about…",["2.5 mm","3.0 mm","3.4 mm"],2,"Holes print small, so add 0.2–0.4 mm to the screw diameter."),
 ("Which gap makes a moving joint that doesn't fuse?",["0.05 mm","0.3–0.4 mm","0 mm"],1,"Below ~0.1 mm the lines merge; 0.3–0.4 mm slides freely."),
 ("Best shape for a horizontal round hole you can't rotate?",["Circle","Teardrop","Square"],1,"A teardrop's peak is 45°, so it prints without support."),
 ("Why chamfer the bottom edge?",["Hide elephant foot","Print faster","Improve colour"],0,"The squished first layers bulge outward; a chamfer absorbs that."),
])}
""",
    ["Apply the core numbers", "Size holes and fits", "Orient and split for printing"],
)

# ───────────────────────── 05 EDIT / REPAIR ─────────────────────────
P["05-edit-and-repair"] = page(
    "05-edit-and-repair", "Module 5", "Edit, repair and remix models",
    ["Choose the right edit route: CAD, Bambu Studio or Blender",
     "Detect and repair non-manifold and flipped-normal meshes",
     "Remix a MakerWorld model respecting its licence"],
    f"""
<h2>Which route for which edit?</h2>
{table(["You have","You want","Route"],[
 ["STEP or CAD file","Change dimensions","Open in CAD, edit parameters or features"],
 ["STL/3MF mesh","Cut it, add a block, add text, scale","Bambu Studio (cut, add shapes, text emboss, boolean)"],
 ["Broken or messy mesh","Repair holes, merge, decimate","Blender (3D-Print Toolbox) or Bambu Studio's import repair"],
 ["Mesh","Exact dimensional change (e.g. move a hole)","Rebuild in CAD using the mesh as reference"],
])}
<div class="callout"><strong>Rule:</strong> edit as upstream as possible. Fixing the CAD source beats fixing the mesh; fixing the mesh beats fixing it in the slicer.</div>

<h2>What 'broken' means</h2>
<ul><li><strong>Non-manifold edges</strong>: an edge shared by more or fewer than two faces. The slicer can't tell inside from outside.</li><li><strong>Holes</strong>: missing triangles in the surface.</li><li><strong>Flipped normals</strong>: faces pointing inward.</li><li><strong>Intersecting / duplicate geometry</strong>: overlapping shells or doubled vertices.</li></ul>
<p>Bambu Studio flags many of these with a warning icon on import and attempts a repair. Check the preview anyway: missing walls or odd gaps in the sliced layers mean the repair didn't fix it.</p>

<h2>Worked example: repair in Blender</h2>
<ol><li>Import the STL. Set Scene Properties → Units → Metric, Unit Scale <code>0.001</code>, Length <em>Millimetres</em> so the dimensions you see are real.</li><li>Tab into Edit Mode. Select → Select All by Trait → <em>Non Manifold</em>. Whatever highlights is a problem area.</li><li>Merge near-duplicate vertices, then recalculate normals outward, then fill holes (select the boundary loop, press <code>F</code>).</li><li>Enable the <em>3D-Print Toolbox</em> extension and run Check All: it lists non-manifold edges, intersections, thin walls and overhangs.</li><li>Export STL or 3MF in millimetres.</li></ol>
<p>The same steps by script (run in Blender's Scripting tab with the object active):</p>
<pre><code>import bpy
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)       # merge near-duplicate vertices
bpy.ops.mesh.normals_make_consistent(inside=False)  # point normals outward
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_non_manifold()                   # highlights what is still broken
</code></pre>

<h2>Remixing from MakerWorld</h2>
<ul><li>Read the model's <strong>licence</strong>. Some allow remixing with credit; some forbid derivatives or commercial use.</li><li>Prefer downloading the project 3MF: it carries the author's tested orientation, colours and profile.</li><li>Quick modifications (cut a piece off, add a hole, emboss your name) can be done in Bambu Studio without CAD.</li><li>Credit the original author when you share a remix.</li></ul>

<h2>Exercises</h2>
{ex(1,"Pick the route","(a) Make a downloaded STEP bracket 10 mm longer. (b) Add your name on top of a downloaded STL. (c) A scan has pinholes. Which tool for each?","Match the table.","(a) CAD parameter edit. (b) Bambu Studio text emboss / add shape. (c) Blender fill holes / merge vertices, then 3D-Print Toolbox check.")}
{ex(2,"Find the problem","The sliced preview shows a missing wall on one side. What do you check first and which Blender selection finds it?","Think non-manifold.","Likely a hole or non-manifold edge in the mesh. In Blender: Edit Mode → Select → Select All by Trait → Non Manifold, then fill or merge.")}
{ex(3,"Licence check","You want to sell a remixed phone stand you found online. What do you check before printing 50?","Not every licence allows commerce.","The model's licence terms: commercial use, derivatives and attribution. If unclear, ask the author or choose a different base model.")}
{quiz([
 ("Best tool for changing a hole position on a STEP file?",["Blender","Your CAD app","Bambu Studio paint tool"],1,"STEP is editable solid geometry; CAD keeps dimensions accurate."),
 ("'Non-manifold' means…",["The mesh is too big","Edges aren't shared by exactly two faces","It's an OBJ file"],1,"The mesh surface isn't a clean closed shell."),
 ("What should you do before remixing a MakerWorld model?",["Read the licence","Delete the metadata","Convert to STEP"],0,"Licences define whether modification and commercial use are allowed."),
 ("In Blender, STL dimensions look wrong unless you…",["Set the unit scale/length to millimetres","Switch to Cycles","Add a camera"],0,"Blender's default unit is metres; STL import needs the unit set correctly."),
])}
""",
    ["Select the right editing route", "Repair a broken mesh", "Remix with the right licence checks"],
)

# ───────────────────────── 06 SLICING ─────────────────────────
P["06-slicing"] = page(
    "06-slicing", "Module 6", "Slicing in Bambu Studio",
    ["Walk the Prepare → Slice → Print workflow",
     "Set quality, walls, infill and supports for a purpose",
     "Read the preview to catch problems before wasting filament"],
    f"""
<h2>The Bambu Studio flow</h2>
<ol><li><strong>Prepare tab:</strong> select your printer, plate type and filament. Import the model (File → Import, or drag-and-drop).</li><li><strong>Place and orient:</strong> <code>R</code> (rotate), <code>S</code> (scale), the lay-on-face tool, and the Cut and Support-paint tools. Check dimensions in the object info panel.</li><li><strong>Process settings:</strong> quality, strength, supports, others.</li><li><strong>Slice plate</strong>, then scrub through the layer slider in Preview.</li><li><strong>Print plate</strong> (send to printer) or export G-code/3MF.</li></ol>

<h2>The settings that matter most</h2>
{table(["Setting","What it does","Starting point"],[
 ["Layer height","Surface smoothness vs time","0.20 mm everyday; 0.12–0.16 for detail; 0.28 for quick drafts"],
 ["Wall loops","Strength + stiffness (more than infill!)","3 for general, 4–5 for functional"],
 ["Top / bottom shell layers","Closed skins","≈ 0.8–1.2 mm worth of layers"],
 ["Sparse infill density","Internal fill","10–15% display, 20–30% for functional"],
 ["Infill pattern","Strength vs time","Gyroid, cubic or grid for general use"],
 ["Supports","Holds overhangs","Tree supports for organic shapes; normal supports for flat undersides"],
 ["Brim","Extra first-layer adhesion","On for tall, thin or warping-prone parts"],
 ["Seam position","Where layers start/end","Hide it in a corner or behind a feature"],
])}
<div class="callout"><strong>Strength tip:</strong> walls carry most of the load. Going from 3 to 5 wall loops usually helps a functional part more than raising infill from 15% to 40%.</div>
<div class="callout warn"><strong>Angle conventions differ.</strong> This course measures overhangs as lean from <em>vertical</em> (45° limit). Slicers' “support threshold angle” is measured from <em>horizontal</em> (30° threshold ≈ 60° lean from vertical). Don't mix them up.</div>

<h2>Worked example: slice the cable clip</h2>
<ol><li>Import the clip 3MF. It should show your intended size (≈ 30 mm wide). If it's tiny, revisit module 2.</li><li>Lay it on its flat base. Supports: off (the design avoids them).</li><li>Layer 0.20 mm, 4 wall loops (functional clip), infill 20% gyroid.</li><li>Slice. In Preview, step through layers and check the cable hole is round, the slot is open, and the first layer is a full footprint.</li><li>Print one. Measure the hole with calipers. Is it cable_d + clear? If it is 0.2 mm small, add 0.2 to <code>clear</code> in CAD, re-export, repeat.</li></ol>

<h2>Reading the preview</h2>
<ul><li>Colour by <em>Line type</em>: look at walls, infill, support, bridges.</li><li>Scrub the layer slider through areas with overhangs: gaps under bridges or dense support clusters suggest orientation changes.</li><li>The estimate shows time and filament use. Compare two orientations before committing.</li></ul>

<h2>Exercises</h2>
{ex(1,"Time vs quality","Slice the same part at 0.12, 0.20 and 0.28 mm layer height. Record time and filament. Which would you use for a draft fit-check?","Look at the estimated time on the slice result.","Use the 0.28 mm draft for fit-checks, 0.20 for general, 0.12 for display parts. Expect the 0.12 mm slice to take noticeably longer, often 2× or more compared with 0.28.")}
{ex(2,"Strength experiment","Print two small clips: one with 2 loops/40% infill, one with 5 loops/10% infill. Bend them to failure. Which is stronger and why?","Walls carry bending load.","The 5-loop, 10%-infill clip usually wins: more material is at the outer edges, where bending stress is highest.")}
{ex(3,"Support or redesign?","Your part needs supports under a shelf that leans 60° from vertical. List two redesigns that avoid them.","Change the geometry, not the settings.","Chamfer the shelf to 45°; split the part so the shelf prints flat; add a bridged arch under the shelf.")}
{quiz([
 ("Which usually strengthens a functional part most?",["More wall loops","Higher infill only","Changing colour"],0,"Walls dominate bending strength."),
 ("Preview shows a gap under a bridge. First action?",["Increase flow blindly","Reorient or add support, then re-preview","Print anyway"],1,"Fix it in orientation/support before spending filament."),
 ("A support threshold of 30° is measured from…",["Vertical","Horizontal","The nozzle"],1,"Slicers measure from horizontal; 30° ≈ 60° lean."),
 ("A good everyday layer height with a 0.4 mm nozzle?",["0.02 mm","0.20 mm","0.60 mm"],1,"0.20 mm balances speed and detail."),
])}
""",
    ["Run the slicing workflow", "Set strength and quality purposefully", "Read the preview critically"],
)

# ───────────────────────── 07 X2D + MATERIALS ─────────────────────────
P["07-x2d-and-materials"] = page(
    "07-x2d-and-materials", "Module 7", "The X2D, filaments and upkeep",
    ["Explain what the X2D's dual-nozzle design is for",
     "Choose a filament for a job and handle its storage",
     "Keep a print log and a simple maintenance routine"],
    f"""
<h2>The dual-nozzle toolhead</h2>
<p>Launch coverage describes the X2D as a dual-nozzle machine with a mechanical switching mechanism (no extra motor in the toolhead). One nozzle is the main model nozzle; the second is mainly pitched for <strong>support material</strong>, including soluble supports, rather than for colour changes. In dual-nozzle mode the usable X width and height are reduced compared with the main nozzle alone — reviewers quote roughly 235 × 256 × 256 mm against 256 × 256 × 260 mm. <em>Check the Bambu Wiki for your printer's current figures.</em></p>
<p><strong>Why it matters for design:</strong> you can print complex overhangs with support material that comes off cleanly or dissolves, instead of fighting scarred surfaces. That rewards more ambitious geometry: internal channels, bridged cavities and nested parts.</p>
<div class="callout warn"><strong>Not verified here:</strong> exact Bambu Studio menu steps for assigning the second nozzle, which support-filament pairs are approved, and AMS compatibility. Read the Wiki page for your model; don't rely on forum guesses.</div>

<h2>The heated chamber</h2>
<p>The enclosure heats up to 65 °C. Hot chambers reduce warping and improve layer bonding in materials that shrink strongly (ABS, ASA, nylon, polycarbonate). Nozzles up to 300 °C cover most common engineering filaments.</p>
<div class="callout"><strong>PLA warning:</strong> PLA softens at low temperatures, and a hot chamber can soften the filament before the nozzle (heat creep). For PLA keep the chamber cool, usually by opening the door/lid as the Wiki recommends.</div>

<h2>Choosing filament</h2>
{table(["Material","Strengths","Watch out for"],[
 ["PLA","Easy, stiff, great detail","Softens near 55–60 °C, brittle; keep out of cars"],
 ["PETG","Tougher, better heat resistance","Stringing; sticks strongly to some plates"],
 ["ABS / ASA","Heat and UV resistance (ASA), post-processing","Needs enclosure; fumes: ventilate"],
 ["TPU","Flexible parts","Slow printing; often needs dry filament"],
 ["PA (nylon) / PC","Strong, tough, high heat","Absorb moisture: dry before printing"],
 ["Carbon/glass fibre blends","Stiff, dimensionally stable","Abrasive: use a hardened nozzle"],
])}
<p>Reviews list a hardened-steel 0.4 mm nozzle on the X2D, which suits abrasive filaments, but confirm what your unit ships with.</p>
<ul><li>Store filament sealed with desiccant. Dry nylon, TPU, PETG and PVA before printing.</li><li>Use the bundled filament profiles in Bambu Studio: they set temperature, cooling and flow.</li><li>Ventilate when printing ABS/ASA/PC.</li></ul>

<h2>Upkeep routine</h2>
<ul><li><strong>Every print:</strong> check the first layer; wipe the plate with isopropyl alcohol or warm soapy water for adhesion.</li><li><strong>Weekly:</strong> inspect the nozzle for clumps, clear debris from the purge area, check cables and fans.</li><li><strong>Per the Wiki:</strong> follow the lubrication and calibration schedule for your printer. Don't invent intervals.</li><li><strong>Keep a log:</strong> material, settings, result. After 20 entries you'll have your own cookbook.</li></ul>

<h2>Exercises</h2>
{ex(1,"Material choice","Choose filament for: (a) a car-dash phone mount in summer; (b) a quick visual prototype; (c) a flexible drone-camera mount; (d) a gear that sees friction and heat.","Think heat, stiffness, flexibility.","(a) ASA or PETG (heat/UV). (b) PLA. (c) TPU. (d) Nylon (PA) or carbon-filled nylon, dried, with a hardened nozzle.")}
{ex(2,"Design for the support nozzle","Sketch (on paper) a part that would be hard with normal supports but easy with dissolvable ones.","Internal cavities are hard to reach.","A box with a captive internal ball joint, or a hollow channel with overhanging roofs. After printing, soluble support washes out of spaces tools can't reach.")}
{ex(3,"Start your log","Create a table with columns: date, file, material, layer/loops/infill, result, next change. Log your next print.","Use your notes box or a spreadsheet.","Consistent logging beats memory. After a month, sort by result to see which settings work for you.")}
{quiz([
 ("The X2D's second nozzle is mainly intended for…",["Support material","Cooling","Cutting filament"],0,"It's pitched at (soluble) supports, not multicolour printing."),
 ("Why take care with PLA in a hot chamber?",["It gets stronger","The filament can soften and jam before the nozzle","It changes colour"],1,"Heat creep. Open the chamber door/lid for PLA as the Wiki advises."),
 ("Which filament absorbs moisture strongly and should be dried?",["Nylon (PA)","PLA only","None do"],0,"PA, TPU, PETG and PVA all benefit from drying."),
 ("Where do you find exact X2D maintenance intervals?",["Guess","Bambu Lab Wiki","The slicer preview"],1,"The official wiki is authoritative."),
])}
""",
    ["Explain the dual-nozzle idea", "Choose filament by job", "Maintain and log your printing"],
)

# ───────────────────────── CAPSTONE ─────────────────────────
P["capstone"] = page(
    "capstone", "Capstone", "Capstone: a snap-fit box",
    ["Design a two-part parametric box with a snap-fit lid",
     "Calculate whether the snap hooks will survive",
     "Print, measure, adjust and document the result"],
    f"""
<h2>The brief</h2>
<p>Design and print a small storage box (inner size about 60 × 40 × 25 mm) with a lid that snaps shut without screws. It must close firmly, open without breaking, print without supports, and be fully parametric so you can resize it for anything (SD cards, coins, spare screws).</p>

<h2>Specification</h2>
<ul><li>Two bodies: <strong>box</strong> and <strong>lid</strong>, both with a flat face on the plate.</li><li>Named parameters: <code>in_w, in_d, in_h, wall, clear, snap_t, snap_len, snap_y</code>.</li><li>Walls ≥ 2 mm; all outside bottom edges chamfered 0.5 mm; inside corners filleted ≥ 1 mm.</li><li>Lid lip fits inside the box with <code>clear</code> = 0.25 mm per side.</li><li>Two cantilever snap hooks on the short sides.</li><li>Prints without supports.</li></ul>

<h2>Milestones</h2>
<ol><li><strong>M1 – Parameters and box body</strong> (module 3).</li><li><strong>M2 – Lid and lip</strong> with clearance (module 4).</li><li><strong>M3 – Snap hooks</strong> and strain check (below).</li><li><strong>M4 – Export</strong> 3MF in mm, slice in Bambu Studio, check the preview (modules 2 and 6).</li><li><strong>M5 – Print, measure, iterate</strong> until the fit is right. Log every change.</li></ol>

<h2>Snap-hook check</h2>
<p>For a straight rectangular cantilever hook, the peak strain when the tip deflects by <code>y</code> is approximately:</p>
<pre><code>strain = 1.5 * t * y / L**2     # t = beam thickness, y = tip deflection, L = beam length (same units)</code></pre>
<p>Example: t = 1.5 mm, y = 0.6 mm, L = 12 mm → 1.5 × 1.5 × 0.6 / 144 ≈ 0.0094 = 0.94%. That is comfortable for PETG; PLA is brittle, so prefer lower strain or a longer beam. Longer, thinner beams flex more safely, and beams printed with layers along their length stay strong, so orient the hooks so layers run along them.</p>

<h2>Rubric (self-assessment)</h2>
{table(["Criterion","Pass looks like"],[
 ["Parametric","Changing in_w, in_d, in_h rebuilds without errors"],
 ["Fit","Lid snaps on with a clear click, opens by hand, no gap > 0.5 mm"],
 ["Printability","No supports; first layer full; no elephant-foot jamming"],
 ["Durability","Survives 50 open/close cycles without cracking"],
 ["Documentation","Notes list each iteration, the change and the measurement"],
])}

<h2>Reference solution</h2>
<details class="solution"><summary>Show one reference design</summary><div>
<p><strong>Parameters:</strong> in_w 60, in_d 40, in_h 25, wall 2.0, clear 0.25, snap_t 1.5, snap_len 12, snap_y 0.6.</p>
<ol><li>Box outer = inner + 2×wall; extrude to in_h + wall. Shell open top. Fillet vertical outside edges 2 mm, inside corners 1 mm. Chamfer the bottom outside edge 0.5 mm.</li><li>On both short walls, cut a rectangular window 8 mm wide near the rim and leave a catch ledge 0.6 mm deep (snap_y).</li><li>Lid plate = outer size × 2 mm thick. Lip below it = inner size − 2×clear, 4 mm tall, wall 1.6 mm.</li><li>On the lip's short sides add a flexible hook: beam thickness snap_t, length snap_len, end bump height snap_y with a 45° lead-in chamfer (easy closing) and a steeper back face (holds firmly).</li><li>Export both bodies to one 3MF; print the lid upside-down so the plate is flat on the bed and the lip points up.</li><li>First-print result to expect: if the lid is too loose, reduce clear to 0.2 or raise snap_y to 0.7; if it is too tight or the hooks crack, raise clear to 0.3 or lengthen snap_len to 14.</li></ol>
</div></details>

{ex(1,"Stretch goal","Add a thumb notch at the lid edge and a text label on the lid (emboss 0.6 mm in Bambu Studio).","Text emboss is in Bambu Studio's right-click menu.","Use a bold font at least 6 mm tall so strokes are ≥ 0.8 mm; keep the text on the top flat face.")}
{ex(2,"Stress test","Open and close the lid 50 times. Where does it wear first? Redesign that spot.","Look at the hook root.","Cracks at the hook root mean strain is too high. Lengthen the beam, thin it, or add a larger root fillet.")}
{quiz([
 ("How should snap hook layers run?",["Along the beam length","Across the beam","It doesn't matter"],0,"Layers along the beam prevent inter-layer failure at the root."),
 ("Strain formula for a rectangular cantilever hook…",["1.5·t·y / L²","t + y + L","y / t"],0,"Longer beams (L²) cut strain quickly."),
 ("Lid too loose. First try…",["Reduce clearance a little or raise snap bump height","Print slower","Use more infill"],0,"Fit changes come from geometry, not infill."),
 ("Why print the lid upside-down?",["Flat plate on the bed, lip pointing up, no supports","Looks better","Uses less filament"],0,"A flat face on the bed gives adhesion and avoids supports."),
])}
""",
    ["Build a parametric two-part product", "Verify snap-fit strain by calculation", "Iterate with measurements"],
)

# ───────────────────────── REFERENCE ─────────────────────────
P["reference"] = page(
    "reference", "Reference", "Cheat sheet, glossary and troubleshooting",
    ["Look up core numbers quickly", "Diagnose common print defects", "Know where to go next"],
    f"""
<h2>Cheat sheet</h2>
{table(["Topic","Number"],[
 ["Line width (0.4 nozzle)","≈ 0.42–0.45 mm"],["Everyday layer height","0.20 mm"],["Min wall / structural wall","1.2 mm / ≥ 2.0 mm"],
 ["Overhang without support","≤ 45° from vertical"],["Bridge","≤ ~25 mm clean"],["Hole add-on","+0.2 to +0.4 mm"],
 ["M3 clearance hole","3.2–3.4 mm"],["Sliding / snug gap","0.3–0.4 / 0.2 mm"],["Bottom chamfer","0.4–0.6 mm"],["Inch → mm","× 25.4"],
])}

<h2>Troubleshooting</h2>
{table(["Symptom","Likely cause","Try"],[
 ["First layer won't stick","Dirty plate, wrong plate setting, wrong first-layer calibration","Clean the plate; verify plate type in the slicer; re-run calibration"],
 ["Corners lifting (warping)","Cooling/shrinkage, large footprint","Brim, enclosure heat for ABS/ASA, avoid sharp base corners"],
 ["Stringing","Wet filament, temperature too high","Dry the filament; reduce temperature; check retraction settings"],
 ["Rough overhang undersides","Overhang > 45°","Reorient, chamfer, or add support"],
 ["Holes too small","Normal plastic behaviour","Add clearance in CAD"],
 ["Layers separated","Under-extrusion or cold hotend","Check filament dryness and temperature; increase wall loops"],
 ["Supports won't come off","Support interface too dense/close","Increase the support gap in the slicer; use the support nozzle for supports"],
 ["Parts won't fit together","Tolerance too tight","Add 0.1 mm clearance and reprint"],
])}

<h2>Glossary</h2>
<dl>
<dt>B-rep</dt><dd>Boundary representation: exact solid surfaces used by CAD and STEP.</dd>
<dt>Brim</dt><dd>A flat ring around the first layer to improve adhesion.</dd>
<dt>Elephant foot</dt><dd>Bulge at the bottom edge caused by first-layer squish.</dd>
<dt>G-code</dt><dd>The machine instructions the slicer generates.</dd>
<dt>Infill</dt><dd>Internal sparse fill pattern.</dd>
<dt>Manifold</dt><dd>A watertight mesh where each edge belongs to exactly two faces.</dd>
<dt>Perimeter / wall loop</dt><dd>One outline pass of extruded line.</dd>
<dt>Slicer</dt><dd>Software that cuts a model into layers and makes toolpaths (Bambu Studio).</dd>
<dt>Tessellation</dt><dd>Converting curved surfaces into triangles.</dd>
</dl>

<h2>Where to go next</h2>
<ul><li>Bambu Lab Wiki for your printer: the authority for settings and maintenance.</li><li>MakerWorld: download, remix and share models with proper credit.</li><li>Learn assemblies and joints in Fusion or Onshape; learn sculpting in Blender.</li><li>Print temperature towers, retraction tests and tolerance coupons to build your own data.</li><li>Redo the capstone with a hinged lid or a dissolvable-support design on the X2D.</li></ul>
""",
    ["Look up key numbers", "Troubleshoot defects", "Plan what to learn next"], with_mark=False,
)

# ───────────────────────── INDEX ─────────────────────────
curr = "".join(
    f'<li><a href="{s}.html"><span class="n">{n:02d}</span><span>{t}</span><span class="st" data-st="{s}"></span></a></li>'
    for n, (s, t) in enumerate(ORDER)
)
P["index"] = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>3D Printing Bootcamp · Bambu Lab X2D</title><link rel="stylesheet" href="assets/css/main.css"></head><body>
<header class="top"><a class="brand" href="index.html">3DP Bootcamp</a><div class="bar" role="progressbar" aria-label="Course progress"><i></i></div><button id="theme" type="button" aria-label="Toggle dark mode">◐</button></header>
<main><div class="kicker">Zero → hero · built for the Bambu Lab X2D</div>
<h1>3D Printing Bootcamp</h1>
<p>Design a model, edit and repair it, convert it, slice it and print it. Eight short modules, a capstone project, quizzes with explanations, and an on-page design-for-print checker. Your progress is saved in this browser.</p>
<p><a id="resume" class="btn primary" href="00-orientation.html">Start here</a> &nbsp; Progress: <strong data-pct>0%</strong></p>
<h2>Who it's for</h2>
<p>You own an X2D (or any FDM printer) and want to move from downloading models to making your own. No prior CAD or slicing knowledge needed. You'll need a computer, calipers and filament.</p>
<h2>Curriculum</h2>
<ol class="curriculum">{curr}</ol>
<h2>Outcomes</h2>
<ul><li>Design a parametric part and export it correctly.</li><li>Repair and remix downloaded models legally and cleanly.</li><li>Pick settings by purpose, not by habit.</li><li>Print a snap-fit box that works.</li></ul>
<div class="callout"><strong>About the printer.</strong> The course assumes your “XT2D” is the Bambu Lab X2D. X2D-specific claims are limited to what launch coverage confirms; for everything else, follow the official Bambu Lab Wiki.</div>
</main><script src="assets/js/main.js"></script></body></html>"""

OUT.mkdir(exist_ok=True)
for slug, content in P.items():
    (OUT / f"{slug}.html").write_text(content, encoding="utf-8")
print("wrote", len(P), "pages")
