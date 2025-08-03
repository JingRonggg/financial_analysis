import './App.css'
import Dashboard from './Components/dashboard'
import Home from './Pages/HomePage/Home'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/ticker/:ticker" element={<Dashboard/>}/>
        </Routes>
      </div>
    </Router>
  )
}

export default App
