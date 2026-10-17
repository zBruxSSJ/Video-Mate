"""Escena 6 — Repaso y conclusión (~45 s / 1080 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 45
N_FRAMES = DURATION_S * su.FPS

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)

CARD_W, CARD_H = 0.44, 0.30
CENTERS = {
    "continua": (0.27, 0.69),
    "evitable": (0.73, 0.69),
    "salto": (0.27, 0.345),
    "infinita": (0.73, 0.345),
}
BOX_W, BOX_H = 0.30, 0.125
STARTS = {"continua": 80, "evitable": 170, "salto": 260, "infinita": 350}


def map_box(xs, ys, xr, yr, box):
    x0, y0, w, h = box
    X = x0 + (xs - xr[0]) / (xr[1] - xr[0]) * w
    Y = y0 + (ys - yr[0]) / (yr[1] - yr[0]) * h
    return X, Y


def quad_box(key):
    cx, cy = CENTERS[key]
    x0 = cx - BOX_W / 2
    y0 = cy - BOX_H / 2 - 0.012
    return (x0, y0, BOX_W, BOX_H)


def draw_card_frame(key, color, title, subtitle, p):
    cx, cy = CENTERS[key]
    scale = 0.85 + 0.15 * p
    su.rounded_card(ax, cx, cy, CARD_W, CARD_H, facecolor=su.rgba(su.CARD_BG, p),
                     edgecolor=color, radius=0.025, lw=2.0, scale=scale)
    ax.text(cx, cy + CARD_H / 2 - 0.042, title, fontsize=16.5, fontfamily=su.FONT_BODY_SB,
             color=su.rgba(color, p), ha="center", va="center")
    ax.text(cx, cy - CARD_H / 2 + 0.032, subtitle, fontsize=12, fontfamily=su.FONT_BODY,
             color=su.rgba(su.TEXT_DIM, p), ha="center", va="center")


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 28)
    if p_title > 0:
        y = 0.955 - (1 - p_title) * 0.02
        ax.text(0.5, y, "REPASO: LOS 4 CASOS", fontsize=34,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.seg_progress(frame, 24, 30)
    if p_sub > 0:
        ax.text(0.5, 0.895, "Comparemos continuidad y los tres tipos de discontinuidad:",
                 fontsize=14.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    # --- 1. Continua: f(x) = x^2 ---
    p = su.seg_progress(frame, STARTS["continua"], 35)
    if p > 0:
        draw_card_frame("continua", su.GREEN, "CONTINUA", "Se cumplen las 3 condiciones", p)
        box = quad_box("continua")
        pc = su.seg_progress(frame, STARTS["continua"] + 15, 45)
        if pc > 0:
            xs = np.linspace(0, pc * 2, 80)
            X, Y = map_box(xs, xs ** 2, (0, 2), (0, 4), box)
            su.glow_plot(ax, X, Y, su.CELESTE, lw=2.2, alpha_core=min(p, 1.0))

    # --- 2. Evitable: g(x) ---
    p = su.seg_progress(frame, STARTS["evitable"], 35)
    if p > 0:
        draw_card_frame("evitable", su.AMBER, "EVITABLE", "El límite ≠ el valor de la función", p)
        box = quad_box("evitable")
        pc = su.seg_progress(frame, STARTS["evitable"] + 15, 45)
        if pc > 0:
            xL = np.linspace(0, min(pc * 2, 1) if pc * 2 > 0 else 0, 40)
            if len(xL) > 1:
                X, Y = map_box(xL, 3 * xL - 1, (0, 2), (-1, 5), box)
                su.glow_plot(ax, X, Y, su.CELESTE, lw=2.0, alpha_core=min(p, 1.0))
            if pc * 2 > 1:
                xR = np.linspace(1, min(pc * 2, 2), 40)
                X, Y = map_box(xR, xR ** 2 + 1, (0, 2), (-1, 5), box)
                su.glow_plot(ax, X, Y, su.VIOLET, lw=2.0, alpha_core=min(p, 1.0))
            if pc > 0.9:
                Xo, Yo = map_box(np.array([1]), np.array([2]), (0, 2), (-1, 5), box)
                su.open_point(ax, Xo[0], Yo[0], su.CELESTE_SOFT, size=7, zorder=7)
                Xc, Yc = map_box(np.array([1]), np.array([4]), (0, 2), (-1, 5), box)
                su.closed_point(ax, Xc[0], Yc[0], su.ROSE, size=7, zorder=7)

    # --- 3. Salto: p(x) ---
    p = su.seg_progress(frame, STARTS["salto"], 35)
    if p > 0:
        draw_card_frame("salto", su.VIOLET, "INEVITABLE FINITA", "Límites laterales distintos", p)
        box = quad_box("salto")
        pc = su.seg_progress(frame, STARTS["salto"] + 15, 45)
        if pc > 0:
            xL = np.linspace(-1.5, -1.5 + min(pc * 2, 1) * 1.5, 30)
            X, Y = map_box(xL, np.full_like(xL, 1.0), (-1.5, 1.5), (0, 4), box)
            su.glow_plot(ax, X, Y, su.CELESTE, lw=2.0, alpha_core=min(p, 1.0))
            if pc > 0.5:
                xR = np.linspace(0, min((pc - 0.5) * 2, 1) * 1.5, 30)
                X, Y = map_box(xR, np.full_like(xR, 3.0), (-1.5, 1.5), (0, 4), box)
                su.glow_plot(ax, X, Y, su.VIOLET, lw=2.0, alpha_core=min(p, 1.0))
            if pc > 0.9:
                Xo, Yo = map_box(np.array([0]), np.array([1]), (-1.5, 1.5), (0, 4), box)
                su.open_point(ax, Xo[0], Yo[0], su.CELESTE_SOFT, size=7, zorder=7)
                Xc, Yc = map_box(np.array([0]), np.array([3]), (-1.5, 1.5), (0, 4), box)
                su.closed_point(ax, Xc[0], Yc[0], su.VIOLET, size=7, zorder=7)

    # --- 4. Infinita: h(x) ---
    p = su.seg_progress(frame, STARTS["infinita"], 35)
    if p > 0:
        draw_card_frame("infinita", su.ROSE, "INEVITABLE INFINITA", "Comportamiento infinito", p)
        box = quad_box("infinita")
        xr, yr = (-5.3, -0.7), (-6, 6)
        x_asym = -3
        x_left_end = x_asym - 2.0 / 6
        x_right_start = x_asym + 2.0 / 6
        pc = su.seg_progress(frame, STARTS["infinita"] + 15, 45)
        if pc > 0:
            xL = np.linspace(xr[0], xr[0] + min(pc * 2, 1) * (x_left_end - xr[0]), 60)
            X, Y = map_box(xL, 2 / (xL + 3), xr, yr, box)
            su.glow_plot(ax, X, Y, su.VIOLET, lw=2.0, alpha_core=min(p, 1.0))
            if pc > 0.5:
                t = min((pc - 0.5) * 2, 1)
                xR = np.linspace(xr[1] - t * (xr[1] - x_right_start), xr[1], 60)
                X, Y = map_box(xR, 2 / (xR + 3), xr, yr, box)
                su.glow_plot(ax, X, Y, su.ROSE, lw=2.0, alpha_core=min(p, 1.0))
            if pc > 0.3:
                Xa, _ = map_box(np.array([x_asym]), np.array([0]), xr, yr, box)
                ax.plot([Xa[0], Xa[0]], [box[1], box[1] + box[3]], linestyle=(0, (3, 2)),
                         color=su.TEXT_LIGHT, lw=1.1, alpha=0.5 * min(pc, 1.0), zorder=3)

    p_final = su.seg_progress(frame, 500, 45)
    if p_final > 0:
        pulse = 1.0 if frame < 545 else 0.85 + 0.15 * (0.5 + 0.5 * np.sin((frame - 545) / 16.0))
        su.rounded_card(ax, 0.5, 0.10, 0.90, 0.165,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_final), edgecolor=su.GREEN,
                         radius=0.025, lw=2.2 * pulse if p_final >= 1 else 2.2,
                         scale=0.9 + 0.1 * p_final)
        ax.text(0.5, 0.135,
                 "Antes de decidir si una función es continua,\n"
                 "comprobá siempre las tres condiciones.",
                 fontsize=16, fontfamily=su.FONT_BODY_SB, color=su.rgba(su.TEXT_LIGHT, p_final),
                 ha="center", va="center", linespacing=1.5)

    p_credits = su.seg_progress(frame, 545, 35)
    if p_credits > 0:
        ax.text(0.5, 0.045,
                 "Sofía Cabrera  ·  Micaela Cubilla  ·  Fabrizio Riquelme  ·  Jerónimo Lovera",
                 fontsize=13, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_credits),
                 ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene6_repaso.mp4"))
