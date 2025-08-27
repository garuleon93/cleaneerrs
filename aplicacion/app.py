from controlador.controlador_principal import Controlador_Principal
import flet as ft

def main(page: ft.Page):
    page.bgcolor = ft.colors.WHITE
    page.title="Gestor de Contratos"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    #age.theme = ft.Theme(color_scheme=ft.colorScheme(primary=ft.colors.BLACK))
  

    controlador = Controlador_Principal(page)
    controlador.mostrar_vista()

 

ft.app(target=main) 