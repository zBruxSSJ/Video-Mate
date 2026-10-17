"""Escena 1 — Introducción (~25 s / 600 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 25
N_FRAMES = DURATION_S * su.FPS

XMIN, XMAX = -4.2, 4.2
YMIN, YMAX = -3.2, 5.6

fig = su.make_base_figure()
gax = fig.add_axes([0, 0, 1, 1])
ax = su.setup_full_axes(fig)


def style_gax():
    gax.set_facecolor("none")
    gax.set_xlim(XMIN, XMAX)
    gax.set_ylim(YMIN, YMAX)
    gax.axis("off")


def curve_fn(x):
    return 1.6 * np.sin(x * 0.85) + 0.6


def draw(frame):
    su.clear_axes(ax)
    gax.cla()
    style_gax()

    # --- Plano cartesiano decorativo ---
    p_axes = su.seg_progress(frame, 0, 45)
    if p_axes > 0:
        xw = (XMAX - XMIN) / 2 * p_axes
        yw = (YMAX - YMIN) / 2 * p_axes
        su.glow_plot(gax, [-xw, xw], [0, 0], su.TEXT_FAINT, lw=1.6, alpha_core=0.5 * p_axes)
        su.glow_plot(gax, [0, 0], [-yw, yw], su.TEXT_FAINT, lw=1.6, alpha_core=0.5 * p_axes)
        if p_axes > 0.97:
            for gx in range(int(XMIN) + 1, int(XMAX)):
                if gx != 0:
                    gax.plot([gx, gx], [YMIN, YMAX], color=su.TEXT_FAINT, lw=0.6,
                              alpha=0.10, zorder=1)
            for gy in range(int(YMIN) + 1, int(YMAX)):
                if gy != 0:
                    gax.plot([XMIN, XMAX], [gy, gy], color=su.TEXT_FAINT, lw=0.6,
                              alpha=0.10, zorder=1)

    # --- Curva que se dibuja progresivamente ---
    p_curve = su.seg_progress(frame, 35, 150)
    if p_curve > 0:
        x_cur = XMIN + p_curve * (XMAX - XMIN)
        xs = np.linspace(XMIN, x_cur, 220)
        ys = curve_fn(xs)
        su.glow_plot(gax, xs, ys, su.CELESTE, lw=3.4, alpha_core=0.9, zorder=5)
        if p_curve < 1.0:
            hx = x_cur
            hy = curve_fn(hx)
            su.glow_point(gax, hx, hy, su.WHITE, size=8, zorder=8)

    # --- Tarjeta de título ---
    p_card = su.seg_progress(frame, 150, 40)
    if p_card > 0:
        scale = 0.85 + 0.15 * p_card
        su.rounded_card(ax, 0.5, 0.50, 0.70, 0.40, facecolor=su.rgba(su.CARD_BG, p_card * 0.97),
                         edgecolor=su.CELESTE, radius=0.025, lw=2.0, scale=scale)

    p_title = su.seg_progress(frame, 170, 40)
    if p_title > 0:
        y = 0.615 - (1 - p_title) * 0.02
        ax.text(0.5, y, "DETECTIVES DE LA\nCONTINUIDAD", fontsize=42,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center", linespacing=1.15)

    p_bar = su.seg_progress(frame, 195, 20)
    if p_bar > 0:
        bar_w = 0.22 * p_bar
        su.glow_plot(ax, [0.5 - bar_w / 2, 0.5 + bar_w / 2], [0.505, 0.505],
                     su.VIOLET, lw=2.6, alpha_core=p_bar)

    p_sub = su.seg_progress(frame, 210, 30)
    if p_sub > 0:
        ax.text(0.5, 0.455, "Develando los secretos de las funciones", fontsize=20,
                 fontfamily=su.FONT_TITLE_MD, color=su.rgba(su.CELESTE_SOFT, p_sub),
                 ha="center", va="center")

    p_road = su.seg_progress(frame, 250, 40)
    if p_road > 0:
        ax.text(0.5, 0.375,
                 "Hoy vamos a descubrir qué es la continuidad\n"
                 "y cómo identificar los distintos tipos de discontinuidad.",
                 fontsize=15, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_road),
                 ha="center", va="center", linespacing=1.6)

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene1_intro.mp4"))
