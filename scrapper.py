from playwright.sync_api import sync_playwright
import re
from Clases.productos import Producto
from Clases.pagina import Pagina
from tkinter import messagebox


class Scrapper:
    @staticmethod
    def verificarSelector(url, selector):
        """
        Se le envia una url y un selector, de no poder encontrar ese selector en la pagina retorna falso.

        """
        with sync_playwright() as p:
            # Lanzamos el navegador en modo headless 
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Navegamos a la URL
            page.goto(url)
            try:
                # Esperamos que el elemento esté presente en el DOM
                page.wait_for_selector(selector)
            
                # Extraemos el texto del elemento seleccionado
                element_text = page.locator(selector).inner_text()
            except : 
                return False    
            finally:
                browser.close()
            temp_text = element_text.replace('.', '#TEMP#')  # Paso temporal para no confundir los cambios
            temp_text = temp_text.replace(',', '.')          # Reemplaza las comas por puntos
            final_text = temp_text.replace('#TEMP#', ',')    # Reemplaza el temporal por comas

        #Eliminamos cualquier otro símbolo no deseado, dejando solo números, comas y puntos
            final_text = re.sub(r'[^0-9.,]', '', final_text)    
            
            return final_text

    @staticmethod
    def actualizarProductos():
        productos = Producto.obtener_productos()
        # por cada producto va nombre, link,precio,categoria y pagina
        for producto in productos:
            selector = Pagina.traer_pagina(producto[4])[0]
            precio = Scrapper.verificarSelector(producto[1],selector[1])
            if (precio == False):
                precio = 0
            Producto.actualizar_precio(producto[0],precio)    
        messagebox.showinfo("Actualización","Productos actualizados.") 

        
# Ejemplo de uso
# url = "https://www.mercadolibre.com.ar/galletitas-dulces-rellenas-con-crema-oreo-354gr/p/MLA22652988?pdp_filters=deal:MLA930902-1#searchVariation=MLA22652988&position=1&search_layout=grid&type=product&tracking_id=df6eb780-694c-4441-a305-fc7be692f6b2"
# selector = "#maincontent > div > div.product-simple.container > div.col-12.col-sm-6.section-detail-scrool > div > div.section-detail > div.container-price-quotas > div > div.prices-add-to-cart-actions.prices-pdp > div > div > div > div > span > span > div > span"  # Cambia este selector al que quieras extraer

# # Ejecutamos la función
# respuesta = Scrapper.extract_element(url, selector)
# if(respuesta == False):
#         print("no se pudo");
# else:
#     print(f"Texto del elemento seleccionado: {respuesta}")