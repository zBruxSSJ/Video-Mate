"""Escena 5 — Condición de continuidad en x = 3 (~35 s / 840 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 35
N_FRAMES = DURATION_S * su.FPS

CARD_W = 0.80
CARD_H = 0.165
CARD_YS = [0.665, 0.455, 0.245]
CARD_STARTS = [90, 210, 330]

STEPS = [
    ("①", su.ORANGE, "Límite lateral izquierdo en x = 3 (tramo ax + b)",
     r"$\lim_{x \to 3^-} (ax+b) = 3a + b$", "Nos acercamos a x = 3 por la izquierda."),
    ("②", su.RED, "Valor de g en x = 3 (tramo 3x)",
     r"$g(3) = 3(3) = 9$", "x = 3 pertenece al tercer tramo: x ≥ 3."),
    ("③", su.GOLD, "Igualamos para que sea continua",
     r"$3a + b = 9$", "El límite y el valor de la función deben coincidir."),
]

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 40)
    if p_title > 0:
        y = 0.925 - (1 - p_title) * 0.03
        ax.text(0.5, y, "CONDICIÓN EN x = 3", fontsize=32,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.seg_progress(frame, 30, 40)
    if p_sub > 0:
        ax.text(0.5, 0.855,
                 "Repetimos el mismo análisis en el segundo punto de unión:",
                 fontsize=15, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    for (badge, color, title, formula, note), cy, start in zip(STEPS, CARD_YS, CARD_STARTS):
        p = su.seg_progress(frame, start, 50)
        su.step_card(ax, 0.5, cy, CARD_W, CARD_H, badge, color, title, formula, note, p)

    p_eq = su.seg_progress(frame, 410, 45)
    if p_eq > 0:
        pulse = 1.0 if frame < 455 else 0.88 + 0.12 * (0.5 + 0.5 * np.sin((frame - 455) / 14.0))
        scale = 0.6 + 0.4 * p_eq
        su.rounded_card(ax, 0.5, 0.075, 0.52, 0.11,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_eq), edgecolor=su.GOLD,
                         radius=0.02, lw=2.4 * pulse if p_eq >= 1 else 2.4, scale=scale)
        ax.text(0.5, 0.075, r"ECUACIÓN 2:      $3a + b = 9$", fontsize=21,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.GOLD, p_eq),
                 ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene5_condicion_x3.mp4"))
