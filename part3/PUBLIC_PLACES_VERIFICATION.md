# Public Places Endpoints – Verification Report

## Summary

The **GET** endpoints for places are **public**: they do not use `@jwt_required` and work **without** an `Authorization` header or JWT token. This document gives the exact cURL commands to test them and the expected responses.

---

## Exact cURL Commands

Run these **without** any `Authorization` or `Bearer` headers. Ensure the API is running at `http://127.0.0.1:5000` (e.g. `python app.py` from `part3`).

### 1. List all places

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/"
```

**Optional (with status code):**

```bash
curl -s -w "\nHTTP Status: %{http_code}\n" -X GET "http://127.0.0.1:5000/api/v1/places/"
```

### 2. Get place by ID

Replace `<place_id>` with a real UUID (e.g. from the list response) or use a sample UUID to trigger 404:

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>"
```

**Example with a concrete ID:**

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/00000000-0000-0000-0000-000000000001"
```

**Optional (with status code):**

```bash
curl -s -w "\nHTTP Status: %{http_code}\n" -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>"
```

---

## What Each Test Verifies

| Test | Endpoint | Verifies | Expected HTTP |
|------|----------|----------|---------------|
| **1** | `GET /api/v1/places/` | List of places is returned **without** JWT | **200** |
| **2** | `GET /api/v1/places/<place_id>` | Place details are returned **without** JWT | **200** (found) or **404** (not found) |

Both endpoints must respond successfully when called **without** `Authorization` or any JWT. If they did require JWT, you would get **401 Unauthorized** instead of **200** (or **404** for detail when the place does not exist).

---

## Expected HTTP Status Codes

- **`GET /api/v1/places/`**  
  - **200 OK** – Always, even when the list is empty (`[]`).

- **`GET /api/v1/places/<place_id>`**  
  - **200 OK** – Place exists.  
  - **404 Not Found** – No place with that ID.

---

## Expected Response Structure

### List – `GET /api/v1/places/`

- **Content-Type:** `application/json`
- **Body:** JSON array of place summaries.

**Current implementation** (`api/v1/places.py`, `place_summary_model` / list view) returns objects with:

- `id`
- `title`
- `latitude`
- `longitude`

**Note:** The list view does **not** currently include `price`. If you expect `id`, `title`, `price` in the list, that would require an API change. The **detail** endpoint does include `price`.

**Example (non-empty):**

```json
[
  { "id": "...", "title": "...", "latitude": 37.77, "longitude": -122.42 },
  ...
]
```

**Example (empty):**

```json
[]
```

### Detail – `GET /api/v1/places/<place_id>`

- **Content-Type:** `application/json`
- **Body:** Single JSON object (from `Place.to_dict()`).

**Includes:**

- `id`, `title`, `description`, `price`, `latitude`, `longitude`
- `owner_id`, `owner` (nested), `amenities`, `reviews`
- `created_at`, `updated_at`

**Example (200):**

```json
{
  "id": "...",
  "title": "...",
  "description": "...",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "...",
  "owner": { ... },
  "amenities": [ ... ],
  "reviews": [ ... ],
  "created_at": "...",
  "updated_at": "..."
}
```

**Example (404):**

```json
{ "error": "Place not found" }
```

---

## Code Confirmation – Public Access

- In `api/v1/places.py`, the **GET** handlers for:
  - `PlaceList.get` (`GET /`)
  - `PlaceResource.get` (`GET /<place_id>`)
- do **not** use `@jwt_required` (or any similar decorator). The same file uses no `jwt_required` at all.
- A project-wide search for `@jwt_required` / `jwt_required` shows **no** usage in this codebase.

Therefore, **`GET /api/v1/places/`** and **`GET /api/v1/places/<place_id>`** are **public** and do not require JWT.

---

## How to Run the Tests

1. **Start the API** (from `part3`):

   ```bash
   python app.py
   ```

2. In another terminal, run the cURL commands above (or use the provided scripts):

   - **Bash:** `bash test_public_places_curl.sh`
   - **PowerShell:** `.\test_public_places_curl.ps1`

3. Confirm:
   - **List:** HTTP **200**, JSON array (possibly empty).
   - **Detail:** HTTP **200** when the place exists, **404** when it does not.
   - No `Authorization` header is used in any of these requests.

---

## Conclusion

- **`GET /api/v1/places/`** and **`GET /api/v1/places/<place_id>`** are **public**.
- They can be called **without** JWT or `Authorization`.
- Expected status: **200** for list and for detail when the place exists; **404** for detail when the place does not.
- Response structure matches the formats described above, with list items containing `id`, `title`, `latitude`, `longitude` (and detail including `id`, `title`, `description`, `price`, `latitude`, `longitude`, etc.).
