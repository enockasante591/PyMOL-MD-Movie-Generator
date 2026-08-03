# PyMOL-MD-Movie-Generator
utomated PyMOL workflow for generating high-quality molecular dynamics movies from GROMACS trajectories. Produces publication-ready protein–ligand animations with automatic interaction detection, membrane visualization, cinematic camera movement, frame rendering, and FFmpeg video export.
# PyMOL MD Movie Generator

## Overview

This repository provides an automated PyMOL workflow for generating high-quality molecular dynamics (MD) movies from GROMACS trajectories. The pipeline is designed for protein–ligand systems, particularly membrane proteins, and produces publication-ready animations with minimal manual intervention.

The workflow automatically loads trajectories, styles proteins, ligands, and membrane components, identifies ligand–protein interactions, renders trajectory frames, and compiles them into an MP4 movie using FFmpeg.

---

## Features

### Molecular Visualization

- Automatic loading of GROMACS trajectory files
- Cartoon representation of proteins
- Ligand stick representation
- Automatic coloring of molecular components
- Publication-quality visualization settings

### Interaction Analysis

- Automatic hydrogen bond detection
- Automatic hydrophobic contact identification
- Highlighting of interacting residues
- Dynamic interaction visualization during the movie

### Membrane Visualization

- POPC lipid representation
- Cholesterol visualization
- Distinct coloring for membrane components
- Adjustable transparency for improved clarity

### Camera Animation

- Smooth trajectory playback
- Slow cinematic rotation
- Automatic zoom into the ligand-binding pocket
- Final close-up of the binding pose

### Rendering

- High-resolution PNG frame generation
- Resume interrupted rendering
- Automatic frame numbering
- FFmpeg-based MP4 movie generation

---

## Requirements

### Software

- PyMOL (Open Source or Incentive)
- FFmpeg
- Python 3.8+

### Python Modules

- os
- glob
- subprocess

(All are included in the Python standard library.)

---

## Input Files

The workflow expects:

```
movie_structure.gro
movie_pymol.xtc
```

These files should contain the structure and trajectory prepared for visualization.

---

## Usage

Run the script from within PyMOL:

```bash
pymol -cq movie_generator.py
```

---

## Workflow

The pipeline automatically performs:

1. Load structure and trajectory
2. Style protein and ligand
3. Detect hydrogen bonds
4. Detect hydrophobic contacts
5. Style membrane lipids
6. Apply publication-quality visualization settings
7. Render trajectory frames
8. Resume rendering if interrupted
9. Generate an MP4 movie using FFmpeg

---

## Output

```
movie_frames/
    frame_00001.png
    frame_00002.png
    ...

GLP1R_400_500ns.mp4
```

---

## Applications

This workflow is suitable for:

- Molecular dynamics visualization
- GPCR simulations
- Membrane protein studies
- Protein–ligand interaction movies
- Drug discovery presentations
- Scientific publications
- Conference presentations
- Educational molecular animations

---

## License

MIT License
