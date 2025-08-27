import flet as ft
from controlador import controlador_contratista
from controlador import controlador_factura


class Vista_Localidades:
    def __init__(self, page):
        self.page = page

    def construir(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Gestión de Localidades", size=24, weight="bold", color=ft.colors.BLUE_800),
                ft.Text("Aquí se podrán agregar, modificar o eliminar localidades asociadas a contratos."),
                ft.Row([
                    ft.TextField(label="Nombre de la localidad", width=300),
                    ft.ElevatedButton(text="Agregar", icon=ft.icons.ADD)
                ]),
                ft.Divider(),
                ft.Text("Listado de localidades:", size=18, weight="bold"),
                ft.ListView(
                    expand=True,
                    spacing=10,
                    padding=20,
                    auto_scroll=True,
                    controls=[
                        ft.Text("Localidad 1"),
                        ft.Text("Localidad 2"),
                        ft.Text("Localidad 3")
                    ]
                )
            ]),
            padding=20,
            expand=True
        )
    
def obtener_pantalla_localidades():
    return Vista_Localidades(None).construir()