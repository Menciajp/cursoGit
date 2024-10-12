import tkinter as tk
from tkinter import messagebox
from Ui.newCat import NewCat
from Ui.newPag import NewPag
from Ui.newProd import NewProd
from persistencia import Persistencia
from scrapper import Scrapper
from formateador import Formateador
import playwright.sync_api

class App:
    def __init__(self, root):
        self.root = root
        # Deshabilitar la opción de redimensionar la ventana
        self.root.resizable(True, True)

        # Centrar la ventana en la pantalla
        self.centrar_ventana()

        # Crear un Frame para las páginas
        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(fill="both", expand=True)

        # Crear un Frame para las secciones
        self.frame_seccion = tk.Frame(self.frame_principal)
        self.frame_seccion.pack(pady=10)

        # Botón para Nueva Categoría
        self.boton_categoria = tk.Button(self.frame_seccion, text="Categorías", command=self.mostrar_categoria)
        self.boton_categoria.pack(side=tk.LEFT, padx=5)

        # Botón para Nueva Página
        self.boton_pagina = tk.Button(self.frame_seccion, text="Páginas", command=self.mostrar_pagina)
        self.boton_pagina.pack(side=tk.LEFT, padx=5)

        # Botón Nuevo Producto
        self.boton_producto = tk.Button(self.frame_seccion, text="Productos", command=self.mostrar_producto)
        self.boton_producto.pack(side=tk.LEFT, padx=5)
        # Botón para Actualizar precios
        self.boton_actPrecios = tk.Button(self.frame_seccion, text="Actualizar Productos", command=Scrapper.actualizarProductos)
        self.boton_actPrecios.pack(side=tk.LEFT, padx=5)
        #crearArchivo
        self.boton_archivo = tk.Button(self.frame_seccion, text="Crear archivo", command=self.crearExcel)
        self.boton_archivo.pack(side=tk.LEFT, padx=5)
        # Frame para mostrar las secciones (NewCat y NewPag)
        self.frame_contenido = tk.Frame(self.frame_principal)
        self.frame_contenido.pack(fill="both", expand=True)

        # Mostrar la sección de Nueva Categoría al inicio
        self.mostrar_categoria()

    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        window_width = 1250
        window_height = 600

        # Obtener la posición de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular la posición para centrar
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Establecer la geometría de la ventana
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
    def mostrar_categoria(self):
        """Mostrar la sección de Nueva Categoría"""
        self.limpiar_contenido()  # Limpiar el contenido actual
        self.new_cat = NewCat(self.frame_contenido)  # Instanciar NewCat en el frame de contenido

    def mostrar_producto(self):
        """Mostrar la sección de Nuevo Producto"""
        self.limpiar_contenido()  # Limpiar el contenido actual
        self.new_prod = NewProd(self.frame_contenido)  # Instanciar NewCat en el frame de contenido

    def mostrar_pagina(self):
        """Mostrar la sección de Nueva Página"""
        self.limpiar_contenido()  # Limpiar el contenido actual
        self.new_pag = NewPag(self.frame_contenido)  # Instanciar NewPag en el frame de contenido

    def limpiar_contenido(self):
        """Limpiar el contenido del frame de contenido"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()  # Eliminar todos los widgets en el frame de contenido

    def crearExcel(self):
        try:
            formateador = Formateador()
            archivo_excel = formateador.crear_archivo_excel()
            formateador.cargar_en_una_hoja(archivo_excel)
            messagebox.showinfo("!!!","Archivo creado correctamente")
        except:
            messagebox.showerror("Uo!","Algo salio mal.")
        

if __name__ == "__main__":
    playwright.sync_api.sync_playwright().start()
    Persistencia.crear_tablas()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    



