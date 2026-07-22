import subprocess
import os
import sys
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def _find_gs():
    """Auto-detect Ghostscript executable."""
    # 1. Try PATH first
    import shutil
    gs = shutil.which("gswin64c") or shutil.which("gswin32c")
    if gs:
        return gs
    # 2. Search common install dirs
    for root in ["C:\\Program Files\\gs", "C:\\Program Files (x86)\\gs"]:
        pattern = os.path.join(root, "gs*", "bin", "gswin64c.exe")
        matches = glob.glob(pattern)
        if matches:
            return matches[-1]  # latest version
    return "gswin64c"

def convert_rgb_to_cmyk_windows(input_file, output_file, log_func=print):
    if not os.path.exists(input_file):
        log_func(f"Error: File '{input_file}' tidak ditemukan!")
        return False

    gs_cmd = _find_gs()

    gs_command = [
        gs_cmd,
        '-dSAFER',
        '-dBATCH',
        '-dNOPAUSE',
        '-sDEVICE=pdfwrite',
        '-sColorConversionStrategy=CMYK',
        '-dProcessColorModel=/DeviceCMYK',
        '-dEmbedAllFonts=true',
        '-dPDFSETTINGS=/prepress',
        f'-sOutputFile={output_file}',
        input_file
    ]

    log_func(f"Memproses '{os.path.basename(input_file)}' menjadi CMYK...")
    
    try:
        subprocess.run(gs_command, check=True)
        log_func(f"Sukses! -> '{os.path.basename(output_file)}'")
        return True
        
    except FileNotFoundError:
        log_func(f"\n[ERROR] '{gs_cmd}' tidak ditemukan.")
        log_func("Pastikan Ghostscript sudah terinstal.")
        log_func("Atau edit variabel 'gs_cmd' dengan path lengkap instalasi Ghostscript.")
    except subprocess.CalledProcessError as e:
        log_func("\n[ERROR] Gagal melakukan konversi.")
        err = e.stderr.decode(errors='replace') if e.stderr else "(no output)"
        log_func(f"Detail: {err}")
    
    return False


def cli_main():
    if len(sys.argv) < 2:
        return False
    
    args = sys.argv[1:]
    
    if len(args) == 1:
        input_file = args[0]
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_cmyk{ext}"
    elif len(args) >= 2:
        input_file = args[0]
        output_file = args[1]
    
    convert_rgb_to_cmyk_windows(input_file, output_file)
    return True


class CmykConverterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Convert RGB to CMYK")
        self.root.geometry("640x480")
        self.root.resizable(True, True)
        
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        self._build_ui()
        
    def _build_ui(self):
        # Input file
        frame_in = ttk.LabelFrame(self.root, text="File Input", padding=10)
        frame_in.pack(fill="x", padx=10, pady=(10, 5))
        
        ttk.Entry(frame_in, textvariable=self.input_file).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(frame_in, text="Browse...", command=self._browse_input).pack(side="right")
        
        # Output file
        frame_out = ttk.LabelFrame(self.root, text="Output File", padding=10)
        frame_out.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(frame_out, textvariable=self.output_file).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(frame_out, text="Browse...", command=self._browse_output).pack(side="right")
        
        # Convert button
        ttk.Button(self.root, text="Convert to CMYK", command=self._convert).pack(pady=10)
        
        # Log
        frame_log = ttk.LabelFrame(self.root, text="Log", padding=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(frame_log, height=10, state="disabled", wrap="word")
        scrollbar = ttk.Scrollbar(frame_log, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _browse_input(self):
        path = filedialog.askopenfilename(title="Pilih file PDF", filetypes=[("PDF files", "*.pdf")])
        if path:
            self.input_file.set(path)
            base, ext = os.path.splitext(path)
            self.output_file.set(f"{base}_cmyk{ext}")
    
    def _browse_output(self):
        path = filedialog.asksaveasfilename(title="Simpan sebagai", defaultextension=".pdf",
                                            filetypes=[("PDF files", "*.pdf")])
        if path:
            self.output_file.set(path)
    
    def _log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.root.update()
    
    def _convert(self):
        inp = self.input_file.get()
        out = self.output_file.get()
        
        if not inp:
            messagebox.showerror("Error", "Pilih file input dulu!")
            return
        if not out:
            messagebox.showerror("Error", "Tentukan file output!")
            return
        
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        
        ok = convert_rgb_to_cmyk_windows(inp, out, log_func=self._log)
        
        if ok:
            messagebox.showinfo("Selesai", f"Konversi berhasil!\n{out}")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if not cli_main():
        app = CmykConverterGUI()
        app.run()
