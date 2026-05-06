import flet as ft
from controlador import controlador_contratista
from controlador import controlador_localidades as ctrl_loc

class vista_Localidades:
    def __init__(self, page: ft.Page):
        self.page = page
        ctrl_loc.init_tabla_localidades()

        # UI state
        self.contratistas = controlador_contratista.obtener_contratistas()
        self.contratista_por_nombre = {c[2]: c[0] for c in self.contratistas}  # nombre -> id
        self.nombre_por_id = {c[0]: c[2] for c in self.contratistas}           # id -> nombre

        self.sel_contratista = ft.Dropdown(
            label="Contratista",
            hint_text="Filtrar por contratista",
            options=[ft.dropdown.Option(c[2]) for c in self.contratistas],
            on_change=self._on_filtrar,
            width=360,
        )
        self.buscar = ft.TextField(label="Buscar (provincia, cantón, localidad, delegado…)",
                                   on_submit=self._on_filtrar, width=420)

        self.btn_importar = ft.ElevatedButton("Importar Excel…", icon=ft.icons.UPLOAD_FILE, on_click=self._on_importar)
        self.btn_eliminar = ft.OutlinedButton("Eliminar seleccionados", icon=ft.icons.DELETE, on_click=self._on_eliminar)

        # File picker
        self.picker = ft.FilePicker(on_result=self._on_pick_file)
        if self.page:
            self.page.overlay.append(self.picker)

        # Table
        self.tabla = ft.DataTable(
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
            columns=[
                ft.DataColumn(ft.Text("✓")),
                ft.DataColumn(ft.Text("Contratista")),
                ft.DataColumn(ft.Text("Provincia")),
                ft.DataColumn(ft.Text("Cantón")),
                ft.DataColumn(ft.Text("Localidad")),
                ft.DataColumn(ft.Text("Delegado")),
                ft.DataColumn(ft.Text("Ubicación")),
                ft.DataColumn(ft.Text("Metros")),
                ft.DataColumn(ft.Text("P. unitario")),
                ft.DataColumn(ft.Text("P. total")),
            ],
            rows=[],
        )

        self._rows_checked = set()  # ids marcados
        self._recargar()
        
        self.tabla_scroll = ft.Container(
            content=ft.Column(
                controls=[ft.Row([self.tabla], scroll=ft.ScrollMode.ALWAYS)],  # horizontal
                scroll=ft.ScrollMode.ALWAYS,   # vertical
                expand=True
            ),
            height=520,   # ajusta a tu layout
            expand=True
        )
    # ---------------- UI handlers ----------------

    def _on_filtrar(self, e=None):
        self._recargar()

    def _on_importar(self, e):
        # Si se selecciona un contratista, lo usamos como fallback
        if self.picker.page is None:
            e.page.overlay.append(self.picker)
            e.page.update()
        self.picker.pick_files(
            dialog_title="Selecciona Localidades.xlsx",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["xlsx", "xls"]
        )

    def _on_pick_file(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return
        ruta = e.files[0].path
        fallback_cid = None
        if self.sel_contratista.value:
            fallback_cid = self.contratista_por_nombre.get(self.sel_contratista.value)

        try:
            n = ctrl_loc.importar_excel_a_localidades(ruta, fallback_contratista_id=fallback_cid)
            self._toast(f"Importados {n} registros desde Excel")
        except Exception as ex:
            self._toast(f"Error al importar: {ex}", error=True)
        self._recargar()

    def _on_eliminar(self, e):
        if not self._rows_checked:
            self._toast("No hay filas seleccionadas", error=True); return
        borradas = ctrl_loc.eliminar_localidades(self._rows_checked)
        self._rows_checked.clear()
        self._toast(f"Eliminadas {borradas} filas")
        self._recargar()

    # ---------------- Data & render ----------------

    def _recargar(self):
        self.tabla.rows.clear()
        texto = (self.buscar.value or "").strip()
        cid = None
        if self.sel_contratista.value:
            cid = self.contratista_por_nombre.get(self.sel_contratista.value)

        filas = ctrl_loc.obtener_localidades(cid, texto)

        def chk_factory(_id: int):
            cb = ft.Checkbox(value=False)
            def on_change(ev):
                if cb.value:
                    self._rows_checked.add(_id)
                else:
                    self._rows_checked.discard(_id)
            cb.on_change = on_change
            return cb

        def _cell(val):
            return ft.DataCell(ft.Text("" if val is None else str(val), color=ft.Colors.BLACK))

        for (id_, contratista_id, prov, cant, loc, delegado, ubic, metros, p_u, p_t) in filas:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(chk_factory(id_)),
                        _cell(self.nombre_por_id.get(contratista_id, str(contratista_id))),
                        _cell(prov),
                        _cell(cant),
                        _cell(loc),
                        _cell(delegado),
                        _cell(ubic),
                        _cell(metros),
                        _cell(p_u),
                        _cell(p_t),
                    ]
                )
            )
        if self.page:
            self.page.update()

    def _toast(self, msg: str, error: bool=False):
        if not self.page: return
        self.page.snack_bar = ft.SnackBar(
            ft.Text(msg),
            bgcolor=ft.Colors.RED_400 if error else ft.Colors.BLUE_GREY_700,
        )
        self.page.snack_bar.open = True
        self.page.update()

    # ---------------- Public API ----------------

    def construir(self):
        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row([
                        ft.Text("Gestión de Localidades", size=22, weight="bold", color=ft.Colors.BLUE_800),
                        ft.Container(expand=True),
                        self.btn_importar,
                        self.btn_eliminar,
                    ]),
                    ft.Row([self.sel_contratista, self.buscar]),
                    self.tabla_scroll,
                    #ft.Container(self.tabla, expand=True),
                ],
            )
        )

def obtener_pantalla_localidades(page: ft.Page):
    # Mantén compatibilidad con tu vista principal
    return vista_Localidades(page).construir()