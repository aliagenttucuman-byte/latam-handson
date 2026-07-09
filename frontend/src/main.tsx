import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'

// TODO: Reemplazar con el tema de LATAM
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
