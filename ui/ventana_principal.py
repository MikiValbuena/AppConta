"""
Ventana principal de AppConta - Frontend 2025.
Interfaz con ttkbootstrap mostrando datos del ano 2025.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import os

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
        self.place_window_center()

        # Verificar que existe Conta.xlsx
        if not os.path.exists("Conta.xlsx"):
            self._mostrar_error("No se encontró Conta.xlsx en la carpeta del programa")
            return

        # Mostrar splash de carga
        self._mostrar_carga()

        # Cargar datos en segundo plano
        self.datos = None
        self._cargar_datos_en_hilo()

    def _mostrar_carga(self):
        """Muestra pantalla de carga mientras se migran/verifican datos."""
        self.carga_frame = ttk.Frame(self, padding=80)
        self.carga_frame.pack(expand=YES, fill=BOTH)

        ttk.Label(
            self.carga_frame,
            text="AppConta",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary",
        ).pack()

        ttk.Label(
            self.carga_frame,
            text="Contabilidad Personal",
            font=("Segoe UI", 12),
            bootstyle="secondary",
        ).pack(pady=(5, 20))

        self.progress = ttk.Progressbar(
            self.carga_frame,
            mode="indeterminate",
            bootstyle="primary-striped",
            length=300,
        )
        self.progress.pack(pady=10)
        self.progress.start(10)

        self.estado_label = ttk.Label(
            self.carga_frame,
            text="Cargando datos...",
            font=("Segoe UI", 9),
            bootstyle="secondary",
        )
        self.estado_label.pack()

    def _cargar_datos_en_hilo(self):
        """Carga los datos en un hilo separado."""
        def cargar():
            try:
                self.datos = DataLoader(ruta_excel="Conta.xlsx", hoja="2025")
                self.after(0, self._carga_completada)
            except Exception as e:
                self.after(0, lambda: self._carga_error(str(e)))

        hilo = threading.Thread(target=cargar, daemon=True)
        hilo.start()

    def _carga_completada(self):
        """Callback cuando la carga termina exitosamente."""
        if self.carga_frame:
            self.carga_frame.destroy()
            self.carga_frame = None

        self._construir_header()
        if self.datos:
            self._construir_resumen_cards()
            self._construir_notebook()
            self._cargar_selectores()

            if getattr(self.datos, 'migrado', False):
                self._mostrar_notificacion_migracion()

        self.bind("<Escape>", lambda e: self.destroy())

    def _carga_error(self, mensaje):
        """Callback cuando la carga falla."""
        if self.carga_frame:
            self.carga_frame.destroy()
            self.carga_frame = None
        self._mostrar_error(f"Error al cargar datos: {mensaje}")

    def _mostrar_notificacion_migracion(self):
        """Muestra un toast indicando que se migraron datos del Excel."""
        try:
            from ttkbootstrap.toast import ToastNotification
            toast = ToastNotification(
                title="Migración completada",
                message="Datos importados desde Conta.xlsx correctamente",
                duration=4000,
            )
            toast.show_toast()
        except Exception:
            pass

    # ─── UI ─────────────────────────────────────────────────

    def _construir_header(self):
        """Header con titulo y selector de ano."""
        header = ttk.Frame(self, padding=15)
        header.pack(fill=X)

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

        self.ano_var = tk.StringVar(value="2025")
        self.ano_combo = ttk.Combobox(
            header,
            textvariable=self.ano_var,
            values=["2025", "2024", "2023", "2022", "2021",
                    "2020", "2019", "2018", "2017", "2016"],
            state="readonly",
            width=8,
            font=("Segoe UI", 11),
            bootstyle="primary",
        )
        self.ano_combo.pack(side=RIGHT, padx=(5, 0))
        self.ano_combo.bind("<<ComboboxSelected>>", self._cambiar_ano)

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

        self._crear_card(row, "Total Ingresos",
                         f"{resumen['ingresos']:,.2f} EUR", "success", 0)
        self._crear_card(row, "Total Gastos",
                         f"{resumen['gastos']:,.2f} EUR", "danger", 1)
        balance = resumen["balance"]
        color = "success" if balance >= 0 else "danger"
        self._crear_card(row, "Balance Anual",
                         f"{balance:,.2f} EUR", color, 2)
        self._crear_card(row, "Movimientos",
                         str(resumen["total_movimientos"]), "info", 3)

    def _crear_card(self, parent, titulo, valor, color, col):
        card = ttk.Frame(parent, bootstyle=f"{color}-secondary", padding=12)
        card.grid(row=0, column=col, padx=5, pady=0, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        ttk.Label(card, text=titulo, font=("Segoe UI", 9),
                  bootstyle="secondary").pack(anchor="w")
        ttk.Label(card, text=valor, font=("Segoe UI", 16, "bold"),
                  bootstyle=color).pack(anchor="w", pady=(2, 0))

    def _construir_notebook(self):
        if not self.datos:
            return

        self.notebook = ttk.Notebook(self, padding=5)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=(0, 10))

        self.panel_mov = PanelMovimientos(self.notebook, self.datos)
        self.notebook.add(self.panel_mov, text="  Movimientos  ")

        self.panel_resumen = PanelResumen(self.notebook, self.datos)
        self.notebook.add(self.panel_resumen, text="  Resumen  ")

        self.panel_balance = PanelBalance(self.notebook, self.datos)
        self.notebook.add(self.panel_balance, text="  Balance Mensual  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _cargar_selectores(self):
        if not self.datos:
            return
        meses = self.datos.get_meses_disponibles()
        if hasattr(self, 'panel_mov') and self.panel_mov:
            self.panel_mov.cargar_meses(meses)

    def _cambiar_ano(self, event=None):
        """Cambia el ano activo y recarga los datos."""
        año = self.ano_var.get()
        try:
            self.datos.hoja_activa = año

            # Recargar pestana de movimientos
            if hasattr(self, 'panel_mov') and self.panel_mov:
                self.panel_mov._cargar_filtros()
                self.panel_mov._cargar_datos()

            # Actualizar cards
            resumen = self.datos.get_resumen_anual()
            for w in self.winfo_children():
                if isinstance(w, ttk.Frame):
                    for child in w.winfo_children():
                        if isinstance(child, ttk.Frame):
                            for label in child.winfo_children():
                                if isinstance(label, ttk.Label):
                                    txt = label.cget("text")
                                    if "EUR" in txt or txt.isdigit():
                                        pass  # Se actualizaran abajo

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar de año: {e}")

    def _on_tab_change(self, event=None):
        tab = self.notebook.index(self.notebook.select())
        if tab == 1:
            self.panel_resumen.actualizar_graficos()

    def _mostrar_error(self, mensaje):
        frame = ttk.Frame(self, padding=50)
        frame.pack(expand=YES, fill=BOTH)

        ttk.Label(frame, text="Error",
                  font=("Segoe UI", 18, "bold"),
                  bootstyle="danger").pack()

        ttk.Label(frame, text=mensaje,
                  font=("Segoe UI", 11)).pack(pady=10)

        ttk.Button(frame, text="Cerrar",
                   bootstyle="danger-outline",
                   command=self.destroy, width=20).pack(pady=20)
