"""共用繪圖元件：所有作品圖皆為 800x500 的 SVG，只使用 Python 標準函式庫。"""
import math
import random
from html import escape

W, H = 800, 500
FONT = "'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif"
MONO = "'JetBrains Mono',Consolas,'Courier New',monospace"
SHADOW = ('<filter id="sh" x="-10%" y="-10%" width="120%" height="130%">'
          '<feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.28"/></filter>'
          '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
          '<feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


# ---------- 基本圖形 ----------
def svg(body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500" '
            f'font-family="{FONT}"><defs>{SHADOW}{defs}</defs>{body}</svg>\n')


def t(x, y, s, size=12, fill="#111", weight=400, anchor="start", mono=False, extra=""):
    fam = f' font-family="{MONO}"' if mono else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{fam} {extra}>{escape(str(s), quote=False)}</text>')


def r(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def c(cx, cy, rad, fill, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{fill}" {extra}/>'


def ln(x1, y1, x2, y2, stroke, width=1, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def poly(points, fill, extra=""):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" {extra}/>'


def path(d, fill, extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def g(content, extra=""):
    return f'<g {extra}>{content}</g>'


def shadow(content):
    return f'<g filter="url(#sh)">{content}</g>'


def outline_text(x, y, s, size, fill, stroke, sw=4, anchor="middle", weight=900, mono=False):
    return t(x, y, s, size, fill, weight, anchor, mono, f'stroke="{stroke}" stroke-width="{sw}" paint-order="stroke" stroke-linejoin="round"')


def lin_grad(gid, c1, c2, vertical=True, o1=1, o2=1):
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{c1}" stop-opacity="{o1}"/>'
            f'<stop offset="1" stop-color="{c2}" stop-opacity="{o2}"/></linearGradient>')


def diag_grad(gid, c1, c2):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/>'
            f'<stop offset="1" stop-color="{c2}"/></linearGradient>')


def rad_grad(gid, c1, c2, o1=1, o2=0, cx="0.5", cy="0.5", rr="0.5"):
    return (f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{rr}"><stop offset="0" stop-color="{c1}" stop-opacity="{o1}"/>'
            f'<stop offset="1" stop-color="{c2}" stop-opacity="{o2}"/></radialGradient>')


# ---------- 文字與控制項 ----------
def tw(s, size):
    """估算文字寬度（中日韓字元約等於字級，英數約 0.58 倍）。"""
    return sum(size if ord(ch) > 0x2E80 else size * 0.58 for ch in str(s))


def btn(x, y, w, h, label, fill, color="#fff", size=12, rx=None, weight=700, extra=""):
    rx = h / 2 if rx is None else rx
    return r(x, y, w, h, fill, rx, extra) + t(x + w / 2, y + h / 2 + size * 0.36, label, size, color, weight, "middle")


def outline_btn(x, y, w, h, label, color, size=12, rx=None, fill="none"):
    rx = h / 2 if rx is None else rx
    return (r(x, y, w, h, fill, rx, f'stroke="{color}" stroke-width="1.5"')
            + t(x + w / 2, y + h / 2 + size * 0.36, label, size, color, 700, "middle"))


def pill(x, y, label, fill, color, size=10, pad=8):
    w = tw(label, size) + pad * 2
    h = size + 8
    return r(x, y, round(w, 1), h, fill, h / 2) + t(round(x + w / 2, 1), y + h / 2 + size * 0.36, label, size, color, 700, "middle")


def field(x, y, w, label, value="", h=30, dark=False, muted=False, size=12):
    lab_c, box, border, val_c = (("#94a3b8", "#0f172a", "#334155", "#e2e8f0") if dark
                                 else ("#475569", "#fff", "#cbd5e1", "#0f172a"))
    out = t(x, y, label, 11, lab_c, 700) if label else ""
    out += r(x, y + 8, w, h, box, 6, f'stroke="{border}"')
    if value:
        out += t(x + 10, y + 8 + h / 2 + size * 0.36, value, size, "#94a3b8" if muted else val_c)
    return out


def checkbox(x, y, checked, color="#2563eb", size=14):
    if checked:
        return r(x, y, size, size, color, 3) + path(f"M{x+3} {y+size/2} l{size*0.25} {size*0.25} l{size*0.4} -{size*0.45}", "none", 'stroke="#fff" stroke-width="2"')
    return r(x, y, size, size, "#fff", 3, 'stroke="#94a3b8"')


def radio(x, y, checked, color="#2563eb", rad=7):
    out = c(x, y, rad, "#fff", f'stroke="{color if checked else "#94a3b8"}" stroke-width="{2 if checked else 1}"')
    return out + (c(x, y, rad - 3.5, color) if checked else "")


def toggle(x, y, on, color="#22c55e"):
    return r(x, y, 34, 18, color if on else "#cbd5e1", 9) + c(x + (25 if on else 9), y + 9, 7, "#fff")


def avatar(cx, cy, rad, color, letter="", size=None, fg="#fff"):
    out = c(cx, cy, rad, color)
    if letter:
        size = size or rad
        out += t(cx, cy + size * 0.36, letter, size, fg, 900, "middle")
    return out


# ---------- 外框 ----------
def browser_bar(url: str, dark: bool = False) -> str:
    bg, fld, txt = ("#1f2937", "#111827", "#9ca3af") if dark else ("#e5e7eb", "#ffffff", "#6b7280")
    return (r(0, 0, 800, 36, bg) + c(18, 18, 6, "#ff5f57") + c(36, 18, 6, "#febc2e") + c(54, 18, 6, "#28c840")
            + r(90, 8, 520, 20, fld, 10) + t(106, 22, "🔒 " + url, 11, txt))


def phone(x, y, w, h, screen="#fff"):
    return (shadow(r(x, y, w, h, "#111", 30)) + r(x + 9, y + 9, w - 18, h - 18, screen, 22)
            + r(x + w / 2 - 34, y + 15, 68, 7, "#111", 4))


def app_window(x, y, w, h, title, body="#f8fafc", bar="#fff", title_color="#111827"):
    return (shadow(r(x, y, w, h, body, 10)) + r(x, y, w, 32, bar, 10) + r(x, y + 20, w, 12, bar)
            + r(x + 12, y + 9, 14, 14, "#2563eb", 3) + t(x + 34, y + 21, title, 12, title_color, 700)
            + t(x + w - 14, y + 21, "—   ☐   ✕", 12, "#6b7280", 400, "end") + ln(x, y + 32, x + w, y + 32, "#e5e7eb"))


def mac_window(x, y, w, h, title, body="#0d1117", bar="#161b22", title_color="#8b949e"):
    return (shadow(r(x, y, w, h, body, 10)) + r(x, y, w, 30, bar, 10) + r(x, y + 20, w, 10, bar)
            + c(x + 18, y + 15, 5, "#ff5f57") + c(x + 34, y + 15, 5, "#febc2e") + c(x + 50, y + 15, 5, "#28c840")
            + t(x + w / 2, y + 20, title, 11, title_color, 400, "middle", True))


def side_nav(x, y, w, items, active, gap=34, text="#475569", active_text="#1d4ed8", active_bg="#dbeafe", size=12.5, bar=None):
    out = []
    for i, label in enumerate(items):
        yy = y + i * gap
        if i == active:
            out.append(r(x + 8, yy - 18, w - 16, 28, active_bg, 6))
            if bar:
                out.append(r(x + 8, yy - 18, 3, 28, bar))
        out.append(t(x + 24, yy, label, size, active_text if i == active else text, 700 if i == active else 400))
    return "".join(out)


# ---------- 表格與圖表 ----------
def table(x, y, widths, headers, rows, row_h=26, head_h=26, head_fill="#f1f5f9", head_color="#334155",
          text_color="#0f172a", stripe=None, line="#e5e7eb", size=11, aligns=None, cell=None, mono_cols=()):
    """通用表格；cell(ri, ci, value, x, baseline_y, width) 可回傳自訂 SVG（回傳 None 用預設文字）。"""
    total_w = sum(widths)
    aligns = aligns or ["start"] * len(widths)
    out = [r(x, y, total_w, head_h, head_fill, 4)] if head_fill else []
    xs = [x]
    for w in widths:
        xs.append(xs[-1] + w)
    for ci, h in enumerate(headers):
        tx = xs[ci] + 10 if aligns[ci] == "start" else (xs[ci + 1] - 10 if aligns[ci] == "end" else xs[ci] + widths[ci] / 2)
        out.append(t(tx, y + head_h / 2 + 4, h, size, head_color, 700, aligns[ci]))
    for ri, row in enumerate(rows):
        ry = y + head_h + ri * row_h
        if stripe and ri % 2:
            out.append(r(x, ry, total_w, row_h, stripe))
        base = ry + row_h / 2 + size * 0.36
        for ci, val in enumerate(row):
            custom = cell(ri, ci, val, xs[ci], base, widths[ci]) if cell else None
            if custom is not None:
                out.append(custom)
                continue
            tx = xs[ci] + 10 if aligns[ci] == "start" else (xs[ci + 1] - 10 if aligns[ci] == "end" else xs[ci] + widths[ci] / 2)
            out.append(t(round(tx, 1), round(base, 1), val, size, text_color, 400, aligns[ci], ci in mono_cols))
        if line:
            out.append(ln(x, ry + row_h, x + total_w, ry + row_h, line))
    return "".join(out)


def walk(seed, n, start, lo, hi, dmin, dmax):
    rnd = random.Random(seed)
    v, vals = start, []
    for _ in range(n):
        v = max(lo, min(hi, v + rnd.uniform(dmin, dmax)))
        vals.append(v)
    return vals


def line_chart(x, y, w, h, vals, color, width=2.2, area=None, vmin=None, vmax=None, dots=False, dash=None):
    vmin = min(vals) if vmin is None else vmin
    vmax = max(vals) if vmax is None else vmax
    span = (vmax - vmin) or 1
    pts = [(x + i * w / (len(vals) - 1), y + h - (v - vmin) / span * h) for i, v in enumerate(vals)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out = ""
    if area:
        out += f'<polygon points="{x},{y+h} {line} {x+w},{y+h}" fill="url(#{area})"/>'
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    out += f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"{extra}/>'
    if dots:
        out += "".join(c(round(px, 1), round(py, 1), 3, color, 'stroke="#fff" stroke-width="1.5"') for px, py in pts)
    return out


def grid_lines(x, y, w, h, n=4, color="#e5e7eb"):
    return "".join(ln(x, round(y + k * h / n, 1), x + w, round(y + k * h / n, 1), color) for k in range(n + 1))


def bar_chart(x, y, w, h, vals, colors, gap=0.35, vmax=None, rx=2):
    vmax = vmax or max(vals)
    slot = w / len(vals)
    bw = slot * (1 - gap)
    out = []
    for i, v in enumerate(vals):
        bh = v / vmax * h
        col = colors[i % len(colors)] if isinstance(colors, (list, tuple)) else colors
        out.append(r(round(x + i * slot + (slot - bw) / 2, 1), round(y + h - bh, 1), round(bw, 1), round(bh, 1), col, rx))
    return "".join(out)


def donut(cx, cy, rad, segs, width=14):
    circ = 2 * math.pi * rad
    off, out = 0.0, []
    for frac, col in segs:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{col}" stroke-width="{width}" '
                   f'stroke-dasharray="{frac*circ:.1f} {circ:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {cx} {cy})"/>')
        off += frac * circ
    return "".join(out)


def sparkline(x, y, w, h, vals, color):
    return line_chart(x, y, w, h, vals, color, 1.6)


def progress(x, y, w, h, frac, fill, bg="#e5e7eb"):
    return r(x, y, w, h, bg, h / 2) + r(x, y, round(max(w * frac, h), 1), h, fill, h / 2)


def stars(seed, n, x0=0, y0=0, w=800, h=500, color="#fff"):
    rnd = random.Random(seed)
    return "".join(c(rnd.randint(x0, x0 + w), rnd.randint(y0, y0 + h), round(rnd.uniform(0.5, 1.8), 1), color,
                     f'opacity="{rnd.uniform(0.25, 1):.2f}"') for _ in range(n))


def barcode(x, y, w, h, seed=1, color="#111"):
    rnd = random.Random(seed)
    out, cx = [], x
    while cx < x + w - 2:
        bw = rnd.choice((1, 1, 2, 3))
        if rnd.random() > 0.35:
            out.append(r(cx, y, bw, h, color))
        cx += bw + rnd.choice((1, 2))
    return "".join(out)


# ---------- 人物 ----------
def portrait(cx, cy, s, skin="#f6d2b3", hair="#3b2a20", cloth="#2563eb", style=0, accent="#fbbf24"):
    """半身人像，(cx, cy) 為頭部中心，s 為縮放倍率（s=1 約 110px 高）。"""
    hair_paths = {
        0: "M-25 -2 q0 -40 25 -40 q27 0 25 40 q-6 -20 -25 -22 q-17 2 -25 22z",
        1: "M-27 30 v-34 q0 -40 27 -40 q29 0 27 40 v34 h-9 v-40 q-8 -14 -18 -16 q-10 2 -18 16 v40z",
        2: "M-26 -4 l-6 -20 l14 6 l2 -22 l12 14 l6 -18 l8 18 l12 -12 l-2 20 l14 -4 l-10 20 q-6 -18 -25 -20 q-19 2 -25 22z",
        3: "M-25 -2 q-2 -42 25 -42 q27 0 25 42 l-4 -14 q-10 -6 -21 -18 q-6 14 -25 32z",
    }
    body = (path("M-46 70 q4 -38 46 -42 q42 4 46 42z", cloth)
            + path("M-12 28 l12 16 l12 -16", "none", f'stroke="{accent}" stroke-width="3"')
            + r(-8, 14, 16, 16, skin, 4)
            + f'<ellipse cx="0" cy="-4" rx="23" ry="27" fill="{skin}"/>'
            + f'<ellipse cx="-9" cy="-2" rx="3" ry="4" fill="#1f2937"/><ellipse cx="9" cy="-2" rx="3" ry="4" fill="#1f2937"/>'
            + path("M-5 12 q5 4 10 0", "none", 'stroke="#9a3412" stroke-width="2" stroke-linecap="round"')
            + path(hair_paths.get(style, hair_paths[0]), hair))
    return f'<g transform="translate({cx} {cy}) scale({s})">{body}</g>'
