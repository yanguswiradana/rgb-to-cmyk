# RGB to CMYK Converter

Konverter PDF RGB ke CMYK untuk cetak profesional. GUI + CLI. Windows-only.

## Requirements

- **Python 3.7+**
- **Ghostscript 10.x** — [Download](https://ghostscript.com/releases/gsdnld.html)

Install dependency:

```bash
pip install pillow
```

*Note: `pillow` hanya untuk keperluan preview/fallback. Konversi utama tetap pakai Ghostscript.*

## Cara Pakai

### GUI (double-click / tanpa argumen)

```bash
python app.py
```

1. Klik **Browse...** — pilih file PDF
2. Output path otomatis terisi (`namafile_cmyk.pdf`)
3. Klik **Convert to CMYK**
4. Selesai!

### CLI (batch / automation)

```bash
# output otomatis: namafile_cmyk.pdf
python app.py input.pdf

# custom output
python app.py input.pdf output.pdf
```

## Output

- Format: **PDF** (CMYK, print-ready)
- Embed all fonts
- Prepress preset
- LZW compression on images

## Troubleshooting

**"gswin64c tidak ditemukan"** → script auto-detect di `C:\Program Files\gs\gs*\bin\`. Kalau tetap error, cek:

1. Ghostscript sudah terinstal?
2. Install di folder default (`C:\Program Files\gs`)?
3. Kalau pakai path kustom, edit manual di `_find_gs()`.

## License

MIT
