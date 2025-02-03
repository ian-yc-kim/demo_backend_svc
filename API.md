# API Documentation

## Authentication Endpoints

### POST /auth/signup

**Description:**
Endpoint to register a new user. This endpoint creates a new user account after validating the provided credentials.

**HTTP Method:**
POST

**Route:**
/auth/signup

**Request Requirements:**
- **Headers:**
  - Content-Type: application/json
- **Body:**
  - username: (string) Must be 3-30 characters long and can contain alphanumeric characters and underscores.
  - password: (string) Must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.
  - full_name: (optional, string) Full name of the user.

**Response Formats:**

- **Success (201):**
  - **Body:**
    ```json
    { "user_id": "generated-user-id", "username": "newuser" }
    ```

- **Error (400):**
  - Example:
    ```json
    { "detail": "Username already exists" }
    ```

**Examples:**

**Request Example:**
```http
POST /auth/signup HTTP/1.1
Host: <your_domain>
Content-Type: application/json

{
  "username": "newuser",
  "password": "Password@123",
  "full_name": "New User"
}
```

**Successful Response Example:**
```json
{ "user_id": "generated-user-id", "username": "newuser" }
```

---

### POST /auth/login

**Description:**
Endpoint to authenticate a user. Accepts a username and password, and returns a session token upon successful verification.

**HTTP Method:**
POST

**Route:**
/auth/login

**Request Requirements:**
- **Headers:**
  - Content-Type: application/json
- **Body:**
  - username: (string)
  - password: (string)

**Response Formats:**

- **Success (200):**
  - **Body:**
    ```json
    { "session_token": "generated-session-token" }
    ```

- **Error (401):**
  - Example:
    ```json
    { "detail": "Invalid username or password" }
    ```

**Examples:**

**Request Example:**
```http
POST /auth/login HTTP/1.1
Host: <your_domain>
Content-Type: application/json

{
  "username": "existinguser",
  "password": "UserPassword@123"
}
```

**Successful Response Example:**
```json
{ "session_token": "generated-session-token" }
```

---

### POST /auth/logout

**Description:**
Endpoint to log out a user by invalidating the session token.

**HTTP Method:**
POST

**Route:**
/auth/logout

**Request Requirements:**
- **Headers:**
  - Authorization: Must include a valid session token. The token may be prefixed with `Bearer `, which should be removed before processing.
- **Body:**
  No additional payload is required.

**Response Formats:**

- **Success (200):**
  - **Body:**
    ```json
    { "message": "Logout successful" }
    ```

- **Error Cases (401):**
  - **Missing Token:**
    ```json
    { "detail": "Missing session token" }
    ```
  - **Invalid Token:**
    ```json
    { "detail": "Invalid session token" }
    ```
  - **Expired Token:**
    ```json
    { "detail": "Session token expired" }
    ```

- **Internal Server Error (500):**
  - **Body:**
    ```json
    { "detail": "Internal server error" }
    ```

**Examples:**

**Request Example:**
```http
POST /auth/logout HTTP/1.1
Host: <your_domain>
Authorization: Bearer your_session_token
```

**Successful Response Example:**
```json
{ "message": "Logout successful" }
```

---

### GET /auth/session

**Description:**
Endpoint to validate a session token and return the corresponding user's details.

**HTTP Method:**
GET

**Route:**
/auth/session

**Request Requirements:**
Clients must provide the session token either via the header (`session_token`) or as a query parameter (`session_token`).

- **Header:**
  - Key: `session_token`
  - Value: your session token
- **Query Parameter:**
  - Key: `session_token`
  - Value: your session token

If the session token is not provided, the server responds with a 401 Unauthorized error:

```json
{ "detail": "Session token is missing" }
```

**Response Formats:**

- **Success (200):**
  - **Body:**
    ```json
    { "username": "exampleuser", "full_name": "Example User" }
    ```

- **Error Cases (401):**
  - **Missing Token:**
    ```json
    { "detail": "Session token is missing" }
    ```
  - **Invalid Token:**
    ```json
    { "detail": "Invalid session token" }
    ```
  - **Expired Token:**
    ```json
    { "detail": "Session token expired" }
    ```

- **Internal Server Error (500):**
  - **Body:**
    ```json
    { "detail": "Internal server error" }
    ```

**Examples:**

**Request Example using Header:**
```http
GET /auth/session HTTP/1.1
Host: <your_domain>
session_token: your_session_token
```

**Request Example using Query Parameter:**
```http
GET /auth/session?session_token=your_session_token HTTP/1.1
Host: <your_domain>
```

**Successful Response Example:**
```json
{ "username": "exampleuser", "full_name": "Example User" }
```