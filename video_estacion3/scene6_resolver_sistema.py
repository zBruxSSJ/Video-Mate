"""Escena 6 — Resolver el sistema (~28 s / 672 frames)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scene_utils as su

DURATION_S = 28
N_FRAMES = DURATION_S * su.FPS

fig = su.make_base_figure()
ax = su.setup_full_axes(fig)

# --- Fase 1: sistema y resta -> a = 7/2 --------------------------------
P1_OUT = 330
P1_OUT_DUR = 28
# --- Fase 2: sustitución -> b = -3/2 ------------------------------------
P2_IN = 370
P2_OUT = 555
P2_OUT_DUR = 25
# --- Fase 3: resultado final --------------------------------------------
P3_IN = 580


def draw(frame):
    su.clear_axes(ax)

    p_title = su.seg_progress(frame, 0, 25)
    if p_title > 0:
        y = 0.93 - (1 - p_title) * 0.03
        ax.text(0.5, y, "RESOLVEMOS EL SISTEMA", fontsize=30,
                 fontfamily=su.FONT_TITLE_XB, color=su.rgba(su.TEXT_LIGHT, p_title),
                 ha="center", va="center")

    # ---------------- FASE 1 ----------------
    p_eq1 = su.inout_progress(frame, 40, 22, P1_OUT, P1_OUT_DUR)
    if p_eq1 > 0:
        ax.text(0.5, 0.775, r"Ecuación 1:   $a + b = 2$", fontsize=22,
                 fontfamily=su.FONT_BODY_MD, color=su.rgba(su.TURQUOISE, p_eq1),
                 ha="center", va="center")

    p_eq2 = su.inout_progress(frame, 68, 22, P1_OUT, P1_OUT_DUR)
    if p_eq2 > 0:
        ax.text(0.5, 0.695, r"Ecuación 2:   $3a + b = 9$", fontsize=22,
                 fontfamily=su.FONT_BODY_MD, color=su.rgba(su.ORANGE, p_eq2),
                 ha="center", va="center")

    p_op = su.inout_progress(frame, 108, 22, P1_OUT, P1_OUT_DUR)
    if p_op > 0:
        ax.text(0.5, 0.585, "Restamos:  Ecuación 2 − Ecuación 1", fontsize=17,
                 fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_op),
                 ha="center", va="center")

    p_sub = su.inout_progress(frame, 140, 25, P1_OUT, P1_OUT_DUR)
    if p_sub > 0:
        ax.text(0.5, 0.49, r"$(3a + b) - (a + b) = 9 - 2$", fontsize=22,
                 fontfamily=su.FONT_BODY_MD, color=su.rgba(su.TEXT_LIGHT, p_sub),
                 ha="center", va="center")

    p_simp = su.inout_progress(frame, 176, 22, P1_OUT, P1_OUT_DUR)
    if p_simp > 0:
        ax.text(0.5, 0.40, r"$2a = 7$", fontsize=26,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.TEXT_LIGHT, p_simp),
                 ha="center", va="center")

    p_a = su.inout_progress(frame, 212, 29, P1_OUT, P1_OUT_DUR)
    if p_a > 0:
        scale = 0.6 + 0.4 * min(p_a / 0.6, 1.0) if p_a < 1 else 1.0
        su.rounded_card(ax, 0.5, 0.22, 0.42, 0.135,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_a), edgecolor=su.GOLD,
                         radius=0.022, lw=2.2, scale=scale)
        ax.text(0.5, 0.22, r"$a = \frac{7}{2} = 3{,}5$", fontsize=26,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.GOLD, p_a),
                 ha="center", va="center")

    # ---------------- FASE 2 ----------------
    p_hdr2 = su.inout_progress(frame, P2_IN, 22, P2_OUT, P2_OUT_DUR)
    if p_hdr2 > 0:
        ax.text(0.5, 0.78, "Sustituimos a en la Ecuación 1:", fontsize=17,
                 fontfamily=su.FONT_BODY, color=su.rgba(su.TEXT_DIM, p_hdr2),
                 ha="center", va="center")

    p_s1 = su.inout_progress(frame, P2_IN + 25, 25, P2_OUT, P2_OUT_DUR)
    if p_s1 > 0:
        ax.text(0.5, 0.67, r"$\frac{7}{2} + b = 2$", fontsize=25,
                 fontfamily=su.FONT_BODY_MD, color=su.rgba(su.TEXT_LIGHT, p_s1),
                 ha="center", va="center")

    p_s2 = su.inout_progress(frame, P2_IN + 65, 25, P2_OUT, P2_OUT_DUR)
    if p_s2 > 0:
        ax.text(0.5, 0.53, r"$b = 2 - \frac{7}{2}$", fontsize=25,
                 fontfamily=su.FONT_BODY_MD, color=su.rgba(su.TEXT_LIGHT, p_s2),
                 ha="center", va="center")

    p_b = su.inout_progress(frame, P2_IN + 104, 29, P2_OUT, P2_OUT_DUR)
    if p_b > 0:
        scale = 0.6 + 0.4 * min(p_b / 0.6, 1.0) if p_b < 1 else 1.0
        su.rounded_card(ax, 0.5, 0.30, 0.46, 0.135,
                         facecolor=su.rgba(su.CARD_BG_ALT, p_b), edgecolor=su.VIOLET,
                         radius=0.022, lw=2.2, scale=scale)
        ax.text(0.5, 0.30, r"$b = -\frac{3}{2} = -1{,}5$", fontsize=26,
                 fontfamily=su.FONT_BODY_SB, color=su.rgba(su.VIOLET, p_b),
                 ha="center", va="center")

    # ---------------- FASE 3: resultado final ----------------
    p3 = su.seg_progress(frame, P3_IN, 40)
    if p3 > 0:
        y_lbl = 0.80 - (1 - p3) * 0.03
        ax.text(0.5, y_lbl, "SOLUCIÓN DEL SISTEMA", fontsize=20,
                 fontfamily=su.FONT_TITLE_SB, color=su.rgba(su.TEXT_LIGHT, p3),
                 ha="center", va="center")

        for cx, color, label, value in [
            (0.335, su.GOLD, "a", r"$\frac{7}{2}$"),
            (0.665, su.VIOLET, "b", r"$-\frac{3}{2}$"),
        ]:
            x_off = (1 - p3) * (0.10 if cx < 0.5 else -0.10)
            scale = 0.8 + 0.2 * p3
            su.rounded_card(ax, cx + x_off, 0.55, 0.34, 0.26,
                             facecolor=su.rgba(su.CARD_BG, p3), edgecolor=color,
                             radius=0.025, lw=2.2, scale=scale)
            ax.text(cx + x_off, 0.635, label, fontsize=20, fontfamily=su.FONT_BODY_SB,
                     color=su.rgba(color, p3), ha="center", va="center")
            ax.text(cx + x_off, 0.50, value, fontsize=34, fontfamily=su.FONT_BODY_SB,
                     color=su.rgba(su.TEXT_LIGHT, p3), ha="center", va="center")

        p_check = su.seg_progress(frame, P3_IN + 45, 28)
        if p_check > 0:
            su.rounded_card(ax, 0.5, 0.185, 0.72, 0.10,
                             facecolor=su.rgba(su.CARD_BG_ALT, p_check), edgecolor=su.GREEN,
                             radius=0.02, lw=1.8)
            ax.text(0.5, 0.185, "a + b = 3,5 − 1,5 = 2 ✓     3a + b = 10,5 − 1,5 = 9 ✓",
                     fontsize=15, fontfamily=su.FONT_BODY_SB,
                     color=su.rgba(su.GREEN, p_check), ha="center", va="center")

    return []


anim = FuncAnimation(fig, draw, frames=N_FRAMES, blit=False)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "renders")
    os.makedirs(out_dir, exist_ok=True)
    su.save_animation(anim, os.path.join(out_dir, "scene6_resolver_sistema.mp4"))
