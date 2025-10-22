// Centralized tiny wrapper around fetch
// Dev: use '' so requests are relative and go through Vite proxy
// Prod: fall back to your Render URL unless VITE_API_BASE is set
const API_BASE =
  (import.meta.env.VITE_API_BASE ?? '') ||
  (import.meta.env.DEV ? '' : 'https://mechanic-shop-db.onrender.com');


async function request(path, { method = 'GET', body, headers } = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(headers || {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`${res.status}: ${msg || res.statusText}`);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  // Customers
  listCustomers: () => request('/api/customers'),
  createCustomer: (data) => request('/api/customers', { method: 'POST', body: data }),
  getCustomer: (id) => request(`/api/customers/${id}`),
  updateCustomer: (id, data) => request(`/api/customers/${id}`, { method: 'PUT', body: data }),
  deleteCustomer: (id) => request(`/api/customers/${id}`, { method: 'DELETE' }),

  // Vehicles (adjust paths if different)
  listVehicles: () => request('/api/vehicles'),
  // Tickets
  listTickets: () => request('/api/tickets'),
};
