"""Escena 8 — Cierre (~19 s / 456 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 19
N_FRAMES = DURATION_S * su.FPS

CARDS = [
    ("1", su.TURQUOISE, "Puntos de corte",
     "Identificamos los puntos de unión del dominio: x = 1 y x = 3."),
    ("2", su.ORANGE, "Plantear la condición",
     "Igualamos el límite lateral con el valor de la función en cada punto."),
    ("3", su.GOLD, "Resolver el sistema",
     "Restamos las dos ecuaciones y despejamos a y b."),
    ("4", su.VIOLET, "Resultado final",
     r"$a = \frac{7}{2}\;\;\;\;\;b = -\frac{3}{2}$"),
]

CENTERS = [(0.285, 0.645), (0.715, 0.645), (0.285, 0.345), (0.715, 0.345)]
CARD_W, CARD_H = 0.40, 0.255
STARTS = [55, 100, 145, 190]

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 24)
    if p_title > 0:
        y = 0.935 - (1 - p_title) * 0.03
        ax.text(0.5, y, "RESUMEN DEL PROCEDIMIENTO", fontsize=28,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    for (num, color, title, desc), (cx, cy), start in zip(CARDS, CENTERS, STARTS):
        p = su.seg_progress(frame, start, 30)
        if p <= 0:
            continue
        scale = 0.82 + 0.18 * p
        su.rounded_card(ax, cx, cy, CARD_W, CARD_H, facecolor=su.rgba(su.CARD_BG, p),
                         edgecolor=color, radius=0.028, lw=2.0, scale=scale)
        text_alpha = su.fade_alpha(p, 0.4, 1.0)
        su.circle_patch(ax, cx, cy + CARD_H * 0.37, 0.028,
                         facecolor=su.rgba(color, text_alpha * 0.2), edgecolor=color,
                         linewidth=1.8, zorder=6)
        ax.text(cx, cy + CARD_H * 0.37, num, fontsize=13, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, text_alpha), ha="center", va="center", zorder=7)
        ax.text(cx, cy + CARD_H * 0.11, title, fontsize=16, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(color, text_alpha), ha="center", va="center")
        ax.text(cx, cy - CARD_H * 0.20, desc, fontsize=11.5, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_LIGHT, text_alpha), ha="center", va="center",
                 wrap=True)

    p_thanks = su.seg_progress(frame, 255, 30)
    if p_thanks > 0:
        y = 0.095 - (1 - p_thanks) * 0.02
        ax.text(0.5, y, "¡Gracias por ver!", fontsize=24, fontfamily=su.FONT_TITLE_B,
                 color=su.rgba(su.GOLD, p_thanks), ha="center", va="center")

    p_names = su.seg_progress(frame, 280, 30)
    if p_names > 0:
        ax.text(0.5, 0.045,
                 "Bruno Ferro · Fabrizio Osorio · Sebastián Cardoso · Eugenia Pérez",
                 fontsize=12.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_names),
                 ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene8_cierre.mp4"))
