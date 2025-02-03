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


Ensure that this documentation aligns with the implemented functionality in `src/demo_backend_svc/routers/logout.py`.