-- Esquema de base de datos AppConta

CREATE TABLE IF NOT EXISTS cuentas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL DEFAULT 'corriente'
        CHECK(tipo IN ('corriente','efectivo','inversion')),
    orden INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    nivel INTEGER DEFAULT 1
        CHECK(nivel IN (1,2,3)),
    padre_id INTEGER REFERENCES categorias(id) ON DELETE CASCADE,
    UNIQUE(nombre, nivel, padre_id)
);

CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    categoria1 TEXT NOT NULL,
    categoria2 TEXT DEFAULT '',
    categoria3 TEXT DEFAULT '',
    cuenta TEXT NOT NULL,
    tipo TEXT NOT NULL
        CHECK(tipo IN ('ingreso','gasto','invertido','retorno')),
    importe REAL NOT NULL
        CHECK(importe != 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_movimientos_fecha
    ON movimientos(fecha);

CREATE INDEX IF NOT EXISTS idx_movimientos_categoria
    ON movimientos(categoria1);

CREATE INDEX IF NOT EXISTS idx_movimientos_cuenta
    ON movimientos(cuenta);

-- Vistas utiles
CREATE VIEW IF NOT EXISTS v_resumen_anual AS
SELECT
    strftime('%Y', fecha) AS año,
    tipo,
    COUNT(*) AS total_movs,
    SUM(importe) AS total_importe
FROM movimientos
GROUP BY año, tipo
ORDER BY año;

CREATE VIEW IF NOT EXISTS v_gastos_por_categoria AS
SELECT
    categoria1,
    COUNT(*) AS num_movs,
    SUM(importe) AS total_gasto
FROM movimientos
WHERE tipo = 'gasto'
GROUP BY categoria1
ORDER BY total_gasto DESC;

CREATE VIEW IF NOT EXISTS v_balance_mensual AS
SELECT
    strftime('%Y', fecha) AS año,
    CAST(strftime('%m', fecha) AS INTEGER) AS mes_num,
    CASE CAST(strftime('%m', fecha) AS INTEGER)
        WHEN 1 THEN 'Enero' WHEN 2 THEN 'Febrero'
        WHEN 3 THEN 'Marzo' WHEN 4 THEN 'Abril'
        WHEN 5 THEN 'Mayo' WHEN 6 THEN 'Junio'
        WHEN 7 THEN 'Julio' WHEN 8 THEN 'Agosto'
        WHEN 9 THEN 'Septiembre' WHEN 10 THEN 'Octubre'
        WHEN 11 THEN 'Noviembre' WHEN 12 THEN 'Diciembre'
    END AS mes,
    COALESCE(SUM(CASE WHEN tipo = 'ingreso' THEN importe END), 0) AS ingresos,
    COALESCE(SUM(CASE WHEN tipo = 'gasto' THEN importe END), 0) AS gastos,
    COALESCE(SUM(CASE WHEN tipo = 'ingreso' THEN importe END), 0) -
    COALESCE(SUM(CASE WHEN tipo = 'gasto' THEN importe END), 0) AS balance
FROM movimientos
GROUP BY año, mes_num
ORDER BY año, mes_num;
