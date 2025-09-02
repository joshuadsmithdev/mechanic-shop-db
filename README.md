## Postman Collection

- Collection: `postman/Mechanic-Shop-API.postman_collection.json`
- Environment (optional): `postman/Mechanic-Shop-Local.postman_environment.json`

### How to Use
1. Open Postman → **Import** → select the files above.
2. Choose the environment (or create one) and set:
   - `baseUrl` = `http://127.0.0.1:5000` (or your deployed URL)
   - `token` = `<paste a valid JWT here>`
3. Run requests from the **Mechanic Shop API** collection.

> Notes:
> - Some routes require a Bearer token in `{{token}}`.
> - If you’re testing locally, start the server first.
