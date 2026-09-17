# Bee platform v0 — whoop-scale dual-rotor dual-elevon tailsitter (mm)
# VTOL orientation (sits on tail): +Z up, +Y span, +X face-forward
#   LE + props at high Z; TE + elevons at low Z (ground)
# Prefix BEE_ for rebuild-safe deletes. Do not touch DualRotorTailsitter docs.
import FreeCAD as App
import Part
import Mesh
import MeshPart
import math
import json
import os

DOC_NAME = "BeeWhoopTailsitter"
OUT_DIR = os.environ.get("BEE_OUT_DIR")
if not OUT_DIR:
    if os.path.isdir("/Users/theronrogers/Documents/VibeCAD"):
        OUT_DIR = "/Users/theronrogers/Documents/VibeCAD"
    else:
        OUT_DIR = "/workspace"
FCSTD_PATH = os.path.join(OUT_DIR, "BeeWhoopTailsitter.FCStd")
STL_PATH = os.path.join(OUT_DIR, "BeeWhoopTailsitter.stl")
SCRIPT_COPY = os.path.join(OUT_DIR, "build_bee_whoop_tailsitter.py")

# Prefer active doc named BeeWhoopTailsitter; else new. Never touch DualRotor*.
doc = App.ActiveDocument
if doc is None or not doc.Name.startswith("Bee"):
    # Close accidental unnamed empties carefully — only create new
    doc = App.newDocument(DOC_NAME)

for obj in list(doc.Objects):
    if obj.Name.startswith("BEE_"):
        doc.removeObject(obj.Name)

# --- Specs (Bee platform v0) ---
SPAN = 120.0
ROOT_CHORD = 52.0
TIP_CHORD = 44.0
MEAN_CHORD = 0.5 * (ROOT_CHORD + TIP_CHORD)  # 48
S_MM2 = SPAN * MEAN_CHORD  # 5760
AUW_G = 100.0
PROP_D = 40.0
MOTOR_Y = 30.0  # ±30 mm — discs clear each other (gap 20 mm) and tips
ELEVON_CHORD = 15.0  # ~30% of mean chord
ELEVON_ROOT_GAP = 8.0  # mm gap at center for servo arms
ELEVON_TIP_CLEAR = 2.0
ELEVON_T = 2.2
HINGE_GAP = 0.8

# Wing body (excludes elevon): LE at high Z
WING_TE_Z = ELEVON_CHORD + HINGE_GAP / 2.0  # hinge bottom of wing body
# Total chord root from TE(z=0) to LE
ROOT_LE_Z = ROOT_CHORD
TIP_LE_Z = TIP_CHORD
# Straight hinge at constant Z
HINGE_Z = ELEVON_CHORD
WING_BODY_ROOT = ROOT_LE_Z - WING_TE_Z
WING_BODY_TIP = TIP_LE_Z - WING_TE_Z

THICK_T_C = 0.12
WINGLET_H = 8.0
WINGLET_T = 1.2

# Hardware placeholders
AIO_SIZE = (32.0, 36.0, 8.0)  # X,Y,Z — whoop AIO-ish, slightly large
BAT_SIZE = (8.0, 40.0, 12.0)  # thin 1S cue near LE (X thick, Y long, Z chordwise-ish)
SERVO_SIZE = (9.0, 12.0, 22.0)  # 9×12×22 micro
MOTOR_CAN_D = 10.0  # 0802-ish OD
MOTOR_CAN_H = 12.0

# Colors (RGB 0-1)
COL_WING = (0.72, 0.78, 0.84)      # light blue-grey
COL_PETG = (0.35, 0.40, 0.46)      # darker hardpoints
COL_ELEV = (0.95, 0.45, 0.12)      # orange
COL_AIO = (0.20, 0.75, 0.35)       # green
COL_PROP = (0.12, 0.12, 0.14)      # dark
COL_DISC = (0.35, 0.55, 0.95)      # transparent blue
COL_BAT = (0.55, 0.55, 0.20)
COL_GROUND = (0.25, 0.28, 0.30)

def add(shape, name, color, transparency=0):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    o.Label = name
    try:
        vo = o.ViewObject
        vo.ShapeColor = color
        vo.Visibility = True
        vo.Transparency = int(transparency)
        vo.DisplayMode = "Shaded"
    except Exception:
        pass
    return o

def box(size, center):
    sx, sy, sz = size
    cx, cy, cz = center
    s = Part.makeBox(sx, sy, sz)
    s.translate(App.Vector(cx - sx / 2, cy - sy / 2, cz - sz / 2))
    return s

def naca_yt(t_frac, t_c):
    x = max(min(t_frac, 1.0), 0.0)
    return 5.0 * t_c * (
        0.2969 * math.sqrt(x)
        - 0.1260 * x
        - 0.3516 * x * x
        + 0.2843 * x ** 3
        - 0.1036 * x ** 4
    )

def foil_wire(y, z_le, z_te, t_c, camber=0.03):
    """Airfoil in X-Z plane at span station y. Chord along -Z from LE(high Z) to TE(low Z).
    Thickness (+camber) along +X (face)."""
    chord = z_le - z_te
    if chord <= 0.5:
        chord = 0.5
    xs = [0.0, 0.005, 0.012, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20,
          0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.88, 0.94, 0.98, 1.0]
    upper, lower = [], []
    for xf in xs:
        # xf=0 at LE (high Z), xf=1 at TE (low Z)
        z = z_le - xf * chord
        yt = naca_yt(xf, t_c) * chord
        cam = camber * chord * math.sin(math.pi * xf)
        if xf > 0.97:
            yt *= 0.45 + 0.55 * (1.0 - xf) / 0.03
        upper.append(App.Vector(cam + yt, y, z))
        lower.append(App.Vector(cam - yt * 0.92, y, z))
    pts = upper + list(reversed(lower))
    pts.append(pts[0])
    try:
        bs = Part.BSplineCurve()
        bs.interpolate(pts[:-1])
        wire = Part.Wire([bs.toShape()])
        if not wire.isClosed():
            wire = Part.Wire(Part.makePolygon(pts))
        return wire
    except Exception:
        return Part.makePolygon(pts)

def half_wing(sign):
    tip_le = TIP_LE_Z
    root = foil_wire(0.0, ROOT_LE_Z, WING_TE_Z, THICK_T_C, camber=0.035)
    mid = foil_wire(sign * SPAN * 0.32, 0.5 * (ROOT_LE_Z + tip_le), WING_TE_Z, 0.115, camber=0.03)
    tip = foil_wire(sign * SPAN / 2.0, tip_le, WING_TE_Z, 0.105, camber=0.02)
    return Part.makeLoft([root, mid, tip], True)

try:
    wing = half_wing(1).fuse(half_wing(-1))
except Exception:
    # Fallback: simple tapered box wing
    def trap_wing(sign):
        # trapezoid loft of rectangles
        t_root = THICK_T_C * WING_BODY_ROOT
        t_tip = THICK_T_C * WING_BODY_TIP
        r = box((t_root, 2.0, WING_BODY_ROOT), (0, sign * 1.0, WING_TE_Z + WING_BODY_ROOT / 2))
        tip_y = sign * SPAN / 2.0
        tbox = box((t_tip, 2.0, WING_BODY_TIP), (0, tip_y, WING_TE_Z + WING_BODY_TIP / 2))
        return r.fuse(tbox)
    wing = trap_wing(1).fuse(trap_wing(-1))
    # solid fill via loft of boxes along span
    secs = []
    for i, yf in enumerate([0.0, 0.35, 0.7, 1.0]):
        y = yf * SPAN / 2.0
        ch = ROOT_CHORD + (TIP_CHORD - ROOT_CHORD) * yf
        z_le = ch
        body = z_le - WING_TE_Z
        t = THICK_T_C * body
        w = Part.makePolygon([
            App.Vector(-t / 2, y, WING_TE_Z),
            App.Vector(t / 2, y, WING_TE_Z),
            App.Vector(t / 2 * 0.6, y, z_le),
            App.Vector(-t / 2 * 0.5, y, z_le),
            App.Vector(-t / 2, y, WING_TE_Z),
        ])
        secs.append(w)
    try:
        wing_r = Part.makeLoft(secs, True)
        secs_l = []
        for w in secs:
            # mirror by rebuilding with -y — simpler fuse mirrored
            pass
        wing = wing_r.fuse(wing_r.mirror(App.Vector(0, 0, 0), App.Vector(0, 1, 0)))
    except Exception:
        # Ultimate fallback: single plate
        wing = box((THICK_T_C * MEAN_CHORD, SPAN, WING_BODY_ROOT),
                   (0, 0, WING_TE_Z + WING_BODY_ROOT / 2))

add(wing, "BEE_Wing", COL_WING)

# Tip winglets (small)
def winglet(sign):
    y_tip = sign * SPAN / 2.0
    ch = TIP_CHORD
    z_c = WING_TE_Z + WING_BODY_TIP * 0.45
    fin = box((WINGLET_T, 1.5, WINGLET_H), (sign * 0.5, y_tip - sign * 0.8, z_c + 1.0))
    # cant slightly
    fin.rotate(App.Vector(0, y_tip, z_c), App.Vector(0, 0, 1), sign * -8.0)
    return fin

add(winglet(1), "BEE_Winglet_R", COL_PETG)
add(winglet(-1), "BEE_Winglet_L", COL_PETG)

# Elevons — two panels left/right with root gap
def elevon(sign, tag):
    y_inner = (ELEVON_ROOT_GAP / 2.0) * sign
    y_outer = (SPAN / 2.0 - ELEVON_TIP_CLEAR) * sign
    mid_y = (y_inner + y_outer) / 2.0
    span_e = abs(y_outer - y_inner)
    # Panel from Z=0.3 to Z=HINGE_Z - gap/2
    z0 = 0.4
    z1 = HINGE_Z - HINGE_GAP / 2.0
    chord = z1 - z0
    panel = box((ELEVON_T, span_e, chord), (0.0, mid_y, (z0 + z1) / 2.0))
    # hinge bead
    tube = Part.makeCylinder(
        ELEVON_T * 0.45, span_e * 0.96,
        App.Vector(0, mid_y - sign * span_e * 0.48, HINGE_Z - 0.2),
        App.Vector(0, sign, 0),
    )
    try:
        shape = panel.fuse(tube)
    except Exception:
        shape = panel
    add(shape, f"BEE_Elevon_{tag}", COL_ELEV)
    return span_e

elevon(1, "R")
elevon(-1, "L")

# Motor mounts + 0802 cans + props + discs (props at +Z above LE)
def rotor(y, tag):
    # Local LE height at this Y (linear taper)
    yf = abs(y) / (SPAN / 2.0)
    z_le = ROOT_LE_Z + (TIP_LE_Z - ROOT_LE_Z) * yf
    # Motor axis along +Z (thrust up in VTOL)
    prop_z = z_le + 6.0
    # PETG hardpoint pad on wing upper surface near LE
    pad = box((14.0, 14.0, 3.0), (0.0, y, z_le - 1.5))
    # Motor can (0802)
    can = Part.makeCylinder(MOTOR_CAN_D / 2.0, MOTOR_CAN_H,
                            App.Vector(0, y, z_le - 1.0), App.Vector(0, 0, 1))
    # Bell / spinner
    spin = Part.makeSphere(MOTOR_CAN_D * 0.35)
    spin.translate(App.Vector(0, y, prop_z + 1.5))
    try:
        mount = pad.fuse(can).fuse(spin)
    except Exception:
        mount = pad.fuse(can)
    add(mount, f"BEE_MotorMount_{tag}", COL_PETG)

    # Prop: cross blades in XY at prop_z
    hub = Part.makeCylinder(3.0, 3.0, App.Vector(0, y, prop_z), App.Vector(0, 0, 1))
    b1 = box((PROP_D * 0.92, 3.0, 1.2), (0, y, prop_z + 2.0))
    b2 = box((3.0, PROP_D * 0.92, 1.2), (0, y, prop_z + 2.0))
    try:
        prop = hub.fuse(b1).fuse(b2)
    except Exception:
        prop = hub.fuse(b1)
    add(prop, f"BEE_Prop_{tag}", COL_PROP)

    # Clearance disc (thin cylinder, transparent)
    disc = Part.makeCylinder(PROP_D / 2.0, 0.8,
                             App.Vector(0, y, prop_z + 1.5), App.Vector(0, 0, 1))
    add(disc, f"BEE_Disc_{tag}", COL_DISC, 65)
    return prop_z, z_le

pz_r, le_r = rotor(MOTOR_Y, "R")
pz_l, le_l = rotor(-MOTOR_Y, "L")

# Micro servos near root TE (PETG mounts)
def servo(sign, tag):
    # Place just outboard of elevon root gap, near TE hinge, slightly forward (+X) of wing
    y = sign * (ELEVON_ROOT_GAP / 2.0 + SERVO_SIZE[1] / 2.0 + 1.0)
    z = HINGE_Z + SERVO_SIZE[2] / 2.0 + 1.0
    x = THICK_T_C * MEAN_CHORD * 0.55 + SERVO_SIZE[0] / 2.0 + 1.0
    body = box(SERVO_SIZE, (x, y, z))
    mount = box((SERVO_SIZE[0] + 2, SERVO_SIZE[1] + 2, 2.0), (x, y, z - SERVO_SIZE[2] / 2.0 - 1.0))
    try:
        shape = body.fuse(mount)
    except Exception:
        shape = body
    add(shape, f"BEE_Servo_{tag}", COL_PETG)
    # horn cue into elevon gap
    horn = box((1.5, 6.0, 1.5), (0.5, sign * (ELEVON_ROOT_GAP / 2.0 + 2.0), HINGE_Z - 2.0))
    add(horn, f"BEE_ServoHorn_{tag}", COL_PETG)

servo(1, "R")
servo(-1, "L")

# AIO placeholder centered on wing, near CG (~33% MAC from LE)
# MAC from LE: 0.33 * MEAN_CHORD below LE → z_cg = ROOT-ish LE - 0.33*MAC
# Use mean: z_le_mean ≈ MEAN_CHORD, z_cg = MEAN_CHORD - 0.33*MEAN_CHORD = 0.67*MEAN_CHORD
z_cg = MEAN_CHORD * (1.0 - 0.33)
aio = box(AIO_SIZE, (THICK_T_C * MEAN_CHORD * 0.15, 0.0, z_cg))
add(aio, "BEE_AIO", COL_AIO)

# Battery cue near LE (thin 1S)
bat = box(BAT_SIZE, (THICK_T_C * MEAN_CHORD * 0.35 + 2.0, 0.0, ROOT_LE_Z - 8.0))
add(bat, "BEE_Battery", COL_BAT)

# TE skids / ground contact pads under elevon TE corners
for sign, tag in [(1, "R"), (-1, "L")]:
    skid = box((6.0, 8.0, 2.0), (0.0, sign * (SPAN / 2.0 - 10.0), 1.0))
    add(skid, f"BEE_Skid_{tag}", COL_PETG)

# Optional thin ground plane under TE (visualization)
ground = box((80.0, SPAN + 20.0, 0.4), (0.0, 0.0, -0.5))
add(ground, "BEE_Ground", COL_GROUND, 50)

# AeroConfig if available
try:
    existing = [o for o in doc.Objects if "AeroConfig" in o.Name or (hasattr(o, "Label") and "Aero" in str(o.Label))]
    cfg = None
    for o in doc.Objects:
        if o.Name == "AeroConfig" or getattr(o, "TypeId", "") == "App::FeaturePython" and "Aero" in o.Name:
            cfg = o
            break
    # Best-effort: set dynamic properties on a plain FeaturePython / App::Feature
    if cfg is None:
        cfg = doc.addObject("App::FeaturePython", "BEE_AeroConfig")
    for k, v in [
        ("auw_g", AUW_G),
        ("span_mm", SPAN),
        ("chord_mm", MEAN_CHORD),
        ("n_props", 2),
        ("prop_diameter_mm", PROP_D),
        ("thrust_to_weight", 2.0),
        ("vehicle_type", "tailsitter"),
        ("airfoil", "e63"),
    ]:
        try:
            if not hasattr(cfg, k):
                cfg.addProperty("App::PropertyFloat" if isinstance(v, float) else
                                ("App::PropertyInteger" if isinstance(v, int) else "App::PropertyString"),
                                k, "Bee", k)
            setattr(cfg, k, v)
        except Exception:
            pass
except Exception as e:
    aero_err = str(e)
else:
    aero_err = None

doc.recompute()

# Save FCStd
try:
    doc.saveAs(FCSTD_PATH)
except Exception as e:
    save_err = str(e)
else:
    save_err = None

# Export STL of BEE_* (skip ground)
meshes = []
export_names = []
for obj in doc.Objects:
    if not obj.Name.startswith("BEE_"):
        continue
    if "Ground" in obj.Name:
        continue
    if not hasattr(obj, "Shape") or obj.Shape is None or obj.Shape.isNull():
        continue
    try:
        m = MeshPart.meshFromShape(Shape=obj.Shape, LinearDeflection=0.25, AngularDeflection=0.35, Relative=False)
        meshes.append(m)
        export_names.append(obj.Name)
    except Exception:
        try:
            m = Mesh.Mesh(obj.Shape.tessellate(0.3))
            meshes.append(m)
            export_names.append(obj.Name)
        except Exception:
            pass

if meshes:
    combined = Mesh.Mesh()
    for m in meshes:
        combined.addMesh(m)
    combined.write(STL_PATH)

# Geometry summary
disc_gap = 2 * MOTOR_Y - PROP_D  # center-to-center minus diameters
tip_clear_r = (SPAN / 2.0) - (MOTOR_Y + PROP_D / 2.0)
S_m2 = S_MM2 / 1e6
wing_loading_kg_m2 = (AUW_G / 1000.0) / S_m2
wing_loading_psf = wing_loading_kg_m2 / 4.88243
disk_area_m2 = 2 * math.pi * (PROP_D / 2000.0) ** 2
disk_loading_kg_m2 = (AUW_G / 1000.0) / disk_area_m2

result = {
    "ok": True,
    "doc": doc.Name,
    "orientation": "VTOL (+Z up LE/props, TE/elevons at bottom, +Y span, +X face)",
    "span_mm": SPAN,
    "root_chord_mm": ROOT_CHORD,
    "tip_chord_mm": TIP_CHORD,
    "mean_chord_mm": MEAN_CHORD,
    "S_mm2": S_MM2,
    "S_m2": round(S_m2, 6),
    "motor_Y_mm": MOTOR_Y,
    "prop_D_mm": PROP_D,
    "elevon_chord_mm": ELEVON_CHORD,
    "elevon_root_gap_mm": ELEVON_ROOT_GAP,
    "aio_mm": list(AIO_SIZE),
    "battery_mm": list(BAT_SIZE),
    "servo_mm": list(SERVO_SIZE),
    "auw_g": AUW_G,
    "wing_loading_kg_m2": round(wing_loading_kg_m2, 2),
    "wing_loading_psf": round(wing_loading_psf, 2),
    "disk_loading_kg_m2": round(disk_loading_kg_m2, 2),
    "thrust_to_weight_target": 2.0,
    "prop_disc_gap_mm": round(disc_gap, 2),
    "prop_tip_to_wingtip_clear_mm": round(tip_clear_r, 2),
    "cg_z_mm_from_TE": round(z_cg, 2),
    "cg_note": "AIO centered at ~33% MAC from LE (z≈0.67*MAC from TE); battery near LE; motors at LE — CG should land near AIO with battery/motor balance",
    "objects": [o.Name for o in doc.Objects if o.Name.startswith("BEE_")],
    "stl_exported": export_names,
    "fcstd": FCSTD_PATH,
    "stl": STL_PATH,
    "save_err": save_err,
    "aero_err": aero_err,
    "printability": {
        "min_wall_mm": ELEVON_T,
        "flags": [
            "PETG hardpoints (motor pads, servo mounts, skids) — print strong",
            "Wing core light blue-grey — LW-PLA/AirPLA candidate for AUW~100g",
            "Elevons orange — print separate or as hinge-living thin sections",
            "Prop discs viz-only — do not print",
            "Ground plane viz-only — skipped in STL",
            f"Prop disc mutual clearance {disc_gap:.1f} mm (OK if >5)",
            f"Prop-to-wingtip clearance {tip_clear_r:.1f} mm",
            "T/W=2.0 at 100g needs ~200g thrust total (~100g/motor) — typical 0802+1.5in whoop props on 1S may be marginal; verify static thrust",
        ],
    },
}

# Write result JSON beside outputs
with open(os.path.join(OUT_DIR, "bee_whoop_result.json"), "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
