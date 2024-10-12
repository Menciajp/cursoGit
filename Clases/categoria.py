import sqlite3
from persistencia import Persistencia

class Categoria:
 # --- Métodos de CRUD con manejo de errores ---
    @staticmethod
    def agregar_categoria(nombre):
        """Agrega una nueva categoría."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("INSERT INTO Categoria (nombre) VALUES (?)", (nombre.upper(),))
            conn.commit()
            print("Categoría agregada correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al agregar categoría: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def editar_categoria(nombre, nuevo_nombre):
        """Edita el nombre de una categoría."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute('''
                UPDATE Categoria
                SET nombre = ?
                WHERE nombre = ?
            ''', (nuevo_nombre.upper(), nombre.upper()))
            conn.commit()
            print("Categoría editada correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al editar categoría: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar_categoria(nombre):
        """Elimina una categoría por su nombre (en cascada eliminará los productos asociados)."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("DELETE FROM Categoria WHERE nombre = ?", (nombre,))
            conn.commit()
            print(f"Categoría '{nombre}' eliminada correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar categoría: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def nombre_categorias():
        """Trae array de nombre de categorias."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("SELECT * FROM Categoria")
            categorias = cursor.fetchall()
            nombres_categorias = [categoria[0] for categoria in categorias]
            return nombres_categorias
        except sqlite3.Error as e:
            return False
        finally:
            if conn:
                conn.close()             