from database.database import crear_conexion

def agregar_factura(factura):
        
        conexion = crear_conexion()

        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO facturas (
                id_contratista, nro_factura, fecha, mes_pago, anio_pago, nro_dias, valor_factura, dias_multa, dia_inicial, dia_final
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            factura['id_contratista'],factura['nro_factura'],factura['fecha'] , factura['mes_pago'], factura['anio_pago'], factura['nro_dias'], factura['valor_factura'], factura['dias_multa'], factura['dia_inicial'], factura['dia_final']
        ))
        conexion.commit()
        conexion.close()

def obtener_facturas():
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM facturas')
        return cursor.fetchall()