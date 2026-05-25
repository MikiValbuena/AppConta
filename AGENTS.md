# AppConta - Sistema Multi-Agente

## Agentes del sistema

| Agente | Rol | Modelo | Modo |
|--------|-----|--------|------|
| `@gestor` | Orquestador principal | Big Pickle | primary |
| `@especialista-windows` | Experto en Windows/WSL | DeepSeek V4 Flash Free | subagent |
| `@especialista-docker` | Experto en Docker | DeepSeek V4 Flash Free | subagent |
| `@programador` | Implementa el código | DeepSeek V4 Flash Free | subagent |
| `@revisor` | Revisa calidad del código | Big Pickle | subagent |

## Workflow obligatorio

```
Usuario → @gestor
             │
             ▼
       ¿Necesita especialistas?
       ├── Sí → @especialista-windows / @especialista-docker → @gestor
       └── No ────────────────────────────────────────────────┘
             │
             ▼
       @programador (implementa)
             │
             ▼
       @revisor (revisa)
             │
        ┌────┴────┐
        ▼         ▼
     ¿Issues?  ✅ Sin issues
        │         │
        │         ▼
        │    Usuario valida
        │         │
        │    ┌────┴────┐
        │    ▼         ▼
        │  ¿Aprueba?  ❌ Rechaza
        │    │         │
        │    │         └──→ @programador (ajustes) → @revisor
        │    ▼
        │  ✅ Aprueba → git commit
        │
        └──→ @programador (corrige) → @revisor (revisa de nuevo)
```

### Reglas del workflow

1. **@gestor** es el único punto de entrada. Siempre invocar @gestor primero.
2. **Especialistas** solo se consultan cuando la tarea lo requiere.
3. **@programador** implementa siguiendo indicaciones. No decide arquitectura.
4. **@revisor** revisa TODO el código antes de presentarlo al usuario.
5. **Máximo 3 ciclos** de revisión-corrección entre @revisor y @programador.
6. **Nunca hacer commit** sin aprobación explícita del usuario.
7. **Si el usuario rechaza** los cambios, vuelve a @programador para ajustes, luego pasa otra vez por @revisor.

## Stack técnico
- **Backend**: Pendiente de definir
- **Frontend**: Pendiente de definir
- **Contenedores**: Docker + Docker Compose
- **SO objetivo**: Windows 10/11 con WSL 2
