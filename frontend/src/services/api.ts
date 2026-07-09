// TODO: Reemplazar con la URL real del chatbot backend (Cloud Run service).
// Formato: https://<service-name>-<hash>-uc.a.run.app
// Lo encontrás en: GCP Console → Cloud Run → chatbot-backend → URL

const CHATBOT_API = 'https://PLACEHOLDER-CHATBOT-BACKEND-URL/chat'

export async function sendMessage(message: string): Promise<string> {
  const response = await fetch(CHATBOT_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error(`Chatbot API error: ${response.status}`)
  }

  const data = await response.json()
  return data.response
}
