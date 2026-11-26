import './site.css'
import './App.css'
import AppRoutes from './AppRoutes'
import { AuthProvider } from './auth/AuthProvider'

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App
