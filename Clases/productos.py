import sqlite3
from persistencia import Persistencia

class Producto:
    
    @staticmethod
    def agregar_producto(nombre, link, precio, categoria_nombre, pagina_nombre):
        """Agrega un nuevo producto."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")

            cursor.execute('''
                INSERT INTO Producto (nombre, link, precio, categoria_nombre, pagina_nombre)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre.upper(), link, precio, categoria_nombre, pagina_nombre))
            conn.commit()
            print("Producto agregado correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al agregar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()            

    @staticmethod
    def actualizar_producto(nombre, nuevo_link, nuevo_precio, nueva_categoria_nombre, nueva_pagina_nombre):
        """Actualiza un producto existente."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            # Actualizar los campos con los nuevos valores
            cursor.execute('''
                UPDATE Producto
                SET link = ?, precio = ?, categoria_nombre = ?, pagina_nombre = ?
                WHERE nombre = ?
            ''', (nuevo_link, nuevo_precio, nueva_categoria_nombre, nueva_pagina_nombre, nombre.upper()))
            
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No se encontró el producto con el nombre: {nombre}")
                return False

            print("Producto actualizado correctamente.")
            return True

        except sqlite3.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()
    @staticmethod
    def actualizar_link_pagina(nombre, nuevo_link, nueva_pagina):
        """Actualiza el link y la categoría de un producto existente en la base de datos."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute('''
                UPDATE Producto
                SET link = ?, pagina_nombre = ?
                WHERE nombre = ?
            ''', (nuevo_link, nueva_pagina, nombre))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Producto '{nombre}' actualizado correctamente (link y categoría).")
                return True
            else:
                print(f"No se encontró ningún producto con el nombre '{nombre}'.")
                return False
        except sqlite3.Error as e:
            print(f"Error al actualizar link y categoría del producto: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def actualizar_precio(nombre, nuevo_precio):
        """Actualiza el precio de un producto existente en la base de datos."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute('''
                UPDATE Producto
                SET precio = ?
                WHERE nombre = ?
            ''', (nuevo_precio, nombre))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Precio del producto '{nombre}' actualizado correctamente.")
                return True
            else:
                print(f"No se encontró ningún producto con el nombre '{nombre}'.")
                return False
        except sqlite3.Error as e:
            print(f"Error al actualizar el precio del producto: {e}")
            return False
        finally:
            if conn:
                conn.close()


    @staticmethod
    def obtener_productos_por_categoria(categoria_nombre):
        """Obtiene todos los productos de una categoría específica."""
        conn, cursor = Persistencia.conectar()
        cursor.execute("SELECT * FROM Producto WHERE categoria_nombre = ?", (categoria_nombre,))
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    @staticmethod
    def obtener_productos():
        """Obtiene todos los productos."""
        conn, cursor = Persistencia.conectar()
        cursor.execute("SELECT * FROM Producto")
        productos = cursor.fetchall()
        conn.close()
        return productos
    
    @staticmethod
    def eliminar_producto(nombre):
        """Elimina un producto por su nombre."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")

            # Eliminar el producto
            cursor.execute('''
                DELETE FROM Producto
                WHERE nombre = ?
            ''', (nombre.upper(),))
            conn.commit()

            # Verificar si se eliminó algún producto
            if cursor.rowcount > 0:
                print("Producto eliminado correctamente.")
                return True
            else:
                print("No se encontró un producto con ese nombre.")
                return False
        except sqlite3.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False
        finally:
            if conn:
                conn.close()