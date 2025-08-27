import sqlite3


def crear_conexion():
    conexion = sqlite3.connect('gestionContratos.db')
    return conexion


def crear_tabla_contratos():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden TEXT NOT NULL,
            empresa TEXT NOT NULL,
            monto_contrato REAL NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_finalizacion TEXT NOT NULL,
            fecha_emision TEXT NOT NULL,
            fecha_suscripcion TEXT NOT NULL,
            ruc TEXT NOT NULL,
            costo_mensual REAL NOT NULL,
            localidad TEXT NOT NULL,
            provincia TEXT NOT NULL,
            ficha TEXT NOT NULL,
            anticipo REAL NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def crear_tabla_facturas():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contratista INTEGER NOT NULL,
            nro_factura TEXT NOT NULL,
            fecha TEXT NOT NULL,
            mes_pago TEXT NOT NULL,
            anio_pago TEXT NOT NULL,
            nro_dias INTEGER NOT NULL,
            valor_factura REAL NOT NULL,
            dias_multa INTEGER NOT NULL,
            dia_inicial INTEGER NOT NULL,
            dia_final INTEGER NOT NULL,       
            FOREIGN KEY (id_contratista) REFERENCES contratistas(id)
        )
    ''')
    conexion.commit()
    conexion.close()
