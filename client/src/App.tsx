import './App.css'
import Home from './Pages/Home'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/ticker/:ticker"/>
        </Routes>
      </div>
    </Router>
  )
}

export default App
