---
title: Informe de Análisis - AppConta
date: 2026-05-25
version: 1.0
---

# 📋 Informe Completo: Análisis de Conta.xlsx y Plan de Desarrollo

## 1. Estructura General del Archivo

| Aspecto | Valor |
|---------|-------|
| **Total hojas** | 15 |
| **Total fórmulas** | 4.224 |
| **Total celdas** | ~119.000 |
| **Rango de años** | 2016 – 2026 (10 años de datos) |

### Hojas encontradas

| Hoja | Filas | Fórmulas | Propósito |
|------|-------|----------|-----------|
| **2026** | 307 | 550 | Año actual en curso |
| **2025** | 683 | 546 | Año anterior |
| **2024** | 624 | 371 | Histórico |
| **2023** | 704 | 278 | Histórico |
| **2022** | 973 | 282 | Histórico |
| **2021** | 737 | 240 | Histórico |
| **2020** | 582 | 281 | Histórico |
| **2019** | 708 | 281 | Histórico |
| **2018** | 683 | 281 | Histórico |
| **2017** | 623 | 281 | Histórico |
| **2016** | 184 | 86 | Histórico |
| **Acciones** | 39 | 96 | Cartera de inversión (IBKR + Degiro) |
| **Préstamos** | 85 | 74 | Préstamos personales |
| **AnualGlobal** | 59 | 492 | Consolidación anual multi-cuenta |
| **PrestCompletos** | 76 | 85 | Amortización hipotecaria detallada |

---

## 2. Estructura de Columnas (Hoja de cada año)

```
B: Año
C: Mes
D: Fecha
E: Categoría 1 (Cat.1)  → 23 categorías
F: Categoría 2 (Cat.2)  → 44 subcategorías
G: Categoría 3 (Cat.3)  → Detalle adicional

CUENTAS BANCARIAS:
  H: Ingreso  | I: Gasto   → OpenBank Principal
  J: Ingreso  | K: Gasto   → OpenBank Socuéllamos
  L: Ingreso  | M: Gasto   → Efectivo
  N: Invertido| O: Retorno → Interactive Broker (acciones)
  P: Invertido| Q: Retorno → Degiro (acciones)

INFORMACIÓN:
  R-S: Número de cuenta / tarjeta
```

### Categorías principales (23)

| Categoría | Tipo | Ejemplos de subcategorías |
|-----------|------|---------------------------|
| Caza | Gasto | Cartuchos, Licencia, Seguro, Desayuno |
| Hogar | Gasto | Consumibles, Higiene, Ferretería, Zapatería |
| Impuestos | Gasto | IRPF, Autónomos |
| Informática | Gasto | PC Casa, Hosting |
| Inversión Acciones | Inversión | Compra/Venta valores |
| Lotería | Gasto | Navidad, Primitiva |
| Ocio | Gasto | Restaurantes, Bares, Copas, Cine |
| Otros | Gasto | Limosna, Varios |
| Piso Madrid | Gasto | Alquiler, Suministros, Comunidad |
| Piso Socuéllamos | Gasto | Hipoteca, Comunidad, Electricidad, Gas, Agua |
| Regalos | Gasto | Cumpleaños, Navidad, Anita |
| Retornos | Ingreso | Devoluciones, Reembolsos |
| Salud | Gasto | Asisa, Farmacia, Seguro |
| Semana Santa | Gasto | Viajes, Comidas |
| Telefonía | Gasto | Móvil, Internet |
| Trabajo | Ingreso | Nómina |
| Vacaciones | Gasto | Viajes, Alojamiento |
| Vehículos | Gasto | Combustible, Mantenimiento, Parking, Seguro |
| Yeguada Trimena | Gasto | Manutención, Veterinario |
| Efectivo | Movimiento | Retiradas/Ingresos de efectivo |
| Balance Año | Control | Saldo anual |
| Total Gasto Año | Control | Sumatorio anual |
| Total Ingreso Año | Control | Sumatorio anual |

### Subcategorías principales (44)

`Alquiler` · `Restaurantes` · `Combustible` · `Consumibles` · `Comunidad` · `Nómina` · `Suministros` · `Farmacia` · `Mantenimiento` · `Bares` · `Móvil` · `Seguros` · `Hipoteca` · `Cuota` · `IRPF` · `Navidad` · `Anita` · `Asisa` · `Basuras` · `Chinos` · `Comida` · `Garaje Perseo` · `Gimnasio` · `Hermandades` · `Higiene` · `IBKR Cta-1/2/3` · `JHS Jesús Nazareno` · `Jarandilla` · `Juli` · `Libros` · `Limosna` · `Manjavacas` · `Milla` · `Mota` · `Pablo` · `Pepe Roji` · `Picazo` · `Primitiva` · `Rancho` · `Semana Santa` · `Tintorería` · `Triumph_5060MDM` · `Vehículos`

---

## 3. Tipos de Fórmulas

| Tipo | Veces | Uso |
|------|-------|-----|
| `=SUM(...)` | 920 | Sumas de ingresos/gastos mensuales y anuales |
| `=COUNTA(...)` | 526 | Conteo de movimientos |
| `=CONCATENATE(...)` | 52 | Descripciones compuestas |
| `=AVERAGE(...)` | 6 | Promedios mensuales |
| Referencias directas `=Hoja!Celda` | 2.645 | Arrastre de saldos entre años |

**Patrón clave:** Cada año referencia al anterior para arrastrar el saldo final.
Ejemplo: `'2026'!D4 = '2025'!D680`

---

## 4. Funcionalidades que la App debe Reemplazar

### 🟢 Módulo 1: Libro Diario / Registro de Movimientos
- Añadir transacciones con: **Fecha, Categoría 1, Categoría 2, Categoría 3, Importe**
- Asignar automáticamente a la cuenta bancaria correspondiente
- Diferenciar **Ingreso** vs **Gasto** vs **Invertido** vs **Retorno**

### 🟢 Módulo 2: Múltiples Cuentas
- OpenBank Principal
- OpenBank Socuéllamos
- Efectivo
- Interactive Broker (con tracking Invertido/Retorno)
- Degiro (con tracking Invertido/Retorno)
- CCM / Santander (cuentas históricas)
- Saldo consolidado automático

### 🟢 Módulo 3: Balance Mensual por Cuenta
- Total Ingresos del mes por cuenta
- Total Gastos del mes por cuenta
- Balance = Ingresos - Gastos
- Saldo final = Saldo anterior + Balance

### 🟢 Módulo 4: Cierre Anual
- Totales anuales por cuenta
- Balance anual consolidado
- Arrastre automático de saldo al año siguiente

### 🟢 Módulo 5: Categorización y Reportes
- Resumen por categoría
- Promedios mensuales
- Comparativa entre años
- Gráficos de gastos por categoría

### 🟢 Módulo 6: Gestión de Préstamos
- Préstamos personales (Aníbal, Anita, Eva, Memé, Juan Manuel)
- Amortización hipotecaria con desglose Capital + Intereses
- Calendario de pagos

### 🟢 Módulo 7: Cartera de Acciones
- Seguimiento de compra/venta (Interactive Broker + Degiro)
- Cálculo de beneficios/pérdidas
- IRPF y comisiones

### 🟢 Módulo 8: Consolidación Anual Global
- Vista multi-anual de todas las cuentas
- Comparativa año contra año
- Dashboard resumen

---

## 5. Stack Tecnológico Recomendado

### 🏆 Opción 1: Python + ttkbootstrap + SQLite + PyInstaller (RECOMENDADA)

| Componente | Tecnología | Propósito |
|-----------|-----------|-----------|
| **Lenguaje** | Python 3.12+ | Portable, fácil, ideal para contabilidad |
| **UI Desktop** | `ttkbootstrap` (Tkinter moderno) | Tema visual profesional, nativo Windows |
| **Base de datos** | SQLite (vía `sqlite3`) | Un solo archivo `.db`, sin servidor |
| **Gráficos** | `matplotlib` | Reportes visuales por categoría |
| **Importación** | `openpyxl` | Migrar datos del Excel actual |
| **Exportación** | `fpdf2` / `openpyxl` | Informes PDF o Excel |
| **Empaquetado** | `PyInstaller` | Genera un solo `.exe` portable |

**Ventajas:**
- ✅ **Portable**: Un solo `.exe` + archivo `.db` = todo el sistema
- ✅ **Sin instalación**: No requiere runtime ni dependencias externas
- ✅ **Funciona en Windows 10 y 11**
- ✅ **Código abierto, gratuito, fácil de mantener**

### 🥈 Opción 2: C# .NET 8 + WinForms (Alternativa)

| Componente | Tecnología |
|-----------|-----------|
| Lenguaje | C# .NET 8 |
| UI | WinForms o WPF |
| BD | SQLite (`Microsoft.Data.Sqlite`) |
| Empaquetado | Self-contained deployment |

**Ventajas:** Mejor integración con Windows.
**Desventajas:** Más complejo, requiere Visual Studio, mayor curva de aprendizaje.

### ❌ Opciones Descartadas

| Tecnología | Motivo |
|-----------|--------|
| **Electron / Tauri** | Demasiado pesado para app de escritorio simple |
| **Java** | Requiere JRE, no es portable |
| **Access / VBA** | Obsoleto, no es portable |
| **PHP + servidor** | No es desktop, requiere servidor |
| **Node.js + NW.js** | Pesado, sobrecomplejidad |

---

## 6. Programas y Requisitos a Instalar

### 🖥️ Para DESARROLLO

| Programa | Versión | Descarga |
|----------|---------|----------|
| **Python** | 3.12.x | https://python.org |
| **Git** | Última | https://git-scm.com (opcional) |
| **VS Code** | Última | https://code.visualstudio.com (opcional) |

### 📦 Paquetes Python (vía pip)

```bash
pip install ttkbootstrap       # UI moderna con temas
pip install matplotlib         # Gráficos y reportes visuales
pip install openpyxl           # Importar datos del Excel
pip install fpdf2              # Exportar informes PDF
pip install pyinstaller        # Empaquetar a .exe portable
```

### 📦 Para el USUARIO FINAL

**Ninguno.** El `.exe` generado con PyInstaller es 100% portable:
- No requiere instalar Python
- No requiere instalar librerías
- Funciona en Windows 10 y 11 (64-bit)
- Se puede ejecutar desde USB

---

## 7. Arquitectura Propuesta

```
AppConta/
├── main.py                    # Punto de entrada
├── database/
│   ├── schema.sql             # Esquema SQLite
│   ├── conexion.py            # Gestión de conexión BD
│   └── migrador.py            # Importación desde Excel
├── models/
│   ├── movimiento.py          # Transacciones
│   ├── cuenta.py              # Cuentas bancarias
│   ├── categoria.py           # Categorías y subcategorías
│   ├── prestamo.py            # Préstamos
│   └── accion.py              # Cartera de acciones
├── ui/
│   ├── ventana_principal.py   # Dashboard general
│   ├── registro.py            # Alta de movimientos
│   ├── balance_mensual.py     # Balance por mes/cuenta
│   ├── reportes.py            # Reportes y gráficos
│   ├── prestamos.py           # Gestión de préstamos
│   ├── acciones.py            # Cartera de acciones
│   └── anual.py               # Consolidación anual
├── utils/
│   ├── calculos.py            # Fórmulas y balances
│   └── exportar.py            # Exportación a Excel/PDF
├── data/
│   └── AppConta.db            # Base de datos SQLite
└── assets/
    └── icono.ico              # Icono de la aplicación
```

### Esquema de Base de Datos (SQLite)

```sql
-- Cuentas bancarias
CREATE TABLE cuentas (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('corriente','efectivo','inversion')),
    saldo_inicial REAL DEFAULT 0
);

-- Categorías
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    nivel INTEGER DEFAULT 1,
    padre_id INTEGER REFERENCES categorias(id)
);

-- Movimientos (corazón de la app)
CREATE TABLE movimientos (
    id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    categoria1_id INTEGER REFERENCES categorias(id),
    categoria2_id INTEGER REFERENCES categorias(id),
    categoria3_id INTEGER REFERENCES categorias(id),
    concepto TEXT,
    cuenta_id INTEGER REFERENCES cuentas(id),
    tipo TEXT CHECK(tipo IN ('ingreso','gasto','invertido','retorno')),
    importe REAL NOT NULL,
    año INTEGER GENERATED ALWAYS AS (strftime('%Y', fecha)) STORED,
    mes INTEGER GENERATED ALWAYS AS (strftime('%m', fecha)) STORED
);

-- Préstamos
CREATE TABLE prestamos (
    id INTEGER PRIMARY KEY,
    persona TEXT NOT NULL,
    concepto TEXT,
    importe_total REAL,
    fecha DATE
);

CREATE TABLE pagos_prestamo (
    id INTEGER PRIMARY KEY,
    prestamo_id INTEGER REFERENCES prestamos(id),
    fecha DATE,
    importe REAL,
    tipo TEXT CHECK(tipo IN ('capital','interes'))
);

-- Cartera de acciones
CREATE TABLE operaciones_acciones (
    id INTEGER PRIMARY KEY,
    broker TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('compra','venta')),
    fecha DATE,
    ticker TEXT,
    cantidad INTEGER,
    precio REAL,
    comision REAL
);
```

---

## 8. Plan de Desarrollo y Tiempos

| Fase | Duración | Entregable |
|------|----------|------------|
| **Fase 1** - Migración de datos Excel → SQLite | 2 días | Script que importa todo el Excel |
| **Fase 2** - UI base + formulario de registro | 4 días | Pantalla principal + alta de movimientos |
| **Fase 3** - Balances mensuales por cuenta | 3 días | Vista de balance por cuenta y mes |
| **Fase 4** - Reportes y gráficos | 3 días | Dashboard con gráficos por categoría |
| **Fase 5** - Cierre anual automático | 2 días | Cálculo anual y arrastre de saldos |
| **Fase 6** - Gestión de préstamos | 2 días | Préstamos personales + hipoteca |
| **Fase 7** - Cartera de acciones | 2 días | Seguimiento IBKR + Degiro |
| **Fase 8** - Consolidación AnualGlobal | 2 días | Vista multi-anual |
| **Fase 9** - Empaquetado .exe portable | 1 día | PyInstaller → AppConta.exe |
| **Total** | **~21 días** | App completa portable |

---

## 9. Conclusión

**Stack elegido:** Python + ttkbootstrap + SQLite + PyInstaller

### ¿Por qué?
1. **Portabilidad real**: Un solo .exe que funciona en Windows 10/11 sin instalar nada
2. **Complejidad ajustada**: Las 4.224 fórmulas del Excel son en su mayoría SUM y arrastres → SQLite lo simplifica drásticamente
3. **Migración directa**: openpyxl permite importar los 10 años de datos existentes
4. **Sin dependencias**: PyInstaller empaqueta todo en un .exe autónomo
5. **Evolutivo**: Si en el futuro se necesita multi-dispositivo, se puede extender con Django

### Resumen de requisitos

| Para | Qué instalar |
|------|-------------|
| **Desarrollar** | Python 3.12 + `pip install ttkbootstrap matplotlib openpyxl fpdf2 pyinstaller` |
| **Usar la app** | Nada. Solo ejecutar `AppConta.exe` |

---

*Documento generado el 25 de mayo de 2026 tras análisis automatizado de Conta.xlsx*
