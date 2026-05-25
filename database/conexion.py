"""
Gestor de base de datos SQLite.
Maneja conexion, esquema, y operaciones CRUD de movimientos.
"""

import sqlite3
import os
from datetime import datetime, date


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "AppConta.db")


class DatabaseManager:
    """Singleton para gestionar la base de datos."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conexion = None
        return cls._instance

    @property
    def conexion(self):
        if self._conexion is None:
            self._conectar()
        return self._conexion

    def _conectar(self):
        """Abre conexion y crea esquema si no existe."""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._conexion = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._conexion.row_factory = sqlite3.Row
        self._conexion.execute("PRAGMA journal_mode=WAL")
        self._conexion.execute("PRAGMA foreign_keys=ON")
        self._crear_esquema()

    def _crear_esquema(self):
        """Ejecuta el schema.sql."""
        schema_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "schema.sql"
        )
        with open(schema_path, "r", encoding="utf-8") as f:
            self._conexion.executescript(f.read())
        self._conexion.commit()

    def cerrar(self):
        if self._conexion:
            self._conexion.close()
            self._conexion = None

    # ─── CRUD Movimientos ──────────────────────────────────────

    def insertar_movimiento(self, fecha, categoria1, importe,
                            categoria2="", categoria3="",
                            cuenta="Efectivo", tipo="gasto"):
        """Inserta un nuevo movimiento."""
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        if isinstance(fecha, date):
            fecha = fecha.isoformat()

        cursor = self.conexion.execute(
            """INSERT INTO movimientos
               (fecha, categoria1, categoria2, categoria3, cuenta, tipo, importe)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (fecha, categoria1, categoria2, categoria3, cuenta, tipo, importe)
        )
        self.conexion.commit()
        return cursor.lastrowid

    def actualizar_movimiento(self, id_mov, fecha, categoria1, importe,
                               categoria2="", categoria3="",
                               cuenta="Efectivo", tipo="gasto"):
        """Actualiza un movimiento existente."""
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        if isinstance(fecha, date):
            fecha = fecha.isoformat()

        self.conexion.execute(
            """UPDATE movimientos SET
               fecha=?, categoria1=?, categoria2=?, categoria3=?,
               cuenta=?, tipo=?, importe=?,
               updated_at=CURRENT_TIMESTAMP
               WHERE id=?""",
            (fecha, categoria1, categoria2, categoria3,
             cuenta, tipo, importe, id_mov)
        )
        self.conexion.commit()
        return self.conexion.total_changes > 0

    def eliminar_movimiento(self, id_mov):
        """Elimina un movimiento por ID."""
        self.conexion.execute("DELETE FROM movimientos WHERE id=?", (id_mov,))
        self.conexion.commit()
        return self.conexion.total_changes > 0

    def obtener_movimiento(self, id_mov):
        """Obtiene un movimiento por ID."""
        cur = self.conexion.execute(
            "SELECT * FROM movimientos WHERE id=?", (id_mov,)
        )
        row = cur.fetchone()
        if row:
            return dict(row)
        return None

    def listar_movimientos(self, año=None, mes=None, categoria=None,
                           cuenta=None, tipo=None, limite=1000):
        """Lista movimientos con filtros opcionales."""
        sql = "SELECT * FROM movimientos WHERE 1=1"
        params = []

        if año:
            sql += " AND strftime('%Y', fecha) = ?"
            params.append(str(año))
        if mes:
            sql += " AND CAST(strftime('%m', fecha) AS INTEGER) = ?"
            params.append(int(mes))
        if categoria:
            sql += " AND categoria1 = ?"
            params.append(categoria)
        if cuenta:
            sql += " AND cuenta = ?"
            params.append(cuenta)
        if tipo:
            sql += " AND tipo = ?"
            params.append(tipo)

        sql += " ORDER BY fecha DESC, id DESC LIMIT ?"
        params.append(limite)

        cur = self.conexion.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]

    # ─── Consultas agregadas ──────────────────────────────────

    def total_ingresos(self, año=None):
        """Suma total de ingresos."""
        sql = "SELECT COALESCE(SUM(importe),0) FROM movimientos WHERE tipo='ingreso'"
        params = []
        if año:
            sql += " AND strftime('%Y',fecha)=?"
            params.append(str(año))
        return self.conexion.execute(sql, params).fetchone()[0]

    def total_gastos(self, año=None):
        """Suma total de gastos."""
        sql = "SELECT COALESCE(SUM(importe),0) FROM movimientos WHERE tipo='gasto'"
        params = []
        if año:
            sql += " AND strftime('%Y',fecha)=?"
            params.append(str(año))
        return self.conexion.execute(sql, params).fetchone()[0]

    def contar_movimientos(self, año=None):
        """Numero total de movimientos."""
        sql = "SELECT COUNT(*) FROM movimientos WHERE 1=1"
        params = []
        if año:
            sql += " AND strftime('%Y',fecha)=?"
            params.append(str(año))
        return self.conexion.execute(sql, params).fetchone()[0]

    def gastos_por_categoria(self, año=None):
        """Gastos agrupados por categoria."""
        sql = """SELECT categoria1, SUM(importe) as total
                 FROM movimientos WHERE tipo='gasto'"""
        params = []
        if año:
            sql += " AND strftime('%Y',fecha)=?"
            params.append(str(año))
        sql += " GROUP BY categoria1 ORDER BY total DESC"
        cur = self.conexion.execute(sql, params)
        return {r["categoria1"]: r["total"] for r in cur.fetchall()}

    def ingresos_por_categoria(self, año=None):
        """Ingresos agrupados por categoria."""
        sql = """SELECT categoria1, SUM(importe) as total
                 FROM movimientos WHERE tipo='ingreso'"""
        params = []
        if año:
            sql += " AND strftime('%Y',fecha)=?"
            params.append(str(año))
        sql += " GROUP BY categoria1 ORDER BY total DESC"
        cur = self.conexion.execute(sql, params)
        return {r["categoria1"]: r["total"] for r in cur.fetchall()}

    def balance_mensual(self, año=None):
        """Balance por mes."""
        sql = """SELECT
                   CAST(strftime('%m', fecha) AS INTEGER) as mes_num,
                   COALESCE(SUM(CASE WHEN tipo='ingreso' THEN importe END),0) as ingresos,
                   COALESCE(SUM(CASE WHEN tipo='gasto' THEN importe END),0) as gastos
                 FROM movimientos WHERE 1=1"""
        params = []
        if año:
            sql += " AND strftime('%Y',fecha)=?"
            params.append(str(año))
        sql += " GROUP BY mes_num ORDER BY mes_num"
        cur = self.conexion.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]

    def categorias_distinct(self, nivel=1):
        """Lista de categorias distintas."""
        col = f"categoria{nivel}"
        cur = self.conexion.execute(
            f"SELECT DISTINCT {col} FROM movimientos WHERE {col} != '' ORDER BY {col}"
        )
        return [r[0] for r in cur.fetchall()]

    def cuentas_distinct(self):
        """Lista de cuentas distintas."""
        cur = self.conexion.execute(
            "SELECT DISTINCT cuenta FROM movimientos ORDER BY cuenta"
        )
        return [r[0] for r in cur.fetchall()]
