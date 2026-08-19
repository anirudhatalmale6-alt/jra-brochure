# JRA Interpretation and Translation Services — Tri-Fold Brochure

Six-panel tri-fold built from the existing JRA flyer. Same navy (`#02275b`),
gold (`#c8a24a`), logo and typography as jrainterpretation.com, so the printed
piece and the website read as one brand.

## Files

| File | Use |
|---|---|
| `JRA-Brochure-PRINT.pdf` | 11 × 8.5 in, no marks. Office printer or copy shop. |
| `JRA-Brochure-PRESS.pdf` | 11.5 × 9 in, 1/8 in bleed, crop marks and fold ticks. Commercial printer. |
| `JRA-Brochure-OUTSIDE.jpg` / `-INSIDE.jpg` | On-screen previews. |
| `build.py` | Rebuilds every file from source. |

## Panels

```
OUTSIDE  [ flap 3.625" ][ back cover 3.6875" ][ front cover 3.6875" ]
INSIDE   [ interpretation 3.6875" ][ translation 3.6875" ][ flap inner 3.625" ]
```

Fold the left third in, then the right third over it. The flap is 1/16 in
narrower on purpose — three equal thirds buckle against the spine.

## The QR code

Static, pointing at `https://www.jrainterpretation.com/` — no QR service to
expire. Verified by decoding it back out of the finished PDF at 150/200/300/600
dpi, and again after blur, a 7° rotation, downscaling and heavy JPEG
recompression.

## Known limitation

The photograph is lifted from the WhatsApp copy of the flyer (400 × 360 px
before upscaling). It is fine for digital and acceptable in print at this size,
but the original full-resolution photo would be better.
