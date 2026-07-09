// TODO: Componente raíz del frontend.
// La UI básica tiene: ChatWindow + InputBox.
// Si querés customizar (tema LATAM, logo, etc.), reemplazá este componente.

import { useState } from 'react'
import { sendMessage } from './services/api'

function App() {
  const [messages, setMessages] = useState<Array<{ from: 'user' | 'bot'; text: string }>>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  // TODO: Conectar con el backend real
  async function handleSend() {
    if (!input.trim()) return
    
    const userMessage = input
    setMessages([...messages, { from: 'user', text: userMessage }])
    setInput('')
    setLoading(true)
    
    try {
      const response = await sendMessage(userMessage)
      setMessages(prev => [...prev, { from: 'bot', text: response }])
    } catch (error) {
      setMessages(prev => [...prev, { from: 'bot', text: 'Error al conectar con el chatbot.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <h1>Chatbot Propensión LATAM</h1>
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.from}`}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="message bot">Pensando...</div>}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Preguntame sobre propensión de compra o políticas..."
        />
        <button onClick={handleSend} disabled={loading}>
          Enviar
        </button>
      </div>
    </div>
  )
}

export default App
