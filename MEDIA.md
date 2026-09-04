# Preparing media for a case study

The fiddliest part of adding a case study. Getting the video values wrong is
what produces the dark corner.

Everything lives in `assets/img/` and `assets/video/`; the content file refers
to bare filenames.

---

## Images

Convert to JPEG at max 2000px wide. Anything larger is wasted — the widest a
figure ever renders is 1120px.

```bash
sips -s format jpeg -s formatOptions 80 -Z 2000 "source.png" --out assets/img/my-image.jpg
```

Keep PNG only where you need transparency. The generator reads each file's real
pixel size and writes `width`/`height` onto the `<img>`, so the browser
reserves space before the image loads — no layout shift, and the scrolly row
heights are right from the first paint. Nothing to do for that; just make sure
the file is in `assets/img/` before you build.

---

## Video

Two steps: transcode, then measure the crop.

### 1 · Transcode

Screen recordings are usually huge. macOS has `avconvert` built in, no install:

```bash
avconvert --source "My Recording.mov" --output assets/video/my-clip.mp4 --preset Preset1280x720
```

That took the Launchpad set from 128 MB to 31 MB. Videos are `preload="none"`
with a poster, so nothing downloads until play — but they *do* autoplay on
scroll, so a full read still pulls them. Keep clips short.

### 2 · Poster frame

```bash
qlmanage -t -s 1600 -o /tmp "My Recording.mov"
sips -s format jpeg -s formatOptions 72 -Z 1500 "/tmp/My Recording.mov.png" \
     --out assets/img/my-clip-poster.jpg
```

### 3 · Measure the crop — this is the important bit

Screen recordings almost always carry a **black letterbox bar** along one edge,
and often a **rounded corner baked into the pixels**. A `border-radius` cannot
remove either: it just rounds the bar, and a baked corner larger than the mask
shows through as a dark arc.

The fix is `ar` (the aspect ratio of the *content*, excluding the bar) plus
`op` (which edge to crop against). Measure them:

```bash
python3 - <<'PY'
from PIL import Image          # pip install pillow in a venv if needed
f = 'assets/img/my-clip-poster.jpg'
im = Image.open(f).convert('RGB'); W, H = im.size; px = im.load()
dark = lambda c: sum(c)/3 < 110
def bar(axis):
    if axis == 'top':
        for y in range(H):
            if not dark(px[W//2, y]): return y
    if axis == 'bottom':
        for y in range(H-1, -1, -1):
            if not dark(px[W//2, y]): return H-1-y
    return 0
t, b = bar('top'), bar('bottom')
print(f'frame {W}x{H}   top bar {t}px   bottom bar {b}px')
print(f'  ar = "{W} / {H - t - b}"')
print(f'  op = "{"bottom" if t > b else "top" if b > t else "center"}"')
PY
```

Then put those in the content file:

```python
("fig", {"video": "my-clip.mp4", "poster": "my-clip-poster.jpg",
         "ar": "1500 / 853", "op": "bottom",
         "caption": "What to watch for."})
```

**Why it works:** the box gets the content's aspect ratio, `object-fit: cover`
scales the frame to fill it, and `object-position` pushes the resulting
overflow off the barred edge — removing exactly the bar. The media then reaches
the box edges, so the 16px radius clips its corners properly.

A separate 2.1% scale-up inside the clip wrapper handles the baked corner.
That is already in the CSS and applies to everything; 7px was the smallest
inset that left zero dark pixels across all five Launchpad videos.

### Measured values, for reference

| Clip | Frame | Top bar | `ar` | `op` |
|---|---|---|---|---|
| `lp-filters` | 1500×936 | 83px | `1500 / 853` | `bottom` |
| `lp-multiselect` | 1500×937 | — | `1500 / 937` | `center` |
| `lp-sidebar` | 1313×1500 | — | `1313 / 1500` | `center` |
| `lp-adaptive-detail` | 1500×935 | 53px | `1500 / 882` | `bottom` |
| `lp-dynamic-viewport` | 1500×936 | 54px | `1500 / 882` | `bottom` |

---

## Checking your work

After building, look at the top-left corner of every video at full size. If you
see a dark arc, `ar` or `op` is wrong — re-measure. Nothing else in the system
produces that artefact.

Source masters (the original `.mov` files) are not committed. Keep them
somewhere safe; the repo only carries the web-ready derivatives.
