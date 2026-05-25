"""
Panel de movimientos - Lista de transacciones con CRUD.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from ui.formulario_movimiento import FormularioMovimiento


class PanelMovimientos(ttk.Frame):
    """Lista de movimientos con filtros y CRUD."""

    def __init__(self, parent, datos):
        super().__init__(parent)
        self.datos = datos
        self.db = datos.db
        self._construir()

    def _construir(self):
        # --- Toolbar CRUD ---
        toolbar = ttk.Frame(self, padding=(10, 10, 10, 5))
        toolbar.pack(fill=X)

        ttk.Label(toolbar, text="Movimientos",
                  font=("Segoe UI", 12, "bold")).pack(side=LEFT)

        ttk.Button(
            toolbar, text="+ Nuevo", bootstyle="success",
            width=12, command=self._nuevo_movimiento,
        ).pack(side=RIGHT, padx=(5, 0))

        ttk.Button(
            toolbar, text="Editar", bootstyle="info-outline",
            width=10, command=self._editar_movimiento,
        ).pack(side=RIGHT, padx=5)

        ttk.Button(
            toolbar, text="Eliminar", bootstyle="danger-outline",
            width=10, command=self._eliminar_movimiento,
        ).pack(side=RIGHT, padx=5)

        # --- Filtros ---
        filtros = ttk.Frame(self, padding=(10, 0, 10, 5))
        filtros.pack(fill=X)

        ttk.Label(filtros, text="Filtrar:", font=("Segoe UI", 9, "bold")).pack(side=LEFT, padx=(0, 10))

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
        self.cat_combo = ttk.Combobox(
            filtros, textvariable=self.cat_var,
            values=["Todas"], state="readonly",
            width=20, font=("Segoe UI", 9),
        )
        self.cat_combo.pack(side=LEFT, padx=2)
        self.cat_combo.bind("<<ComboboxSelected>>", self._filtrar)

        # Boton limpiar
        ttk.Button(
            filtros, text="Limpiar", bootstyle="secondary-outline",
            width=8, command=self._limpiar_filtros,
        ).pack(side=RIGHT, padx=(10, 0))

        # Contador
        self.contador_label = ttk.Label(filtros, text="", font=("Segoe UI", 9))
        self.contador_label.pack(side=RIGHT, padx=10)

        # --- Tabla ---
        self._construir_tabla()

    def _construir_tabla(self):
        """Construye la tabla de movimientos."""
        container = ttk.Frame(self, padding=(10, 0, 10, 10))
        container.pack(fill=BOTH, expand=YES)

        frame_tabla = ttk.Frame(container)
        frame_tabla.pack(fill=BOTH, expand=YES)

        scroll_y = ttk.Scrollbar(frame_tabla, orient=VERTICAL)
        scroll_x = ttk.Scrollbar(frame_tabla, orient=HORIZONTAL)

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Fecha", "Categoria", "Subcat.", "Detalle",
                     "Cuenta", "Tipo", "Importe"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            bootstyle="primary",
            height=20,
        )

        scroll_y.config(command=self.tabla.yview)
        scroll_x.config(command=self.tabla.xview)

        # Columnas
        cols = [
            ("ID", 50, False),
            ("Fecha", 100, False),
            ("Categoria", 130, False),
            ("Subcat.", 120, False),
            ("Detalle", 180, True),
            ("Cuenta", 140, False),
            ("Tipo", 80, False),
            ("Importe", 110, False),
        ]
        for texto, ancho, stretch in cols:
            self.tabla.heading(texto, text=texto)
            self.tabla.column(texto, width=ancho, stretch=stretch)

        # Ocultar columna ID
        self.tabla.column("ID", width=0, stretch=False)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        # Tags de color
        self.tabla.tag_configure("ingreso", foreground="#28a745")
        self.tabla.tag_configure("gasto", foreground="#dc3545")
        self.tabla.tag_configure("invertido", foreground="#FF6B35")
        self.tabla.tag_configure("retorno", foreground="#0078D4")

        # Eventos
        self.tabla.bind("<Double-1>", lambda e: self._editar_movimiento())
        self.tabla.bind("<Delete>", lambda e: self._eliminar_movimiento())
        self.tabla.bind("<Return>", lambda e: self._editar_movimiento())

        # Menu contextual
        self._menu_contextual = tk.Menu(self, tearoff=0)
        self._menu_contextual.add_command(label="Editar", command=self._editar_movimiento)
        self._menu_contextual.add_command(label="Eliminar", command=self._eliminar_movimiento)
        self.tabla.bind("<Button-3>", self._mostrar_menu)

        # Cargar datos
        self._cargar_filtros()
        self._cargar_datos()

    def cargar_meses(self, meses):
        """Carga los meses disponibles."""
        nombres = ["Todos"] + [self.datos.nombre_mes(m) for m in meses]
        self.mes_combo["values"] = nombres
        self.mes_combo.current(0)

    def _cargar_filtros(self):
        """Carga los valores de los filtros."""
        # Meses
        meses = self.datos.get_meses_disponibles()
        self.cargar_meses(meses)

        # Categorias
        cats = ["Todas"] + sorted(self.datos.categorias)
        self.cat_combo["values"] = cats
        self.cat_combo.current(0)

    def _cargar_datos(self, movs=None):
        """Carga los movimientos en la tabla."""
        if movs is None:
            movs = self.datos.get_movimientos()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for m in movs:
            fecha = m["fecha"]
            if isinstance(fecha, str):
                try:
                    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
                    fecha_str = fecha_dt.strftime("%d/%m/%Y")
                except ValueError:
                    fecha_str = fecha
            else:
                fecha_str = str(fecha)

            tag = m["tipo"]
            self.tabla.insert("", END, values=(
                m["id"],
                fecha_str,
                m["categoria1"],
                m.get("categoria2", ""),
                m.get("categoria3", ""),
                m["cuenta"],
                m["tipo"].capitalize(),
                f"{m['importe']:,.2f} EUR",
            ), tags=(tag,))

        self.contador_label.config(text=f"{len(movs)} movimientos")

    def _filtrar(self, event=None):
        """Aplica filtros a la tabla."""
        movs = self.datos.get_movimientos()

        # Filtro mes
        mes_sel = self.mes_var.get()
        if mes_sel and mes_sel != "Todos":
            for num in range(1, 13):
                if self.datos.nombre_mes(num) == mes_sel:
                    movs = [m for m in movs
                            if isinstance(m["fecha"], str)
                            and m["fecha"].startswith(f"2025-{num:02d}")]
                    break

        # Filtro categoria
        cat_sel = self.cat_var.get()
        if cat_sel and cat_sel != "Todas":
            movs = [m for m in movs if m["categoria1"] == cat_sel]

        self._cargar_datos(movs)

    def _limpiar_filtros(self):
        """Limpia filtros."""
        self.mes_var.set("Todos")
        self.cat_var.set("Todas")
        self._cargar_datos(self.datos.get_movimientos())

    # ─── CRUD ─────────────────────────────────────────────

    def _obtener_seleccionado(self):
        """Devuelve el ID del movimiento seleccionado o None."""
        sel = self.tabla.selection()
        if not sel:
            messagebox.showinfo("Seleccion", "Selecciona un movimiento primero")
            return None
        return int(self.tabla.item(sel[0], "values")[0])

    def _nuevo_movimiento(self):
        """Abre formulario para nuevo movimiento."""
        form = FormularioMovimiento(self.winfo_toplevel(), self.db)
        if form.resultado:
            try:
                self.db.insertar_movimiento(**form.resultado)
                messagebox.showinfo("Exito", "Movimiento anadido correctamente")
                self._filtrar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def _editar_movimiento(self):
        """Abre formulario para editar movimiento seleccionado."""
        id_mov = self._obtener_seleccionado()
        if id_mov is None:
            return

        mov = self.db.obtener_movimiento(id_mov)
        if not mov:
            messagebox.showerror("Error", "Movimiento no encontrado")
            return

        form = FormularioMovimiento(self.winfo_toplevel(), self.db, mov=mov)
        if form.resultado:
            try:
                self.db.actualizar_movimiento(**form.resultado)
                messagebox.showinfo("Exito", "Movimiento actualizado correctamente")
                self._filtrar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def _eliminar_movimiento(self):
        """Elimina el movimiento seleccionado."""
        id_mov = self._obtener_seleccionado()
        if id_mov is None:
            return

        mov = self.db.obtener_movimiento(id_mov)
        if not mov:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Eliminar movimiento del {mov['fecha']} por {mov['importe']:.2f} EUR?",
        )
        if confirmar:
            try:
                self.db.eliminar_movimiento(id_mov)
                messagebox.showinfo("Exito", "Movimiento eliminado")
                self._filtrar()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def _mostrar_menu(self, event):
        """Muestra menu contextual en la tabla."""
        item = self.tabla.identify_row(event.y)
        if item:
            self.tabla.selection_set(item)
            self._menu_contextual.post(event.x_root, event.y_root)
