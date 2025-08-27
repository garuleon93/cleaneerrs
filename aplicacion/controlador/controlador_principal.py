from vista.vista_principal import Vista_Principal

class Controlador_Principal:
    def __init__(self, page):
        self.page = page
        self.vista_principal=Vista_Principal(self.page)
        
    def mostrar_vista(self):
        self.vista_principal.crear_pantalla_principal()
    