import { useEffect, useState } from "react";
import { api } from "../services/api";
import Loader from "../components/Loader";

export default function Customers() {
  const [items, setItems] = useState(null);
  const [err, setErr] = useState("");
  const [form, setForm] = useState({ first_name: "", last_name: "", email: "", password: "" });

  async function load() {
    try {
      setErr("");
      const data = await api.listCustomers();
      setItems(data);
    } catch (e) { setErr(e.message); }
  }

  useEffect(() => { load(); }, []);

  async function onCreate(e) {
    e.preventDefault();
    try {
      setErr("");
      await api.createCustomer(form);
      setForm({ first_name: "", last_name: "", email: "", password: "" });
      await load();
    } catch (e) { setErr(e.message); }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-semibold">Customers</h1>

      <form onSubmit={onCreate} className="grid sm:grid-cols-4 gap-3 bg-white p-4 rounded-xl border">
        <input className="input" placeholder="First name" value={form.first_name}
               onChange={e=>setForm(f=>({...f, first_name:e.target.value}))} required />
        <input className="input" placeholder="Last name" value={form.last_name}
               onChange={e=>setForm(f=>({...f, last_name:e.target.value}))} required />
        <input className="input" type="email" placeholder="Email" value={form.email}
               onChange={e=>setForm(f=>({...f, email:e.target.value}))} required />
        <input className="input" type="password" placeholder="Password" value={form.password}
               onChange={e=>setForm(f=>({...f, password:e.target.value}))} />
        <div className="sm:col-span-4">
          <button className="btn">Create</button>
        </div>
      </form>

      {err && <div className="bg-red-50 text-red-700 border border-red-200 p-3 rounded">{err}</div>}

      {!items ? <Loader/> : (
        <div className="bg-white rounded-xl border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left">
              <tr>
                <th className="th">ID</th>
                <th className="th">Name</th>
                <th className="th">Email</th>
                <th className="th">Phone</th>
              </tr>
            </thead>
            <tbody>
              {items.map(c => (
                <tr key={c.customer_id} className="border-t">
                  <td className="td">{c.customer_id}</td>
                  <td className="td">{c.first_name} {c.last_name}</td>
                  <td className="td">{c.email}</td>
                  <td className="td">{c.phone || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
