"""Escena 2 — Las 3 condiciones de continuidad (~38 s / 912 frames)."""
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 38
N_FRAMES = DURATION_S * su.FPS

CONDITIONS = [
    ("①", su.TURQUOISE, "Existencia",
     r"$g(a)$ debe existir",
     "El valor de la función en x = a está definido en su dominio."),
    ("②", su.ORANGE, "Existencia del límite",
     r"límite lateral izquierdo = límite lateral derecho",
     "El límite lateral izquierdo y el límite lateral derecho en x = a existen y son iguales."),
    ("③", su.VIOLET, "Igualdad",
     r"$\lim_{x \to a} g(x) = g(a)$",
     "El límite de la función debe coincidir con el valor g(a)."),
]

CARD_W = 0.80
CARD_H = 0.165
CARD_YS = [0.615, 0.385, 0.155]
CARD_STARTS = [90, 190, 290]

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 40)
    if p_title > 0:
        y = 0.905 - (1 - p_title) * 0.03
        ax.text(0.5, y, "CONDICIONES DE CONTINUIDAD", fontsize=32,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.seg_progress(frame, 35, 40)
    if p_sub > 0:
        y = 0.825 - (1 - p_sub) * 0.02
        ax.text(0.5, y, "Para que g sea continua en x = a, deben cumplirse tres condiciones:",
                 fontsize=16.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    for (num, color, name, formula, desc), cy, start in zip(CONDITIONS, CARD_YS, CARD_STARTS):
        p = su.seg_progress(frame, start, 45)
        if p <= 0:
            continue
        x_off = (1 - p) * 0.12
        cx = 0.5 - x_off
        scale = 0.85 + 0.15 * p
        su.rounded_card(ax, cx, cy, CARD_W, CARD_H,
                         facecolor=su.rgba(su.CARD_BG, p), edgecolor=color,
                         radius=0.022, lw=1.8, scale=scale)

        text_alpha = su.fade_alpha(p, 0.35, 1.0)
        # Número circular a la izquierda
        badge_x = cx - CARD_W / 2 + 0.075
        su.circle_patch(ax, badge_x, cy, 0.052, facecolor=su.rgba(color, text_alpha * 0.18),
                         edgecolor=color, linewidth=2, zorder=4)
        ax.text(badge_x, cy, num, fontsize=26, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, text_alpha), ha="center", va="center", zorder=5)

        text_x = cx - CARD_W / 2 + 0.165
        ax.text(text_x, cy + 0.042, name, fontsize=17, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, text_alpha), ha="left", va="center")
        ax.text(text_x, cy, formula, fontsize=17.5, fontfamily=su.FONT_BODY_MD,
                 color=su.rgba(su.TEXT_LIGHT, text_alpha), ha="left", va="center")
        ax.text(text_x, cy - 0.045, desc, fontsize=12.5, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, text_alpha), ha="left", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene2_condiciones.mp4"))
