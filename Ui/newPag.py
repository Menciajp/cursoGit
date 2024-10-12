from scrapper import Scrapper
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from Clases.pagina import Pagina  # Asegúrate de que esta clase esté definida
from Ui.editPag import EditPageForm

class NewPag:
    def __init__(self, frame):
        self.frame = frame

        # Definir fuentes
        self.titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        
        # Título
        self.titulo_label = tk.Label(frame, text="Agregar Página", font=self.titulo_font)
        self.titulo_label.pack(pady=20)

        # Etiqueta para el nombre de la página
        self.label_nombre = tk.Label(frame, text="Nombre de la Página:", font=self.label_font)
        self.label_nombre.pack(pady=5)

        # Campo de entrada para el nombre de la página
        self.nombre_entry = tk.Entry(frame, width=35, font=self.label_font)
        self.nombre_entry.pack(pady=5)

        # Etiqueta para el enlace
        self.label_link = tk.Label(frame, text="Link de la Página:", font=self.label_font)
        self.label_link.pack(pady=5)

        # Campo de entrada para el enlace
        self.link_entry = tk.Entry(frame, width=35, font=self.label_font)
        self.link_entry.pack(pady=5)
        
        # Etiqueta para el selector
        self.label_selector = tk.Label(frame, text="Selector de la Página:", font=self.label_font)
        self.label_selector.pack(pady=5)

        # Campo de entrada para el selector
        self.selector_entry = tk.Entry(frame, width=35, font=self.label_font)
        self.selector_entry.pack(pady=5)

        # Botón para guardar
        self.save_button = tk.Button(frame, text="Guardar Página", width=20, height=2, command=self.guardar_pagina, bg="#4CAF50", fg="white", font=self.label_font)
        self.save_button.pack(pady=20)

        # Crear la tabla
        self.crear_tabla()
        self.actualizar_tabla()

    def crear_tabla(self):
        """Crear la tabla para mostrar las páginas"""
        frame_tabla = tk.Frame(self.frame)
        frame_tabla.pack(pady=20, fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Definir columnas
        columnas = ('#1', '#2')

        # Crear el Treeview
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scrollbar.set, height=5)
        self.tabla.bind("<Double-1>", self.on_doble_click)
        
        # Configurar el scrollbar
        scrollbar.config(command=self.tabla.yview)

        # Definir encabezados
        self.tabla.heading('#1', text='Nombre de la Página')
        self.tabla.heading('#2', text='Selector')

        # Empaquetar la tabla
        self.tabla.pack(fill="both", expand=True)

    def on_doble_click(self, event):
        selected_item = self.tabla.selection()
        if selected_item:
            nombre = self.tabla.item(selected_item, 'values')[0]
            selector = self.tabla.item(selected_item, 'values')[1]
            root = tk.Tk()
            root.withdraw()
            edit_page_form = EditPageForm(root, nombre_pagina=nombre, selector=selector)
            root.mainloop()


    def actualizar_tabla(self):
        """Actualizar la tabla con las páginas almacenadas"""
        # Limpiar la tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Obtener páginas y insertar en la tabla
        paginas = Pagina.traer_paginas()  # Asegúrate de que esta función esté definida
        for pagina in paginas:
            self.tabla.insert("", tk.END, values=(pagina[0], pagina[1]))  # Ajusta según la estructura de tus datos

    def guardar_pagina(self):
        nombre = self.nombre_entry.get()
        link = self.link_entry.get()
        selector = self.selector_entry.get()
        if nombre.strip() == "" or link.strip() == "" or selector.strip() == "":
            messagebox.showwarning("Entrada Inválida", "El nombre, el link y el selector de la página no pueden estar vacíos.")
        else:
            pruebaScrap = Scrapper.verificarSelector(link,selector)
            if(pruebaScrap != False):
                respuesta = messagebox.askyesno("Confirmar dato", f"¿El precio en el link es: '{pruebaScrap}'?")
                if (respuesta):
                    if(Pagina.agregar_pagina(nombre,selector)):
                        messagebox.showinfo("Éxito", f"Página '{nombre}' guardada exitosamente.")
                        self.nombre_entry.delete(0, tk.END)
                        self.link_entry.delete(0, tk.END)
                        self.selector_entry.delete(0, tk.END)
                        self.actualizar_tabla()
                    else:
                        messagebox.showerror("Error", "Ya existe la página que intenta cargar.")
                else: 
                    self.selector_entry.delete(0, tk.END)
                    messagebox.showwarning("!!!", "Intentemos nuevamente.")
            else:
                self.selector_entry.delete(0, tk.END)
                messagebox.showerror("Error", "No se encontro dicho selector en la pagina.")
