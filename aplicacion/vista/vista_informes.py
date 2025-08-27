import flet as ft
from controlador import controlador_contratista
from controlador import controlador_factura
from controlador.controlador_documentos import Generar_Docs
import tkinter as tk
from tkinter import messagebox


def obtener_pantalla_informes(): #debo hacer validaciones
        

        administrador = ft.TextField(dense=True,label="Ingrese el administrador", border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        def dropdown_change_contratista(e):
            contratista_id=""
            for contratista in contratistas:
                if dropdown_contratista.value==contratista[2]:
                    contratista_id = contratista[0]
            
            print("Contratista id: "+str(contratista_id))
            c.value = f"Seleccionado: {contratista_id}"

            # Limpiar opciones anteriores
            dropdown_factura.options.clear()

            # Obtener nuevas facturas según el contratista seleccionado
            facturas = controlador_factura.obtener_facturas_por_contratista(contratista_id)
            
            # Agregar nuevas opciones al dropdown de facturas
            for factura in facturas:
                dropdown_factura.options.append(ft.dropdown.Option(f"{factura[4]} {factura[5]}"))

            # Refrescar la UI
            e.page.update()

        def dropdown_change_facturas(e):
            f.value = f"Seleccionado: {dropdown_factura.value}"
            e.page.update()

        c = ft.Text()
        f = ft.Text()

        # Dropdown de contratistas
        dropdown_contratista = ft.Dropdown(
            on_change=dropdown_change_contratista, 
            label="Contratista", 
            hint_text="Escoja un contratista", 
            autofocus=True
        )

        contratistas = controlador_contratista.obtener_contratistas()
        for contratista in contratistas:
            dropdown_contratista.options.append(ft.dropdown.Option(contratista[2]))

        # Dropdown de facturas
        dropdown_factura = ft.Dropdown(
            on_change=dropdown_change_facturas, 
            label="Factura", 
            hint_text="Escoja el mes de facturación", 
            autofocus=True
        )
        
        
        def generar_informes(e):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)  # Asegurar que esté al frente
            root.update()  # Refrescar la ventana antes de abrir el diálogo
                      
            if word.value==pdf.value==excel.value==False:
                messagebox.showerror("Aviso", "Seleccione almenos un formato")
                 
            else:
                if c1.value==c2.value==c3.value==excel.value==False:
                    messagebox.showerror("Aviso", "Seleccione almenos un documento para generar")
                    
                else:
                    listaDocs=[c1.value,c2.value,c3.value]
                    listaWP=[word.value,pdf.value,excel.value]


                    # Obtener el contratista seleccionado
                    
                    contratista_id = next((c[0] for c in contratistas if c[2] == dropdown_contratista.value), None)
                    contratista_seleccionado = next((c for c in contratistas if c[2] == dropdown_contratista.value), None)
                    
                    # Obtener la lista de facturas del contratista seleccionado
                    facturas_contratista = controlador_factura.obtener_facturas_por_contratista(contratista_id)

                    # Buscar la factura seleccionada basándose en el texto del dropdown
                    factura_seleccionada = next((f for f in facturas_contratista if f"{f[4]} {f[5]}" == dropdown_factura.value), None)


                    contDocs=Generar_Docs(listaDocs,listaWP,administrador.value,contratista_seleccionado,factura_seleccionada,facturas_contratista)
                    valor=contDocs.generar() 
                    
                    if valor == True:
                        messagebox.showinfo("Éxito", "Documento(s) generados con éxito")
                    else:
                        messagebox.showerror("Aviso", "No se generó ningún Documento")

                    
                            
                      
        
        c1 = ft.Checkbox(label="Acta de Entrega/Recepción", value=False)
        c2 = ft.Checkbox(label="Informe Administrador", value=False)
        c3 = ft.Checkbox(label="Modelo Quipux", value=False)
        word = ft.Checkbox(label="Crear Editables", value=False)
        pdf = ft.Checkbox(label="Crear PDF", value=False)
        excel = ft.Checkbox(label="Generar Excel de la planilla de Pago", value=False)
       
        generar_button = ft.ElevatedButton(
            text="Generar",
            icon=ft.icons.ADD_CIRCLE,
            icon_color="white",
            style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
            on_click=generar_informes,
            animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
            on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
        )

        formulario = ft.Container(
            bgcolor= ft.colors.WHITE10,
            border_radius=50,
            padding=ft.padding.all(50),
            
            content= ft.Column(   
                expand=True,           
                controls=[
                    administrador,
                    dropdown_contratista,
                    dropdown_factura,
                    ft.Divider(color=ft.colors.BLACK12, thickness=2),
                    ft.Row(controls=[ft.Text("Seleccione los documentos a generar:"),]),
                    ft.Row(
                        controls=[c1, c2, c3,excel],
                    ),
                    ft.Divider(color=ft.colors.BLACK, thickness=2),
                    ft.Row(controls=[ft.Text("Seleccione el formato:"),]),
                    ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[word, pdf],
                    ),
                    ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[generar_button],
                    ),
                ]
            )
        )
        
        conent = ft.ResponsiveRow(
            controls=[
                formulario,
            ]
        )

        return ft.Container(
                        ft.Column(
                controls=[
                    ft.Text("Gestión de Informes", size=24, weight="bold", color=ft.colors.BLUE_800),
                    conent
                ]
            )
        ) 