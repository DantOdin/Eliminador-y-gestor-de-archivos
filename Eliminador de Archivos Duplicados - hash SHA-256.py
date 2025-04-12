import os
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import platform
import subprocess
import humanize
from collections import defaultdict
from queue import Queue

class DuplicateByHashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicados por Hash SHA-256")

        # Ayuda e instrucciones
        ttk.Label(root, text="Usa Ctrl + clic o Shift para seleccionar múltiples archivos.").pack(pady=(10, 0))

        # Selector de carpeta
        self.path_frame = ttk.Frame(root)
        self.path_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(self.path_frame, text="Ruta:").pack(side="left")
        self.path_entry = ttk.Entry(self.path_frame, width=60)
        self.path_entry.pack(side="left", padx=5)
        self.browse_btn = ttk.Button(self.path_frame, text="Seleccionar Carpeta", command=self.select_folder)
        self.browse_btn.pack(side="left")

        # Barra de progreso
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=(5, 0))
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=(0, 5))

        # Tabla
        self.tree = ttk.Treeview(root, columns=("grupo", "nombre", "ruta", "peso"), show="headings", selectmode="extended")
        for col in ("grupo", "nombre", "ruta", "peso"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="w", width=80 if col == "grupo" else (150 if col == "nombre" else 300))
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Botones
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(pady=10)
        self.delete_btn = ttk.Button(self.btn_frame, text="Eliminar Seleccionados", command=self.confirm_delete)
        self.delete_btn.pack(side="left", padx=10)
        self.open_btn = ttk.Button(self.btn_frame, text="Abrir Carpeta", command=self.open_selected_folder)
        self.open_btn.pack(side="left", padx=10)
        self.cancel_btn = ttk.Button(self.btn_frame, text="Cancelar", command=self.root.quit)
        self.cancel_btn.pack(side="left", padx=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.start_threaded_hash_scan(folder)

    def start_threaded_hash_scan(self, folder):
        self.disable_ui()
        self.tree.delete(*self.tree.get_children())
        self.progress["value"] = 0
        self.status_label["text"] = "Escaneando archivos..."

        thread = threading.Thread(target=self.find_hash_duplicates, args=(folder,))
        thread.start()

    def get_file_hash(self, path, chunk_size=65536):
        hasher = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None

    def find_hash_duplicates(self, folder):
        hash_map = defaultdict(list)
        all_files = []

        for root_dir, _, files in os.walk(folder):
            for f in files:
                all_files.append(os.path.join(root_dir, f))

        total_files = len(all_files)
        self.root.after(0, self.progress.config, {"maximum": total_files})

        for i, full_path in enumerate(all_files):
            file_hash = self.get_file_hash(full_path)
            if file_hash:
                hash_map[file_hash].append(full_path)

            # Actualizar barra de progreso desde el hilo principal
            self.root.after(0, self.progress.step, 1)
            self.root.after(0, self.status_label.config, {"text": f"Analizando {i+1} / {total_files}"})

        # Mostrar duplicados
        self.root.after(0, lambda: self.display_duplicates(hash_map))

    def display_duplicates(self, hash_map):
        group_id = 1
        for file_list in hash_map.values():
            if len(file_list) > 1:
                for path in file_list:
                    try:
                        size = os.path.getsize(path)
                        self.tree.insert("", "end", values=(
                            f"G{group_id}",
                            os.path.basename(path),
                            path,
                            humanize.naturalsize(size)
                        ))
                    except:
                        pass
                group_id += 1

        self.status_label["text"] = "Análisis completo."
        self.enable_ui()

    def confirm_delete(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Sin selección", "No has seleccionado ningún archivo para eliminar.")
            return

        selected_paths = [self.tree.item(item)["values"][2] for item in selected_items]
        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar {len(selected_paths)} archivo(s)?")
        if confirm:
            self.delete_files(selected_paths)

    def delete_files(self, files):
        errores = []
        for path in files:
            try:
                os.remove(path)
            except Exception as e:
                errores.append((path, str(e)))

        if errores:
            msg = "\n".join(f"{p}: {e}" for p, e in errores)
            messagebox.showerror("Errores al eliminar", msg)
        else:
            messagebox.showinfo("Completado", "Archivos eliminados con éxito.")
        self.start_threaded_hash_scan(self.path_entry.get())

    def open_selected_folder(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Sin selección", "Selecciona al menos un archivo.")
            return

        opened = set()
        for item in selected_items:
            file_path = self.tree.item(item)["values"][2]
            folder = os.path.dirname(file_path)
            if folder not in opened:
                self.open_folder(folder)
                opened.add(folder)

    def open_folder(self, path):
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{e}")

    def disable_ui(self):
        self.browse_btn["state"] = "disabled"
        self.delete_btn["state"] = "disabled"
        self.open_btn["state"] = "disabled"
        self.cancel_btn["state"] = "disabled"

    def enable_ui(self):
        self.browse_btn["state"] = "normal"
        self.delete_btn["state"] = "normal"
        self.open_btn["state"] = "normal"
        self.cancel_btn["state"] = "normal"

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateByHashApp(root)
    root.mainloop()
