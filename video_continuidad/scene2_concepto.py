"""Escena 2 — Concepto de continuidad (~50 s / 1200 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 50
N_FRAMES = DURATION_S * su.FPS

CONDITIONS = [
    ("①", su.CELESTE, "f(a) existe",
     r"$f(a)$ está definido", "El punto x = a pertenece al dominio de f."),
    ("②", su.VIOLET, "El límite existe",
     r"$\lim_{x \to a} f(x)$ es finito", "Los límites laterales son iguales."),
    ("③", su.AMBER, "Coinciden",
     r"$\lim_{x \to a} f(x) = f(a)$", "El límite y el valor de la función son iguales."),
]
CARD_YS = [0.665, 0.455, 0.245]
CARD_STARTS = [75, 150, 225]

# Fase 2
P1_OUT = 330
P1_OUT_DUR = 35
P2_IN = 380

XMIN, XMAX = -0.6, 4.2
YMIN, YMAX = -1.0, 9.5

fig = su.make_base_figure()
gax = fig.add_axes([0.07, 0.10, 0.50, 0.68])
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
    gax.set_xticks(range(0, 5))
    gax.set_yticks(range(0, 10, 2))
    gax.grid(True, color=su.TEXT_FAINT, alpha=0.12, linewidth=0.8)
    for lbl in gax.get_xticklabels() + gax.get_yticklabels():
        lbl.set_fontfamily(su.FONT_BODY)
    gax.set_axisbelow(True)


def f(x):
    return x ** 2


def draw(frame):
    su.clear_axes(ax)
    gax.cla()
    gax.axis("off")

    # ---------------- FASE 1: las 3 condiciones ----------------
    p_title = su.inout_progress(frame, 0, 28, P1_OUT, P1_OUT_DUR)
    if p_title > 0:
        y = 0.915 - (1 - p_title) * 0.03
        ax.text(0.5, y, "¿QUÉ ES LA CONTINUIDAD?", fontsize=36,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.inout_progress(frame, 24, 28, P1_OUT, P1_OUT_DUR)
    if p_sub > 0:
        ax.text(0.5, 0.845,
                 "Una función f es continua en x = a cuando se cumplen,\n"
                 "al mismo tiempo, estas tres condiciones:",
                 fontsize=16, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center", linespacing=1.5)

    for (num, color, name, formula, desc), cy, start in zip(CONDITIONS, CARD_YS, CARD_STARTS):
        p_raw = su.seg_progress(frame, start, 40)
        p_out = 1.0 if frame < P1_OUT else max(0.0, 1 - (frame - P1_OUT) / P1_OUT_DUR)
        p = p_raw * p_out
        if p <= 0:
            continue
        scale = 0.85 + 0.15 * p
        su.rounded_card(ax, 0.5, cy, 0.80, 0.165, facecolor=su.rgba(su.CARD_BG, p),
                         edgecolor=color, radius=0.02, lw=1.8, scale=scale)
        text_alpha = su.fade_alpha(p, 0.35, 1.0)
        badge_x = 0.5 - 0.80 / 2 + 0.075
        su.circle_patch(ax, badge_x, cy, 0.048, facecolor=su.rgba(color, text_alpha * 0.18),
                         edgecolor=color, linewidth=2, zorder=4)
        ax.text(badge_x, cy, num, fontsize=24, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, text_alpha), ha="center", va="center", zorder=5)
        text_x = 0.5 - 0.80 / 2 + 0.165
        ax.text(text_x, cy + 0.042, name, fontsize=18, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, text_alpha), ha="left", va="center")
        ax.text(text_x, cy, formula, fontsize=18, fontfamily=su.FONT_BODY_MD,
                 color=su.rgba(su.TEXT_LIGHT, text_alpha), ha="left", va="center")
        ax.text(text_x, cy - 0.045, desc, fontsize=13, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, text_alpha), ha="left", va="center")

    # ---------------- FASE 2: ejemplo f(x) = x^2 ----------------
    p_head2 = su.seg_progress(frame, P2_IN, 28)
    if p_head2 > 0:
        y = 0.925 - (1 - p_head2) * 0.02
        ax.text(0.5, y, "EJEMPLO: ¿ES CONTINUA EN x = 2?", fontsize=28,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_head2),
                 ha="center", va="center")

    p_formula = su.seg_progress(frame, P2_IN + 25, 28)
    if p_formula > 0:
        ax.text(0.5, 0.855, r"$f(x) = x^2$", fontsize=24, fontfamily=su.FONT_BODY_MD,
                 color=su.rgba(su.CELESTE, p_formula), ha="center", va="center")

    if p_head2 > 0:
        style_gax()

    p_curve = su.seg_progress(frame, P2_IN + 60, 110)
    if p_curve > 0:
        x_cur = p_curve * XMAX
        xs = np.linspace(0, max(x_cur, 0.001), 150)
        su.glow_plot(gax, xs, f(xs), su.CELESTE, lw=3.4, alpha_core=1.0, zorder=5)

    p_point = su.seg_progress(frame, P2_IN + 175, 35)
    if p_point > 0:
        gax.plot([2, 2], [YMIN, 4], linestyle=(0, (4, 3)), color=su.TEXT_FAINT,
                  linewidth=1.3, alpha=0.5 * p_point, zorder=3)
        gax.plot([XMIN, 2], [4, 4], linestyle=(0, (4, 3)), color=su.TEXT_FAINT,
                  linewidth=1.3, alpha=0.5 * p_point, zorder=3)
        su.closed_point(gax, 2, 4, su.VIOLET, size=12, zorder=7)
        gax.text(2.15, 4.35, "(2, 4)", fontsize=14, fontfamily=su.FONT_BODY_SB,
                  color=su.rgba(su.VIOLET, p_point), zorder=7)

    # Panel lateral de verificación
    panel_x0 = 0.635
    steps = [
        (f"f(2) = {2}² = 4", su.CELESTE, P2_IN + 175),
        (r"$\lim_{x \to 2} x^2 = 4$", su.VIOLET, P2_IN + 225),
        ("¡Coinciden! f es continua en x = 2", su.GREEN, P2_IN + 275),
    ]
    step_ys = [0.70, 0.58, 0.44]
    for (text, color, start), y in zip(steps, step_ys):
        p = su.seg_progress(frame, start, 32)
        if p <= 0:
            continue
        h = 0.135 if y != 0.44 else 0.155
        su.rounded_card(ax, panel_x0 + 0.165, y, 0.33, h, facecolor=su.rgba(su.CARD_BG, p),
                         edgecolor=color, radius=0.02, lw=1.8, scale=0.88 + 0.12 * p)
        ax.text(panel_x0 + 0.165, y, text, fontsize=15.5, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, p), ha="center", va="center", wrap=True)

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene2_concepto.mp4"))
