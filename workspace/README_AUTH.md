# User Authentication API

## Endpoints

### Register New User
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Login & Get JWT Token
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Get Current User Profile
```
GET /api/auth/me
Authorization: Bearer {token}
```

### Logout
```
POST /api/auth/logout
Authorization: Bearer {token}
```

## Security Features
- JWT token authentication (30 min expiry)
- bcrypt password hashing
- Email validation
- CORS ready for frontend integration