import { NavLink } from "react-router-dom";

export default function Navbar() {
  const link = "px-3 py-2 rounded-md hover:bg-gray-100";
  const active = "bg-gray-200";
  return (
    <header className="border-b bg-white">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center gap-3">
        <div className="font-bold">Mechanic Shop</div>
        <nav className="flex gap-2">
          <NavLink to="/" className={({isActive}) => `${link} ${isActive?active:''}`}>Customers</NavLink>
          <NavLink to="/vehicles" className={({isActive}) => `${link} ${isActive?active:''}`}>Vehicles</NavLink>
          <NavLink to="/tickets" className={({isActive}) => `${link} ${isActive?active:''}`}>Tickets</NavLink>
        </nav>
      </div>
    </header>
  );
}
