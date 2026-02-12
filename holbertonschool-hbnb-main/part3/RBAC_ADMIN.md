# RBAC & Admin-Only Endpoints

## Overview

- **JWT payload**: `identity` = user id; `additional_claims`: `email`, `is_admin`.
- **Admins**: `is_admin === true` in JWT. Admins can access admin-only endpoints and bypass ownership checks on places/reviews.
- **Protected endpoints**: Use `@jwt_required()`. Admin-only endpoints use `@admin_required` (JWT + `is_admin` check); non-admin → **403**.

## Assumptions

1. **Login**: `POST /api/v1/auth/login` with JSON `{ "email": "...", "password": "..." }`. Returns `{ "access_token": "..." }`. Token includes `id`, `email`, `is_admin`.
2. **Admin bootstrap**: On startup, if no admin exists, one is created: `admin@example.com` / `admin123`. Use this for testing admin-only flows.
3. **User create/update**: Passwords hashed with Flask-Bcrypt. Email must be unique.
4. **Ownership**: For places (owner_id) and reviews (user_id), only the owner/author or an admin can modify/delete. Admins bypass ownership.

## Admin-Only Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Create user (admin only) |
| PUT | `/api/v1/users/<user_id>` | Update any user (admin only) |
| POST | `/api/v1/amenities/` | Create amenity (admin only) |
| PUT | `/api/v1/amenities/<amenity_id>` | Update amenity (admin only) |

## Example cURL Commands

Base URL: `http://127.0.0.1:5000`. Replace `TOKEN` with the `access_token` from login.

### 1. Login (admin)

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

Save the `access_token` as `TOKEN` for later calls.

### 2. Create user (admin only)

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"jane@example.com","password":"secret123","is_admin":false}'
```

### 3. Update user (admin only)

```bash
curl -s -X PUT "http://127.0.0.1:5000/api/v1/users/<user_id>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"first_name":"Jane","last_name":"Smith","email":"jane.smith@example.com"}'
```

To change password:

```bash
curl -s -X PUT "http://127.0.0.1:5000/api/v1/users/<user_id>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"password":"newpassword456"}'
```

### 4. Create amenity (admin only)

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Parking"}'
```

### 5. Update amenity (admin only)

```bash
curl -s -X PUT "http://127.0.0.1:5000/api/v1/amenities/<amenity_id>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Free Parking"}'
```

### 6. List users (JWT required, any authenticated user)

```bash
curl -s -X GET "http://127.0.0.1:5000/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Non-admin calling admin-only endpoint → 403

Login as a non-admin (e.g. user created in step 2), then:

```bash
curl -s -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NON_ADMIN_TOKEN" \
  -d '{"name":"Pool"}'
```

Expected: `403` with `{"error": "Admin access required"}`.

### 8. Places PUT – owner or admin only

As owner (or admin):

```bash
curl -s -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Updated Title","description":"...","price":120,"latitude":37.77,"longitude":-122.42,"owner_id":"<owner_id>","amenities":[]}'
```

As non-owner, non-admin: expected **403** `Only the place owner or an admin can update this place`.

### 9. Reviews DELETE – author or admin only

```bash
curl -s -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<review_id>" \
  -H "Authorization: Bearer $TOKEN"
```

Non-author, non-admin: **403** `Only the review author or an admin can delete this review`.

## Public Endpoints (no JWT)

- `GET /api/v1/places/`
- `GET /api/v1/places/<place_id>`
- `GET /api/v1/places/<place_id>/reviews`
- `GET /api/v1/amenities/`
- `GET /api/v1/amenities/<amenity_id>`
- `GET /api/v1/reviews/`
- `GET /api/v1/reviews/<review_id>`

## Running the API

From `part3`:

```bash
python app.py
```

Admin user `admin@example.com` / `admin123` is created on first run if no admin exists.
