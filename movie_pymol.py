from pymol import cmd
import os
import glob
import subprocess

# ============================================================
# FILES
# ============================================================

gro = "movie_400_500ns/movie_structure.gro"
xtc = "movie_400_500ns/movie_pymol.xtc"

FRAME_DIR = "movie_frames_test_5"
MOVIE_FILE = "GLP1R_400_500ns_5.mp4"

os.makedirs(FRAME_DIR, exist_ok=True)

# ============================================================
# PERFORMANCE
# ============================================================

cmd.set("defer_builds_mode", 3)

# ============================================================
# LOAD SYSTEM
# ============================================================

cmd.bg_color("white")

cmd.load(gro, "complex")
cmd.load_traj(xtc, "complex")

cmd.hide("everything")

# ============================================================
# PROTEIN
# ============================================================

cmd.show("cartoon", "polymer.protein")
cmd.color("red", "polymer.protein")

# ============================================================
# LIGAND
# ============================================================

cmd.select("lig", "resn UNK")

cmd.show("sticks", "lig")
cmd.color("yellow", "lig")
cmd.set("stick_radius", 0.25, "lig")

# ============================================================
# AUTOMATIC POLAR & HYDROPHOBIC INTERACTIONS
# ============================================================

# --- 1. Identify Interacting Atoms ---
cmd.select("protein_polar", "(polymer.protein within 3.5 of lig) and (name N or name O or name S)")
cmd.select("lig_polar", "lig and (name N or name O or name S)")

cmd.select("protein_hydrophobic", "(polymer.protein within 4.0 of lig) and (name C and not name C+CA)")
cmd.select("lig_hydrophobic", "lig and name C")

# --- 2. Generate Interaction Dashes ---
cmd.distance("hbonds", "protein_polar", "lig_polar", cutoff=3.5, mode=2)
cmd.distance("hydrophobic_contacts", "protein_hydrophobic", "lig_hydrophobic", cutoff=4.0, mode=2)

# --- 3. Group and Style Residues ---
cmd.select("interacting_res", "byres (protein_polar or protein_hydrophobic)")

cmd.color("orange", "interacting_res")
cmd.set("stick_radius", 0.18, "interacting_res")

# --- 4. Distinct Colors for Dashes ---
cmd.set("dash_color", "cyan", "hbonds")
cmd.set("dash_color", "salmon", "hydrophobic_contacts")

# Global dash aesthetics
cmd.set("dash_radius", 0.04)
cmd.set("dash_gap", 0.3)

# --- 5. Initial Hide ---
cmd.hide("sticks", "interacting_res")
cmd.hide("dash", "hbonds")
cmd.hide("dash", "hydrophobic_contacts")

# ============================================================
# MEMBRANE SEPARATION & DISTINCT COLORING
# ============================================================

cmd.select("popc", "resn POPC")
cmd.select("chl", "resn CHL1")

cmd.hide("everything", "popc")
cmd.hide("everything", "chl")

# --- POPC Styling ---
cmd.show("sticks", "popc and not name P")
cmd.show("spheres", "popc and name P")
cmd.set("sphere_scale", 0.8, "popc and name P")

cmd.color("grey80", "popc")
cmd.util.cnc("popc")
cmd.color("blue", "popc and name P")

# --- Cholesterol Styling ---
cmd.show("sticks", "chl")
cmd.color("wheat", "chl")
cmd.util.cnc("chl")

# --- Clean Up & Transparency ---
cmd.hide("everything", "(popc or chl) and hydrogens")

cmd.set("stick_transparency", 0.7, "popc")
cmd.set("sphere_transparency", 0.7, "popc")
cmd.set("stick_transparency", 0.7, "chl")

# ============================================================
# FIXED PUBLICATION VIEW (Starting Position)
# ============================================================

cmd.set_view((
    -0.962045550,    0.145212397,   -0.231043801,
     0.253799051,    0.165028155,   -0.953075051,
    -0.100269608,   -0.975540042,   -0.195619375,
     0.000000000,    0.000000000, -336.312286377,
    44.668159485,   48.434650421,   67.680931091,
   265.151184082,  407.473388672,  -20.000000000
))

# ============================================================
# QUALITY
# ============================================================

cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_smooth_loops", 1)

cmd.set("depth_cue", 0)
cmd.set("ray_shadows", 0)

cmd.set("specular", 0.2)

# ============================================================
# FRAME COUNT / RESUME SUPPORT
# ============================================================

states = cmd.count_states()
print(f"Trajectory contains {states} frames")

existing_frames = sorted(glob.glob(f"{FRAME_DIR}/frame_*.png"))

if existing_frames:
    last_frame = int(
        os.path.basename(existing_frames[-1])
        .replace("frame_", "")
        .replace(".png", "")
    )
    start_frame = last_frame + 1
    print(f"Found {len(existing_frames)} existing frames. Resuming from frame {start_frame}")
else:
    start_frame = 1
    print("Starting new render")

# ============================================================
# RENDER LOOP
# ============================================================

for i in range(start_frame, states + 1):

    cmd.frame(i)

    # Slow cinematic rotation
    cmd.turn("y", 0.2)

    # Zoom into pocket during last quarter and dynamically reveal interactions
    if i > int(states * 0.75):
        cmd.show("sticks", "interacting_res")
        cmd.hide("sticks", "interacting_res and name N+C+O")
        cmd.show("dash", "hbonds")
        cmd.show("dash", "hydrophobic_contacts")
        cmd.zoom("lig or interacting_res", buffer=5, animate=0)

    # Final binding pose anchor
    if i == states:
        cmd.center("lig")
        cmd.zoom("lig or interacting_res", buffer=4)
        cmd.show("sticks", "interacting_res")
        cmd.hide("sticks", "interacting_res and name N+C+O")
        cmd.show("dash", "hbonds")
        cmd.show("dash", "hydrophobic_contacts")

    outfile = f"{FRAME_DIR}/frame_{i:05d}.png"

    cmd.png(
        outfile,
        width=1280,
        height=720,
        dpi=150,
        ray=0
    )

    print(f"Rendered frame {i}/{states}")

# ============================================================
# CREATE MOVIE — WITHOUT -r (output fps = input fps = 10)
# Slow motion but may appear choppy on some players
# ============================================================

print("All frames rendered")

if os.path.exists(MOVIE_FILE):
    os.remove(MOVIE_FILE)

print("Creating MP4 using FFmpeg (no -r flag)")

subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-framerate", "1",          # Slow: 1 frames consumed per second
        "-i", f"{FRAME_DIR}/frame_%05d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        MOVIE_FILE
    ],
    check=True
)

print(f"Movie saved as {MOVIE_FILE}")
print("Done")
