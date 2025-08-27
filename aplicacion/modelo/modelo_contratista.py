from database.database import crear_conexion

def agregar_contratista(contratista):
        
        conexion = crear_conexion()

        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO contratistas (
                orden, empresa, monto_contrato, fecha_inicio,
                fecha_finalizacion, fecha_emision, fecha_suscripcion,
                ruc, costo_mensual,localidad,provincia,ficha,anticipo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            contratista['orden'], contratista['empresa'], contratista['monto_contrato'],
            contratista['fecha_inicio'], contratista['fecha_finalizacion'],
            contratista['fecha_emision'], contratista['fecha_suscripcion'],
            contratista['ruc'], contratista['costo_mensual'], contratista['localidad'], contratista['provincia'], contratista['ficha'], contratista['anticipo']
        ))
        conexion.commit()
        conexion.close()

def obtener_contratistas():
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM contratistas')
        return cursor.fetchall()