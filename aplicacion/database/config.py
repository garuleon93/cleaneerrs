from pathlib import Path
import sqlite3

# **Una sola BD**: la de la raíz del proyecto
DB_PATH = (Path(__file__).resolve().parents[2] / "gestionContratos.db").resolve()
#   …/EmpresaElectrica/aplicacion/database/config.py
#   parents[2] -> …/EmpresaElectrica/
_printed = False
def show_db_path_once():
    """Imprime la ruta de la BD una sola vez (útil para depurar)."""
    global _printed
    if not _printed:
        print(f"[DB] Usando base de datos en: {DB_PATH}")
        _printed = True

def crear_conexion():
    """Conexión centralizada con FK activas."""
    show_db_path_once()
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    return con        