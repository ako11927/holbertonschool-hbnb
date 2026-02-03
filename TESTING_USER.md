# User API Testing and Verification (part3)

## Database initialization

From the `part3` directory:

```bash
# Optional: use Flask shell to create tables only
flask --app app run  # or use run.py; tables are created on first run via run.py

# Or explicitly in Flask shell:
flask --app app shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

`run.py` already calls `db.create_all()` inside the app context; only the **users** table is created at this stage (other entities use in-memory repositories).

---

## cURL examples

**Base URL:** `http://localhost:5000` (run with `python run.py` from `part3`).

### 1. Create a new user

```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d "{\"first_name\":\"Jane\",\"last_name\":\"Doe\",\"email\":\"jane@example.com\",\"password\":\"secret123\",\"is_admin\":false}"
```

Expected: `201` and JSON with `id`, `first_name`, `last_name`, `email`, `is_admin`, `created_at`, `updated_at` (no `password`).

### 2. Retrieve a user by ID

Use the `id` returned from the create response (UUID string).

```bash
curl -X GET http://localhost:5000/api/v1/users/<USER_ID>
```

Example:

```bash
curl -X GET http://localhost:5000/api/v1/users/550e8400-e29b-41d4-a716-446655440000
```

Expected: `200` and user JSON, or `404` if not found.

### 3. Get all users

```bash
curl -X GET http://localhost:5000/api/v1/users/
```

---

## Verification checklist

1. **Data persisted in SQLite**  
   After creating a user, restart the app and GET the same user by ID or list users. The user should still be there. DB file (development): `instance/development.db` (or path from `SQLALCHEMY_DATABASE_URI`).

2. **Email uniqueness**  
   Create a user, then POST again with the same `email`. Expected: `400` with message like `"Email already exists"`.

3. **Passwords stored hashed**  
   Inspect the database: the `users.password` column must contain a bcrypt hash (e.g. starts with `$2b$`), not the plain text password.

   Example (SQLite):

   ```bash
   sqlite3 instance/development.db "SELECT id, email, password FROM users LIMIT 1;"
   ```

   Or from Flask shell:

   ```python
   from app.models.user import User
   from app import db
   u = db.session.query(User).first()
   print(u.password)  # should look like $2b$12$...
   ```
