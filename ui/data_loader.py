"""
Carga de datos para el frontend.
Usa SQLite con migracion automatica desde Conta.xlsx.
"""

from database.conexion import DatabaseManager
from database.migrador import Migrador
import threading


class DataLoader:
    """Provee datos al frontend desde SQLite."""

    def __init__(self, ruta_excel="Conta.xlsx", hoja="2025"):
        self.ruta_excel = ruta_excel
        self.hoja_activa = hoja
        self.db = DatabaseManager()
        self.migrado = False
        self._migrar_si_necesario()

    def _migrar_si_necesario(self):
        """Migra datos del Excel si la BD esta vacia."""
        migrador = Migrador(self.ruta_excel)
        if migrador.necesita_migracion():
            total = migrador.ejecutar()
            self.migrado = True
        else:
            self.migrado = False

    @property
    def categorias(self):
        return set(self.db.categorias_distinct(1))

    @property
    def subcategorias(self):
        return set(self.db.categorias_distinct(2))

    @property
    def cuentas(self):
        return {
            "OpenBank Principal": {},
            "OpenBank Socu": {},
            "Efectivo": {},
            "IBKR": {},
            "Degiro": {},
        }

    def get_movimientos(self, mes=None, categoria=None):
        """Obtiene movimientos con filtros."""
        año = int(self.hoja_activa)
        return self.db.listar_movimientos(año=año, mes=mes, categoria=categoria)

    def get_gasto_por_categoria(self):
        """Gastos agrupados por categoria."""
        return self.db.gastos_por_categoria(año=int(self.hoja_activa))

    def get_ingreso_por_categoria(self):
        """Ingresos agrupados por categoria."""
        return self.db.ingresos_por_categoria(año=int(self.hoja_activa))

    def get_resumen_anual(self):
        """Resumen anual."""
        año = int(self.hoja_activa)
        return {
            "ingresos": self.db.total_ingresos(año=año),
            "gastos": self.db.total_gastos(año=año),
            "balance": self.db.total_ingresos(año=año) - self.db.total_gastos(año=año),
            "total_movimientos": self.db.contar_movimientos(año=año),
        }

    def get_meses_disponibles(self):
        """Meses con datos."""
        año = int(self.hoja_activa)
        balance = self.db.balance_mensual(año=año)
        return [m["mes_num"] for m in balance]

    @staticmethod
    def nombre_mes(numero):
        nombres = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
        }
        return nombres.get(numero, f"Mes {numero}")
