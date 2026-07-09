# Frontend — Chatbot UI

## ¿Qué hace?

UI minimalista de chat que se conecta al backend (`services/chatbot-backend/`).

## Estructura

```
frontend/
├── src/
│   ├── App.tsx                # Componente raíz
│   ├── components/
│   │   ├── ChatWindow.tsx     # Ventana de chat
│   │   ├── MessageBubble.tsx  # Burbuja de mensaje
│   │   └── InputBox.tsx       # Input de mensaje
│   ├── services/
│   │   └── api.ts             # Cliente HTTP al backend
│   └── main.tsx               # Entry point
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## ¿Qué archivos tocar?

1. **`src/services/api.ts`** — Cambiar la URL del backend.
2. **`src/App.tsx`** — Si querés customizar la UI.

## Configuración

### `src/services/api.ts`

```typescript
// TODO: Reemplazar con la URL real de tu chatbot backend
const CHATBOT_API = "https://<chatbot-backend-url>/chat"

export async function sendMessage(message: string): Promise<string> {
  const response = await fetch(CHATBOT_API, {
    method: 'POST',
    body: JSON.stringify({ message }),
    headers: { 'Content-Type': 'application/json' },
  })
  
  if (!response.ok) {
    throw new Error(`Chatbot API error: ${response.status}`)
  }
  
  const data = await response.json()
  return data.response
}
```

## Cómo correr local

```bash
npm install
npm run dev
# Abrí http://localhost:5173
```

## Cómo deployar

El template "Frontend Template" de Cosmos ya configura el deploy automático:
- Build: `npm run build`
- Output: `dist/`
- Hosting: Cloud Storage + Cloud CDN (estático)

Después de hacer merge a `develop`, el CI/CD:
1. Compila la app
2. Sube el bundle a GCS
3. Invalida el CDN
4. La URL queda disponible (te la pasan por mail o en el MR)

## Referencias

- [Cosmos Frontend Template](https://catalog.cosmos.../templates/frontend)
- [Vite docs](https://vitejs.dev/)
