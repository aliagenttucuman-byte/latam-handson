# Diagramas de Cosmos (draw.io)

Diagramas profesionales de la arquitectura de Cosmos (LATAM Airlines) y el hands-on de propensión de tickets.

## Archivos

### `como-funciona-cosmos.*`
Visión integral de Cosmos en 4 secciones:
1. **Ciclo universal** (5 fases: pregunta → datos → componentes → producto → iteración)
2. **3 capas de infra** (Plataforma, Producto, Compartidos)
3. **Flujo del hands-on** (2 semanas, 6-7 días por componente)
4. **Regla de oro** (no usar `google_*` directo, siempre módulos de cosmos-common)

**Formato**: PNG (compartir), SVG (vectorial para docs), .drawio (editable).

### `arquitectura-3-componentes-v2.*`
Arquitectura técnica detallada con 3 swim lanes:
- **GENAI** (arriba): frontend, chatbot, LangGraph agent, 2 tools, LLM vía GenAI Gateway
- **ML** (medio): training pipeline, model registry, serving pipeline, drift, backtesting, BQ predicciones
- **DATA** (abajo): 6 fuentes, File Ingestor, BQO, master table, GCS bucket, data-to-bucket job

Más leyenda de 7 puntos al pie y stack tecnológico.

**Formato**: PNG (compartir), SVG (vectorial para docs), .drawio (editable).

## Cómo editar

Los archivos `.drawio` se abren directamente en:
- [app.diagrams.net](https://app.diagrams.net) (web)
- draw.io Desktop
- VS Code con la extensión Draw.io Integration

## Cómo regenerar los PNG/SVG

Si editás un `.drawio` y querés regenerar los exports, usá draw.io CLI:

```bash
# PNG
xvfb-run -a drawio --export --format png --output como-funciona-cosmos.png como-funciona-cosmos.drawio

# SVG (vectorial, mejor para docs técnicas)
xvfb-run -a drawio --export --format svg --output como-funciona-cosmos.svg como-funciona-cosmos.drawio
```

El `xvfb-run -a` es necesario en servidores headless (sin display).

## Fuente

Diagramas generados el 2026-07-09 como parte del kit de migración al hands-on de Cosmos.

Ver el contexto conceptual en [`../MAPA_MENTAL_CICLO.md`](../MAPA_MENTAL_CICLO.md).
