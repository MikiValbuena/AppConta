"""
Panel de resumen - Graficos y tabla por categoria.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from collections import defaultdict
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Configurar fuente para graficos
plt.rcParams["font.family"] = "Segoe UI"
plt.rcParams["font.size"] = 9


class PanelResumen(ttk.Frame):
    """Resumen de gastos/ingresos por categoria con graficos."""

    def __init__(self, parent, datos):
        super().__init__(parent)
        self.datos = datos
        self._construir()

    def _construir(self):
        # Panel izquierdo: Tabla de categorias
        left = ttk.Frame(self, padding=10)
        left.pack(side=LEFT, fill=BOTH, expand=YES)

        ttk.Label(left, text="Gastos por Categoria", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        # Frame contenedor para la tabla con scroll
        frame_tabla = ttk.Frame(left)
        frame_tabla.pack(fill=BOTH, expand=YES, pady=(5, 0))

        scroll = ttk.Scrollbar(frame_tabla, orient=VERTICAL)

        self.tabla_cats = ttk.Treeview(
            frame_tabla,
            columns=("Categoria", "Total", "%"),
            show="headings",
            yscrollcommand=scroll.set,
            bootstyle="primary",
            height=18,
        )
        scroll.config(command=self.tabla_cats.yview)

        self.tabla_cats.heading("Categoria", text="Categoria")
        self.tabla_cats.heading("Total", text="Total")
        self.tabla_cats.heading("%", text="% del Total")

        self.tabla_cats.column("Categoria", width=180)
        self.tabla_cats.column("Total", width=120, anchor="e")
        self.tabla_cats.column("%", width=100, anchor="e")

        self.tabla_cats.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)

        # Panel derecho: Grafico
        right = ttk.Frame(self, padding=10)
        right.pack(side=RIGHT, fill=BOTH, expand=YES)

        ttk.Label(right, text="Distribucion de Gastos", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        # Crear figura de matplotlib
        self.fig = Figure(figsize=(5, 4), dpi=100, tight_layout=True)
        self.fig.patch.set_facecolor("#f8f9fa")

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#f8f9fa")

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES, pady=(5, 0))

        # Checkbox para ingresos/gastos
        bottom = ttk.Frame(right)
        bottom.pack(fill=X, pady=(5, 0))

        self.tipo_grafico = ttk.StringVar(value="gastos")
        ttk.Radiobutton(bottom, text="Gastos", variable=self.tipo_grafico,
                        value="gastos", command=self._toggle_grafico).pack(side=LEFT, padx=5)
        ttk.Radiobutton(bottom, text="Ingresos", variable=self.tipo_grafico,
                        value="ingresos", command=self._toggle_grafico).pack(side=LEFT, padx=5)

        # Cargar datos
        self._cargar_tabla()
        self._dibujar_grafico()

    def _cargar_tabla(self):
        """Carga los gastos por categoria en la tabla."""
        gastos = self.datos.get_gasto_por_categoria()
        total = sum(gastos.values())

        for item in self.tabla_cats.get_children():
            self.tabla_cats.delete(item)

        for cat, importe in gastos.items():
            pct = (importe / total * 100) if total > 0 else 0
            self.tabla_cats.insert("", END, values=(
                cat,
                f"{importe:,.2f} €",
                f"{pct:.1f}%",
            ))

    def _dibujar_grafico(self):
        """Dibuja el grafico de torta."""
        self.ax.clear()

        if self.tipo_grafico.get() == "gastos":
            datos = self.datos.get_gasto_por_categoria()
            titulo = "Distribucion de Gastos"
        else:
            datos = self.datos.get_ingreso_por_categoria()
            titulo = "Distribucion de Ingresos"

        if not datos:
            self.ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")
            self.canvas.draw()
            return

        # Colores
        colores = ["#FF6B35", "#0078D4", "#4CAF50", "#E53935", "#FFC107",
                    "#9C27B0", "#00BCD4", "#FF9800", "#795548", "#607D8B",
                    "#F44336", "#2196F3", "#4CAF50", "#FFEB3B", "#9E9E9E"]

        labels = list(datos.keys())
        values = list(datos.values())

        # Si hay muchas categorias, agrupar las pequenas
        if len(labels) > 8:
            otros = sum(values[7:])
            labels = labels[:7] + ["Otros"]
            values = values[:7] + [otros]

        wedges, texts, autotexts = self.ax.pie(
            values,
            labels=None,
            autopct="%1.1f%%",
            startangle=90,
            colors=colores[:len(labels)],
            textprops={"fontsize": 8},
        )

        # Leyenda
        self.ax.legend(
            wedges, [f"{l} ({v:,.0f}€)" for l, v in zip(labels, values)],
            title=titulo,
            loc="center left",
            bbox_to_anchor=(-0.3, 0, 0.5, 1),
            fontsize=7,
        )

        self.ax.set_title(titulo, fontsize=10, pad=10)
        self.canvas.draw()

    def _toggle_grafico(self):
        """Cambia entre grafico de gastos e ingresos."""
        self._dibujar_grafico()

    def actualizar_graficos(self):
        """Actualiza los graficos (llamado al cambiar de pestana)."""
        self._dibujar_grafico()
