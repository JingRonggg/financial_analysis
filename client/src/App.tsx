import './App.css'
// import ChartArea from './Components/Charts/tickerChart'
import Home from './Pages/HomePage/Home'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home/>} />
          {/* <Route path="/ticker/:ticker" element={<ChartArea/>}/> */}
        </Routes>
      </div>
    </Router>
  )
}

export default App
