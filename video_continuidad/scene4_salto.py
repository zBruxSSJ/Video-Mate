"""Escena 4 — Discontinuidad inevitable finita (de salto) (~45 s / 1080 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 45
N_FRAMES = DURATION_S * su.FPS

STEPS = [
    ("①", su.CELESTE, "Límite por la izquierda",
     r"$\lim_{x \to 0^-} p(x) = 1$", "Para x < 0, la función vale 1."),
    ("②", su.VIOLET, "Límite por la derecha",
     r"$\lim_{x \to 0^+} p(x) = 3$", "Para x ≥ 0, la función vale 3."),
    ("③", su.AMBER, "Comparamos",
     r"$1 \neq 3$", "Los límites laterales son finitos, pero distintos."),
]
CARD_YS = [0.665, 0.455, 0.245]
CARD_STARTS = [65, 140, 215]

P1_OUT = 320
P1_OUT_DUR = 32
P2_IN = 365

XMIN, XMAX = -3.2, 3.2
YMIN, YMAX = -0.8, 4.8

fig = su.make_base_figure()
gax = fig.add_axes([0.07, 0.10, 0.52, 0.68])
ax = su.setup_full_axes(fig)


def style_gax():
    gax.axis("on")
    gax.set_facecolor("none")
    gax.set_xlim(XMIN, XMAX)
    gax.set_ylim(YMIN, YMAX)
    for s in ["top", "right"]:
        gax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        gax.spines[s].set_visible(True)
        gax.spines[s].set_color(su.TEXT_FAINT)
        gax.spines[s].set_linewidth(1.2)
    gax.tick_params(colors=su.TEXT_DIM, labelsize=12, left=True, bottom=True,
                     labelleft=True, labelbottom=True)
    gax.set_xticks(range(-3, 4))
    gax.set_yticks(range(0, 5))
    gax.grid(True, color=su.TEXT_FAINT, alpha=0.12, linewidth=0.8)
    for lbl in gax.get_xticklabels() + gax.get_yticklabels():
        lbl.set_fontfamily(su.FONT_BODY)
    gax.set_axisbelow(True)


def draw(frame):
    su.clear_axes(ax)
    gax.cla()
    gax.axis("off")

    # ---------------- FASE 1 ----------------
    p_title = su.inout_progress(frame, 0, 26, P1_OUT, P1_OUT_DUR)
    if p_title > 0:
        y = 0.915 - (1 - p_title) * 0.03
        ax.text(0.5, y, "DISCONTINUIDAD DE SALTO", fontsize=34,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.inout_progress(frame, 22, 26, P1_OUT, P1_OUT_DUR)
    if p_sub > 0:
        ax.text(0.5, 0.845,
                 r"$p(x) = 1$ si $x < 0$;   $p(x) = 3$ si $x \geq 0$."
                 "\n¿Qué pasa con el límite en x = 0?",
                 fontsize=16, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center", linespacing=1.8)

    for (badge, color, title, formula, note), cy, start in zip(STEPS, CARD_YS, CARD_STARTS):
        p_raw = su.seg_progress(frame, start, 36)
        p_out = 1.0 if frame < P1_OUT else max(0.0, 1 - (frame - P1_OUT) / P1_OUT_DUR)
        p = p_raw * p_out
        su.step_card(ax, 0.5, cy, 0.78, 0.165, badge, color, title, formula, note, p)

    # ---------------- FASE 2: gráfico ----------------
    p_head2 = su.seg_progress(frame, P2_IN, 26)
    if p_head2 > 0:
        y = 0.935 - (1 - p_head2) * 0.02
        ax.text(0.33, y, "p(x) EN x = 0", fontsize=24,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_head2),
                 ha="center", va="center")
        style_gax()

    p_left = su.seg_progress(frame, P2_IN + 55, 80)
    if p_left > 0:
        x_cur = XMIN + p_left * (0 - XMIN)
        xs = np.linspace(XMIN, x_cur, 100)
        su.glow_plot(gax, xs, np.full_like(xs, 1.0), su.CELESTE, lw=3.4, alpha_core=1.0, zorder=5)

    p_right = su.seg_progress(frame, P2_IN + 135, 80)
    if p_right > 0:
        x_cur = 0 + p_right * XMAX
        xs = np.linspace(0, x_cur, 100)
        su.glow_plot(gax, xs, np.full_like(xs, 3.0), su.VIOLET, lw=3.4, alpha_core=1.0, zorder=5)

    p_open = su.seg_progress(frame, P2_IN + 235, 28)
    if p_open > 0:
        su.open_point(gax, 0, 1, su.CELESTE_SOFT, size=12, zorder=7)
        gax.text(-0.18, 0.72, "(0, 1)", fontsize=13.5, fontfamily=su.FONT_BODY_SB,
                  color=su.rgba(su.CELESTE_SOFT, p_open), ha="right", zorder=7)

    p_closed = su.seg_progress(frame, P2_IN + 265, 28)
    if p_closed > 0:
        su.closed_point(gax, 0, 3, su.VIOLET, size=12, zorder=7)
        gax.text(0.18, 3.28, "(0, 3)", fontsize=13.5, fontfamily=su.FONT_BODY_SB,
                  color=su.rgba(su.VIOLET, p_closed), zorder=7)

    p_jump = su.seg_progress(frame, P2_IN + 300, 30)
    if p_jump > 0:
        gax.annotate("", xy=(-0.9, 3), xytext=(-0.9, 1),
                      arrowprops=dict(arrowstyle="<->", color=su.AMBER,
                                       alpha=p_jump, lw=1.6))
        gax.text(-1.05, 2.0, "salto", fontsize=12.5, fontfamily=su.FONT_BODY_SB,
                  color=su.rgba(su.AMBER, p_jump), ha="right", va="center", rotation=90)

    panel_x0 = 0.665
    p_panel = su.seg_progress(frame, P2_IN + 335, 32)
    if p_panel > 0:
        su.rounded_card(ax, panel_x0 + 0.155, 0.50, 0.345, 0.225,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_panel), edgecolor=su.AMBER,
                         radius=0.025, lw=2.0, scale=0.85 + 0.15 * p_panel)
        ax.text(panel_x0 + 0.155, 0.575, "INEVITABLE FINITA", fontsize=14.5,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.AMBER, p_panel),
                 ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.525, "(DE SALTO)", fontsize=20, fontfamily=su.FONT_TITLE_XB,
                 color=su.rgba(su.AMBER, p_panel), ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.455,
                 "Los límites laterales son\nfinitos pero diferentes:\nel límite general no existe.",
                 fontsize=12.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_panel),
                 ha="center", va="center", linespacing=1.6)

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene4_salto.mp4"))
