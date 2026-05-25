"""
Dialogo para alta y modificacion de movimientos.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime


class FormularioMovimiento(ttk.Toplevel):
    """Dialogo modal para crear o editar un movimiento."""

    def __init__(self, parent, db, mov=None):
        """
        Args:
            parent: Ventana padre
            db: DatabaseManager
            mov: dict con movimiento existente (None = nuevo)
        """
        super().__init__(parent)
        self.db = db
        self.mov = mov  # None si es nuevo
        self.resultado = None  # Datos del movimiento al guardar

        titulo = "Editar Movimiento" if mov else "Nuevo Movimiento"
        self.title(titulo)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        self._construir()
        if mov:
            self._cargar_datos(mov)

        # Centrar respecto al padre
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self.wait_window()

    def _construir(self):
        """Construye el formulario."""
        pad = {"padx": 15, "pady": 5}
        main = ttk.Frame(self, padding=15)
        main.pack(fill=BOTH, expand=YES)

        # Fecha
        ttk.Label(main, text="Fecha:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", **pad)
        self.fecha_entry = ttk.DateEntry(main, width=22, bootstyle="primary")
        self.fecha_entry.grid(row=0, column=1, sticky="ew", **pad)

        # Tipo (Ingreso/Gasto)
        ttk.Label(main, text="Tipo:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", **pad)
        self.tipo_var = ttk.StringVar(value="gasto")
        tipos_frame = ttk.Frame(main)
        tipos_frame.grid(row=1, column=1, sticky="w", **pad)
        ttk.Radiobutton(tipos_frame, text="Ingreso", variable=self.tipo_var,
                        value="ingreso", bootstyle="success-toolbutton").pack(side=LEFT, padx=2)
        ttk.Radiobutton(tipos_frame, text="Gasto", variable=self.tipo_var,
                        value="gasto", bootstyle="danger-toolbutton").pack(side=LEFT, padx=2)

        # Categoria 1
        ttk.Label(main, text="Categoria:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", **pad)
        self.cat1_combo = ttk.Combobox(main, width=30, state="normal", bootstyle="primary")
        self.cat1_combo.grid(row=2, column=1, sticky="ew", **pad)
        self._cargar_categorias()

        # Categoria 2 (subcategoria)
        ttk.Label(main, text="Subcategoria:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", **pad)
        self.cat2_entry = ttk.Entry(main, width=32, bootstyle="primary")
        self.cat2_entry.grid(row=3, column=1, sticky="ew", **pad)

        # Categoria 3 (detalle)
        ttk.Label(main, text="Detalle:", font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", **pad)
        self.cat3_entry = ttk.Entry(main, width=32, bootstyle="primary")
        self.cat3_entry.grid(row=4, column=1, sticky="ew", **pad)

        # Cuenta
        ttk.Label(main, text="Cuenta:", font=("Segoe UI", 10)).grid(row=5, column=0, sticky="w", **pad)
        self.cuenta_combo = ttk.Combobox(main, width=30, state="readonly", bootstyle="primary")
        self.cuenta_combo.grid(row=5, column=1, sticky="ew", **pad)
        self._cargar_cuentas()

        # Importe
        ttk.Label(main, text="Importe (EUR):", font=("Segoe UI", 10)).grid(row=6, column=0, sticky="w", **pad)
        vcmd = (self.register(self._validar_importe), "%P")
        self.importe_entry = ttk.Entry(main, width=22, font=("Segoe UI", 11, "bold"),
                                       validate="key", validatecommand=vcmd,
                                       bootstyle="primary")
        self.importe_entry.grid(row=6, column=1, sticky="w", **pad)
        self.importe_entry.insert(0, "0.00")

        # Separador
        ttk.Separator(main).grid(row=7, column=0, columnspan=2, sticky="ew", pady=10, padx=15)

        # Botones
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(0, 5))

        ttk.Button(
            btn_frame, text="Cancelar", bootstyle="secondary-outline",
            width=12, command=self.destroy,
        ).pack(side=LEFT, padx=5)

        txt_btn = "Guardar Cambios" if self.mov else "Anadir Movimiento"
        ttk.Button(
            btn_frame, text=txt_btn, bootstyle="primary",
            width=18, command=self._guardar,
        ).pack(side=LEFT, padx=5)

        # Atajo de teclado
        self.bind("<Return>", lambda e: self._guardar())
        self.bind("<Escape>", lambda e: self.destroy())

        # Ancho minimo
        main.columnconfigure(1, weight=1)

    def _cargar_categorias(self):
        """Carga las categorias desde la BD o valores por defecto."""
        cats = self.db.categorias_distinct(1)
        if not cats:
            # Valores por defecto del Excel
            cats = [
                "Caza", "Hogar", "Impuestos", "Informatica", "Loteria",
                "Ocio", "Otros", "Piso Madrid", "Piso Socuellamos",
                "Regalos", "Retornos", "Salud", "Semana Santa",
                "Telefonia", "Trabajo", "Vacaciones", "Vehiculos",
                "Yeguada Trimena", "Efectivo", "Inversion Acciones",
            ]
        self.cat1_combo["values"] = sorted(cats)

    def _cargar_cuentas(self):
        """Carga las cuentas disponibles."""
        cuentas = self.db.cuentas_distinct()
        if not cuentas:
            cuentas = ["OpenBank Principal", "OpenBank Socu",
                       "Efectivo", "IBKR", "Degiro"]
        self.cuenta_combo["values"] = cuentas
        if cuentas:
            self.cuenta_combo.current(0)

    def _cargar_datos(self, mov):
        """Rellena el formulario con datos existentes."""
        try:
            self.fecha_entry.entry.delete(0, "end")
            fecha = mov["fecha"]
            if isinstance(fecha, str):
                self.fecha_entry.entry.insert(0, fecha)
            else:
                self.fecha_entry.entry.insert(0, str(fecha))
        except Exception:
            pass

        self.tipo_var.set(mov.get("tipo", "gasto"))

        # Categoria 1
        cat1 = mov.get("categoria1", "")
        if cat1 in self.cat1_combo["values"]:
            self.cat1_combo.set(cat1)
        else:
            self.cat1_combo.set(cat1)

        self.cat2_entry.delete(0, "end")
        self.cat2_entry.insert(0, mov.get("categoria2", ""))

        self.cat3_entry.delete(0, "end")
        self.cat3_entry.insert(0, mov.get("categoria3", ""))

        cuenta = mov.get("cuenta", "")
        if cuenta in self.cuenta_combo["values"]:
            self.cuenta_combo.set(cuenta)

        self.importe_entry.delete(0, "end")
        self.importe_entry.insert(0, f"{mov.get('importe', 0):.2f}")

    def _validar_importe(self, valor):
        """Valida que el importe sea un numero valido."""
        if valor == "" or valor == "-":
            return True
        try:
            float(valor.replace(",", "."))
            return True
        except ValueError:
            return False

    def _guardar(self):
        """Valida y guarda el movimiento."""
        # Validar campos
        fecha = self.fecha_entry.entry.get()
        if not fecha:
            messagebox.showwarning("Validacion", "La fecha es obligatoria", parent=self)
            return

        cat1 = self.cat1_combo.get().strip()
        if not cat1:
            messagebox.showwarning("Validacion", "La categoria es obligatoria", parent=self)
            return

        importe_str = self.importe_entry.get().strip().replace(",", ".")
        if not importe_str:
            messagebox.showwarning("Validacion", "El importe es obligatorio", parent=self)
            return

        try:
            importe = float(importe_str)
            if importe <= 0:
                messagebox.showwarning("Validacion", "El importe debe ser positivo", parent=self)
                return
        except ValueError:
            messagebox.showwarning("Validacion", "Importe invalido", parent=self)
            return

        # Guardar resultado
        self.resultado = {
            "fecha": fecha,
            "categoria1": cat1,
            "categoria2": self.cat2_entry.get().strip(),
            "categoria3": self.cat3_entry.get().strip(),
            "cuenta": self.cuenta_combo.get(),
            "tipo": self.tipo_var.get(),
            "importe": importe,
        }

        if self.mov:
            self.resultado["id"] = self.mov["id"]

        self.destroy()
