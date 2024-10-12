import tkinter as tk
from tkinter import ttk, font, messagebox
from Clases.pagina import Pagina
from Clases.categoria import Categoria
from Clases.productos import Producto
from scrapper import Scrapper

class ProductForm:
    def __init__(self, root, nombre_producto, link_producto, paginas, categoria):
        # Crear una nueva ventana Toplevel
        self.window = tk.Toplevel(root)
        self.window.title("Agregar Producto")
        self.window.geometry("400x500")

        # Definir fuentes
        self.titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)

        # Título
        self.titulo_label = tk.Label(self.window, text="Agregar Producto", font=self.titulo_font)
        self.titulo_label.pack(pady=20)

        # Nombre del producto
        self.nombre_label = tk.Label(self.window, text="Nombre del Producto:", font=self.label_font)
        self.nombre_label.pack(pady=10)
        
        self.nombre_entry = tk.Entry(self.window, width=35, font=self.label_font, state="normal")
        self.nombre_entry.pack(pady=5)
        self.nombre_entry.insert(0, nombre_producto)
        self.nombre_entry.config(state="readonly")

        # Link del producto
        self.link_label = tk.Label(self.window, text="Link del Producto:", font=self.label_font)
        self.link_label.pack(pady=10)

        
        self.link_entry = tk.Entry(self.window, width=35, font=self.label_font, state="normal")
        self.link_entry.pack(pady=5)
        self.link_entry.insert(0, link_producto)

        # Combobox para seleccionar la página
        self.pagina_label = tk.Label(self.window, text="Seleccionar Página:", font=self.label_font)
        self.pagina_label.pack(pady=10)

        
        self.pagina_combobox = ttk.Combobox(self.window, state="readonly", font=self.label_font)
        self.pagina_combobox.pack(pady=5)
        self.cargar_paginas()
        self.pagina_combobox.set(paginas)

        # Combobox para seleccionar la categoría
        self.categoria_label = tk.Label(self.window, text="Seleccionar Categoría:", font=self.label_font)
        self.categoria_label.pack(pady=10)


        self.categoria_combobox = ttk.Combobox(self.window, state="readonly", font=self.label_font)
        self.categoria_combobox.pack(pady=5)
        self.cargar_categorias()
        self.categoria_combobox.set(categoria)

        # Botón para guardar
        self.save_button = tk.Button(self.window, text="Guardar Producto", width=20, height=2, command=self.guardar_producto, bg="#4CAF50", fg="white", font=self.label_font)
        self.save_button.pack(pady=20)

        # Botón para eliminar
        self.delete_button = tk.Button(self.window, text="Eliminar Producto", width=20, height=2, command=self.eliminar_producto, bg="#F44336", fg="white", font=self.label_font)
        self.delete_button.pack(pady=10)

   

    def cargar_paginas(self):
        """Método para cargar las páginas desde la base de datos"""
        # Aquí deberías extraer las páginas de la base de datos y asignarlas al combobox
        paginas =  Pagina.traerNombre_paginas()# Obtener lista de páginas desde la base de datos
        self.pagina_combobox['values'] = paginas  # Implementar carga de páginas desde la base de datos

    def cargar_categorias(self):
        """Método para cargar las categorías desde la base de datos"""
        # Aquí deberías extraer las categorías de la base de datos y asignarlas al combobox
        categorias = Categoria.nombre_categorias() # Obtener lista de categorías desde la base de datos
        self.categoria_combobox['values'] = categorias

    def guardar_producto(self):
        
        nombre = self.nombre_entry.get()
        link = self.link_entry.get()
        pagina = self.pagina_combobox.get()
        categoria = self.categoria_combobox.get()
        selector = Pagina.traer_pagina(pagina)[0][1]
        precio = Scrapper.verificarSelector(link,selector)
        if(precio != False):
            Producto.actualizar_producto(nombre,link,precio,categoria,pagina)
            messagebox.showinfo("EXITO","Producto actualizado.")
            self.window.destroy()
        else:
            messagebox.showerror("Error","Problema en la estracción de precio, cambios no guardados.")
        pass  # Implementar lógica de guardar producto

    def eliminar_producto(self):
        nombre = self.nombre_entry.get()
        respuesta = messagebox.askyesno("Eliminar producto",f"Seguro que quieres eliminar el producto {nombre}?")
        if(respuesta):
            Producto.eliminar_producto(nombre)
            messagebox.showinfo("EXITO","Producto eliminado.")
            self.window.destroy()
        pass  # Implementar lógica de eliminar producto
