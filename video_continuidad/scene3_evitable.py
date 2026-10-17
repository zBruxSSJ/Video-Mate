"""Escena 3 — Discontinuidad evitable (~50 s / 1200 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 50
N_FRAMES = DURATION_S * su.FPS

STEPS = [
    ("①", su.CELESTE, "Valor de la función",
     r"$g(1) = 4$", "Por definición, en x = 1 la función vale 4."),
    ("②", su.VIOLET, "Límites laterales",
     r"$\lim_{x \to 1^-}(3x{-}1){=}2 \;\;\; \lim_{x \to 1^+}(x^2{+}1){=}2$",
     "Izquierda y derecha dan el mismo valor: el límite es 2."),
    ("③", su.AMBER, "Comparamos",
     r"$2 \neq 4$", "El límite existe, pero no coincide con g(1)."),
]
CARD_YS = [0.665, 0.455, 0.245]
CARD_STARTS = [70, 150, 230]

P1_OUT = 350
P1_OUT_DUR = 35
P2_IN = 400

XMIN, XMAX = -1.0, 3.3
YMIN, YMAX = -3.5, 11.0

fig = su.make_base_figure()
gax = fig.add_axes([0.05, 0.08, 0.56, 0.70])
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
    gax.set_xticks(range(-1, 4))
    gax.set_yticks(range(-2, 11, 2))
    gax.grid(True, color=su.TEXT_FAINT, alpha=0.12, linewidth=0.8)
    for lbl in gax.get_xticklabels() + gax.get_yticklabels():
        lbl.set_fontfamily(su.FONT_BODY)
    gax.set_axisbelow(True)


def gL(x):
    return 3 * x - 1


def gR(x):
    return x ** 2 + 1


def draw(frame):
    su.clear_axes(ax)
    gax.cla()
    gax.axis("off")

    # ---------------- FASE 1: pasos de análisis ----------------
    p_title = su.inout_progress(frame, 0, 28, P1_OUT, P1_OUT_DUR)
    if p_title > 0:
        y = 0.915 - (1 - p_title) * 0.03
        ax.text(0.5, y, "DISCONTINUIDAD EVITABLE", fontsize=34,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.inout_progress(frame, 24, 28, P1_OUT, P1_OUT_DUR)
    if p_sub > 0:
        ax.text(0.5, 0.845,
                 r"$g(x) = 3x{-}1$ si $x{<}1$;   $g(1){=}4$;   $g(x){=}x^2{+}1$ si $x{>}1$."
                 "\nAnalicemos qué pasa en x = 1.",
                 fontsize=15.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center", linespacing=1.8)

    for (badge, color, title, formula, note), cy, start in zip(STEPS, CARD_YS, CARD_STARTS):
        p_raw = su.seg_progress(frame, start, 40)
        p_out = 1.0 if frame < P1_OUT else max(0.0, 1 - (frame - P1_OUT) / P1_OUT_DUR)
        p = p_raw * p_out
        su.step_card(ax, 0.5, cy, 0.82, 0.165, badge, color, title, formula, note, p,
                     formula_size=19)

    # ---------------- FASE 2: gráfico ----------------
    p_head2 = su.seg_progress(frame, P2_IN, 28)
    if p_head2 > 0:
        y = 0.935 - (1 - p_head2) * 0.02
        ax.text(0.30, y, "g(x) EN x = 1", fontsize=24,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_head2),
                 ha="center", va="center")
        style_gax()

    p_left = su.seg_progress(frame, P2_IN + 60, 90)
    if p_left > 0:
        x_cur = XMIN + p_left * (1 - XMIN)
        xs = np.linspace(XMIN, x_cur, 120)
        su.glow_plot(gax, xs, gL(xs), su.CELESTE, lw=3.2, alpha_core=1.0, zorder=5)

    p_right = su.seg_progress(frame, P2_IN + 160, 90)
    if p_right > 0:
        x_cur = 1 + p_right * (XMAX - 1)
        xs = np.linspace(1, x_cur, 120)
        su.glow_plot(gax, xs, gR(xs), su.VIOLET, lw=3.2, alpha_core=1.0, zorder=5)

    p_open = su.seg_progress(frame, P2_IN + 270, 30)
    if p_open > 0:
        su.open_point(gax, 1, 2, su.CELESTE_SOFT, size=12, zorder=7)
        gax.text(0.68, 1.1, "(1, 2)", fontsize=13.5, fontfamily=su.FONT_BODY_SB,
                  color=su.rgba(su.CELESTE_SOFT, p_open), ha="right", zorder=7)

    p_closed = su.seg_progress(frame, P2_IN + 305, 30)
    if p_closed > 0:
        su.closed_point(gax, 1, 4, su.ROSE, size=12, zorder=7)
        gax.text(1.15, 4.3, "(1, 4)", fontsize=13.5, fontfamily=su.FONT_BODY_SB,
                  color=su.rgba(su.ROSE, p_closed), zorder=7)

    # Panel lateral
    panel_x0 = 0.665
    p_panel = su.seg_progress(frame, P2_IN + 340, 35)
    if p_panel > 0:
        su.rounded_card(ax, panel_x0 + 0.155, 0.56, 0.345, 0.20,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_panel), edgecolor=su.AMBER,
                         radius=0.025, lw=2.0, scale=0.85 + 0.15 * p_panel)
        ax.text(panel_x0 + 0.155, 0.625, "DISCONTINUIDAD", fontsize=15, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(su.AMBER, p_panel), ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.575, "EVITABLE", fontsize=22, fontfamily=su.FONT_TITLE_XB,
                 color=su.rgba(su.AMBER, p_panel), ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.515, "El límite existe (2),\npero g(1) = 4.",
                 fontsize=13, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_panel),
                 ha="center", va="center", linespacing=1.5)

    p_fix = su.seg_progress(frame, P2_IN + 385, 35)
    if p_fix > 0:
        su.rounded_card(ax, panel_x0 + 0.155, 0.335, 0.345, 0.135,
                         facecolor=su.rgba(su.CARD_BG, p_fix), edgecolor=su.GREEN,
                         radius=0.022, lw=1.8, scale=0.85 + 0.15 * p_fix)
        ax.text(panel_x0 + 0.155, 0.37, "¿Cómo se arregla?", fontsize=13,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.GREEN, p_fix),
                 ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.31, "Redefiniendo g(1) = 2", fontsize=15.5,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.TEXT_LIGHT, p_fix),
                 ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene3_evitable.mp4"))
