"""Escena 4 — Condición de continuidad en x = 1 (~40 s / 960 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 40
N_FRAMES = DURATION_S * su.FPS

CARD_W = 0.80
CARD_H = 0.165
CARD_YS = [0.665, 0.455, 0.245]
CARD_STARTS = [90, 220, 350]

STEPS = [
    ("①", su.TURQUOISE, "Límite lateral izquierdo en x = 1 (tramo x + 1)",
     r"$\lim_{x \to 1^-} (x+1) = 2$", "Nos acercamos a x = 1 por la izquierda."),
    ("②", su.ORANGE, "Valor de g en x = 1 (tramo ax + b)",
     r"$g(1) = a(1) + b = a + b$", "x = 1 pertenece al segundo tramo: 1 ≤ x < 3."),
    ("③", su.GOLD, "Igualamos para que sea continua",
     r"$a + b = 2$", "El límite y el valor de la función deben coincidir."),
]

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 40)
    if p_title > 0:
        y = 0.925 - (1 - p_title) * 0.03
        ax.text(0.5, y, "CONDICIÓN EN x = 1", fontsize=32,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.seg_progress(frame, 30, 40)
    if p_sub > 0:
        ax.text(0.5, 0.855,
                 "Verifiquemos las tres condiciones de continuidad en el punto de unión:",
                 fontsize=15, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    for (badge, color, title, formula, note), cy, start in zip(STEPS, CARD_YS, CARD_STARTS):
        p = su.seg_progress(frame, start, 50)
        su.step_card(ax, 0.5, cy, CARD_W, CARD_H, badge, color, title, formula, note, p)

    # Caja final: Ecuación 1
    p_eq = su.seg_progress(frame, 430, 45)
    if p_eq > 0:
        pulse = 1.0 if frame < 475 else 0.88 + 0.12 * (0.5 + 0.5 * np.sin((frame - 475) / 14.0))
        scale = (0.6 + 0.4 * p_eq) * (1.0 if p_eq < 1 else 1.0)
        su.rounded_card(ax, 0.5, 0.075, 0.52, 0.11,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_eq), edgecolor=su.GOLD,
                         radius=0.02, lw=2.4 * pulse if p_eq >= 1 else 2.4, scale=scale)
        ax.text(0.5, 0.075, r"ECUACIÓN 1:      $a + b = 2$", fontsize=21,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.GOLD, p_eq),
                 ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene4_condicion_x1.mp4"))
