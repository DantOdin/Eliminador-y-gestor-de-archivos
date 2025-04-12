import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import defaultdict
import humanize

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Archivos Duplicados")

        # Sección de selección de carpeta
        self.path_frame = ttk.Frame(root)
        self.path_frame.pack(fill="x", pady=10, padx=10)
        self.path_label = ttk.Label(self.path_frame, text="Ruta:")
        self.path_label.pack(side="left")
        self.path_entry = ttk.Entry(self.path_frame, width=60)
        self.path_entry.pack(side="left", padx=5)
        self.browse_btn = ttk.Button(self.path_frame, text="Seleccionar Carpeta", command=self.select_folder)
        self.browse_btn.pack(side="left")

        # Tabla con duplicados (selección múltiple)
        self.tree = ttk.Treeview(root, columns=("nombre", "ruta", "peso"), show="headings", selectmode="extended")
        for col in ("nombre", "ruta", "peso"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="w", width=150 if col == "nombre" else 300)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones de acción
        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.delete_btn = ttk.Button(self.btn_frame, text="Eliminar Seleccionados", command=self.confirm_delete)
        self.delete_btn.pack(side="left", padx=10)
        self.cancel_btn = ttk.Button(self.btn_frame, text="Cancelar", command=self.root.quit)
        self.cancel_btn.pack(side="left", padx=10)

        self.path_entry.focus()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.find_duplicates(folder)

    def find_duplicates(self, folder):
        self.tree.delete(*self.tree.get_children())

        name_map = defaultdict(list)  # nombre -> [(ruta, peso)]

        for root_dir, _, files in os.walk(folder):
            for f in files:
                full_path = os.path.join(root_dir, f)
                try:
                    size = os.path.getsize(full_path)
                    name_map[f].append((full_path, size))
                except Exception as e:
                    print(f"Error leyendo {full_path}: {e}")

        for name, entries in name_map.items():
            if len(entries) > 1:
                for path, size in entries:
                    self.tree.insert("", "end", values=(name, path, humanize.naturalsize(size)))

    def confirm_delete(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Sin selección", "No has seleccionado ningún archivo para eliminar.")
            return

        selected_paths = [self.tree.item(item)["values"][1] for item in selected_items]

        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro que quieres eliminar {len(selected_paths)} archivo(s)?")
        if confirm:
            self.delete_files(selected_paths)

    def delete_files(self, files):
        errors = []
        for path in files:
            try:
                os.remove(path)
            except Exception as e:
                errors.append((path, str(e)))

        if errors:
            msg = "\n".join(f"{p}: {e}" for p, e in errors)
            messagebox.showerror("Errores al eliminar", msg)
        else:
            messagebox.showinfo("Completado", "Archivos eliminados con éxito.")

        self.find_duplicates(self.path_entry.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()
