import './App.css'
import { Routes, Route } from "react-router-dom";
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';

function App() {

  return (
    <Routes>
      <Route path='/' element={<Login />} />
      <Route path='/dashboard' element={<AdminDashboard />} />
    </Routes>
  )
}

export default App