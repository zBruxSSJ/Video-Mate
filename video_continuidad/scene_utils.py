"""
Módulo compartido para las escenas animadas de
"Detectives de la continuidad: develando los secretos de las funciones".
Paleta azul oscuro / celeste / blanco / violeta, 1920x1080, 24 fps.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Ellipse
from matplotlib.animation import FFMpegWriter

# ---------------------------------------------------------------------------
# Resolución / timing
# ---------------------------------------------------------------------------
W_PX, H_PX, DPI = 1920, 1080, 120
FIGSIZE = (W_PX / DPI, H_PX / DPI)
FPS = 24
ASPECT_CORRECTION = W_PX / H_PX

# ---------------------------------------------------------------------------
# Tipografías (Poppins para títulos, Inter para cuerpo y símbolos)
# ---------------------------------------------------------------------------
_POPPINS_DIR = "/usr/share/fonts/truetype/poppins"
for fname in ["Poppins-400.ttf", "Poppins-500.ttf", "Poppins-600.ttf",
              "Poppins-700.ttf", "Poppins-800.ttf"]:
    path = os.path.join(_POPPINS_DIR, fname)
    if os.path.exists(path):
        fm.fontManager.addfont(path)

FONT_TITLE_XB = "Poppins ExtraBold"
FONT_TITLE_B = "Poppins"
FONT_TITLE_SB = "Poppins SemiBold"
FONT_TITLE_MD = "Poppins Medium"
FONT_BODY = "Inter"
FONT_BODY_MD = "Inter Medium"
FONT_BODY_SB = "Inter SemiBold"

plt.rcParams["font.family"] = FONT_BODY
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Inter"
plt.rcParams["mathtext.it"] = "Inter:italic"
plt.rcParams["mathtext.bf"] = "Inter SemiBold"
plt.rcParams["axes.unicode_minus"] = True

# ---------------------------------------------------------------------------
# Paleta: azul oscuro, celeste, blanco, violeta
# ---------------------------------------------------------------------------
BG_TOP = "#060f1f"
BG_BOTTOM = "#0f2341"

CELESTE = "#38bdf8"
CELESTE_SOFT = "#7dd3fc"
VIOLET = "#a78bfa"
VIOLET_SOFT = "#c4b5fd"
WHITE = "#f8fafc"
ROSE = "#fb7185"
GREEN = "#34d399"
AMBER = "#fbbf24"

TEXT_LIGHT = "#f8fafc"
TEXT_DIM = "#94a3b8"
TEXT_FAINT = "#64748b"

CARD_BG = "#132a4a"
CARD_BG_ALT = "#17335a"
CARD_BORDER = "#24496f"

PERSON_COLORS = {
    "P1": CELESTE,
    "P2": VIOLET,
    "P3": AMBER,
    "P4": ROSE,
}

# ---------------------------------------------------------------------------
# Easing
# ---------------------------------------------------------------------------
def ease_out_cubic(t):
    t = np.clip(t, 0.0, 1.0)
    return 1 - (1 - t) ** 3


def ease_in_out_cubic(t):
    t = np.clip(t, 0.0, 1.0)
    return np.where(t < 0.5, 4 * t ** 3, 1 - (-2 * t + 2) ** 3 / 2)


def clamp01(t):
    return max(0.0, min(1.0, t))


def seg_progress(frame, start, dur, ease=ease_out_cubic):
    t = clamp01((frame - start) / max(dur, 1))
    return float(ease(t))


def inout_progress(frame, in_start, in_dur, out_start=None, out_dur=20, ease=ease_out_cubic):
    if frame < in_start:
        return 0.0
    if frame < in_start + in_dur:
        return float(ease((frame - in_start) / max(in_dur, 1)))
    if out_start is None or frame < out_start:
        return 1.0
    if frame < out_start + out_dur:
        return float(1.0 - ease((frame - out_start) / max(out_dur, 1)))
    return 0.0


# ---------------------------------------------------------------------------
# Fondo degradado
# ---------------------------------------------------------------------------
def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def draw_gradient_background(fig, top=BG_TOP, bottom=BG_BOTTOM):
    bg_ax = fig.add_axes([0, 0, 1, 1], zorder=-100)
    bg_ax.set_xticks([])
    bg_ax.set_yticks([])
    for s in bg_ax.spines.values():
        s.set_visible(False)
    top_rgb = np.array(_hex_to_rgb(top))
    bot_rgb = np.array(_hex_to_rgb(bottom))
    n = 256
    grad = np.linspace(0, 1, n)[:, None]
    img = (top_rgb[None, None, :] * (1 - grad[:, :, None]) +
           bot_rgb[None, None, :] * grad[:, :, None])
    bg_ax.imshow(img, extent=[0, 1, 0, 1], aspect="auto", origin="upper",
                 zorder=-100, interpolation="bilinear")
    bg_ax.set_xlim(0, 1)
    bg_ax.set_ylim(0, 1)
    return bg_ax


def make_base_figure():
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    fig.patch.set_facecolor(BG_TOP)
    draw_gradient_background(fig)
    return fig


def setup_full_axes(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return ax


def clear_axes(ax):
    ax.cla()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


# ---------------------------------------------------------------------------
# Glow: varias capas de línea con transparencia decreciente
# ---------------------------------------------------------------------------
def glow_plot(ax, xs, ys, color, lw=3.0, n_layers=4, glow_width_mult=3.2,
              alpha_core=1.0, zorder=5, solid_capstyle="round", linestyle="-"):
    lines = []
    for i in range(n_layers, 0, -1):
        width = lw * (1 + (glow_width_mult - 1) * i / n_layers)
        alpha = alpha_core * 0.10 * (i / n_layers)
        ln, = ax.plot(xs, ys, color=color, linewidth=width, alpha=alpha,
                       solid_capstyle=solid_capstyle, zorder=zorder, linestyle=linestyle)
        lines.append(ln)
    core, = ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha_core,
                     solid_capstyle=solid_capstyle, zorder=zorder + 1, linestyle=linestyle)
    lines.append(core)
    return lines


def glow_point(ax, x, y, color, size=10, n_layers=4, zorder=6):
    arts = []
    for i in range(n_layers, 0, -1):
        s = size * (1 + 2.2 * i / n_layers)
        a = 0.10 * (i / n_layers)
        sc = ax.scatter([x], [y], s=s ** 2, color=color, alpha=a,
                         zorder=zorder, linewidths=0)
        arts.append(sc)
    core = ax.scatter([x], [y], s=size ** 2, color=color, zorder=zorder + 1,
                       edgecolors=TEXT_LIGHT, linewidths=1.4)
    arts.append(core)
    return arts


def open_point(ax, x, y, color, size=11, zorder=7, bg=None):
    """Círculo abierto (hueco): borde de color, relleno del color de fondo."""
    fill = bg if bg is not None else BG_TOP
    halo = ax.scatter([x], [y], s=(size * 1.9) ** 2, color=color, alpha=0.14,
                       zorder=zorder - 1, linewidths=0)
    outer = ax.scatter([x], [y], s=size ** 2, facecolors=fill, edgecolors=color,
                        linewidths=2.4, zorder=zorder)
    return [halo, outer]


def closed_point(ax, x, y, color, size=11, zorder=7):
    """Círculo cerrado (relleno sólido)."""
    halo = ax.scatter([x], [y], s=(size * 1.9) ** 2, color=color, alpha=0.16,
                       zorder=zorder - 1, linewidths=0)
    core = ax.scatter([x], [y], s=size ** 2, color=color, edgecolors=TEXT_LIGHT,
                       linewidths=1.3, zorder=zorder)
    return [halo, core]


# ---------------------------------------------------------------------------
# Tarjetas redondeadas (relleno SÓLIDO)
# ---------------------------------------------------------------------------
def rounded_card(ax, x, y, width, height, facecolor=CARD_BG,
                  edgecolor=CARD_BORDER, radius=0.03, lw=1.5, zorder=3,
                  scale=1.0, alpha=1.0):
    w = width * scale
    h = height * scale
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw,
        zorder=zorder, mutation_aspect=1.0, alpha=alpha,
    )
    ax.add_patch(box)
    return box


def circle_patch(ax, x, y, r, **kwargs):
    e = Ellipse((x, y), width=2 * r, height=2 * r * ASPECT_CORRECTION, **kwargs)
    ax.add_patch(e)
    return e


def step_card(ax, cx, cy, width, height, badge, color, title, formula, note,
              progress, slide=0.10, badge_r=0.045, title_size=18, formula_size=21,
              note_size=13.5):
    p = progress
    if p <= 0:
        return
    x_off = (1 - p) * slide
    cxp = cx - x_off
    scale = 0.85 + 0.15 * p
    rounded_card(ax, cxp, cy, width, height, facecolor=rgba(CARD_BG, p),
                 edgecolor=color, radius=0.02, lw=1.8, scale=scale)
    text_alpha = fade_alpha(p, 0.35, 1.0)
    badge_x = cxp - width / 2 + 0.065
    circle_patch(ax, badge_x, cy, badge_r, facecolor=rgba(color, text_alpha * 0.18),
                 edgecolor=color, linewidth=2, zorder=4)
    ax.text(badge_x, cy, badge, fontsize=20, fontfamily=FONT_BODY_SB,
             color=rgba(color, text_alpha), ha="center", va="center", zorder=5)
    text_x = cxp - width / 2 + 0.14
    if title:
        ax.text(text_x, cy + height * 0.27, title, fontsize=title_size,
                 fontfamily=FONT_BODY_SB, color=rgba(color, text_alpha),
                 ha="left", va="center")
    ax.text(text_x, cy, formula, fontsize=formula_size, fontfamily=FONT_BODY_MD,
             color=rgba(TEXT_LIGHT, text_alpha), ha="left", va="center")
    if note:
        ax.text(text_x, cy - height * 0.30, note, fontsize=note_size,
                 fontfamily=FONT_BODY, color=rgba(TEXT_DIM, text_alpha),
                 ha="left", va="center")


# ---------------------------------------------------------------------------
# Helpers de color / alpha
# ---------------------------------------------------------------------------
def rgba(hex_color, alpha):
    r, g, b = _hex_to_rgb(hex_color)
    return (r, g, b, float(np.clip(alpha, 0, 1)))


def fade_alpha(progress, start=0.0, end=1.0):
    return float(np.clip((progress - start) / max(end - start, 1e-6), 0, 1))


# ---------------------------------------------------------------------------
# Guardado
# ---------------------------------------------------------------------------
def save_animation(anim, filepath, fps=FPS, bitrate=9000, dpi=DPI):
    writer = FFMpegWriter(
        fps=fps, bitrate=bitrate, codec="libx264",
        extra_args=["-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart"],
    )
    anim.save(filepath, writer=writer, dpi=dpi)
    print(f"[OK] Guardado: {filepath}")
