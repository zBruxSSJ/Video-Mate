"""Escena 3 — Planteo del problema (~33 s / 792 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 33
N_FRAMES = DURATION_S * su.FPS

ROW_Y = [0.715, 0.575, 0.435]
BRACE_X = 0.335
GX_X = 0.305
FORMULA_X = 0.375
COND_X = 0.635

ROWS = [
    (su.TURQUOISE, r"$x + 1$", r"si  $x < 1$"),
    (su.ORANGE, r"$ax + b$", r"si  $1 \leq x < 3$"),
    (su.RED, r"$3x$", r"si  $x \geq 3$"),
]

# Recta numérica
NL_Y = 0.145
NL_X0, NL_X1 = 0.12, 0.88
NL_VMIN, NL_VMAX = -1, 5


def v2x(v):
    return NL_X0 + (v - NL_VMIN) / (NL_VMAX - NL_VMIN) * (NL_X1 - NL_X0)


fig = su.make_base_figure()
ax = su.setup_full_axes(fig)


def draw_brace(ax, x, y_center, height, color, alpha, width=0.022):
    half = height / 2
    verts = [
        (x, y_center + half),
        (x - width, y_center + half),
        (x - width, y_center + 0.18 * half),
        (x - width * 1.9, y_center),
        (x - width, y_center - 0.18 * half),
        (x - width, y_center - half),
        (x, y_center - half),
    ]
    codes = [1, 2, 3, 3, 3, 2, 2]
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    mid = [
        (x, y_center + half),
        (x - width, y_center + half * 0.55),
        (x - width, y_center + half * 0.12),
        (x - width * 1.9, y_center),
    ]
    mid2 = [
        (x - width * 1.9, y_center),
        (x - width, y_center - half * 0.12),
        (x - width, y_center - half * 0.55),
        (x, y_center - half),
    ]
    pverts = [mid[0], mid[1], mid[2], mid[3], mid2[1], mid2[2], mid2[3]]
    pcodes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
              Path.CURVE4, Path.CURVE4, Path.CURVE4]
    path = Path(pverts, pcodes)
    patch = PathPatch(path, facecolor="none", edgecolor=su.rgba(color, alpha),
                       linewidth=3.0, zorder=4, capstyle="round")
    ax.add_patch(patch)


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 26)
    if p_title > 0:
        y = 0.925 - (1 - p_title) * 0.03
        ax.text(0.5, y, "PLANTEO DEL PROBLEMA", fontsize=30,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.seg_progress(frame, 22, 24)
    if p_sub > 0:
        ax.text(0.5, 0.855, "Analicemos la función definida por partes:", fontsize=15.5,
                 fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    # g(x) = y llave
    p_gx = su.seg_progress(frame, 60, 34)
    if p_gx > 0:
        ax.text(GX_X, ROW_Y[1], r"$g(x) =$", fontsize=24, fontfamily=su.FONT_BODY_MD,
                 color=su.rgba(su.TEXT_LIGHT, p_gx), ha="right", va="center")
        brace_h = (ROW_Y[0] - ROW_Y[2]) + 0.10
        draw_brace(ax, BRACE_X, ROW_Y[1], brace_h * p_gx, su.TEXT_LIGHT, p_gx)

    row_starts = [110, 160, 210]
    for (color, formula, cond), y, start in zip(ROWS, ROW_Y, row_starts):
        p = su.seg_progress(frame, start, 34)
        if p <= 0:
            continue
        x_off = (1 - p) * 0.05
        ax.text(FORMULA_X + x_off, y, formula, fontsize=23, fontfamily=su.FONT_BODY_MD,
                 color=su.rgba(color, p), ha="left", va="center")
        ax.text(COND_X + x_off, y, cond, fontsize=17, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, p), ha="left", va="center")

    # Nota: cada tramo es lineal
    p_note = su.seg_progress(frame, 280, 34)
    if p_note > 0:
        su.rounded_card(ax, 0.5, 0.325, 0.80, 0.085, facecolor=su.rgba(su.CARD_BG_ALT, p_note),
                         edgecolor=su.GREEN, radius=0.018, lw=1.5)
        ax.text(0.5, 0.325,
                 "Cada tramo es lineal  →  es continuo dentro de su propio intervalo.",
                 fontsize=15.5, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(su.TEXT_LIGHT, p_note), ha="center", va="center")

    # Recta numérica
    p_line = su.seg_progress(frame, 350, 50)
    if p_line > 0:
        x_end = NL_X0 + (NL_X1 - NL_X0) * p_line
        su.glow_plot(ax, [NL_X0, x_end], [NL_Y, NL_Y], su.TEXT_DIM, lw=2.2,
                     alpha_core=p_line)
        if p_line > 0.95:
            for v in range(NL_VMIN, NL_VMAX + 1):
                xt = v2x(v)
                ax.plot([xt, xt], [NL_Y - 0.012, NL_Y + 0.012], color=su.TEXT_FAINT,
                         lw=1.3, alpha=p_line, zorder=3)
                if v not in (1, 3):
                    ax.text(xt, NL_Y - 0.045, str(v), fontsize=11, fontfamily=su.FONT_BODY,
                             color=su.rgba(su.TEXT_FAINT, p_line), ha="center", va="center")

    p_pt1 = su.seg_progress(frame, 410, 38)
    if p_pt1 > 0:
        xt = v2x(1)
        su.glow_point(ax, xt, NL_Y, su.TURQUOISE, size=11, zorder=6)
        ax.text(xt, NL_Y - 0.055, "x = 1", fontsize=14.5, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(su.TURQUOISE, p_pt1), ha="center", va="center")
        ax.text(xt, NL_Y + 0.05, "riesgo", fontsize=10.5, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, p_pt1), ha="center", va="center")

    p_pt3 = su.seg_progress(frame, 456, 38)
    if p_pt3 > 0:
        xt = v2x(3)
        su.glow_point(ax, xt, NL_Y, su.RED, size=11, zorder=6)
        ax.text(xt, NL_Y - 0.055, "x = 3", fontsize=14.5, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(su.RED, p_pt3), ha="center", va="center")
        ax.text(xt, NL_Y + 0.05, "riesgo", fontsize=10.5, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, p_pt3), ha="center", va="center")

    p_final = su.seg_progress(frame, 540, 40)
    if p_final > 0:
        ax.text(0.5, 0.045,
                 "Los únicos puntos en riesgo de discontinuidad son x = 1 y x = 3.",
                 fontsize=14, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_LIGHT, p_final),
                 ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene3_planteo.mp4"))
