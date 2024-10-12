import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from Clases.categoria import Categoria

class NewCat:
    def __init__(self, frame):
        self.frame = frame


        # Definir fuentes
        self.titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        
        # Título
        self.titulo_label = tk.Label(frame, text="Agregar Categoría", font=self.titulo_font)
        self.titulo_label.pack(pady=20)

        # Etiqueta
        self.label = tk.Label(frame, text="Nombre de la Categoría:", font=self.label_font)
        self.label.pack(pady=10)

        # Campo de entrada
        self.categoria_entry = tk.Entry(frame, width=35, font=self.label_font)
        self.categoria_entry.pack(pady=5)

        # Botón para guardar
        self.save_button = tk.Button(frame, text="Guardar Categoría", width=20, height=2, command=self.guardar_categoria, bg="#4CAF50", fg="white", font=self.label_font)
        self.save_button.pack(pady=20)

        # Para la tabla que contiene las categorias
        self.crear_tabla()
        self.actualizar_tabla()
        
    def crear_tabla(self):
        """Crear la tabla debajo del input para mostrar las categorías"""
        # Frame para contener la tabla y el scrollbar
        frame_tabla = tk.Frame(self.frame)
        frame_tabla.pack(pady=20, fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Definir columnas
        columnas = ('#1',)

        # Crear el Treeview
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scrollbar.set, height=5)
        self.tabla.bind("<Double-1>", self.on_doble_click)
        # Configurar el scrollbar
        scrollbar.config(command=self.tabla.yview)

        # Definir encabezados
        self.tabla.heading('#1', text='Categorías')

        # Empaquetar la tabla
        self.tabla.pack(fill="both", expand=True)

    def on_doble_click(self, event):
        selected_item = self.tabla.selection()
        if selected_item:
            categoria = self.tabla.item(selected_item, 'values')[0]
            respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la categoría '{categoria}'? Esto eliminara tanto la categoria como sus elementos asociados.")
            if respuesta:
                Categoria.eliminar_categoria(categoria)
                self.actualizar_tabla()
    def actualizar_tabla(self):
        """Actualizar la tabla con las categorías almacenadas"""
        self.categorias = Categoria.nombre_categorias()
        # Limpiar la tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        # Insertar cada categoría en la tabla
        if(self.categorias != False):
            for categoria in self.categorias:
                self.tabla.insert("", tk.END, values=(categoria,))

    def guardar_categoria(self):
        categoria = self.categoria_entry.get()
        if categoria.strip() == "":
            messagebox.showwarning("Entrada Inválida", "El nombre de la categoría no puede estar vacío.")
        else:
            if(Categoria.agregar_categoria(categoria)):
                messagebox.showinfo("Éxito", f"Categoría '{categoria}' guardada exitosamente.")
                self.categoria_entry.delete(0, tk.END)
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "Ya existe la categoria que intenta cargar.")      
