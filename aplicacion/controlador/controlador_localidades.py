# aplicacion/controlador/controlador_localidades.py
import sqlite3
from pathlib import Path
from typing import Iterable, Dict, Any, List, Optional


# IMPORT dual: funciona como módulo o como script
try:
    from aplicacion.database.config import crear_conexion
except ModuleNotFoundError:
    from database.config import crear_conexion

def _conn():
    #show_db_path_once()
    return crear_conexion()

def init_tabla_localidades() -> None:
    """
    Crea la tabla 'localidades' si no existe.
    """
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS localidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_contratista INTEGER NOT NULL,
                provincia TEXT,
                canton TEXT,
                localidad TEXT,
                delegado TEXT,
                ubicacion TEXT,
                metros REAL,
                p_unitario REAL,
                p_total REAL,
                -- Evita duplicados exactos por contratista
                UNIQUE(id_contratista, provincia, canton, localidad)
            );
        """)
        con.execute("CREATE INDEX IF NOT EXISTS idx_localidades_contratista ON localidades(id_contratista);")
        con.commit()

def limpiar_localidades_contratista(id_contratista: int) -> None:
    with _conn() as con:
        con.execute("DELETE FROM localidades WHERE id_contratista = ?", (id_contratista,))
        con.commit()

def insertar_localidades(rows: Iterable[Dict[str, Any]]) -> int:
    """
    Inserta/actualiza localidades. rows: dicts con las claves abajo.
    Claves esperadas:
      contratista_id, provincia, canton, localidad, delegado, ubicacion, metros, p_unitario, p_total
    Retorna el número de filas efectivamente insertadas/actualizadas.
    """
    sql = """
    INSERT INTO localidades
        (id_contratista, provincia, canton, localidad, delegado, ubicacion, metros, p_unitario, p_total)
    VALUES
        (:id_contratista, :provincia, :canton, :localidad, :delegado, :ubicacion, :metros, :p_unitario, :p_total)
    ON CONFLICT(id_contratista, provincia, canton, localidad)
    DO UPDATE SET
        delegado=excluded.delegado,
        ubicacion=excluded.ubicacion,
        metros=excluded.metros,
        p_unitario=excluded.p_unitario,
        p_total=excluded.p_total;
    """
    with _conn() as con:
        cur = con.executemany(sql, list(rows))
        con.commit()
        return cur.rowcount or 0

def obtener_localidades(id_contratista: Optional[int] = None, texto: str = "") -> List[tuple]:
    """
    Lista localidades. Si se pasa contratista_id, filtra; si se pasa texto, busca en varias columnas.
    Retorna filas como tuplas sqlite.
    """
    base = "SELECT id, id_contratista, provincia, canton, localidad, delegado, ubicacion, metros, p_unitario, p_total FROM localidades"
    params: List[Any] = []
    filtros: List[str] = []
    if id_contratista is not None:
        filtros.append("id_contratista = ?")
        params.append(id_contratista)
    if texto:
        like = f"%{texto.strip()}%"
        filtros.append("(provincia LIKE ? OR canton LIKE ? OR localidad LIKE ? OR delegado LIKE ? OR ubicacion LIKE ?)")
        params += [like, like, like, like, like]
    if filtros:
        base += " WHERE " + " AND ".join(filtros)
    base += " ORDER BY provincia, canton, localidad"
    with _conn() as con:
        return list(con.execute(base, params))

def eliminar_localidades(ids: Iterable[int]) -> int:
    ids = list(ids)
    if not ids: return 0
    qmarks = ",".join("?" for _ in ids)
    with _conn() as con:
        cur = con.execute(f"DELETE FROM localidades WHERE id IN ({qmarks})", ids)
        con.commit()
        return cur.rowcount or 0

# ---------- Import helpers ----------
def importar_excel_a_localidades(xlsx_path: str, fallback_contratista_id: Optional[int] = None) -> int:
    """
    Lee un Excel y lo inserta en 'localidades'.
    Soporta columnas:
       'Contratista' (opcional si se pasa fallback_contratista_id),
       'Provincia', 'Cantón' o 'Cantón ', 'Localidad', 'Delegado', 'Ubicación',
       'Metros', 'P. unitario', 'P.Total'
    Retorna el número de filas insertadas/actualizadas.
    """
    try:
        import pandas as pd
    except Exception as e:
        raise RuntimeError("Pandas is required to import Excel. Install with: pip install pandas openpyxl") from e

    df = pd.read_excel(xlsx_path)

    # Normaliza nombres de columnas (maneja 'Cantón ' con espacio final)
    cols = {c.strip().lower(): c for c in df.columns}
    def get(colname: str) -> str:
        # colname: normalized
        for k, original in cols.items():
            if k == colname: return original
        raise KeyError(f"Missing column '{colname}' in Excel")

    # Contratista: puede venir en Excel o por parámetro
    has_col_contratista = "contratista" in cols

    registros = []
    for _, r in df.iterrows():
        if has_col_contratista:
            cid = r[cols["contratista"]]
            if pd.isna(cid) and fallback_contratista_id is None:
                # skip rows sin contratista
                continue
            id_contratista = int(cid) if not pd.isna(cid) else int(fallback_contratista_id)
        else:
            if fallback_contratista_id is None:
                raise KeyError("Excel has no 'Contratista' column and no fallback_contratista_id was provided.")
            id_contratista = int(fallback_contratista_id)

        def sval(name, default=""):
            try:
                v = r[cols[name]]
                return "" if (v is None or (isinstance(v, float) and pd.isna(v))) else str(v).strip()
            except KeyError:
                return default

        def fval(name):
            try:
                v = r[cols[name]]
            except KeyError:
                return None
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return None
            try:
                return float(str(v).replace(",", "."))
            except Exception:
                return None

        provincia = sval("provincia")
        canton = sval("cantón") if "cantón" in cols else sval("cantón")
        localidad = sval("localidad")
        delegado = sval("delegado")
        ubicacion = sval("ubicación")
        metros = fval("metros")
        p_unitario = fval("p. unitario")
        p_total = fval("p.total")

        registros.append(dict(
            id_contratista=id_contratista,
            provincia=provincia,
            canton=canton,
            localidad=localidad,
            delegado=delegado,
            ubicacion=ubicacion,
            metros=metros,
            p_unitario=p_unitario,
            p_total=p_total
        ))

    return insertar_localidades(registros)