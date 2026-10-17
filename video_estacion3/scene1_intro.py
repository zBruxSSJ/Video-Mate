"""Escena 1 — Intro (~14 s / 336 frames a 24 fps)."""
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 14
N_FRAMES = DURATION_S * su.FPS

NAMES = [
    ("Bruno Ferro", su.PERSON_COLORS["Bruno"]),
    ("Fabrizio Osorio", su.PERSON_COLORS["Fabrizio"]),
    ("Sebastián Cardoso", su.PERSON_COLORS["Sebastian"]),
    ("Eugenia Pérez", su.PERSON_COLORS["Eugenia"]),
]

CARD_W = 0.205
CARD_H = 0.13
GAP = 0.02
LEFT = 0.06
CENTERS = [LEFT + CARD_W / 2 + i * (CARD_W + GAP) for i in range(4)]
CARD_Y = 0.21

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)


def draw(frame):
    su.clear_axes(ax)

    # Título principal: PROBLEMA 2
    p_title = su.seg_progress(frame, 0, 26)
    if p_title > 0:
        y = 0.855 - (1 - p_title) * 0.035
        ax.text(0.5, y, "PROBLEMA 2", fontsize=46,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    # Barra decorativa con glow debajo del título
    p_bar = su.seg_progress(frame, 20, 18)
    if p_bar > 0:
        bar_w = 0.26 * p_bar
        xs = [0.5 - bar_w / 2, 0.5 + bar_w / 2]
        ys = [0.782, 0.782]
        su.glow_plot(ax, xs, ys, su.TURQUOISE, lw=3.0, alpha_core=p_bar)

    # Enunciado del problema (destacado)
    p_problem = su.seg_progress(frame, 34, 24)
    if p_problem > 0:
        y = 0.705 - (1 - p_problem) * 0.02
        ax.text(0.5, y, "Hallar a y b para que g(x) sea continua en R", fontsize=20,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.GOLD, p_problem),
                 ha="center", va="center")

    # Subtítulo de curso
    p_sub = su.seg_progress(frame, 54, 20)
    if p_sub > 0:
        y = 0.625 - (1 - p_sub) * 0.02
        ax.text(0.5, y, "Matemática  ·  3° BATIN  ·  Estación 3", fontsize=17,
                 fontfamily=su.FONT_BODY_MD, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    # Colegio
    p_school = su.seg_progress(frame, 72, 20)
    if p_school > 0:
        y = 0.565 - (1 - p_school) * 0.02
        ax.text(0.5, y, "San Ignacio de Loyola School  ·  Paraguay", fontsize=14,
                 fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_FAINT, p_school),
                 ha="center", va="center", style="italic")

    # Etiqueta "Equipo"
    p_lbl = su.seg_progress(frame, 92, 16)
    if p_lbl > 0:
        ax.text(0.5, 0.375, "EQUIPO", fontsize=13,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.TEXT_FAINT, p_lbl),
                 ha="center", va="center")

    # Tarjetas de integrantes (aparición escalonada)
    starts = [106, 128, 150, 172]
    for (name, color), cx, start in zip(NAMES, CENTERS, starts):
        p = su.seg_progress(frame, start, 24)
        if p <= 0:
            continue
        scale = 0.75 + 0.25 * p
        su.rounded_card(ax, cx, CARD_Y, CARD_W, CARD_H,
                         facecolor=su.rgba(su.CARD_BG, p), edgecolor=color,
                         radius=0.018, lw=1.8, scale=scale)
        if p > 0.4:
            text_alpha = su.fade_alpha(p, 0.4, 1.0)
            ax.text(cx, CARD_Y, name, fontsize=14.5, fontfamily=su.FONT_BODY_SB,
                     color=su.rgba(su.TEXT_LIGHT, text_alpha), ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene1_intro.mp4"))
