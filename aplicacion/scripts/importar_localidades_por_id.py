import pandas as pd
import sqlite3
from pathlib import Path
import sys

# ------------------ Configuración mínima ------------------
# 1) Intentar usar la ruta centralizada si existe
try:
    from aplicacion.database.config import DB_PATH
except Exception:
    # 2) Si no hay config.py aún, probamos primero la BD en la RAÍZ del repo
    DB_PATH = (Path(__file__).resolve().parents[2] / "gestionContratos.db").resolve()
    if not DB_PATH.exists():
        # 3) Fallback: BD dentro de /aplicacion
        DB_PATH = (Path(__file__).resolve().parents[1] / "gestionContratos.db").resolve()

# Ruta del Excel: puedes pasarla por argumento o se asume en la RAÍZ del repo
XLS = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else \
      (Path(__file__).resolve().parents[2] / "Localidades.xlsx").resolve()

print(f"[INFO] BD: {DB_PATH}")
print(f"[INFO] Excel: {XLS}")

if not XLS.exists():
    sys.exit(f"No se encontró el Excel: {XLS}")

# ------------------ Lectura del Excel ------------------
df = pd.read_excel(XLS)
# quita espacios colgantes en nombres de columnas (p.ej. 'Cantón ')
df.columns = [c.strip() for c in df.columns]

# Mínimos nombres esperados (el Excel “nuevo” ya viene adaptado)
# Aceptamos pequeñas variantes típicas sin normalización pesada
def pick(*names):
    for n in names:
        if n in df.columns:
            return n
    raise SystemExit(f"Falta columna obligatoria. Ninguna de {names} está en el Excel.\n"
                     f"Columnas reales: {list(df.columns)}")

COL_ID  = pick("id_contratista", "Contratista")
COL_PRO = pick("Provincia")
COL_CAN = pick("Cantón", "Canton", "Cantón ")
COL_LOC = pick("Localidad")
COL_DEL = pick("Delegado")
COL_UBI = pick("Ubicación", "Ubicacion")
COL_MET = pick("Metros")
COL_PU  = pick("P. unitario", "P.Unitario", "P unitario", "Precio unitario")
COL_PT  = pick("P.Total", "P. Total", "P Total", "Total")

# Limpieza ligera
def s(v):
    if pd.isna(v): return None
    v = str(v).strip()
    return v if v != "" else None

def f(v):
    if pd.isna(v) or v == "": return None
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return None

df_out = pd.DataFrame({
    "id_contratista": df[COL_ID].map(lambda x: int(x) if pd.notna(x) else None),
    "provincia":      df[COL_PRO].map(s),
    "canton":         df[COL_CAN].map(s),
    "localidad":      df[COL_LOC].map(s),
    "delegado":       df[COL_DEL].map(s) if COL_DEL in df.columns else None,
    "ubicacion":      df[COL_UBI].map(s) if COL_UBI in df.columns else None,
    "metros":         df[COL_MET].map(f) if COL_MET in df.columns else None,
    "p_unitario":     df[COL_PU].map(f)  if COL_PU in df.columns else None,
    "p_total":        df[COL_PT].map(f)  if COL_PT in df.columns else None,
})

# Validación mínima de claves
oblig = ["id_contratista","provincia","canton","localidad"]
if df_out[oblig].isnull().any().any():
    filas = df_out[df_out[oblig].isnull().any(axis=1)]
    print(f"[ERROR] Hay filas con valores obligatorios nulos en {oblig}:")
    print(filas[oblig])
    sys.exit(1)

# ------------------ Inserción en SQLite (UPSERT) ------------------
con = sqlite3.connect(DB_PATH)
with con:
    con.executescript("""
    DROP TABLE IF EXISTS localidades;  
                      
    CREATE TABLE localidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contratista INTEGER NOT NULL,
    provincia TEXT, canton TEXT, localidad TEXT,
    delegado TEXT, ubicacion TEXT,
    metros REAL, p_unitario REAL, p_total REAL,
    -- ¡NUEVA clave incluye ubicacion!
    UNIQUE(id_contratista, provincia, canton, localidad, ubicacion),
    FOREIGN KEY (id_contratista) REFERENCES contratistas(id)
    );

    CREATE INDEX IF NOT EXISTS idx_localidades_contratista ON localidades(id_contratista);
    """)
    sql = """
    INSERT INTO localidades
      (id_contratista, provincia, canton, localidad, delegado, ubicacion, metros, p_unitario, p_total)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id_contratista, provincia, canton, localidad, ubicacion)
    DO UPDATE SET
      delegado   = excluded.delegado,
      ubicacion  = excluded.ubicacion,
      metros     = excluded.metros,
      p_unitario = excluded.p_unitario,
      p_total    = excluded.p_total;
    """
    tuplas = list(df_out[["id_contratista","provincia","canton","localidad","delegado","ubicacion","metros","p_unitario","p_total"]]
                  .itertuples(index=False, name=None))
    cur = con.executemany(sql, tuplas)

print(f"[OK] Filas procesadas: {len(tuplas)}")