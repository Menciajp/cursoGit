import sqlite3
from persistencia import Persistencia


class Pagina:
    @staticmethod
    def agregar_pagina(nombre, selector):
        """Agrega una nueva página. Retorna True si fue exitoso o False si la pagina ya existe"""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("INSERT INTO Pagina (nombre, selector) VALUES (?, ?)", (nombre.upper(), selector))
            conn.commit()
            print("Página agregada correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al agregar página: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def editar_pagina(nombre, nuevo_selector):
        """Edita el selector de una página."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute('''
                UPDATE Pagina
                SET selector = ?
                WHERE nombre = ?
            ''', (nuevo_selector, nombre.upper()))
            conn.commit()
            print("Página editada correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al editar página: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar_pagina(nombre):
        """Elimina una página por su nombre."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("DELETE FROM Pagina WHERE nombre = ?", (nombre,))
            conn.commit()
            print(f"Página '{nombre}' eliminada correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al eliminar página: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def traer_pagina(pagina):
        """Trae toda la info de una pagina."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("SELECT * FROM Pagina WHERE nombre = ?",(pagina,))
            paginas = cursor.fetchall()
            return paginas
        except sqlite3.Error as e:
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def traer_paginas():
        """Trae todas las paginas."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("SELECT * FROM Pagina")
            paginas = cursor.fetchall()
            return paginas
        except sqlite3.Error as e:
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def traerNombre_paginas():
        """Trae nombre de todas las paginas."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")
            
            cursor.execute("SELECT nombre FROM Pagina")
            paginas = cursor.fetchall()
            nombre_paginas = [pagina[0] for pagina in paginas]
            return nombre_paginas
        except sqlite3.Error as e:
            return False
        finally:
            if conn:
                conn.close()         