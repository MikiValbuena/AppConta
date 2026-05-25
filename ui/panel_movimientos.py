"""
Panel de movimientos - Lista de transacciones con filtros.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from datetime import datetime
from tkinter import ttk as ttk_widgets


class PanelMovimientos(ttk.Frame):
    """Lista de movimientos con filtros."""

    def __init__(self, parent, datos):
        super().__init__(parent)
        self.datos = datos
        self._construir()

    def _construir(self):
        # Filtros
        filtros = ttk.Frame(self, padding=10)
        filtros.pack(fill=X)

        ttk.Label(filtros, text="Filtrar por:", font=("Segoe UI", 10, "bold")).pack(side=LEFT, padx=(0, 10))

        # Filtro mes
        ttk.Label(filtros, text="Mes:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(5, 2))
        self.mes_var = ttk.StringVar(value="Todos")
        self.mes_combo = ttk.Combobox(
            filtros, textvariable=self.mes_var,
            values=["Todos"], state="readonly",
            width=15, font=("Segoe UI", 9),
        )
        self.mes_combo.pack(side=LEFT, padx=2)
        self.mes_combo.bind("<<ComboboxSelected>>", self._filtrar)

        # Filtro categoria
        ttk.Label(filtros, text="Categoria:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(10, 2))
        self.cat_var = ttk.StringVar(value="Todas")
        cats = ["Todas"] + sorted(self.datos.categorias)
        self.cat_combo = ttk.Combobox(
            filtros, textvariable=self.cat_var,
            values=cats, state="readonly",
            width=20, font=("Segoe UI", 9),
        )
        self.cat_combo.pack(side=LEFT, padx=2)
        self.cat_combo.bind("<<ComboboxSelected>>", self._filtrar)

        # Boton limpiar
        ttk.Button(
            filtros, text="Limpiar Filtros",
            bootstyle="secondary-outline",
            command=self._limpiar_filtros,
            width=15,
        ).pack(side=RIGHT, padx=(10, 0))

        # Contador de resultados
        self.contador_label = ttk.Label(filtros, text="", font=("Segoe UI", 9))
        self.contador_label.pack(side=RIGHT, padx=10)

        # Tabla de movimientos
        self._construir_tabla()

    def _construir_tabla(self):
        """Construye la tabla de movimientos."""
        container = ttk.Frame(self, padding=(10, 0, 10, 10))
        container.pack(fill=BOTH, expand=YES)

        columnas = [
            {"text": "Fecha", "stretch": False, "width": 100},
            {"text": "Categoria", "stretch": False, "width": 140},
            {"text": "Subcategoria", "stretch": False, "width": 130},
            {"text": "Detalle", "stretch": True, "width": 200},
            {"text": "Cuenta", "stretch": False, "width": 150},
            {"text": "Tipo", "stretch": False, "width": 80},
            {"text": "Importe", "stretch": False, "width": 110},
        ]

        # Treeview con scrollbars
        frame_tabla = ttk.Frame(container)
        frame_tabla.pack(fill=BOTH, expand=YES)

        scroll_y = ttk.Scrollbar(frame_tabla, orient=VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tabla, orient=HORIZONTAL)

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=[c["text"] for c in columnas],
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            bootstyle="primary",
            height=20,
        )

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        for col in columnas:
            self.tabla.heading(col["text"], text=col["text"])
            self.tabla.column(col["text"], width=col["width"], stretch=col["stretch"])

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Colores para filas
        self.tabla.tag_configure("ingreso", foreground="#28a745")
        self.tabla.tag_configure("gasto", foreground="#dc3545")

        # Cargar datos
        self._cargar_datos()

    def cargar_meses(self, meses):
        """Carga los meses disponibles en el combo."""
        nombres = ["Todos"] + [self.datos.nombre_mes(m) for m in meses]
        self.mes_combo["values"] = nombres
        self.mes_combo.current(0)

    def _cargar_datos(self, movs=None):
        """Carga los movimientos en la tabla."""
        if movs is None:
            movs = self.datos.get_movimientos()

        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for m in movs:
            fecha = m["fecha"]
            if isinstance(fecha, datetime):
                fecha_str = fecha.strftime("%d/%m/%Y")
            else:
                fecha_str = str(fecha)

            importe_str = f"{m['importe']:,.2f} €"

            tag = m["tipo"]
            self.tabla.insert("", END, values=(
                fecha_str,
                m["categoria"],
                m["subcategoria"],
                m["detalle"],
                m["cuenta"],
                m["tipo"].capitalize(),
                importe_str,
            ), tags=(tag,))

        self.contador_label.config(text=f"{len(movs)} movimientos")

    def _filtrar(self, event=None):
        """Aplica filtros a la tabla."""
        movs = self.datos.get_movimientos()

        # Filtro por mes
        mes_sel = self.mes_var.get()
        if mes_sel and mes_sel != "Todos":
            # Mapear nombre a numero
            for num in range(1, 13):
                if self.datos.nombre_mes(num) == mes_sel:
                    movs = [m for m in movs if isinstance(m["fecha"], datetime) and m["fecha"].month == num]
                    break

        # Filtro por categoria
        cat_sel = self.cat_var.get()
        if cat_sel and cat_sel != "Todas":
            movs = [m for m in movs if m["categoria"] == cat_sel]

        self._cargar_datos(movs)

    def _limpiar_filtros(self):
        """Limpia todos los filtros."""
        self.mes_var.set("Todos")
        self.cat_var.set("Todas")
        self._cargar_datos(self.datos.get_movimientos())
