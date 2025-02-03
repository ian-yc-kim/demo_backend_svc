# API Documentation

## Authentication Endpoints

### POST /logout

**Description:**  
Endpoint to log out a user by invalidating the session token.

**HTTP Method:**  
POST

**Route:**  
/logout

**Request Requirements:**  
- **Headers:**
  - `Authorization`: Must include a valid session token. The token may be prefixed with `Bearer `, which should be removed before processing.
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
POST /logout HTTP/1.1
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

- **Success (HTTP 200):**
  - **Response Body:**
    ```json
    { "username": "exampleuser", "full_name": "Example User" }
    ```

- **Error Cases (HTTP 401):**
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

- **Internal Server Error (HTTP 500):**
  - **Response Body:**
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