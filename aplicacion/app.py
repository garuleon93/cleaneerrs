from controlador.controlador_principal import Controlador_Principal
from pathlib import Path
import flet as ft
import sys
#   Coloco esto para arreglar ejecución
repo_root = Path(__file__).resolve().parents[1]  # .../EmpresaElectrica
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


# --- APPEND END ---
repo_root = Path(__file__).resolve().parents[1]   # .../EmpresaElectrica
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

def main(page: ft.Page):
    page.bgcolor = ft.Colors.WHITE
    page.title="Gestor de Contratos"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    #age.theme = ft.Theme(color_scheme=ft.colorScheme(primary=ft.colors.BLACK))
  

    controlador = Controlador_Principal(page)
    controlador.mostrar_vista()
 

if __name__ == "__main__":
    ft.app(target=main)