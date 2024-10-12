import tkinter as tk
from tkinter import ttk, font, messagebox
from Ui.editProd import ProductForm
from Clases.pagina import Pagina
from Clases.categoria import Categoria
from Clases.productos import Producto
from scrapper import Scrapper

class NewProd:
    def __init__(self, frame):
        self.frame = frame

        # Definir fuentes
        self.titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)

        # Título
        self.titulo_label = tk.Label(frame, text="Agregar Producto", font=self.titulo_font)
        self.titulo_label.pack(pady=20)

        # Nombre del producto
        self.nombre_label = tk.Label(frame, text="Nombre del Producto:", font=self.label_font)
        self.nombre_label.pack(pady=10)
        self.nombre_entry = tk.Entry(frame, width=35, font=self.label_font)
        self.nombre_entry.pack(pady=5)

        # Link del producto
        self.link_label = tk.Label(frame, text="Link del Producto:", font=self.label_font)
        self.link_label.pack(pady=10)
        self.link_entry = tk.Entry(frame, width=35, font=self.label_font)
        self.link_entry.pack(pady=5)

        # Combobox para seleccionar la página
        self.pagina_label = tk.Label(frame, text="Seleccionar Página:", font=self.label_font)
        self.pagina_label.pack(pady=10)
        self.pagina_combobox = ttk.Combobox(frame, state="readonly", font=self.label_font)
        self.pagina_combobox.pack(pady=5)
        # Aquí debes cargar las páginas desde la BD
        self.cargar_paginas()

        # Combobox para seleccionar la categoría
        self.categoria_label = tk.Label(frame, text="Seleccionar Categoría:", font=self.label_font)
        self.categoria_label.pack(pady=10)
        self.categoria_combobox = ttk.Combobox(frame, state="readonly", font=self.label_font)
        self.categoria_combobox.pack(pady=5)
        # Aquí debes cargar las categorías desde la BD
        self.cargar_categorias()

        # Crear un frame para los botones
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=20)

        # Botón para guardar
        self.save_button = tk.Button(button_frame, text="Guardar Producto", width=20, height=2, command=self.guardar_producto, bg="#4CAF50", fg="white", font=self.label_font)
        self.save_button.pack(side="left", padx=10)

        # Botón para actualizar tabla
        self.update_button = tk.Button(button_frame, text="Actualizar Tabla", width=20, height=2, command=self.actualizar_tabla, bg="#4CAF50", fg="white", font=self.label_font)
        self.update_button.pack(side="left", padx=10)
        # Crear la tabla de productos
        self.crear_tabla()
        self.actualizar_tabla()

    def cargar_paginas(self):
        """Método para cargar las páginas desde la base de datos"""
        # Aquí deberías extraer las páginas de la base de datos y asignarlas al combobox
        paginas =  Pagina.traerNombre_paginas()# Obtener lista de páginas desde la base de datos
        self.pagina_combobox['values'] = paginas

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

        if nombre.strip() == "" or link.strip() == "" or pagina == "" or categoria == "":
            messagebox.showwarning("Entrada Inválida", "Todos los campos son obligatorios.")
        else:
            selector = Pagina.traer_pagina(pagina)
            precio = Scrapper.verificarSelector(link,selector[0][1])
            print(precio)
            if(precio != False):
                Producto.agregar_producto(nombre,link,precio,categoria,pagina)
                messagebox.showinfo("Éxito", "Producto guardado exitosamente.")
                print(precio)
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error","Algo anda mal con el link o selector.")    
           

    def crear_tabla(self):
        """Crear la tabla debajo del input para mostrar los productos"""
        # Frame para contener la tabla y el scrollbar
        frame_tabla = tk.Frame(self.frame)
        frame_tabla.pack(pady=20, fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Definir columnas
        columnas = ('Nombre', 'Link', 'Página', 'Categoría', 'Precio')

        # Crear el Treeview
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scrollbar.set, height=5)
        self.tabla.bind("<Double-1>", self.on_doble_click)
        # Configurar el scrollbar
        scrollbar.config(command=self.tabla.yview)

        # Definir encabezados
        for col in columnas:
            self.tabla.heading(col, text=col)

        # Empaquetar la tabla
        self.tabla.pack(fill="both", expand=True)

    def actualizar_tabla(self):
        """Actualizar la tabla con los productos almacenados"""
        # Aquí debes cargar los productos de la base de datos
        productos = Producto.obtener_productos()

        # Ordenar los productos alfabéticamente por la columna 'Categoría' (producto[3] es la categoría)
        productos.sort(key=lambda producto: (producto[3], producto[0]))

        # Limpiar la tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Crear una etiqueta para las filas rojas
        self.tabla.tag_configure('red', background='red')

        # Insertar cada producto en la tabla
        for producto in productos:
            if producto[2] == 0:  # Si el precio es 0, pintar la fila de rojo
                self.tabla.insert("", tk.END, values=(producto[0], producto[1], producto[4], producto[3], producto[2]), tags=('red',))
            else:
                self.tabla.insert("", tk.END, values=(producto[0], producto[1], producto[4], producto[3], producto[2]))


    def on_doble_click(self, event):
        selected_item = self.tabla.selection()
        if selected_item:
            producto = self.tabla.item(selected_item, 'values')[0]
            respuesta = messagebox.askyesno("Desea editar el producto", f"¿Está seguro de que desea editar el producto: '{producto}'?")
            if respuesta:
                valores = self.tabla.item(selected_item, 'values')
                root = tk.Tk()
                root.withdraw()
                producto_form = ProductForm(root, nombre_producto=valores[0], link_producto=valores[1], paginas=valores[2], categoria=valores[3])
                root.mainloop()
                self.actualizar_tabla()