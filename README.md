# AppConta 📊

**Aplicación de contabilidad personal portable para Windows.**

AppConta nace de la necesidad de reemplazar un archivo Excel con más de 10 años de datos financieros (2016-2026), 4.224 fórmulas y 15 hojas de cálculo por una aplicación de escritorio moderna, portable y sin dependencias.

---

## 🎯 Objetivo

Desarrollar una aplicación de escritorio **portable** para Windows 10/11 que replicate toda la operatividad del Excel de contabilidad personal, permitiendo al usuario final **dejar de usar Excel** para siempre.

### Funcionalidades clave

- **Registro de movimientos** con categorización multinivel (Cat1 → Cat2 → Cat3)
- **Múltiples cuentas**: OpenBank, Efectivo, Interactive Broker, Degiro
- **Balance mensual** consolidado por cuenta y global
- **Cierre anual** automático con arrastre de saldos
- **Reportes y gráficos** por categoría y periodo
- **Gestión de préstamos** personales e hipotecarios
- **Cartera de acciones** con cálculo de beneficios/IRPF
- **Consolidación anual global** multi-ejercicio

---

## 🏗️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Lenguaje** | Python 3.12+ |
| **UI Desktop** | ttkbootstrap (Tkinter moderno) |
| **Base de datos** | SQLite |
| **Gráficos** | matplotlib |
| **Importación Excel** | openpyxl |
| **Empaquetado** | PyInstaller (`.exe` portable) |

**Requisitos de instalación:** Ninguno para el usuario final. Solo ejecutar `AppConta.exe`.

---

## 🧠 Sistema Multi-Agente

Este proyecto se desarrolla con un sistema de **agentes IA** que orquestan el flujo de trabajo:

| Agente | Rol | Modelo |
|--------|-----|--------|
| `@gestor` | Orquestador principal | Big Pickle |
| `@especialista-windows` | Experto en Windows/WSL | DeepSeek V4 Flash Free |
| `@especialista-docker` | Experto en Docker | DeepSeek V4 Flash Free |
| `@programador` | Implementa el código | DeepSeek V4 Flash Free |
| `@revisor` | Revisa calidad del código | Big Pickle |

### Skills instalados

| Skill | Propósito |
|-------|-----------|
| `excel-automation` | Manipulación de archivos Excel |
| `docker-expert` | Contenedorización Docker |
| `security-reviewer` | Auditoría de seguridad |
| `test-master` | Testing y calidad |
| `sql-pro` | Consultas SQL y base de datos |
| `python-pro` | Desarrollo Python |
| `api-designer` | Diseño de APIs |
| `frontend-design` | Diseño de interfaces |
| `code-review-excellence` | Revisiones de código |
| y más... | Ver `.opencode/skills/` |

---

## 📁 Estructura del Proyecto

```
AppConta/
├── main.py                    # Punto de entrada
├── database/                  # Capa de datos
│   ├── schema.sql             # Esquema SQLite
│   ├── conexion.py            # Gestión BD
│   └── migrador.py            # Importación desde Excel
├── models/                    # Modelos de negocio
│   ├── movimiento.py
│   ├── cuenta.py
│   ├── categoria.py
│   ├── prestamo.py
│   └── accion.py
├── ui/                        # Interfaz de usuario
│   ├── ventana_principal.py
│   ├── registro.py
│   ├── balance_mensual.py
│   ├── reportes.py
│   └── ...
├── utils/                     # Utilidades
│   ├── calculos.py
│   └── exportar.py
├── data/                      # Base de datos (local)
│   └── AppConta.db
├── docs/                      # Documentación
│   └── INFORME.md             # Informe de análisis inicial
├── .opencode/                 # Configuración agentes IA
│   ├── agents/                # Definiciones de agentes
│   └── skills/                # Skills instalados
├── AGENTS.md                  # Workflow multi-agente
└── opencode.json              # Configuración OpenCode
```

---

## 🚀 Plan de Desarrollo

| Fase | Descripción | Duración |
|------|-------------|----------|
| 1 | Migración de datos Excel → SQLite | 2 días |
| 2 | UI base + formulario de registro | 4 días |
| 3 | Balances mensuales por cuenta | 3 días |
| 4 | Reportes y gráficos | 3 días |
| 5 | Cierre anual automático | 2 días |
| 6 | Gestión de préstamos | 2 días |
| 7 | Cartera de acciones | 2 días |
| 8 | Consolidación AnualGlobal | 2 días |
| 9 | Empaquetado .exe portable | 1 día |
| | **Total** | **~21 días** |

---

## 🔧 Desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/MikiValbuena/AppConta.git
cd AppConta

# Instalar dependencias
pip install ttkbootstrap matplotlib openpyxl fpdf2 pyinstaller

# Ejecutar en desarrollo
python main.py

# Empaquetar para distribución
pyinstaller --onefile --windowed --icon=assets/icono.ico main.py
```

---

## 📄 Licencia

MIT License
