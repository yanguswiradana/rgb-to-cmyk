# RGB to CMYK Converter

Convert PDF from RGB to CMYK for professional print. GUI + CLI. Windows-only.

## Requirements

- **Python 3.7+**
- **Ghostscript 10.x** — [Download](https://ghostscript.com/releases/gsdnld.html)
- Install to default path (`C:\Program Files\gs`) — auto-detected

## Usage

### GUI (double-click / no arguments)

```bash
python app.py
```

1. Click **Browse...** — select input PDF
2. Output path auto-filled (`filename_cmyk.pdf`)
3. Click **Convert to CMYK**
4. Done!

### CLI (batch / automation)

```bash
# auto output: filename_cmyk.pdf
python app.py input.pdf

# custom output
python app.py input.pdf output.pdf
```

## Output

- Format: **PDF** (CMYK, print-ready)
- Embedded fonts
- Prepress preset
- LZW image compression

## Troubleshooting

**"gswin64c not found"** — script auto-detects in `C:\Program Files\gs\gs*\bin\`. If still failing:

1. Is Ghostscript installed?
2. Installed in default path (`C:\Program Files\gs`)?
3. Using custom path? Edit `_find_gs()` manually.

## License

MIT
