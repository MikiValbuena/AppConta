"""
Ventana principal de AppConta - Frontend 2025.
Interfaz con ttkbootstrap mostrando datos del ano 2025.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.toast import ToastNotification
import tkinter as tk
from tkinter import ttk as ttk_widgets
from datetime import datetime

from ui.data_loader import DataLoader
from ui.panel_movimientos import PanelMovimientos
from ui.panel_resumen import PanelResumen
from ui.panel_balance import PanelBalance


class VentanaPrincipal(ttk.Window):
    """Ventana principal de la aplicacion."""

    def __init__(self):
        super().__init__(
            title="AppConta - Contabilidad Personal 2025",
            themename="cosmo",
            size=(1280, 800),
            minsize=(1024, 600),
            resizable=(True, True),
        )

        # Centrar en pantalla
        self.place_window_center()

        # Cargar datos
        try:
            self.datos = DataLoader(ruta_excel="Conta.xlsx", hoja="2025")
        except FileNotFoundError:
            self.datos = None
            self._mostrar_error("No se encontro Conta.xlsx")
            return
        except Exception as e:
            self.datos = None
            self._mostrar_error(f"Error al cargar datos: {e}")
            return

        # Construir UI
        self._construir_header()
        self._construir_resumen_cards()
        self._construir_notebook()

        # Cargar año en el selector
        self._cargar_selectores()

        # Bind teclas
        self.bind("<Escape>", lambda e: self.destroy())

    def _construir_header(self):
        """Header con titulo y selector de ano."""
        header = ttk.Frame(self, padding=15)
        header.pack(fill=X)

        # Logo / Titulo
        ttk.Label(
            header,
            text="AppConta",
            font=("Segoe UI", 22, "bold"),
            bootstyle="primary",
        ).pack(side=LEFT)

        ttk.Label(
            header,
            text="Contabilidad Personal",
            font=("Segoe UI", 12),
            bootstyle="secondary",
            padding=(10, 0),
        ).pack(side=LEFT)

        # Selector de ano
        self.ano_var = tk.StringVar(value="2025")
        self.ano_combo = ttk.Combobox(
            header,
            textvariable=self.ano_var,
            values=["2025"],
            state="readonly",
            width=8,
            font=("Segoe UI", 11),
            bootstyle="primary",
        )
        self.ano_combo.pack(side=RIGHT, padx=(5, 0))
        self.ano_combo.bind("<<ComboboxSelected>>", self._cambiar_ano)

        # Separador
        ttk.Separator(self, bootstyle="primary").pack(fill=X, padx=15)

    def _construir_resumen_cards(self):
        """Cards de resumen rapido."""
        if not self.datos:
            return

        resumen = self.datos.get_resumen_anual()

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill=X)

        row = ttk.Frame(frame)
        row.pack(fill=X)

        # Card: Ingresos
        self._crear_card(row, "Total Ingresos", f"{resumen['ingresos']:,.2f} €", "success", 0)
        # Card: Gastos
        self._crear_card(row, "Total Gastos", f"{resumen['gastos']:,.2f} €", "danger", 1)
        # Card: Balance
        balance = resumen["balance"]
        color = "success" if balance >= 0 else "danger"
        self._crear_card(row, "Balance Anual", f"{balance:,.2f} €", color, 2)
        # Card: Movimientos
        self._crear_card(row, "Movimientos", str(resumen["total_movimientos"]), "info", 3)

    def _crear_card(self, parent, titulo, valor, color, col):
        """Crea una card con titulo y valor."""
        card = ttk.Frame(
            parent,
            bootstyle=f"{color}-secondary",
            padding=12,
        )
        card.grid(row=0, column=col, padx=5, pady=0, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        ttk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 9),
            bootstyle="secondary",
        ).pack(anchor="w")

        ttk.Label(
            card,
            text=valor,
            font=("Segoe UI", 16, "bold"),
            bootstyle=color,
        ).pack(anchor="w", pady=(2, 0))

    def _construir_notebook(self):
        """Notebook con pestanas."""
        if not self.datos:
            return

        self.notebook = ttk.Notebook(self, padding=5)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=(0, 10))

        # Pestana 1: Movimientos
        self.panel_mov = PanelMovimientos(self.notebook, self.datos)
        self.notebook.add(self.panel_mov, text="  Movimientos  ")

        # Pestana 2: Resumen por categoria
        self.panel_resumen = PanelResumen(self.notebook, self.datos)
        self.notebook.add(self.panel_resumen, text="  Resumen  ")

        # Pestana 3: Balance Mensual
        self.panel_balance = PanelBalance(self.notebook, self.datos)
        self.notebook.add(self.panel_balance, text="  Balance Mensual  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _cargar_selectores(self):
        """Carga los filtros de los paneles."""
        if not self.datos:
            return
        meses = self.datos.get_meses_disponibles()
        self.panel_mov.cargar_meses(meses)

    def _cambiar_ano(self, event=None):
        """Cambia el ano (placeholder para multi-ano)."""
        pass

    def _on_tab_change(self, event=None):
        """Actualiza graficos al cambiar de pestana."""
        tab = self.notebook.index(self.notebook.select())
        if tab == 1:  # Resumen
            self.panel_resumen.actualizar_graficos()

    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error."""
        frame = ttk.Frame(self, padding=50)
        frame.pack(expand=YES, fill=BOTH)

        ttk.Label(
            frame,
            text="Error",
            font=("Segoe UI", 18, "bold"),
            bootstyle="danger",
        ).pack()

        ttk.Label(
            frame,
            text=mensaje,
            font=("Segoe UI", 11),
        ).pack(pady=10)

        ttk.Button(
            frame,
            text="Cerrar",
            bootstyle="danger-outline",
            command=self.destroy,
            width=20,
        ).pack(pady=20)
