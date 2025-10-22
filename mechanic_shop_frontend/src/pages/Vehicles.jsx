import { useEffect, useState } from "react";
import { api } from "../services/api";
import Loader from "../components/Loader";

export default function Vehicles() {
  const [items, setItems] = useState(null);
  const [err, setErr] = useState("");
  useEffect(() => { (async () => {
    try { setItems(await api.listVehicles()); } catch(e){ setErr(e.message); }
  })(); }, []);
  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-semibold">Vehicles</h1>
      {err && <div className="bg-red-50 text-red-700 border border-red-200 p-3 rounded">{err}</div>}
      {!items ? <Loader/> : (
        <div className="bg-white rounded-xl border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left">
              <tr>
                <th className="th">VIN</th>
                <th className="th">Make</th>
                <th className="th">Model</th>
                <th className="th">Year</th>
                <th className="th">Owner ID</th>
              </tr>
            </thead>
            <tbody>
              {items.map(v => (
                <tr key={v.vin} className="border-t">
                  <td className="td">{v.vin}</td>
                  <td className="td">{v.make}</td>
                  <td className="td">{v.model}</td>
                  <td className="td">{v.year}</td>
                  <td className="td">{v.customer_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
