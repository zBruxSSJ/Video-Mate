"""
Módulo compartido para las escenas animadas del video "Desafío de Parámetros".
Provee paleta de colores, tipografías, efectos de glow, tarjetas redondeadas,
funciones de easing y el helper de guardado con FFMpegWriter.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.animation import FFMpegWriter

# ---------------------------------------------------------------------------
# Resolución / timing
# ---------------------------------------------------------------------------
W_PX, H_PX, DPI = 1280, 720, 100
FIGSIZE = (W_PX / DPI, H_PX / DPI)
FPS = 24

# ---------------------------------------------------------------------------
# Tipografías (Poppins para títulos, Inter para cuerpo y símbolos)
# ---------------------------------------------------------------------------
_POPPINS_DIR = "/usr/share/fonts/truetype/poppins"
_FONT_TITLE_BOLD = None
_FONT_TITLE_SEMI = None
_FONT_BODY = "Inter"
_FONT_BODY_MEDIUM = "Inter Medium"
_FONT_BODY_SEMIBOLD = "Inter SemiBold"

for fname, weight in [
    ("Poppins-400.ttf", "regular"),
    ("Poppins-500.ttf", "medium"),
    ("Poppins-600.ttf", "semibold"),
    ("Poppins-700.ttf", "bold"),
    ("Poppins-800.ttf", "extrabold"),
]:
    path = os.path.join(_POPPINS_DIR, fname)
    if os.path.exists(path):
        fm.fontManager.addfont(path)

FONT_TITLE_XB = "Poppins ExtraBold"
FONT_TITLE_B = "Poppins"          # Poppins-700 registers family "Poppins" style Bold
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
# Paleta de colores
# ---------------------------------------------------------------------------
BG_TOP = "#0b1522"
BG_BOTTOM = "#172a42"

TURQUOISE = "#2dd4bf"
ORANGE = "#f59e0b"
RED = "#ef4444"
GREEN = "#34d399"
VIOLET = "#a78bfa"
GOLD = "#fbbf24"
BLUE = "#60a5fa"

TEXT_LIGHT = "#f1f5f9"
TEXT_DIM = "#94a3b8"
TEXT_FAINT = "#64748b"

CARD_BG = "#1b2e47"
CARD_BG_ALT = "#1f3752"
CARD_BORDER = "#2e4a6b"

PERSON_COLORS = {
    "Bruno": GOLD,
    "Fabrizio": TURQUOISE,
    "Sebastian": ORANGE,
    "Eugenia": VIOLET,
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


def inout_progress(frame, in_start, in_dur, out_start=None, out_dur=20, ease=ease_out_cubic):
    """Progreso 0..1 que entra con fade-in y, opcionalmente, sale con fade-out."""
    if frame < in_start:
        return 0.0
    if frame < in_start + in_dur:
        return float(ease((frame - in_start) / max(in_dur, 1)))
    if out_start is None or frame < out_start:
        return 1.0
    if frame < out_start + out_dur:
        return float(1.0 - ease((frame - out_start) / max(out_dur, 1)))
    return 0.0


def seg_progress(frame, start, dur, total_frames=None, ease=ease_out_cubic):
    """Progreso 0..1 de un segmento animado que empieza en el frame `start`
    y dura `dur` frames, aplicando un easing ease-out cubic."""
    t = clamp01((frame - start) / max(dur, 1))
    return float(ease(t))


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


# ---------------------------------------------------------------------------
# Glow: varias capas de línea con transparencia decreciente
# ---------------------------------------------------------------------------
def glow_plot(ax, xs, ys, color, lw=3.0, n_layers=4, glow_width_mult=3.2,
              alpha_core=1.0, zorder=5, solid_capstyle="round"):
    lines = []
    for i in range(n_layers, 0, -1):
        width = lw * (1 + (glow_width_mult - 1) * i / n_layers)
        alpha = alpha_core * 0.10 * (i / n_layers)
        ln, = ax.plot(xs, ys, color=color, linewidth=width, alpha=alpha,
                       solid_capstyle=solid_capstyle, zorder=zorder, zdir=None) \
            if False else ax.plot(xs, ys, color=color, linewidth=width,
                                   alpha=alpha, solid_capstyle=solid_capstyle,
                                   zorder=zorder)
        lines.append(ln)
    core, = ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha_core,
                     solid_capstyle=solid_capstyle, zorder=zorder + 1)
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


# ---------------------------------------------------------------------------
# Tarjetas redondeadas (relleno SÓLIDO)
# ---------------------------------------------------------------------------
def rounded_card(ax, x, y, width, height, facecolor=CARD_BG,
                  edgecolor=CARD_BORDER, radius=0.03, lw=1.5, zorder=3,
                  scale=1.0, alpha=1.0):
    """Dibuja una tarjeta redondeada centrada en (x, y) con tamaño width x height
    (en coordenadas de ejes 0..1), escalable para animaciones de entrada.
    El facecolor es siempre sólido (sin alpha) salvo que se pida explícitamente."""
    w = width * scale
    h = height * scale
    pad = radius
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={pad}",
        facecolor=facecolor, edgecolor=edgecolor, linewidth=lw,
        zorder=zorder, mutation_aspect=1.0, alpha=alpha,
    )
    ax.add_patch(box)
    return box


# ---------------------------------------------------------------------------
# Helper de guardado
# ---------------------------------------------------------------------------
def save_animation(anim, filepath, fps=FPS, bitrate=6000, dpi=DPI):
    writer = FFMpegWriter(
        fps=fps, bitrate=bitrate, codec="libx264",
        extra_args=["-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart"],
    )
    anim.save(filepath, writer=writer, dpi=dpi)
    print(f"[OK] Guardado: {filepath}")


def setup_full_axes(fig):
    """Eje que cubre toda la figura en coordenadas 0..1, sin ejes visibles."""
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return ax


def fade_alpha(progress, start=0.0, end=1.0):
    return float(np.clip((progress - start) / max(end - start, 1e-6), 0, 1))


def rgba(hex_color, alpha):
    r, g, b = _hex_to_rgb(hex_color)
    return (r, g, b, float(np.clip(alpha, 0, 1)))


def clear_axes(ax):
    ax.cla()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def frac_mathtext(num, den, negative=False):
    sign = "-" if negative else ""
    return r"$%s\frac{%s}{%s}$" % (sign, num, den)


# Corrección de aspecto: en un eje 0..1 x 0..1 mapeado a 1280x720 px,
# una "circunferencia" perfecta necesita height = width * (W_PX/H_PX).
ASPECT_CORRECTION = W_PX / H_PX


def circle_patch(ax, x, y, r, **kwargs):
    from matplotlib.patches import Ellipse
    e = Ellipse((x, y), width=2 * r, height=2 * r * ASPECT_CORRECTION, **kwargs)
    ax.add_patch(e)
    return e


def step_card(ax, cx, cy, width, height, badge, color, title, formula, note,
              progress, slide=0.10, badge_r=0.052, title_size=17, formula_size=20,
              note_size=12.5):
    """Tarjeta de 'paso' reutilizable: círculo numerado + título + fórmula + nota.
    `progress` es 0..1 (ya con easing aplicado)."""
    p = progress
    if p <= 0:
        return
    x_off = (1 - p) * slide
    cxp = cx - x_off
    scale = 0.85 + 0.15 * p
    rounded_card(ax, cxp, cy, width, height, facecolor=rgba(CARD_BG, p),
                 edgecolor=color, radius=0.022, lw=1.8, scale=scale)
    text_alpha = fade_alpha(p, 0.35, 1.0)
    badge_x = cxp - width / 2 + 0.075
    circle_patch(ax, badge_x, cy, badge_r, facecolor=rgba(color, text_alpha * 0.18),
                 edgecolor=color, linewidth=2, zorder=4)
    ax.text(badge_x, cy, badge, fontsize=22, fontfamily=FONT_BODY_SB,
             color=rgba(color, text_alpha), ha="center", va="center", zorder=5)
    text_x = cxp - width / 2 + 0.165
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

