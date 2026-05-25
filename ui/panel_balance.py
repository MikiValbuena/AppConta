"""
Panel de balance mensual - Tabla y grafico de evolucion mensual.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from collections import defaultdict
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Segoe UI"
plt.rcParams["font.size"] = 9


class PanelBalance(ttk.Frame):
    """Balance mensual con tabla y grafico de barras."""

    def __init__(self, parent, datos):
        super().__init__(parent)
        self.datos = datos
        self._construir()

    def _construir(self):
        # Panel izquierdo: Tabla de balance mensual
        left = ttk.Frame(self, padding=10)
        left.pack(side=LEFT, fill=BOTH, expand=YES)

        ttk.Label(left, text="Balance Mensual", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        frame_tabla = ttk.Frame(left)
        frame_tabla.pack(fill=BOTH, expand=YES, pady=(5, 0))

        scroll = ttk.Scrollbar(frame_tabla, orient=VERTICAL)

        columnas = ("Mes", "Ingresos", "Gastos", "Balance")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scroll.set,
            bootstyle="primary",
            height=18,
        )
        scroll.config(command=self.tabla.yview)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="e" if col != "Mes" else "w")

        self.tabla.pack(side=LEFT, fill=BOTH, expand=YES)
        scroll.pack(side=RIGHT, fill=Y)

        # Tags de color para balance
        self.tabla.tag_configure("positivo", foreground="#28a745")
        self.tabla.tag_configure("negativo", foreground="#dc3545")

        # Panel derecho: Grafico
        right = ttk.Frame(self, padding=10)
        right.pack(side=RIGHT, fill=BOTH, expand=YES)

        ttk.Label(right, text="Evolucion Mensual", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.fig = Figure(figsize=(5, 4), dpi=100, tight_layout=True)
        self.fig.patch.set_facecolor("#f8f9fa")

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#f8f9fa")

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES, pady=(5, 0))

        # Selector de cuenta
        bottom = ttk.Frame(right)
        bottom.pack(fill=X, pady=(5, 0))

        ttk.Label(bottom, text="Cuenta:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(0, 5))

        self.cuenta_var = ttk.StringVar(value="Todas")
        cuentas = ["Todas"] + list(self.datos.cuentas.keys())
        self.cuenta_combo = ttk.Combobox(
            bottom, textvariable=self.cuenta_var,
            values=cuentas, state="readonly",
            width=20, font=("Segoe UI", 9),
        )
        self.cuenta_combo.pack(side=LEFT)
        self.cuenta_combo.bind("<<ComboboxSelected>>", self._actualizar_vista)

        # Cargar datos
        self._cargar_tabla()
        self._dibujar_grafico()

    def _calcular_balance_mensual_por_cuenta(self, cuenta=None):
        """Calcula ingresos, gastos y balance por mes."""
        meses = defaultdict(lambda: {"ingresos": 0, "gastos": 0})

        for m in self.datos.movimientos:
            if cuenta and cuenta != "Todas" and m["cuenta"] != cuenta:
                continue
            if not isinstance(m["fecha"], datetime):
                continue

            mes = f"{m['fecha'].year}-{m['fecha'].month:02d}"

            if m["tipo"] == "ingreso":
                meses[mes]["ingresos"] += m["importe"]
            else:
                meses[mes]["gastos"] += m["importe"]

        # Ordenar por mes
        return dict(sorted(meses.items()))

    def _cargar_tabla(self):
        """Carga la tabla de balance mensual."""
        cuenta = self.cuenta_var.get()
        datos_meses = self._calcular_balance_mensual_por_cuenta(cuenta)

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        total_ing = 0
        total_gas = 0

        for mes, datos in datos_meses.items():
            balance = datos["ingresos"] - datos["gastos"]
            tag = "positivo" if balance >= 0 else "negativo"

            # Convertir mes clave a nombre
            try:
                ano, num = mes.split("-")
                num = int(num)
                nombres = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
                          7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
                nombre_mes = f"{nombres[num]} {ano}"
            except:
                nombre_mes = mes

            self.tabla.insert("", END, values=(
                nombre_mes,
                f"{datos['ingresos']:,.2f} €",
                f"{datos['gastos']:,.2f} €",
                f"{balance:,.2f} €",
            ), tags=(tag,))

            total_ing += datos["ingresos"]
            total_gas += datos["gastos"]

        # Fila de total
        bal_total = total_ing - total_gas
        tag_total = "positivo" if bal_total >= 0 else "negativo"
        self.tabla.insert("", END, values=(
            "TOTAL",
            f"{total_ing:,.2f} €",
            f"{total_gas:,.2f} €",
            f"{bal_total:,.2f} €",
        ), tags=("positivo" if bal_total >= 0 else "negativo",))

    def _dibujar_grafico(self):
        """Dibuja el grafico de barras de evolucion mensual."""
        self.ax.clear()

        cuenta = self.cuenta_var.get()
        datos_meses = self._calcular_balance_mensual_por_cuenta(cuenta)

        if not datos_meses:
            self.ax.text(0.5, 0.5, "Sin datos", ha="center", va="center")
            self.canvas.draw()
            return

        meses = list(datos_meses.keys())
        ingresos = [d["ingresos"] for d in datos_meses.values()]
        gastos = [d["gastos"] for d in datos_meses.values()]
        balances = [i - g for i, g in zip(ingresos, gastos)]

        # Etiquetas de meses abreviadas
        nombres_mes = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
                      7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
        labels = []
        for m in meses:
            try:
                _, num = m.split("-")
                labels.append(nombres_mes.get(int(num), m))
            except:
                labels.append(m)

        x = range(len(meses))
        width = 0.25

        # Barras
        bars1 = self.ax.bar([i - width for i in x], ingresos, width,
                           label="Ingresos", color="#28a745", alpha=0.8)
        bars2 = self.ax.bar([i for i in x], gastos, width,
                           label="Gastos", color="#dc3545", alpha=0.8)
        bars3 = self.ax.bar([i + width for i in x], balances, width,
                           label="Balance", color="#0078D4", alpha=0.8)

        self.ax.set_xlabel("Mes", fontsize=9)
        self.ax.set_ylabel("Importe (€)", fontsize=9)

        titulo = "Evolucion Mensual"
        if cuenta and cuenta != "Todas":
            titulo += f" - {cuenta}"
        self.ax.set_title(titulo, fontsize=10)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels, fontsize=8)
        self.ax.legend(fontsize=8)
        self.ax.axhline(y=0, color="gray", linewidth=0.5)
        self.ax.grid(axis="y", alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def _actualizar_vista(self, event=None):
        """Actualiza tabla y grafico al cambiar cuenta."""
        self._cargar_tabla()
        self._dibujar_grafico()
