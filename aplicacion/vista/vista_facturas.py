import flet as ft
from controlador import controlador_contratista
from controlador import controlador_factura

datos_contratista={}
fecha = ""
def obtener_pantalla_facturas(): #debo hacer validaciones
        
        nro_factura = ft.TextField(dense=True,label="Número de Factura",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50,color=ft.colors.BLACK)
        #fecha = ft.TextField(dense=True,label="Fecha",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        mes_pago=ft.TextField(dense=True,label="Mes de Pago",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50,color=ft.colors.BLACK)
        anio_pago=ft.TextField(dense=True,label="Año de Pago",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50,color=ft.colors.BLACK)
        nro_dias = ft.TextField(dense=True,label="Número de días",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50,color=ft.colors.BLACK)
        valor_factura = ft.TextField(dense=True,label="Valor de la factura",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50,color=ft.colors.BLACK)
        dias_multa=ft.TextField(dense=True,label="Días de Multa",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50,color=ft.colors.BLACK)
        
        contratos = controlador_contratista.obtener_contratistas()
        def dropdown_changed(e):
            t.value = f"{dropdown_factura.value}"
        t=ft.Text() 

        dropdown_factura =ft.Dropdown(on_change=dropdown_changed, label="Contratista", hint_text="Escoja un contratista", autofocus=True,color=ft.colors.BLACK)
        dropdown_factura.options.clear
        for contrato in contratos:
                dropdown_factura.options.append(ft.dropdown.Option(contrato[2]))
        
        dias = [str(d).zfill(2) for d in range(1, 32)]  # 01 - 31
        meses = {"Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08","Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"}
        anios = [str(a) for a in range(2025, 2030)]  # anios 2000 - 2030

        # Crear Dropdowns con tamanio reducido
        dia = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=80, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        mes = ft.Dropdown( options=[ft.dropdown.Option(m) for m in meses.keys()], width=120, text_size=12,hint_text="Mes", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        anio= ft.Dropdown(options=[ft.dropdown.Option(a) for a in anios],width=80, text_size=12,hint_text="año", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        

        dia_inicial = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=80, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        dia_final = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=80, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        
        def limpiar():
             dias_multa.value=  nro_factura.value  = mes_pago.value=dias_multa.value= anio_pago.value = nro_dias.value  = ""
             dia.value=""  
             mes.value=""  
             anio.value=""   
             
        
        def validar_formulario_factura():
             print("Hay que validar los datos del formulario")
             global fecha
             fecha = f"{dia.value}-{meses[mes.value]}-{anio.value}"
            
             return True
        
        

        
        
    #Botones formulario Contratista
        
        ###boton_guardar=ft.ElevatedButton("Guardar Contratista",on_click=agregar_factura)
        
        campo_busqueda = ft.TextField(                        
                            suffix_icon = ft.icons.SEARCH,
                            label= "Buscar por el nombre",
                            border= ft.InputBorder.UNDERLINE,
                            border_color= ft.colors.BLUE_800,
                            label_style = ft.TextStyle(color= ft.colors.BLUE_800),
                            ###on_change = searh_data,
                        )     
      
        tabla_datos =  ft.DataTable(
                            expand= True,
                            border=ft.border.all(2, "ft.colors.BLUE_800"),
                            #data_row_color = { ft.MaterialState.SELECTED: ft.colors.BLUE_800, ft.MaterialState.PRESSED: "black"},
                            border_radius=10,
                            show_checkbox_column = True,
                            columns=[
                                ft.DataColumn(ft.Text("Contratista", color=ft.colors.BLUE_800, weight = "bold")),
                                ft.DataColumn(ft.Text("Nro Factura", color=ft.colors.BLUE_800, weight = "bold")),
                                ft.DataColumn(ft.Text("Fecha", color=ft.colors.BLUE_800, weight = "bold")),
                                ft.DataColumn(ft.Text("Mes de Pago", color=ft.colors.BLUE_800, weight = "bold")),
                                ft.DataColumn(ft.Text("Año de Pago", color=ft.colors.BLUE_800, weight = "bold"), numeric=True),
                                ft.DataColumn(ft.Text("Valor", color=ft.colors.BLUE_800, weight = "bold"), numeric=True ),
                            ],data_text_style=ft.TextStyle(color=ft.colors.BLACK),
                        )        
        
       
        

        def show_data():
            tabla_datos.rows = []
            
            contratos = controlador_contratista.obtener_contratistas()
            facturas = controlador_factura.obtener_facturas()
            nombre_contratista=ft.Text()
            for factura in facturas:
                for contrato in contratos:
                    if factura[1]==contrato[0]:
                        nombre_contratista=contrato[2]
                        break
                tabla_datos.rows.append(
                    ft.DataRow(
                        ##on_select_changed=get_index, 
                        cells=[
                            ft.DataCell(ft.Text(nombre_contratista)),
                            ft.DataCell(ft.Text(f"{factura[2]}")),  
                            ft.DataCell(ft.Text(f"{factura[3]}")),
                            ft.DataCell(ft.Text(f"{factura[4]}")),
                            ft.DataCell(ft.Text(f"{factura[5]}")),
                            ft.DataCell(ft.Text(f"{factura[5]}"))  
                        ]
                    )
                )
            
        
        show_data()


        def agregar_factura(e): #debo hacer validaciones
            if validar_formulario_factura()==True:
                id_contratista=ft.Text()
                for contrato in contratos:
                    if t.value==contrato[2]:
                        id_contratista=contrato[0]
                        break
                datos_contratista = {
                    'id_contratista':id_contratista,
                    'nro_factura': nro_factura.value,
                    'fecha': fecha,
                    'mes_pago':mes_pago.value,
                    'anio_pago':anio_pago.value,
                    'nro_dias':nro_dias.value,
                    'valor_factura':valor_factura.value,
                    'dias_multa':dias_multa.value,
                    'dia_inicial':dia_inicial.value,
                    'dia_final':dia_final.value,
                }
                controlador_factura.agregar_factura(datos_contratista)
                limpiar()
                show_data()
                e.page.update()
                
                print("Se ha agregado corretamente el contratista")
        

        formulario = ft.Container(
            bgcolor=ft.colors.WHITE,
            border_radius=0,
            col=4,
            padding=ft.padding.all(10),
            content= ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                controls=[
                    dropdown_factura,
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("Fecha:  ",weight=ft.FontWeight.BOLD),dia, mes, anio]
                        )
                    ),
                    nro_factura,
                    #fecha,
                    mes_pago,
                    anio_pago,
                    nro_dias,
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("Periodo desde:  ",weight=ft.FontWeight.BOLD),dia_inicial, dia_final]
                        )
                    ),
                    valor_factura,
                    dias_multa,
                    ft.Container(
                        content= ft.Row(
                            spacing = 5,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls= [
                            ft.ElevatedButton(text="Guardar",
                                        icon = ft.icons.SAVE,
                                        icon_color= "white",
                                        style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
                                        animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
                                        on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
                                        on_click= agregar_factura,
                                        ),
                            ft.ElevatedButton(text="Actualizar",
                                        icon = ft.icons.UPDATE,
                                        icon_color= "white",
                                        style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
                                        animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
                                        on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
                                        ###on_click=update_data,
                                        ),    
                            ft.ElevatedButton(text="Borrar",
                                        icon = ft.icons.DELETE,
                                        icon_color= "white",
                                        style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
                                        animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
                                        on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
                                        ###on_click= delete_data,
                                        ),                          
                            ]
                        )
                        
                    )
                ]
            )
        )

        table = ft.Container(
            bgcolor= ft.colors.WHITE10,
            border_radius=10,
            col = 8,
            padding=ft.padding.all(10),
            content= ft.Column(   
                expand=True,           
                controls=[
                    ft.Container(
                        padding = 10,
                        content= ft.Row(
                            controls=[
                                campo_busqueda,
                                ft.IconButton(
                                    icon= ft.icons.EDIT,
                                    ###on_click= edit_flied_text,
                                    icon_color= ft.colors.GREY_800,
                                ),
                                  
                            ]
                        ),
                    ),

                    ft.Column(
                        expand= True, 
                        scroll="auto",
                        controls=[
                        ft.ResponsiveRow([
                            tabla_datos
                            ]),
                        ]
                    )
                ]
            )
        )
        conent = ft.ResponsiveRow(
            controls=[
                formulario,
                table
            ]
        )

        return ft.Container(conent) 