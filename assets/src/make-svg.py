# Builds assets/banner.svg: the banner with a receipt that prints line by line, once.
# Render the two layers first (Chrome headless, 1280x520 at 2x):
#   base.png  = banner.html with `.receipt{visibility:hidden}`
#   full.png  = banner.html as is
# then run: python3 make-svg.py
import base64, pathlib
here = pathlib.Path(__file__).parent
b64 = lambda p: base64.b64encode((here / p).read_bytes()).decode()
W, H = 1280, 520
L, T, R = 794, 84, 1224           # receipt box (from banner.html)
stops = [84, 168, 183, 224, 252, 280, 296, 334, 360, 376, 424, 462]   # bottom edge of each printed line
start, step = 0.7, 0.16
dur = start + step * (len(stops) - 1) + 0.4
def pct(t): return f"{100 * t / dur:.2f}%"
clip, head = [], []
for i, y in enumerate(stops):
    t = start + step * i
    clip.append(f"{pct(t)}{{clip-path:inset({T}px {W-R}px {H-y}px {L}px)}}")
    head.append(f"{pct(t)}{{transform:translateY({y}px);opacity:1}}")
clip.insert(0, f"0%{{clip-path:inset({T}px {W-R}px {H-T}px {L}px)}}")
clip.append(f"100%{{clip-path:inset({T}px {W-R}px {H-stops[-1]}px {L}px)}}")
head.insert(0, f"0%{{transform:translateY({T}px);opacity:1}}")
head.append(f"{pct(start + step*(len(stops)-1) + 0.25)}{{transform:translateY({stops[-1]}px);opacity:0}}")
head.append(f"100%{{transform:translateY({stops[-1]}px);opacity:0}}")
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Juan David Colorado, product design lead for AI and enterprise software, with a design receipt">
<style>
.p{{animation:print {dur:.2f}s both;animation-timing-function:step-end}}
.h{{animation:head {dur:.2f}s both;animation-timing-function:step-end}}
@keyframes print{{{"".join(clip)}}}
@keyframes head{{{"".join(head)}}}
@media (prefers-reduced-motion:reduce){{.p{{animation:none;clip-path:none}}.h{{display:none}}}}
</style>
<image width="{W}" height="{H}" href="data:image/png;base64,{b64('base.png')}"/>
<image class="p" width="{W}" height="{H}" href="data:image/png;base64,{b64('full.png')}"/>
<rect class="h" x="{L}" y="0" width="{R-L}" height="3" fill="#FF5A26"/>
</svg>
'''
(here.parent / "banner.svg").write_text(svg)
print("banner.svg", len(svg) // 1024, "KB", f"{dur:.2f}s")
