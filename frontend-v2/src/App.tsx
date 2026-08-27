import { useState } from 'react'
import MainLayout from './layouts/MainLayout'
import Operations from './pages/Operations'
import Blueprint from './pages/Blueprint'

function App() {
  const [activeView, setActiveView] = useState<'operations' | 'architecture'>('operations');

  return (
    <MainLayout onViewChange={(view) => setActiveView(view)}>
      {activeView === 'operations' ? <Operations /> : <Blueprint />}
    </MainLayout>
  )
}

export default App
