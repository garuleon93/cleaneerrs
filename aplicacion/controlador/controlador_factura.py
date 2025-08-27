from modelo import modelo_factura

def agregar_factura(datos_factura):
    modelo_factura.agregar_factura(datos_factura)

def obtener_facturas():
    return modelo_factura.obtener_facturas()

def obtener_facturas_por_contratista(contratista_id):
    facturas_contratista=[]
    facturas= modelo_factura.obtener_facturas()
    for fact in facturas:
        if fact[1]==contratista_id:
            facturas_contratista.append(fact)
    return facturas_contratista