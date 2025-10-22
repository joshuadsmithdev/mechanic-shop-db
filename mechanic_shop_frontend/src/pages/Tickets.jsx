import { useEffect, useState } from "react";
import { api } from "../services/api";
import Loader from "../components/Loader";

export default function Tickets() {
  const [items, setItems] = useState(null);
  const [err, setErr] = useState("");
  useEffect(() => { (async () => {
    try { setItems(await api.listTickets()); } catch(e){ setErr(e.message); }
  })(); }, []);
  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-semibold">Service Tickets</h1>
      {err && <div className="bg-red-50 text-red-700 border border-red-200 p-3 rounded">{err}</div>}
      {!items ? <Loader/> : (
        <div className="bg-white rounded-xl border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left">
              <tr>
                <th className="th">ID</th>
                <th className="th">VIN</th>
                <th className="th">Status</th>
                <th className="th">Total</th>
              </tr>
            </thead>
            <tbody>
              {items.map(t => (
                <tr key={t.ticket_id} className="border-t">
                  <td className="td">{t.ticket_id}</td>
                  <td className="td">{t.vin}</td>
                  <td className="td capitalize">{t.status}</td>
                  <td className="td">${Number(t.total_cost ?? 0).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
