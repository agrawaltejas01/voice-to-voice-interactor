import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import AudioRecorder from './audio-recorder'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
    <AudioRecorder />
    </div>
  )
}

export default App
