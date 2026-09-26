# C. Skill Test - API Specification

## 1. Scope

The Golang implementation focuses on the two required capabilities:

1. User Authentication (Login).
2. Screening Schedule Management (Schedule CRUD).

Authorization is enforced via JSON Web Tokens (JWT) obtained from the authentication endpoint.

## 2. Base URL

```text
http://localhost:8088/api/v1
```

## 3. Authentication

Authorization Header:

```http
Authorization: Bearer <JWT>
```

User Roles:

```text
CUSTOMER
ADMIN
```

Role-Based Access Matrix:

| Endpoint | CUSTOMER | ADMIN |
|---|:---:|:---:|
| `GET /schedules` | ✓ | ✓ |
| `GET /schedules/:id` | ✓ | ✓ |
| `POST /schedules` | - | ✓ |
| `PUT /schedules/:id` | - | ✓ |
| `DELETE /schedules/:id` | - | ✓ |

---

# 4. POST /auth/login

Authenticates a user and issues an access token.

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

## Success Response

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

## Invalid Credentials Response

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

Retrieves a list of screening schedules.

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

Retrieves details for a specific schedule by ID.

```http
GET /api/v1/schedules/1
Authorization: Bearer <JWT>
```

Success:

```http
200 OK
```

Not Found:

```http
404 Not Found
```

```json
{
  "error": {
    "code": "SCHEDULE_NOT_FOUND",
    "message": "Schedule not found"
  }
}
```

---

# 7. POST /schedules

Creates a new screening schedule.

Role Required:

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

Input Validation Rules:

```text
movie_id > 0
studio_id > 0
start_time must be valid RFC3339 timestamp
end_time must be valid RFC3339 timestamp
end_time > start_time
```

Business Overlap Validation:

```text
The same studio cannot host two overlapping schedules during the same time window.
```

Success:

```http
201 Created
```

Conflict Response (Overlapping Schedule):

```http
409 Conflict
```

```json
{
  "error": {
    "code": "SCHEDULE_CONFLICT",
    "message": "Studio already has an overlapping schedule in this timeframe"
  }
}
```

---

# 8. PUT /schedules/:id

Updates an existing screening schedule.

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

Role Required:

```text
ADMIN
```

Response:

```http
200 OK
```

---

# 9. DELETE /schedules/:id

Cancels a screening schedule. For enterprise systems, this operation performs a logical cancellation rather than a destructive hard delete.

```http
DELETE /api/v1/schedules/1
Authorization: Bearer <JWT>
```

Role Required:

```text
ADMIN
```

Business Behavior:

```text
status: SCHEDULED → CANCELLED
```

Response:

```http
204 No Content
```

Alternative Response:

```http
200 OK
```

(Returns the updated schedule resource with CANCELLED status).

---

# 10. HTTP Status Codes

The API utilizes standard HTTP status codes:

| Status | Usage |
|---|---|
| `200` | Request succeeded |
| `201` | Resource created successfully |
| `204` | Resource deleted or cancelled successfully |
| `400` | Bad Request / Invalid input validation |
| `401` | Unauthorized / Missing or invalid token |
| `403` | Forbidden / User lacks required role permissions |
| `404` | Resource not found |
| `409` | Conflict with existing business rules (e.g. Studio overlap) |
| `500` | Internal server error |

---

# 11. Error Response Format

A consistent structured error payload is returned on all failures:

```json
{
  "error": {
    "code": "SCHEDULE_NOT_FOUND",
    "message": "Schedule not found"
  }
}
```

Example Conflict Error:

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

Standard token claims:

```text
sub
role
iat
exp
```

Example Payload:

```json
{
  "sub": "1",
  "role": "ADMIN",
  "iat": 1780000000,
  "exp": 1780086400
}
```

- `sub`: User ID
- `role`: Role for RBAC authorization (`ADMIN`, `CUSTOMER`)

---

# 13. Layered Clean Architecture

The API strictly implements clean layered architecture:

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

### Handler Layer
- Parses incoming HTTP requests.
- Validates request payload structures.
- Invokes domain services.
- Formats standard JSON responses and status codes.

### Service Layer
- Enforces domain business logic.
- Verifies authentication credentials.
- Handles authorization decisions.
- Executes schedule overlap collision checks.

### Repository Layer
- Abstracts database persistence.
- Executes GORM queries and relational joins.
- Manages transactional boundaries.

---

# 14. Security Design

Login Workflow:

```text
Email + Password
       ↓
Find User by Email
       ↓
bcrypt.CompareHashAndPassword
       ↓
Generate Signed JWT
```

- Passwords are encrypted using `bcrypt` and never stored in plaintext.
- JWT secret keys and token expiry periods are dynamically loaded from environment variables:

```env
JWT_SECRET=your-secret-key
JWT_EXPIRE_HOURS=24
```

---

# 15. Swagger Documentation

Interactive OpenAPI 2.0 / Swagger documentation provides:

- Authentication endpoint specification.
- Bearer JWT security scheme definition.
- Request and response schemas with data types.
- HTTP status code mapping.
- Interactive Schedule CRUD execution.

Generate Swagger Specification:

```bash
swag init -g cmd/api/main.go
```

Access Swagger UI:

```text
http://localhost:8088/swagger/index.html
```
