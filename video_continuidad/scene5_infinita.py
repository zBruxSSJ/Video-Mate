"""Escena 5 — Discontinuidad inevitable infinita (~55 s / 1320 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 55
N_FRAMES = DURATION_S * su.FPS

STEPS = [
    ("①", su.CELESTE, "Evaluamos h(−3)",
     r"$h(-3) = \frac{2}{0}$  (no definido)", "No se puede dividir entre cero."),
    ("②", su.VIOLET, "Límite por la izquierda",
     r"$\lim_{x \to -3^-} h(x) = -\infty$", "Los valores decrecen sin límite."),
    ("③", su.ROSE, "Límite por la derecha",
     r"$\lim_{x \to -3^+} h(x) = +\infty$", "Los valores crecen sin límite."),
]
CARD_YS = [0.665, 0.455, 0.245]
CARD_STARTS = [65, 140, 215]

P1_OUT = 330
P1_OUT_DUR = 32
P2_IN = 375

XMIN, XMAX = -7.0, 1.0
YMIN, YMAX = -9.5, 9.5
YLIM = 9.0
X_ASYM = -3.0
X_LEFT_END = X_ASYM - 2.0 / YLIM
X_RIGHT_START = X_ASYM + 2.0 / YLIM

fig = su.make_base_figure()
gax = fig.add_axes([0.05, 0.08, 0.56, 0.72])
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
    gax.set_xticks(range(-7, 2))
    gax.set_yticks(range(-8, 9, 4))
    gax.grid(True, color=su.TEXT_FAINT, alpha=0.12, linewidth=0.8)
    for lbl in gax.get_xticklabels() + gax.get_yticklabels():
        lbl.set_fontfamily(su.FONT_BODY)
    gax.set_axisbelow(True)


def h(x):
    return 2.0 / (x + 3.0)


def draw(frame):
    su.clear_axes(ax)
    gax.cla()
    gax.axis("off")

    # ---------------- FASE 1 ----------------
    p_title = su.inout_progress(frame, 0, 26, P1_OUT, P1_OUT_DUR)
    if p_title > 0:
        y = 0.915 - (1 - p_title) * 0.03
        ax.text(0.5, y, "DISCONTINUIDAD INFINITA", fontsize=34,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.inout_progress(frame, 22, 26, P1_OUT, P1_OUT_DUR)
    if p_sub > 0:
        ax.text(0.5, 0.845,
                 r"$h(x) = \frac{2}{x+3}$"
                 "\nAnalicemos qué pasa en x = −3.",
                 fontsize=16, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center", linespacing=1.8)

    for (badge, color, title, formula, note), cy, start in zip(STEPS, CARD_YS, CARD_STARTS):
        p_raw = su.seg_progress(frame, start, 36)
        p_out = 1.0 if frame < P1_OUT else max(0.0, 1 - (frame - P1_OUT) / P1_OUT_DUR)
        p = p_raw * p_out
        su.step_card(ax, 0.5, cy, 0.78, 0.165, badge, color, title, formula, note, p,
                     formula_size=19)

    # ---------------- FASE 2: gráfico ----------------
    p_head2 = su.seg_progress(frame, P2_IN, 26)
    if p_head2 > 0:
        y = 0.945 - (1 - p_head2) * 0.02
        ax.text(0.30, y, "h(x) EN x = −3", fontsize=23,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_head2),
                 ha="center", va="center")
        style_gax()

    p_asym = su.seg_progress(frame, P2_IN + 35, 40)
    if p_asym > 0:
        yh = YMIN + p_asym * (YMAX - YMIN)
        gax.plot([X_ASYM, X_ASYM], [YMIN, yh], linestyle=(0, (5, 3)), color=su.TEXT_LIGHT,
                  linewidth=1.6, alpha=0.55 * p_asym, zorder=3)

    p_left = su.seg_progress(frame, P2_IN + 85, 120)
    if p_left > 0:
        x_cur = XMIN + p_left * (X_LEFT_END - XMIN)
        xs = np.linspace(XMIN, x_cur, 160)
        su.glow_plot(gax, xs, h(xs), su.VIOLET, lw=3.2, alpha_core=1.0, zorder=5)

    p_right = su.seg_progress(frame, P2_IN + 205, 120)
    if p_right > 0:
        x_cur = XMAX - p_right * (XMAX - X_RIGHT_START)
        xs = np.linspace(x_cur, XMAX, 160)
        su.glow_plot(gax, xs, h(xs), su.ROSE, lw=3.2, alpha_core=1.0, zorder=5)

    p_arrows = su.seg_progress(frame, P2_IN + 335, 30)
    if p_arrows > 0:
        gax.annotate("", xy=(X_ASYM - 0.08, YMIN + 0.3), xytext=(X_ASYM - 0.08, YMIN + 1.6),
                      arrowprops=dict(arrowstyle="-|>", color=su.VIOLET, alpha=p_arrows, lw=2))
        gax.text(X_ASYM - 0.25, YMIN + 1.0, r"$-\infty$", fontsize=15, color=su.rgba(su.VIOLET, p_arrows),
                  fontfamily=su.FONT_BODY_SB, ha="right", va="center")
        gax.annotate("", xy=(X_ASYM + 0.08, YMAX - 0.3), xytext=(X_ASYM + 0.08, YMAX - 1.6),
                      arrowprops=dict(arrowstyle="-|>", color=su.ROSE, alpha=p_arrows, lw=2))
        gax.text(X_ASYM + 0.25, YMAX - 1.0, r"$+\infty$", fontsize=15, color=su.rgba(su.ROSE, p_arrows),
                  fontfamily=su.FONT_BODY_SB, ha="left", va="center")

    p_lbl = su.seg_progress(frame, P2_IN + 365, 25)
    if p_lbl > 0:
        gax.text(X_ASYM, YMIN - 0.55, "x = −3\n(asíntota vertical)", fontsize=12.5,
                  fontfamily=su.FONT_BODY_SB, color=su.rgba(su.TEXT_LIGHT, p_lbl),
                  ha="center", va="top", linespacing=1.4)

    # Panel lateral
    panel_x0 = 0.665
    p_err = su.seg_progress(frame, P2_IN + 415, 35)
    if p_err > 0:
        su.rounded_card(ax, panel_x0 + 0.16, 0.705, 0.355, 0.255,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_err), edgecolor=su.ROSE,
                         radius=0.025, lw=2.0, scale=0.85 + 0.15 * p_err)
        ax.text(panel_x0 + 0.16, 0.795, "⚠ ERROR FRECUENTE", fontsize=14.5,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.ROSE, p_err),
                 ha="center", va="center")
        ax.text(panel_x0 + 0.16, 0.705,
                 "Pensar que, como aparece el\ninfinito, el límite existe y\nla función es continua.",
                 fontsize=12.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_LIGHT, p_err),
                 ha="center", va="center", linespacing=1.6)
        ax.text(panel_x0 + 0.16, 0.615, "Es incorrecto: el límite infinito\nNO es un número real.",
                 fontsize=12, fontfamily=su.FONT_BODY_SB, color=su.rgba(su.ROSE, p_err),
                 ha="center", va="center", linespacing=1.5)

    p_concl = su.seg_progress(frame, P2_IN + 460, 35)
    if p_concl > 0:
        su.rounded_card(ax, panel_x0 + 0.16, 0.395, 0.355, 0.185,
                         facecolor=su.rgba(su.CARD_BG, p_concl), edgecolor=su.VIOLET,
                         radius=0.025, lw=2.0, scale=0.85 + 0.15 * p_concl)
        ax.text(panel_x0 + 0.16, 0.45, "INEVITABLE", fontsize=14.5,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.VIOLET, p_concl),
                 ha="center", va="center")
        ax.text(panel_x0 + 0.16, 0.40, "INFINITA", fontsize=21, fontfamily=su.FONT_TITLE_XB,
                 color=su.rgba(su.VIOLET, p_concl), ha="center", va="center")
        ax.text(panel_x0 + 0.16, 0.345, "Comportamiento infinito\ncerca de x = −3.",
                 fontsize=12, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_concl),
                 ha="center", va="center", linespacing=1.5)

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene5_infinita.mp4"))
