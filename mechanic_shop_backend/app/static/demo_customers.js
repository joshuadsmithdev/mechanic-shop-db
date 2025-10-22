
async function createCustomer() {
  const payload = {
    name: document.getElementById("c_name").value,
    email: document.getElementById("c_email").value,
    password: document.getElementById("c_password").value || undefined
  };
  const res = await fetch("/api/customers", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById("createResult").textContent = JSON.stringify(data, null, 2);
}

async function updateCustomer() {
  const id = document.getElementById("u_id").value;
  const body = {};
  const email = document.getElementById("u_email").value;
  const name = document.getElementById("u_name").value;
  if (email) body.email = email;
  if (name) body.name = name;

  const res = await fetch(`/api/customers/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  let text;
  try { text = await res.clone().json(); }
  catch { text = await res.text(); }
  document.getElementById("updateResult").textContent =
    typeof text === "string" ? text : JSON.stringify(text, null, 2);
}

async function deleteCustomer() {
  const id = document.getElementById("d_id").value;
  const res = await fetch(`/api/customers/${id}`, { method: "DELETE" });
  const text = await res.text();
  document.getElementById("deleteResult").textContent = res.status === 204 ? "Deleted (204 No Content)" : text;
}
