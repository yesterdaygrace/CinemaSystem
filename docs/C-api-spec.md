# C. Skill Test - API Specification

## 1. Scope

Implementasi Golang dibatasi pada dua fungsi yang diminta:

1. Login user.
2. CRUD data jadwal tayang.

Authorization menggunakan JWT yang diperoleh dari endpoint login.

## 2. Base URL

```text
http://localhost:8080/api/v1
```

## 3. Authentication

Header:

```http
Authorization: Bearer <JWT>
```

Role:

```text
CUSTOMER
ADMIN
```

Permission:

| Endpoint | CUSTOMER | ADMIN |
|---|---:|---:|
| `GET /schedules` | ✓ | ✓ |
| `GET /schedules/:id` | ✓ | ✓ |
| `POST /schedules` | - | ✓ |
| `PUT /schedules/:id` | - | ✓ |
| `DELETE /schedules/:id` | - | ✓ |

---

# 4. POST /auth/login

## Request

```http
POST /api/v1/auth/login
Content-Type: application/json
```

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

## Success

```http
200 OK
```

```json
{
  "access_token": "<JWT>",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

## Invalid credentials

```http
401 Unauthorized
```

```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

---

# 5. GET /schedules

Mengambil daftar jadwal tayang.

```http
GET /api/v1/schedules
Authorization: Bearer <JWT>
```

Response:

```http
200 OK
```

```json
{
  "data": [
    {
      "id": 1,
      "movie_id": 1,
      "studio_id": 1,
      "start_time": "2026-10-01T19:00:00+07:00",
      "end_time": "2026-10-01T21:10:00+07:00",
      "status": "SCHEDULED"
    }
  ]
}
```

---

# 6. GET /schedules/:id

Mengambil satu schedule.

```http
GET /api/v1/schedules/1
Authorization: Bearer <JWT>
```

Success:

```http
200 OK
```

Not found:

```http
404 Not Found
```

---

# 7. POST /schedules

Membuat schedule baru.

Role:

```text
ADMIN
```

Request:

```http
POST /api/v1/schedules
Authorization: Bearer <JWT>
Content-Type: application/json
```

```json
{
  "movie_id": 1,
  "studio_id": 1,
  "start_time": "2026-10-01T19:00:00+07:00",
  "end_time": "2026-10-01T21:10:00+07:00"
}
```

Validation:

```text
movie_id > 0
studio_id > 0
start_time valid
end_time valid
end_time > start_time
```

Recommended business validation:

```text
Studio yang sama tidak boleh mempunyai dua schedule yang waktunya overlap.
```

Success:

```http
201 Created
```

---

# 8. PUT /schedules/:id

Mengubah schedule.

```http
PUT /api/v1/schedules/1
Authorization: Bearer <JWT>
Content-Type: application/json
```

```json
{
  "movie_id": 1,
  "studio_id": 2,
  "start_time": "2026-10-01T20:00:00+07:00",
  "end_time": "2026-10-01T22:10:00+07:00"
}
```

Role:

```text
ADMIN
```

Response:

```http
200 OK
```

---

# 9. DELETE /schedules/:id

Untuk sistem bisnis, operasi ini lebih baik diperlakukan sebagai cancellation/logical delete.

```http
DELETE /api/v1/schedules/1
Authorization: Bearer <JWT>
```

Role:

```text
ADMIN
```

Business behavior:

```text
status: SCHEDULED → CANCELLED
```

Response:

```http
204 No Content
```

Alternatif response:

```http
200 OK
```

jika API ingin mengembalikan object schedule terbaru.

---

# 10. HTTP Status Code

Gunakan status code berikut:

| Status | Penggunaan |
|---|---|
| `200` | Request berhasil |
| `201` | Resource berhasil dibuat |
| `204` | Resource berhasil dihapus/dibatalkan |
| `400` | Input tidak valid |
| `401` | Authentication tidak valid / token tidak ada |
| `403` | User tidak mempunyai permission |
| `404` | Resource tidak ditemukan |
| `409` | Konflik business rule |
| `500` | Internal server error |

---

# 11. Error Response

Gunakan format konsisten:

```json
{
  "error": {
    "code": "SCHEDULE_NOT_FOUND",
    "message": "Schedule not found"
  }
}
```

Contoh:

```json
{
  "error": {
    "code": "SCHEDULE_CONFLICT",
    "message": "Studio already has an overlapping schedule"
  }
}
```

---

# 12. JWT Claims

Minimal claims:

```text
sub
role
iat
exp
```

Contoh:

```json
{
  "sub": "1",
  "role": "ADMIN",
  "iat": 1780000000,
  "exp": 1780086400
}
```

`sub` berisi user ID.

`role` digunakan untuk authorization.

---

# 13. Layering

Gunakan:

```text
Handler
   ↓
Service
   ↓
Repository
   ↓
GORM
   ↓
PostgreSQL
```

### Handler

- Parse HTTP request.
- Validate request.
- Call service.
- Return response.

### Service

- Business rules.
- Authentication.
- Authorization-related decisions.
- Schedule validation.

### Repository

- Query database.
- Create/update/delete data.
- GORM operations.

---

# 14. Security

Login:

```text
Email + Password
       ↓
Find User
       ↓
bcrypt.CompareHashAndPassword
       ↓
Generate JWT
```

Password tidak pernah disimpan plaintext.

JWT secret dibaca dari environment variable.

Contoh:

```env
JWT_SECRET=change-me
JWT_EXPIRE_HOURS=24
```

---

# 15. Swagger

Swagger harus mendokumentasikan:

- Login.
- Authorization.
- Request schema.
- Response schema.
- HTTP status.
- Schedule CRUD.

Generate:

```bash
swag init -g cmd/api/main.go
```

Open:

```text
http://localhost:8080/swagger/index.html
```
