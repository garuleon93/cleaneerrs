import flet as ft
from vista import vista_contratistas
from vista import vista_facturas
from vista import vista_informes
from vista import vista_localidades

class Vista_Principal:
    def __init__(self, page):
        self.page = page  # Aquí agregamos la página
           

    
    def crear_pantalla_principal(self):

        
        def cambiar_contenido(e):
            if tabs.selected_index==1:
                tab2.content=vista_facturas.obtener_pantalla_facturas()
            if tabs.selected_index==2:
                tab3.content=vista_informes.obtener_pantalla_informes()
            if tabs.selected_index == 3:
                tab4.content = vista_localidades.obtener_pantalla_localidades()    
            tabs.update()

        # Definir tabs con contenido inicial
        tab1 = ft.Tab(text="Contratistas",icon=ft.icons.PERSON,content=vista_contratistas.obtener_pantalla_contratistas())
        tab2 = ft.Tab(text="Facturas",icon=ft.icons.DOCUMENT_SCANNER,content=vista_facturas.obtener_pantalla_facturas())
        tab3 = ft.Tab(text="Informes",icon=ft.icons.SCHEDULE,content=vista_informes.obtener_pantalla_informes())
        tab4 = ft.Tab(text="Localidades",icon=ft.icons.LOCATION_CITY,content=vista_localidades.obtener_pantalla_localidades())

        # Tabs principal
        tabs = ft.Tabs(
            on_change=cambiar_contenido,
            animation_duration=0,
            selected_index=0,
            expand=1,
            label_color=ft.colors.BLUE_800,
            unselected_label_color=ft.colors.BLUE_200,
            tabs=[tab1, tab2, tab3, tab4]
        )

        # Botón para cambiar el contenido de la pestaña 2
        titulo=ft.Text(value="Gestión de Contratistas",size=24,color=ft.colors.BLUE_800)
        
        self.page.add(titulo,tabs)

    
    """def crear_pantalla_principal(self):


        def pantalla_contratistas():
                return vista_contratistas.obtener_pantalla_contratistas()

        def pantalla_facturas():
                return vista_facturas.obtener_pantalla_facturas()
        
        def pantalla_informes():
                return vista_informes.obtener_pantalla_informes()
       
        #TABS PARA  CONTRATISTAS - FACTURAS - GENENRAR NFORMES
        tabs=ft.Tabs(
            selected_index=0,
            animation_duration=50,
            tabs=[
                ft.Tab(text="Contratistas",icon=ft.icons.PERSON,content=pantalla_contratistas()),
                ft.Tab(text="Facturas",icon=ft.icons.DOCUMENT_SCANNER,content=pantalla_facturas()),
                ft.Tab(text="Generar Informes",icon=ft.icons.SCHEDULE,content=pantalla_informes()),
            ],
            expand=1,
            label_color=ft.colors.BLUE_800,
            unselected_label_color=ft.colors.BLUE_200
            
        )
        titulo=ft.Text(value="Gestón de Contratistas",size=24,color=ft.colors.BLUE_800)
        
        self.page.add(titulo,tabs)
        """
