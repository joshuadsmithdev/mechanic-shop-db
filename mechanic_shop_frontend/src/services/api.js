// If VITE_API_BASE is set, we use it. Otherwise we rely on vite proxy and leave it empty.
const API_BASE =
  (import.meta.env.VITE_API_BASE && import.meta.env.VITE_API_BASE.trim()) || ""

async function request(path, { method = "GET", body, headers } = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(headers || {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  })

  const text = await res.text()
  let json = null
  try { json = text ? JSON.parse(text) : null } catch { /* html error page fallback */ }

  if (!res.ok) {
    const msg = json?.message || json?.error || text || res.statusText
    throw new Error(`${res.status}: ${msg}`)
  }
  return json
}

export const api = {
  // Customers
  listCustomers: () => request("/api/customers"),
  createCustomer: (data) => request("/api/customers", { method: "POST", body: data }),
  updateCustomer: (id, data) => request(`/api/customers/${id}`, { method: "PUT", body: data }),
  deleteCustomer: (id) => request(`/api/customers/${id}`, { method: "DELETE" }),

  // Vehicles
  listVehicles: () => request("/api/vehicles"),
  // If you expose /api/customers/:id/vehicles, add:
  listCustomerVehicles: (id) => request(`/api/customers/${id}/vehicles`),

  // Tickets
  listTickets: () => request("/api/service_tickets"),
}
