import sqlite3

class Persistencia:
    # Método para inicializar la conexión y crear las tablas
    @staticmethod
    def conectar(db_name='productos.db'):
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            return conn, cursor
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None, None

    @staticmethod
    def crear_tablas():
        """Crea las tablas necesarias en la base de datos."""
        conn, cursor = None, None
        try:
            conn, cursor = Persistencia.conectar()
            if conn is None or cursor is None:
                raise sqlite3.Error("No se pudo conectar a la base de datos.")

            # Activar la eliminación en cascada para SQLite
            cursor.execute("PRAGMA foreign_keys = ON;")
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categoria (
                nombre TEXT PRIMARY KEY
            );
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pagina (
                nombre TEXT PRIMARY KEY,
                selector TEXT
            );
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Producto (
                nombre TEXT PRIMARY KEY,
                link TEXT NOT NULL,
                precio FLOAT,
                categoria_nombre TEXT,
                pagina_nombre TEXT,
                FOREIGN KEY (categoria_nombre) REFERENCES Categoria(nombre) ON DELETE CASCADE,
                FOREIGN KEY (pagina_nombre) REFERENCES Pagina(nombre) ON DELETE SET NULL
            );
            ''')
            conn.commit()
            print("Tablas creadas exitosamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")
            return False
        finally:
            if conn:
                conn.close()

   

    # --- Otros métodos con el mismo patrón ---
    

