import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Customers from "./pages/Customers";
import Vehicles from "./pages/Vehicles";
import Tickets from "./pages/Tickets";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Customers />} />
          <Route path="/vehicles" element={<Vehicles />} />
          <Route path="/tickets" element={<Tickets />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
