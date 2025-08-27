import flet as ft
from controlador import controlador_contratista
from datetime import datetime

datos_contratista={}
fecha_inicio = ""
fecha_finalizacion = ""
fecha_emision = ""
fecha_suscripcion = ""

def obtener_pantalla_contratistas(): #debo hacer validaciones
            
        orden = ft.TextField(dense=True,label="Orden" ,color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        empresa = ft.TextField(dense=True,label="Empresa",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        monto_contrato = ft.TextField(dense=True,color=ft.colors.BLACK,label="Monto Contrato",border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        
        ruc = ft.TextField(dense=True,label="RUC",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        costo_mensual = ft.TextField(dense=True,label="Costo Mensual",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        localidad = ft.TextField(dense=True,label="Localidad",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        provincia = ft.TextField(dense=True,label="Provincia",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        ficha= ft.TextField(dense=True,label="Ficha Específica",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        anticipo= ft.TextField(dense=True,label="Anticipo",color=ft.colors.BLACK,border_color= ft.colors.GREY_100,bgcolor=ft.colors.GREY_50)
        

        dias = [str(d).zfill(2) for d in range(1, 32)]  # 01 - 31
        meses = {"Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08","Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"}
        anios = [str(a) for a in range(2020, 2030)]  # anios 2000 - 2030

        # Crear Dropdowns con tamanio reducido
        dia_inicio = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=50, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        mes_inicio = ft.Dropdown( options=[ft.dropdown.Option(m) for m in meses.keys()], width=90, text_size=12,hint_text="Mes", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        anio_inicio= ft.Dropdown(options=[ft.dropdown.Option(a) for a in anios],width=70, text_size=12,hint_text="año", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        
        dia_finalizacion  = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=50, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        mes_finalizacion  = ft.Dropdown( options=[ft.dropdown.Option(m) for m in meses.keys()], width=90, text_size=12,hint_text="Mes", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        anio_finalizacion = ft.Dropdown(options=[ft.dropdown.Option(a) for a in anios],width=70, text_size=12,hint_text="año", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        #ME QUEDE AQU  DEBO AGREGAR LOS SELECT A LA INTERFAZ GRAFICA
        dia_emision = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=50, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        mes_emision = ft.Dropdown( options=[ft.dropdown.Option(m) for m in meses.keys()], width=90, text_size=12,hint_text="Mes", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        anio_emision= ft.Dropdown(options=[ft.dropdown.Option(a) for a in anios],width=70, text_size=12,hint_text="año", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        
        dia_suscripcion = ft.Dropdown(options=[ft.dropdown.Option(d) for d in dias],width=50, text_size=12,hint_text="Día", border_radius=8, content_padding=ft.padding.symmetric(horizontal=5, vertical=2) )
        mes_suscripcion = ft.Dropdown( options=[ft.dropdown.Option(m) for m in meses.keys()], width=90, text_size=12,hint_text="Mes", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        anio_suscripcion = ft.Dropdown(options=[ft.dropdown.Option(a) for a in anios],width=70, text_size=12,hint_text="año", border_radius=8,content_padding=ft.padding.symmetric(horizontal=5, vertical=2))
        
        
            
        def limpiar():
            anticipo.value= ficha.value=orden.value = empresa.value = monto_contrato.value =  ruc.value = costo_mensual.value= provincia.value = localidad.value = ""
            dia_inicio.value = mes_inicio.value = anio_inicio.value= ""
            dia_finalizacion.value  = mes_finalizacion.value  = anio_finalizacion.value = ""
            dia_emision.value = mes_emision.value = anio_emision.value= ""
            dia_suscripcion.value = mes_suscripcion.value = anio_suscripcion.value = ""
        
        def validar_formulario_contratista():
            
            print("Hay que validar los datos del formulario")
            global fecha_inicio
            fecha_inicio = f"{dia_inicio.value}-{meses[mes_inicio.value]}-{anio_inicio.value}"
            global fecha_finalizacion
            fecha_finalizacion = f"{dia_finalizacion.value}-{meses[mes_finalizacion.value]}-{anio_finalizacion.value}"
            global fecha_emision
            fecha_emision = f"{dia_emision.value}-{meses[mes_emision.value]}-{anio_emision.value}"
            global fecha_suscripcion
            fecha_suscripcion = f"{dia_suscripcion.value}-{meses[mes_suscripcion.value]}-{anio_suscripcion.value}"
            return True
        
        #me quede aqui no se esta guardando el campo ficha

        def agregar_contratista(e): #debo hacer validaciones
            if validar_formulario_contratista()==True:
                datos_contratista = {
                    'orden': orden.value,
                    'empresa': empresa.value,
                    'monto_contrato': monto_contrato.value,
                    'fecha_inicio': fecha_inicio,
                    'fecha_finalizacion': fecha_finalizacion,
                    'fecha_emision': fecha_emision,
                    'fecha_suscripcion': fecha_suscripcion,
                    'ruc': ruc.value,
                    'costo_mensual': costo_mensual.value,
                    'localidad': localidad.value,
                    'provincia': provincia.value,
                    'ficha':ficha.value,
                    'anticipo':anticipo.value
                }

                controlador_contratista.agregar_contratista(datos_contratista)
                limpiar()
                show_data()
                
                e.page.update()
                print("Se ha agregado corretamente el contratista")
        
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
                                #ft.DataColumn(ft.Text("Id Contratista", color=ft.colors.BLUE_800, weight = "bold")),
                                #ft.DataColumn(ft.Text("Orden", color=ft.colors.BLUE_800, weight = "bold")),
                                ft.DataColumn(ft.Text("Empresa", color=ft.colors.BLUE, weight = "bold")),
                                ft.DataColumn(ft.Text("Monto Total", color=ft.colors.BLUE, weight = "bold"), numeric=True),
                                ft.DataColumn(ft.Text("Costo Mensual", color=ft.colors.BLUE, weight = "bold"), numeric=True ),
                            ],data_text_style=ft.TextStyle(color=ft.colors.BLACK),
                        )        
        
       
        

        def show_data():
            tabla_datos.rows = []
            
            contratos = controlador_contratista.obtener_contratistas()
            
            for contrato in contratos:
                tabla_datos.rows.append(
                    ft.DataRow(
                        ##on_select_changed=get_index, 
                        cells=[
                            #ft.DataCell(ft.Text(f"{contrato[0]}")),
                            #ft.DataCell(ft.Text(f"{contrato[1]}")),  
                            ft.DataCell(ft.Text(f"{contrato[2]}")),  
                            ft.DataCell(ft.Text(f"{contrato[3]}")),
                            ft.DataCell(ft.Text(f"{contrato[9]}")),  
                        ]
                    )
                )
            
        
        show_data()
        
        formulario = ft.Container(
            bgcolor=ft.colors.WHITE,
            border_radius=0,
            col=4,
            padding=ft.padding.all(10),
            content=ft.Column(
                #alignment=ft.MainAxisAlignment.SPACE_AROUND,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Contenedor para organizar en dos columnas
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            # Primera columna
                            ft.Column(
                                expand= True, 
                                scroll="auto",
                                controls=[
                                    
                                    orden,
                                    empresa,
                                    ruc,
                                    ficha,
                                    
                                ]
                            ),
                            # Segunda columna
                            ft.Column(
                                expand= True, 
                                scroll="auto",
                                controls=[
                                    #fecha_inicio,
                                    #fecha_finalizacion,
                                    #fecha_emision,
                                    #fecha_suscripcion,
                                    localidad,
                                    provincia,
                                    monto_contrato,
                                    costo_mensual,
                                ]
                            ),
                        ]
                    ),
                    anticipo,
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            
                            controls=[
                                ft.Text("SELECCIONAR FECHAS",weight=ft.FontWeight.BOLD,)]
                        )
                    ),
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("Inicio:    \t\t\t\t\t\t"),dia_inicio, mes_inicio, anio_inicio]
                        )
                    ),
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("Fin:       \t\t\t\t\t\t\t"),dia_finalizacion, mes_finalizacion, anio_finalizacion]
                        )
                    ),
                                        ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("Emision:   \t\t\t\t"),dia_emision, mes_emision, anio_emision]
                        )
                    ),
                                        ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Text("Suscripción:\t"),dia_suscripcion, mes_suscripcion, anio_suscripcion]
                        )
                    ),


                    
                    
                    # Botones alineados al centro
                    ft.Container(
                        content=ft.Row(
                            
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    text="Guardar",
                                    icon=ft.icons.SAVE,
                                    icon_color="white",
                                    style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
                                    animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
                                    on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
                                    on_click=agregar_contratista,
                                ),
                                ft.ElevatedButton(
                                    text="Actualizar",
                                    icon=ft.icons.UPDATE,
                                    icon_color="white",
                                    style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
                                    animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
                                    on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
                                    # on_click=update_data,
                                ),
                                ft.ElevatedButton(
                                    text="Borrar",
                                    icon=ft.icons.DELETE,
                                    icon_color="white",
                                    style=ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_700,),
                                    animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),  # Animación al hacer clic
                                    on_hover=lambda e: (setattr(e.control, "style", ft.ButtonStyle(color="white",bgcolor=ft.colors.BLUE_900 if e.data == "true" else ft.colors.BLUE_800)),e.control.update()),
                                    # on_click=delete_data,
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