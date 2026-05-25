# Proyecto DockerEjemplos - Sistema Multi-Agente

## Descripción del proyecto
Aplicación web tipo MVC basada en el Excel `Barichara_copia.xlsx` (gestor de cartera de inversiones). Se despliega con Docker en Windows.

## Agentes del sistema

| Agente | Rol | Modo |
|--------|-----|------|
| `@gestor` | Orquestador principal - coordina todo el flujo | primary |
| `@especialista-windows` | Experto en Windows/WSL/Docker Desktop | subagent |
| `@especialista-docker` | Experto en Docker/Docker Compose | subagent |
| `@programador` | Implementa el código | subagent |
| `@revisor` | Revisa calidad del código | subagent |

## Workflow obligatorio

```
Usuario → @gestor → @especialistas (si aplica) → @programador → @revisor
                                                      ↑              │
                                                      │       ¿Issues?
                                                      │       ├── Sí → vuelve a @programador
                                                      │       └── No → Usuario valida
                                                      │                  ↓
                                                      │            ¿Aprueba?
                                                      │            ├── Sí → git commit
                                                      │            └── No → ajustes
```

### Reglas del workflow

1. **@gestor** es el único punto de entrada. Siemora invocar @gestor primero.
2. **Especialistas** solo se consultan cuando la tarea lo requiere (no son obligatorios).
3. **@programador** implementa siguiendo indicaciones. No decide arquitectura.
4. **@revisor** revisa TODO el código antes de presentarlo al usuario. No modifica nada.
5. **Máximo 3 ciclos** de revisión-corrección. Si no se resuelve, decisión humana.
6. **Nunca hacer commit** sin aprobación explícita del usuario.
7. **Mensajes de commit** descriptivos en español.

## Stack técnico
- **Backend**: PHP o Python/Django (MVC)
- **Frontend**: HTML+CSS+JS con diseño separado (MVC)
- **Contenedores**: Docker + Docker Compose
- **Base de datos**: SQLite (simple) o MySQL/MariaDB (en contenedor)
- **SO objetivo**: Windows 10/11 con WSL 2

## Estructura del proyecto
```
/
├── Barichara_copia.xlsx    # Datos fuente
├── AGENTS.md               # Este archivo - reglas del proyecto
├── opencode.json           # Configuración de agentes
├── .opencode/
│   └── agents/             # Definiciones de agentes
│       ├── gestor.md
│       ├── especialista-windows.md
│       ├── especialista-docker.md
│       ├── programador.md
│       └── revisor.md
├── docker-compose.yml      # Orquestación Docker
├── Dockerfile              # Imagen de la app
└── src/                    # Código fuente
    ├── controllers/
    ├── models/
    ├── views/
    └── public/
```

## Comandos útiles
```powershell
# Iniciar proyecto Docker
docker compose up -d

# Detener proyecto Docker
docker compose down

# Ver logs
docker compose logs -f

# Acceder al contenedor
docker compose exec app bash
```
