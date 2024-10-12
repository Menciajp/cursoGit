import tkinter as tk
from tkinter import ttk, font, messagebox
from Clases.pagina import Pagina
from scrapper import Scrapper

class EditPageForm:
    def __init__(self, root, nombre_pagina, selector):
        # Crear una nueva ventana Toplevel
        self.window = tk.Toplevel(root)
        self.window.title("Editar Página")
        self.window.geometry("300x400")

        # Definir fuentes
        self.titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)

        # Título
        self.titulo_label = tk.Label(self.window, text="Editar Página", font=self.titulo_font)
        self.titulo_label.pack(pady=20)

        # Nombre de la página
        self.nombre_label = tk.Label(self.window, text="Nombre de la Página:", font=self.label_font)
        self.nombre_label.pack(pady=10)
        
        self.nombre_entry = tk.Entry(self.window, width=35, font=self.label_font, state="normal")
        self.nombre_entry.pack(pady=5)
        self.nombre_entry.insert(0, nombre_pagina)
        
        # Selector
        self.selector_label = tk.Label(self.window, text="Selector:", font=self.label_font)
        self.selector_label.pack(pady=10)

        self.selector_entry = tk.Entry(self.window, width=35, font=self.label_font, state="normal")
        self.selector_entry.pack(pady=5)
        self.selector_entry.insert(0, selector)

        # Botón para guardar
        self.save_button = tk.Button(self.window, text="Guardar Cambios", width=20, height=2, command=self.guardar_cambios, bg="#4CAF50", fg="white", font=self.label_font)
        self.save_button.pack(pady=10)

        # Botón para eliminar
        self.delete_button = tk.Button(self.window, text="Eliminar Página", width=20, height=2, command=self.eliminar_pagina, bg="#F44336", fg="white", font=self.label_font)
        self.delete_button.pack(pady=10)

    def guardar_cambios(self):
        nombre = self.nombre_entry.get()
        selector = self.selector_entry.get()
        
        if not nombre or not selector:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Aquí llamas al método para actualizar la página en la base de datos
        if Pagina.editar_pagina(nombre, selector):
            messagebox.showinfo("Éxito", "Página actualizada correctamente.")
            self.window.destroy()  # Cerrar la ventana
        else:
            messagebox.showerror("Error", "No se pudo actualizar la página.")

    def eliminar_pagina(self):
        nombre = self.nombre_entry.get()
        respuesta = messagebox.askyesno("Eliminar página", f"¿Está seguro de que desea eliminar la página '{nombre}'?")
        if respuesta:
            if Pagina.eliminar_pagina(nombre):
                messagebox.showinfo("Éxito", "Página eliminada correctamente.")
                self.window.destroy()  # Cerrar la ventana
            else:
                messagebox.showerror("Error", "No se pudo eliminar la página.")
