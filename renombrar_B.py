import os
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading

try:
    from PyPDF2 import PdfReader
except ImportError:
    import sys
    sys.exit("ERROR: PyPDF2 no está instalado. Ejecute: pip install PyPDF2")

TIPO_FACTURA = "B"
TITULO_APP = f"Renombrar Facturas Tipo {TIPO_FACTURA}"


def renombrar_pdf(ruta_archivo_pdf, log_func):
    numero_factura_extraido = None

    log_func(f"\n--- Procesando: {os.path.basename(ruta_archivo_pdf)} ---")

    if not os.path.exists(ruta_archivo_pdf):
        log_func(f"  [ERROR] El archivo no existe: {ruta_archivo_pdf}")
        return

    try:
        with open(ruta_archivo_pdf, 'rb') as file:
            reader = PdfReader(file)
            if reader.pages:
                page = reader.pages[0]
                text = page.extract_text()
                if text:
                    match = re.search(r'(\d{4}\s*-\s*\d{8})', text)
                    if match:
                        numero_factura_con_guion = match.group(1)
                        numero_factura_extraido = numero_factura_con_guion.replace(' ', '').replace('-', '')
                        log_func(f"  Número extraído: {numero_factura_extraido}")
                    else:
                        log_func(f"  [ERROR] No se encontró patrón 'XXXX-XXXXXXXX' en el PDF.")
                else:
                    log_func(f"  [ERROR] No se pudo extraer texto de la primera página.")
            else:
                log_func(f"  [ERROR] El PDF no tiene páginas.")
    except Exception as e:
        log_func(f"  [ERROR] Fallo al leer el PDF: {e}")
        return

    if numero_factura_extraido:
        nuevo_nombre = f"F-{TIPO_FACTURA}{numero_factura_extraido}.pdf"
        directorio = os.path.dirname(ruta_archivo_pdf)
        nueva_ruta = os.path.join(directorio, nuevo_nombre)

        if os.path.basename(ruta_archivo_pdf) == nuevo_nombre:
            log_func(f"  [OMITIDO] El archivo ya tiene el nombre correcto.")
            return

        try:
            os.rename(ruta_archivo_pdf, nueva_ruta)
            log_func(f"  [OK] '{os.path.basename(ruta_archivo_pdf)}' → '{nuevo_nombre}'")
        except OSError as e:
            log_func(f"  [ERROR] No se pudo renombrar: {e}")
    else:
        log_func(f"  [ERROR] No se renombró (sin número de factura válido).")


def procesar_carpeta(carpeta, log_func, btn_iniciar, btn_seleccionar):
    btn_iniciar.config(state=tk.DISABLED)
    btn_seleccionar.config(state=tk.DISABLED)

    log_func(f"\n{'='*50}")
    log_func(f"Iniciando procesamiento en: {carpeta}")
    log_func(f"{'='*50}")

    archivos_pdf = [f for f in os.listdir(carpeta) if f.lower().endswith(".pdf")]

    if not archivos_pdf:
        log_func("\n[AVISO] No se encontraron archivos PDF en la carpeta.")
    else:
        log_func(f"\nArchivos PDF encontrados: {len(archivos_pdf)}")
        for filename in archivos_pdf:
            full_path = os.path.join(carpeta, filename)
            renombrar_pdf(full_path, log_func)

    log_func(f"\n{'='*50}")
    log_func("Procesamiento finalizado.")
    log_func(f"{'='*50}\n")

    btn_iniciar.config(state=tk.NORMAL)
    btn_seleccionar.config(state=tk.NORMAL)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(TITULO_APP)
        self.root.geometry("680x500")
        self.root.resizable(True, True)
        self.carpeta_seleccionada = tk.StringVar()

        # Color verde para tipo B
        color_header = "#1e8449"

        # Header
        header = tk.Frame(root, bg=color_header, pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text=TITULO_APP, font=("Segoe UI", 16, "bold"),
                 bg=color_header, fg="white").pack()

        # Frame selección carpeta
        frame_carpeta = tk.Frame(root, padx=15, pady=10)
        frame_carpeta.pack(fill=tk.X)

        tk.Label(frame_carpeta, text="Carpeta de PDFs:", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 4))

        frame_input = tk.Frame(frame_carpeta)
        frame_input.grid(row=1, column=0, sticky="ew")
        frame_carpeta.columnconfigure(0, weight=1)
        frame_input.columnconfigure(0, weight=1)

        self.entry_carpeta = tk.Entry(frame_input, textvariable=self.carpeta_seleccionada,
                                      font=("Segoe UI", 10), width=55)
        self.entry_carpeta.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.btn_seleccionar = tk.Button(frame_input, text="📁 Examinar",
                                          command=self.seleccionar_carpeta,
                                          font=("Segoe UI", 10), bg="#27ae60", fg="white",
                                          relief=tk.FLAT, padx=12, pady=4, cursor="hand2")
        self.btn_seleccionar.grid(row=0, column=1)

        # Botón iniciar
        frame_btn = tk.Frame(root, padx=15, pady=6)
        frame_btn.pack(fill=tk.X)

        self.btn_iniciar = tk.Button(frame_btn, text=f"▶  Renombrar Facturas ({TIPO_FACTURA})",
                                      command=self.iniciar_procesamiento,
                                      font=("Segoe UI", 11, "bold"),
                                      bg=color_header, fg="white",
                                      relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        self.btn_iniciar.pack(side=tk.LEFT)

        self.btn_limpiar = tk.Button(frame_btn, text="🗑 Limpiar log",
                                      command=self.limpiar_log,
                                      font=("Segoe UI", 10), bg="#7f8c8d", fg="white",
                                      relief=tk.FLAT, padx=12, pady=8, cursor="hand2")
        self.btn_limpiar.pack(side=tk.LEFT, padx=8)

        # Log
        frame_log = tk.Frame(root, padx=15, pady=5)
        frame_log.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame_log, text="Registro de operaciones:", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.log_area = scrolledtext.ScrolledText(frame_log, font=("Consolas", 9),
                                                   bg="#1e1e1e", fg="#d4d4d4",
                                                   insertbackground="white",
                                                   relief=tk.FLAT, padx=8, pady=6)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        self.log_area.config(state=tk.DISABLED)

        # Footer
        footer = tk.Frame(root, bg="#ecf0f1", pady=6)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(footer, text=f"Facturas tipo {TIPO_FACTURA}  •  Formato de salida: F-{TIPO_FACTURA}XXXXXXXXXXXX.pdf",
                 font=("Segoe UI", 9), bg="#ecf0f1", fg="#7f8c8d").pack()

    def log(self, mensaje):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, mensaje + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def limpiar_log(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta con PDFs")
        if carpeta:
            self.carpeta_seleccionada.set(carpeta)

    def iniciar_procesamiento(self):
        carpeta = self.carpeta_seleccionada.get().strip()
        if not carpeta:
            messagebox.showwarning("Carpeta requerida", "Por favor seleccione una carpeta antes de continuar.")
            return
        if not os.path.isdir(carpeta):
            messagebox.showerror("Carpeta inválida", f"La ruta indicada no existe o no es una carpeta:\n{carpeta}")
            return

        hilo = threading.Thread(
            target=procesar_carpeta,
            args=(carpeta, self.log, self.btn_iniciar, self.btn_seleccionar),
            daemon=True
        )
        hilo.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
