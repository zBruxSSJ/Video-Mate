"""Escena 7 — Verificación gráfica (~31 s / 744 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 31
N_FRAMES = DURATION_S * su.FPS

# Dominio / rango de datos del gráfico
XMIN, XMAX = -1.3, 5.3
YMIN, YMAX = -1.5, 16.5

GRAPH_BOX = [0.045, 0.095, 0.565, 0.72]   # left, bottom, width, height (fracción de figura)


def f1(x):
    return x + 1


def f2(x):
    return 3.5 * x - 1.5


def f3(x):
    return 3 * x


fig = su.make_base_figure()
gax = fig.add_axes(GRAPH_BOX)
ax = su.setup_full_axes(fig)   # overlay para título y panel lateral


def style_gax():
    gax.set_facecolor("none")
    gax.set_xlim(XMIN, XMAX)
    gax.set_ylim(YMIN, YMAX)
    for spine in ["top", "right"]:
        gax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        gax.spines[spine].set_color(su.TEXT_FAINT)
        gax.spines[spine].set_linewidth(1.2)
    gax.tick_params(colors=su.TEXT_DIM, labelsize=10.5)
    gax.set_xticks(range(-1, 6))
    gax.set_yticks(range(0, 17, 2))
    gax.grid(True, color=su.TEXT_FAINT, alpha=0.12, linewidth=0.8)
    for lbl in gax.get_xticklabels() + gax.get_yticklabels():
        lbl.set_fontfamily(su.FONT_BODY)
    gax.set_axisbelow(True)


SEGMENTS = [
    (f1, XMIN, 1.0, su.TURQUOISE, 110, 86, "x + 1", (-0.65, 2.4)),
    (f2, 1.0, 3.0, su.ORANGE, 210, 86, r"$\frac{7}{2}x - \frac{3}{2}$", (2.08, 5.9)),
    (f3, 3.0, XMAX, su.RED, 310, 86, "3x", (3.85, 13.6)),
]

CHECKLIST = [
    ("g(a) existe en x = 1 y x = 3", su.TURQUOISE),
    ("Límites laterales iguales", su.ORANGE),
    (r"$\lim g(x) = g(a)$ en ambos puntos", su.VIOLET),
]


def draw(frame):
    su.clear_axes(ax)
    gax.cla()
    style_gax()

    # --- Título ---
    p_title = su.seg_progress(frame, 0, 24)
    if p_title > 0:
        y = 0.955 - (1 - p_title) * 0.02
        ax.text(0.5, y, "VERIFICACIÓN GRÁFICA", fontsize=28,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    p_sub = su.seg_progress(frame, 20, 24)
    if p_sub > 0:
        ax.text(0.5, 0.895, "Dibujamos los tres tramos y comprobamos que no hay saltos ni agujeros:",
                 fontsize=13.5, fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_sub),
                 ha="center", va="center")

    # --- Curvas progresivas ---
    for f, x0, x1, color, start, dur, label, label_pos in SEGMENTS:
        p = su.seg_progress(frame, start, dur)
        if p <= 0:
            continue
        x_cur = x0 + p * (x1 - x0)
        xs = np.linspace(x0, x_cur, 120)
        ys = f(xs)
        su.glow_plot(gax, xs, ys, color, lw=3.2, alpha_core=1.0, zorder=5)
        if p > 0.9:
            la = su.fade_alpha(p, 0.9, 1.0)
            gax.text(label_pos[0], label_pos[1], label, fontsize=14,
                      fontfamily=su.FONT_BODY_SB, color=su.rgba(color, la), zorder=6)

    # --- Puntos de unión con guías punteadas ---
    for (px, py), color, start, lbl_off in [
        ((1, 2), su.TURQUOISE, 410, (0.18, -0.95)),
        ((3, 9), su.RED, 460, (0.18, 0.75)),
    ]:
        p = su.seg_progress(frame, start, 40)
        if p <= 0:
            continue
        gax.plot([XMIN, px], [py, py], linestyle=(0, (4, 3)), color=su.TEXT_FAINT,
                  linewidth=1.3, alpha=0.55 * p, zorder=3)
        gax.plot([px, px], [YMIN, py], linestyle=(0, (4, 3)), color=su.TEXT_FAINT,
                  linewidth=1.3, alpha=0.55 * p, zorder=3)
        su.glow_point(gax, px, py, su.GOLD, size=9, zorder=7)
        gax.text(px + lbl_off[0], py + lbl_off[1], f"({px}, {py})", fontsize=12.5,
                  fontfamily=su.FONT_BODY_SB, color=su.rgba(su.GOLD, p), zorder=7)

    # --- Panel lateral ---
    panel_x0 = 0.655
    p_panel_title = su.seg_progress(frame, 410, 24)
    if p_panel_title > 0:
        ax.text(panel_x0, 0.80, "VERIFICACIÓN", fontsize=16.5, fontfamily=su.FONT_TITLE_SB,
                 color=su.rgba(su.TEXT_LIGHT, p_panel_title), ha="left", va="center")

    item_starts = [440, 480, 520]
    item_ys = [0.685, 0.575, 0.445]
    for (text, color), y, start in zip(CHECKLIST, item_ys, item_starts):
        p = su.seg_progress(frame, start, 34)
        if p <= 0:
            continue
        su.rounded_card(ax, panel_x0 + 0.155, y, 0.31, 0.105,
                         facecolor=su.rgba(su.CARD_BG, p), edgecolor=color,
                         radius=0.02, lw=1.5, scale=0.9 + 0.1 * p)
        check_alpha = su.fade_alpha(p, 0.5, 1.0)
        su.circle_patch(ax, panel_x0 + 0.045, y, 0.028,
                         facecolor=su.rgba(su.GREEN, check_alpha * 0.25), edgecolor=su.GREEN,
                         linewidth=1.6, zorder=6)
        ax.text(panel_x0 + 0.045, y, "✓", fontsize=13, fontfamily=su.FONT_BODY_SB,
                 color=su.rgba(su.GREEN, check_alpha), ha="center", va="center", zorder=7)
        ax.text(panel_x0 + 0.09, y, text, fontsize=11.5, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_LIGHT, p), ha="left", va="center", zorder=7,
                 wrap=True)

    # --- Mensaje final ---
    p_final = su.seg_progress(frame, 590, 40)
    if p_final > 0:
        pulse = 1.0 if frame < 635 else 0.85 + 0.15 * (0.5 + 0.5 * np.sin((frame - 635) / 16.0))
        scale = 0.7 + 0.3 * p_final
        su.rounded_card(ax, panel_x0 + 0.155, 0.235, 0.335, 0.235,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_final), edgecolor=su.GREEN,
                         radius=0.03, lw=2.2 * pulse if p_final >= 1 else 2.2, scale=scale)
        ax.text(panel_x0 + 0.155, 0.285, "g es", fontsize=14, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, p_final), ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.225, "CONTINUA", fontsize=21, fontfamily=su.FONT_TITLE_XB,
                 color=su.rgba(su.GREEN, p_final), ha="center", va="center")
        ax.text(panel_x0 + 0.155, 0.175, "en todo su dominio", fontsize=12, fontfamily=su.FONT_BODY,
                 color=su.rgba(su.TEXT_DIM, p_final), ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene7_verificacion.mp4"))
