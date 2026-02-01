// Initial comment
// Trigger for new frontend app deployment
// Trigger for explicit force push on frontend

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        {/* Add more routes here as we build out the app */}
      </Routes>
    </Router>
  )
}

function Home() {
  return (
    <div>
      <h1>Welcome to Corexus!</h1>
      <p>This is the home page. <a href="/login">Login here</a>.</p>
    </div>
  )
}

function Login() {
  return (
    <div>
      <h1>Login to Corexus</h1>
      <p>Login form will go here...</p>
    </div>
  )
}

export default App
