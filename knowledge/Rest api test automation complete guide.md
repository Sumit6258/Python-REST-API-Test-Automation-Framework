# REST API Test Automation — Complete Guide
### From Zero to Advanced | Technical Interview Preparation | Practical Day-to-Day Reference

---

## TABLE OF CONTENTS

1. [The Internet & How It Works](#1-the-internet--how-it-works)
2. [What is an API?](#2-what-is-an-api)
3. [What is REST?](#3-what-is-rest)
4. [HTTP — The Language of the Web](#4-http--the-language-of-the-web)
5. [HTTP Status Codes — Complete Reference](#5-http-status-codes--complete-reference)
6. [Authentication & Authorization](#6-authentication--authorization)
7. [JSON — The Data Format](#7-json--the-data-format)
8. [What is Software Testing?](#8-what-is-software-testing)
9. [Types of Testing](#9-types-of-testing)
10. [API Testing — Deep Dive](#10-api-testing--deep-dive)
11. [Test Automation — Why and How](#11-test-automation--why-and-how)
12. [Python for Test Automation](#12-python-for-test-automation)
13. [pytest — The Testing Framework](#13-pytest--the-testing-framework)
14. [The requests Library](#14-the-requests-library)
15. [JSON Schema Validation](#15-json-schema-validation)
16. [JWT — JSON Web Tokens](#16-jwt--json-web-tokens)
17. [Our Framework — Architecture Deep Dive](#17-our-framework--architecture-deep-dive)
18. [CI/CD — Automation in the Cloud](#18-cicd--automation-in-the-cloud)
19. [BDD — Behaviour Driven Development](#19-bdd--behaviour-driven-development)
20. [Design Patterns in Test Automation](#20-design-patterns-in-test-automation)
21. [Interview Questions & Answers](#21-interview-questions--answers)
22. [Real-World Scenarios & Troubleshooting](#22-real-world-scenarios--troubleshooting)
23. [Glossary of Terms](#23-glossary-of-terms)

---

## 1. The Internet & How It Works

### What is the Internet?

The internet is a **global network of computers** that communicate with each other using standardised rules called **protocols**. Think of it as the world's largest postal system — where computers send "letters" (data packets) to each other using addresses (IP addresses).

### The Client-Server Model

Every interaction on the internet follows the **client-server model**:

```
CLIENT                          SERVER
(Your Browser/App)              (The Computer Hosting the API)
      |                               |
      |  ------ REQUEST ---------->  |
      |                               |  (processes the request)
      |  <----- RESPONSE ----------  |
      |                               |
```

- **Client**: The one asking for something (your browser, your mobile app, your test script)
- **Server**: The one providing the service (Google's servers, Amazon's servers, DummyJSON's servers)

### Real-World Analogy

Imagine a **restaurant**:
- You (client) sit at a table and look at the menu
- You tell the waiter (HTTP) what you want
- The waiter goes to the kitchen (server) with your order (request)
- The kitchen prepares the food and gives it to the waiter
- The waiter brings it back to you (response)

The menu defines what you *can* order — that's the **API**.

### IP Addresses and DNS

Every computer on the internet has an **IP address** — a unique numerical label like `142.250.80.46`. But we don't type numbers into browsers — we type names like `google.com`. The **DNS (Domain Name System)** translates those names into IP addresses, just like a phone book converts names to phone numbers.

---

## 2. What is an API?

### Definition

**API stands for Application Programming Interface.** It is a defined way for two software applications to communicate with each other.

An API is essentially a **contract**: "If you send me a request in this specific format, I will send you back a response in this specific format."

### Real-World Analogies

#### The Restaurant Menu (Classic Analogy)
The menu is the API. It tells you:
- What you can order (available endpoints)
- What information you need to provide (request parameters)
- What you will receive (response format)
- What you cannot order (restrictions)

You don't know how the kitchen works, how the chef makes the dish, or where the ingredients came from. You just follow the menu. This is called **abstraction** — hiding complexity behind a simple interface.

#### The Power Socket Analogy
A power socket is an API. Every device that follows the standard (two/three prongs, correct voltage) can plug in and use electricity. The device doesn't need to know how electricity is generated at the power plant. The socket is the interface.

#### The ATM Machine
When you insert your card and request cash:
- You are the **client**
- The ATM's interface (buttons, screen, card slot) is the **API**
- The bank's backend systems are the **server**
- Your PIN is **authentication**
- Your account balance check is a **GET request**
- Your cash withdrawal is a **POST/DELETE request** (creates a transaction, reduces balance)

### Why APIs Exist

1. **Separation of concerns** — Frontend doesn't need to know how the database works
2. **Reusability** — One API can serve a website, a mobile app, and a third-party app simultaneously
3. **Security** — Clients never directly access the database
4. **Scalability** — API servers can be scaled independently
5. **Business value** — Companies monetise their data through APIs (Stripe, Twilio, Google Maps)

### Types of APIs

| Type | Description | Example |
|---|---|---|
| **REST** | Uses HTTP, most common | Twitter API, GitHub API |
| **GraphQL** | Query language, flexible | Facebook API |
| **SOAP** | XML-based, older standard | Banking systems |
| **gRPC** | Binary, high performance | Internal microservices |
| **WebSocket** | Real-time, two-way | Chat applications |

---

## 3. What is REST?

### Definition

**REST stands for Representational State Transfer.** It is an **architectural style** (a set of rules/guidelines) for designing APIs over HTTP, defined by Roy Fielding in his 2000 PhD dissertation.

REST is not a protocol or a standard — it's a philosophy. An API that follows REST principles is called **RESTful**.

### The 6 Constraints of REST

#### 1. Client-Server Separation
The client and server are completely independent. The client doesn't know about database schemas. The server doesn't know about UI design. They communicate only through the API interface.

*Real example: Instagram's mobile app (client) and Instagram's servers (server) are completely separate. Instagram can redesign their app without changing the server, and can upgrade their servers without changing the app.*

#### 2. Statelessness ⭐ (Most Important)
**Every request must contain ALL information needed to process it.** The server does not store any client context between requests.

```
STATEFUL (Bad for REST):
Request 1: "Login as user john"       → Server remembers "john is logged in"
Request 2: "Get my profile"           → Server knows to get john's profile
                                         (depends on state from request 1)

STATELESS (REST):
Request 1: "Login" → Server returns token "abc123"
Request 2: "Get profile" + "Authorization: Bearer abc123"
                                      → Server doesn't remember request 1,
                                         but the token tells it everything it needs
```

*Why this matters: Stateless servers can be scaled horizontally — any server in a cluster can handle any request because no state is stored on the server.*

#### 3. Cacheability
Responses should indicate whether they can be cached. GET responses for unchanged resources (like a product list) can be cached by browsers/proxies to reduce server load.

#### 4. Uniform Interface
All REST APIs follow the same conventions — same HTTP methods, same URL structure, same status codes. This makes APIs predictable and learnable.

#### 5. Layered System
The client doesn't need to know whether it's talking directly to the server or through intermediaries (load balancers, caches, gateways). This enables security and scalability.

#### 6. Code on Demand (Optional)
Servers can send executable code to clients (like JavaScript). This is rarely used.

### REST Resources and URLs

In REST, everything is a **resource** — a noun, not a verb.

```
WRONG (verb-based — not RESTful):
GET /getUser
POST /createUser
POST /deleteUser/5

CORRECT (resource-based — RESTful):
GET    /users        ← Get all users
GET    /users/5      ← Get user with ID 5
POST   /users        ← Create a new user
PUT    /users/5      ← Replace user 5 completely
PATCH  /users/5      ← Partially update user 5
DELETE /users/5      ← Delete user 5
```

The URL identifies the **resource** (what). The HTTP method identifies the **action** (how).

### Nested Resources

```
GET  /users/5/posts          ← All posts by user 5
GET  /users/5/posts/12       ← Post 12 by user 5
POST /users/5/posts          ← Create a post for user 5
DELETE /users/5/posts/12     ← Delete post 12 by user 5
```

---

## 4. HTTP — The Language of the Web

### What is HTTP?

**HTTP stands for HyperText Transfer Protocol.** It is the set of rules governing how messages are formatted and transmitted between clients and servers on the web.

**HTTPS** = HTTP + **S**ecure (encrypted using TLS/SSL). Today, almost all APIs use HTTPS.

### Anatomy of an HTTP Request

Every HTTP request has 4 parts:

```
POST /auth/login HTTP/1.1                    ← 1. Request Line (Method + URL + Version)
Host: dummyjson.com                          ← 2. Headers (metadata)
Content-Type: application/json               ←    (key: value pairs)
Authorization: Bearer eyJhbGc...             ←
Accept: application/json                     ←
                                             ← 3. Blank line (separates headers from body)
{                                            ← 4. Body (the actual data being sent)
  "username": "emilys",
  "password": "emilyspass"
}
```

### Anatomy of an HTTP Response

```
HTTP/1.1 200 OK                              ← 1. Status Line (version + code + message)
Content-Type: application/json               ← 2. Headers
Content-Length: 284                          ←
Set-Cookie: session=abc123                   ←
                                             ← 3. Blank line
{                                            ← 4. Body (the data being returned)
  "id": 1,
  "username": "emilys",
  "accessToken": "eyJhbGciOiJIUzI1..."
}
```

### HTTP Methods (Verbs)

| Method | Purpose | Has Body? | Idempotent? | Safe? |
|---|---|---|---|---|
| **GET** | Retrieve data | No | Yes | Yes |
| **POST** | Create new resource | Yes | No | No |
| **PUT** | Replace entire resource | Yes | Yes | No |
| **PATCH** | Partially update resource | Yes | No | No |
| **DELETE** | Remove resource | Sometimes | Yes | No |
| **HEAD** | Like GET but no body | No | Yes | Yes |
| **OPTIONS** | What methods are allowed? | No | Yes | Yes |

**Idempotent** means calling it multiple times produces the same result:
- `DELETE /users/5` called 100 times → user 5 is deleted (same result every time)
- `POST /users` called 100 times → 100 new users created (different result each time!)

**Safe** means it doesn't change server state (read-only).

### Common HTTP Headers

```
REQUEST HEADERS:
Content-Type: application/json      ← "I'm sending JSON"
Accept: application/json            ← "I want JSON back"
Authorization: Bearer <token>       ← "Here's my credentials"
User-Agent: python-requests/2.31    ← "I'm a Python script"
X-Request-ID: abc-123-def           ← "Here's a tracking ID for this request"

RESPONSE HEADERS:
Content-Type: application/json      ← "I'm sending JSON back"
Content-Length: 284                 ← "The body is 284 bytes"
Cache-Control: no-cache             ← "Don't cache this response"
X-RateLimit-Remaining: 99          ← "You have 99 API calls left"
```

### Query Parameters vs Path Parameters vs Request Body

```python
# PATH PARAMETER — Identifies a specific resource
GET /users/42               # 42 is a path parameter — "give me user 42"

# QUERY PARAMETER — Filters/modifies the request
GET /users?limit=10&skip=20  # limit and skip are query parameters
GET /users?search=john&role=admin

# REQUEST BODY — Complex data, used in POST/PUT/PATCH
POST /users/add
Body: {"firstName": "John", "lastName": "Doe", "age": 25}
```

**Interview Tip**: Query parameters appear after `?` in the URL and are separated by `&`. Path parameters are embedded directly in the URL path. Request bodies carry structured data and are used for creating/updating resources.

---

## 5. HTTP Status Codes — Complete Reference

Status codes are 3-digit numbers that tell the client what happened. They are grouped into five families:

### 1xx — Informational (Rare in APIs)

| Code | Name | Meaning |
|---|---|---|
| 100 | Continue | Server received request headers, client should proceed |
| 101 | Switching Protocols | Server is switching to WebSocket |

### 2xx — Success ✅

| Code | Name | When to Use | Real Example |
|---|---|---|---|
| **200** | OK | Standard success for GET, PUT, PATCH | `GET /users/1` → user found |
| **201** | Created | Resource was created (POST) | `POST /users/add` → new user created |
| **202** | Accepted | Request accepted but processing async | File upload queued for processing |
| **204** | No Content | Success but no body to return | `DELETE /users/5` → deleted, nothing to return |

### 3xx — Redirection

| Code | Name | When to Use |
|---|---|---|
| 301 | Moved Permanently | URL has changed forever, update your bookmark |
| 302 | Found | Temporary redirect |
| 304 | Not Modified | Cache is still valid, no need to send data again |

### 4xx — Client Errors ❌ (Your Fault)

| Code | Name | When to Use | Real Example |
|---|---|---|---|
| **400** | Bad Request | Malformed request, validation failed | Missing required field |
| **401** | Unauthorized | Not authenticated (no login) | No token provided |
| **403** | Forbidden | Authenticated but not authorised | Regular user trying to access admin page |
| **404** | Not Found | Resource doesn't exist | `GET /users/9999` → no such user |
| **405** | Method Not Allowed | Wrong HTTP method for this endpoint | `DELETE /users` (can't delete all users) |
| **409** | Conflict | Resource conflict | Creating a user with an email that already exists |
| **422** | Unprocessable Entity | Validation error (correct format, wrong content) | Age field = "abc" instead of a number |
| **429** | Too Many Requests | Rate limit exceeded | Sending 1000 requests per second |

### 5xx — Server Errors 🔥 (Their Fault)

| Code | Name | When to Use | Real Example |
|---|---|---|---|
| **500** | Internal Server Error | Unexpected server crash | Unhandled exception in backend code |
| **502** | Bad Gateway | Server got invalid response from upstream | Load balancer can't reach backend |
| **503** | Service Unavailable | Server is down/overloaded | Maintenance window |
| **504** | Gateway Timeout | Upstream took too long | Database query timeout |

### Interview Tips on Status Codes

> **Q: What's the difference between 401 and 403?**
> A: 401 means "I don't know who you are" (you're not logged in). 403 means "I know who you are, but you're not allowed to do this" (you're logged in but lack permission).

> **Q: When would you use 200 vs 201?**
> A: 200 for successful reads/updates, 201 specifically for when a new resource was created. The difference helps clients know whether something new was created.

> **Q: What's the difference between 400 and 422?**
> A: 400 is for malformed requests (wrong JSON syntax, missing headers). 422 is for well-formed requests with invalid content (correct JSON but the data fails business validation).

---

## 6. Authentication & Authorization

These are two different concepts that are often confused:

### Authentication vs Authorization

```
Authentication = WHO ARE YOU?
"Proving your identity"
Like: Showing your passport at border control

Authorization = WHAT ARE YOU ALLOWED TO DO?
"Proving you have permission"
Like: Having a VIP ticket to enter backstage
```

You can be **authenticated but not authorized** — logged in to Netflix but trying to access someone else's account.

### Common Authentication Methods

#### 1. Basic Authentication
```
Authorization: Basic dXNlcjpwYXNzd29yZA==
```
The username:password are Base64 encoded (not encrypted!). Only use with HTTPS.

#### 2. API Keys
```
Authorization: Api-Key your-api-key-here
# OR
GET /users?api_key=your-api-key-here
```
Simple tokens issued to clients. Used by many public APIs (Google Maps, Stripe). No expiry by default.

#### 3. Bearer Token / JWT (Most Common)
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
A token is issued on login and sent with every subsequent request. The server validates the token without needing to look up a session in a database.

#### 4. OAuth 2.0
A delegated authorisation framework. When you click "Sign in with Google", that's OAuth 2.0. The user grants permission to a third-party app without sharing their password.

```
Flow:
1. User clicks "Login with Google" on your app
2. Your app redirects to Google
3. User logs in to Google and grants permission
4. Google redirects back with an authorization code
5. Your app exchanges the code for an access token
6. Your app uses the access token to call Google APIs
```

### JWT — JSON Web Tokens (Deep Dive)

A JWT is a self-contained token that carries information about the user.

#### Structure (3 parts separated by dots)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJlbWlseXMiLCJleHAiOjE3MDAwMDAwMDB9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
     HEADER                                              PAYLOAD                                                          SIGNATURE
```

```json
// HEADER (decoded)
{
  "alg": "HS256",    // Algorithm used for signing
  "typ": "JWT"       // Token type
}

// PAYLOAD (decoded) — the claims
{
  "id": 1,
  "username": "emilys",
  "email": "emily.johnson@x.dummyjson.com",
  "iat": 1699000000,    // Issued At (Unix timestamp)
  "exp": 1699003600     // Expiry (1 hour later)
}

// SIGNATURE — verifies the token hasn't been tampered with
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

#### Why JWTs are Powerful
- **Stateless**: The server doesn't need to store sessions — all info is in the token
- **Self-contained**: The token carries user info, so no database lookup needed
- **Verifiable**: The signature proves the token wasn't tampered with
- **Cross-domain**: Works across different services (microservices)

#### JWT Security Considerations
- Never put sensitive data (passwords) in JWT payload — it's only Base64 encoded, not encrypted
- Always validate the signature
- Always check expiry (`exp` claim)
- Use short expiry times for access tokens (15 min - 1 hour)
- Use refresh tokens for long-lived sessions

---

## 7. JSON — The Data Format

### What is JSON?

**JSON stands for JavaScript Object Notation.** It is a lightweight, human-readable format for storing and transmitting data. It has become the universal language of REST APIs.

### JSON Data Types

```json
{
  "string_value":  "Hello, World",
  "integer_value": 42,
  "float_value":   3.14159,
  "boolean_true":  true,
  "boolean_false": false,
  "null_value":    null,
  "array_value":   [1, 2, 3, "four", true],
  "object_value":  {
    "nested_key": "nested_value",
    "another_key": 123
  }
}
```

### JSON Rules (Strict Syntax)
- Keys must be **strings in double quotes** (`"key"` not `key` or `'key'`)
- No trailing commas
- No comments
- Strings must use double quotes (not single quotes)
- `true`, `false`, `null` are lowercase

### JSON vs Python Dictionary

```python
# JSON (text string)
json_string = '{"name": "John", "age": 30, "active": true}'

# Python Dictionary (in-memory object)
python_dict = {"name": "John", "age": 30, "active": True}
# Note: true vs True — Python uses capitalised booleans

import json

# JSON string → Python dict
data = json.loads(json_string)

# Python dict → JSON string
text = json.dumps(python_dict)
```

### Common API Response Structures

#### Single Resource
```json
{
  "id": 1,
  "firstName": "Emily",
  "lastName": "Johnson",
  "email": "emily.johnson@x.dummyjson.com",
  "age": 28,
  "image": "https://dummyjson.com/icon/emilys/128"
}
```

#### Collection of Resources
```json
{
  "users": [...],
  "total": 208,
  "skip": 0,
  "limit": 30
}
```

#### Error Response
```json
{
  "message": "User with id '9999' not found"
}
```

---

## 8. What is Software Testing?

### Definition

Software testing is the process of **evaluating software to ensure it meets requirements and works correctly**. It involves executing a program with the intent of finding defects (bugs).

### The Cost of Bugs

The later a bug is found in the software development lifecycle (SDLC), the more expensive it is to fix:

```
Development:     $1      (developer finds bug while coding)
Testing:         $10     (tester finds bug in QA)
UAT:             $100    (user finds bug in acceptance testing)
Production:      $1,000+ (customer finds bug after release)
Critical System: $1M+    (NASA, medical devices, banks)
```

*Famous example: The Ariane 5 rocket explosion in 1996 was caused by a software bug (integer overflow) that cost $370 million.*

### The Testing Pyramid

```
          /\
         /  \
        / E2E\        ← Fewer tests, slow, expensive, fragile
       /------\
      / Integr \      ← Medium number, medium speed
     /----------\
    /    Unit    \    ← Many tests, fast, cheap, reliable
   /______________\
```

#### Unit Tests (Base of pyramid)
- Test a **single function or class in isolation**
- Fast (milliseconds), cheap, run thousands per second
- No database, no network, no external dependencies
- Use **mocks** to simulate dependencies

```python
# Unit test example
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5      # Tests the function in complete isolation
```

#### Integration Tests (Middle)
- Test **how multiple components work together**
- Test that your code + the database work correctly
- Test that your code + an external API work correctly
- Our framework is primarily integration tests (testing our code + DummyJSON API)

#### End-to-End Tests (Top)
- Test **the entire application from user's perspective**
- Browser automation (Selenium, Playwright, Cypress)
- Slow, brittle, expensive, but test the complete user journey

### ISTQB Testing Principles (Standard Theory)

1. **Testing shows the presence of defects, not their absence** — You can't prove software is bug-free, only find bugs
2. **Exhaustive testing is impossible** — Can't test every combination; use risk-based testing
3. **Early testing saves money** — Test as early as possible (shift-left testing)
4. **Defects cluster** — 80% of bugs come from 20% of the code (Pareto principle)
5. **Beware of the pesticide paradox** — Running the same tests repeatedly stops finding new bugs; keep updating tests
6. **Testing is context-dependent** — Testing a pacemaker is different from testing a blog
7. **Absence-of-errors fallacy** — A bug-free system that doesn't meet user needs is still a failure

---

## 9. Types of Testing

### Functional Testing
Tests that the software **does what it's supposed to do**.

| Type | Description | API Example |
|---|---|---|
| **Smoke Testing** | Quick check — is it even alive? | Does `GET /users` return 200? |
| **Sanity Testing** | Focused check on a specific fix | Did fixing login break anything? |
| **Regression Testing** | Ensure new changes didn't break old features | Run all tests after every deployment |
| **Integration Testing** | Components work together | Does login + profile fetch work end-to-end? |
| **System Testing** | Test the complete system | All endpoints, all scenarios |
| **UAT** | User acceptance testing | Business stakeholders validate it works |

### Non-Functional Testing
Tests **how well** the software works.

| Type | Description | API Example |
|---|---|---|
| **Performance Testing** | How fast? | `GET /users` should respond in <200ms |
| **Load Testing** | Can it handle expected traffic? | 100 concurrent users for 30 minutes |
| **Stress Testing** | What's the breaking point? | Ramp up until the server fails |
| **Security Testing** | Is it safe from attacks? | SQL injection, XSS, authentication bypass |
| **Usability Testing** | Is the API easy to use? | Are error messages clear and helpful? |

### Test Levels by Who Performs Them

| Level | Who | Focus |
|---|---|---|
| Unit Testing | Developer | Individual functions |
| Integration Testing | Developer/QA | Component interaction |
| System Testing | QA | Complete application |
| Acceptance Testing | Business/User | Business requirements |

---

## 10. API Testing — Deep Dive

### What Makes API Testing Unique?

Unlike UI testing (clicking buttons), API testing directly calls the **service layer** — bypassing the user interface entirely. This makes it:
- **Faster** — No browser rendering overhead
- **More reliable** — No UI flakiness
- **Earlier** — Can test before the UI is built
- **More comprehensive** — Can test scenarios impossible through UI (invalid data, edge cases)

### The Layers of a Web Application

```
┌──────────────────────────────┐
│     PRESENTATION LAYER       │  ← UI Tests (Selenium, Cypress)
│  (Browser, Mobile App, UI)   │
├──────────────────────────────┤
│       API LAYER              │  ← API Tests (Our Framework!)
│  (REST/GraphQL Endpoints)    │
├──────────────────────────────┤
│       SERVICE LAYER          │  ← Integration Tests
│  (Business Logic)            │
├──────────────────────────────┤
│       DATA LAYER             │  ← Unit Tests
│  (Database, Cache)           │
└──────────────────────────────┘
```

### What to Test in an API

#### 1. Functionality Testing
```python
# Does it return the right data?
response = client.get("/users/1")
assert response.json()["firstName"] == "Emily"

# Does it correctly create resources?
response = client.post("/users/add", json={"firstName": "John"})
assert "id" in response.json()

# Does it correctly update resources?
response = client.put("/users/1", json={"firstName": "Updated"})
assert response.json()["firstName"] == "Updated"
```

#### 2. Status Code Validation
```python
# Happy path
assert response.status_code == 200

# Created
assert response.status_code == 201

# Not found
assert response.status_code == 404

# Unauthorized
assert response.status_code == 401
```

#### 3. Schema Validation
```python
# Structure must match the contract
validate_schema(response.json(), USER_SCHEMA)
# This checks: correct fields, correct types, correct constraints
```

#### 4. Response Time / Performance
```python
import time
start = time.perf_counter()
response = client.get("/users")
elapsed = time.perf_counter() - start
assert elapsed < 2.0, f"Too slow: {elapsed:.2f}s"
```

#### 5. Header Validation
```python
content_type = response.headers.get("Content-Type", "")
assert "application/json" in content_type
```

#### 6. Security Testing
```python
# Endpoint should reject unauthenticated requests
response = client.get("/auth/me")  # no token
assert response.status_code == 401

# Expired/invalid token should be rejected
bad_client = APIClient(token="invalid.token.here")
response = bad_client.get("/auth/me")
assert response.status_code in (401, 403)
```

#### 7. Error Handling / Negative Testing
```python
# Non-existent resource
response = client.get("/users/9999")
assert response.status_code == 404
assert "message" in response.json()  # Meaningful error message

# Invalid data
response = client.post("/auth/login", json={})  # empty body
assert response.status_code == 400
```

#### 8. Boundary Testing
```python
# Large page number
response = client.get("/users", params={"skip": 99999})
assert response.json()["users"] == []

# Very long string
response = client.post("/users/add", json={"firstName": "A" * 300})
assert response.status_code < 500  # Must not crash the server
```

### The CRUD Testing Matrix

For every resource in an API, systematically test:

```
RESOURCE: /users
+----------+--------+------+-------+-------+--------+
| Scenario | GET    | POST | PUT   | PATCH | DELETE |
+----------+--------+------+-------+-------+--------+
| Valid    | 200 ✓  | 201✓ | 200 ✓ | 200 ✓ | 200 ✓  |
| Invalid  | 400 ✓  | 400✓ | 400 ✓ | 400 ✓ | 400 ✓  |
| NotFound | 404 ✓  | N/A  | 404 ✓ | 404 ✓ | 404 ✓  |
| Unauth   | 401 ✓  | 401✓ | 401 ✓ | 401 ✓ | 401 ✓  |
| Forbidden| 403 ✓  | 403✓ | 403 ✓ | 403 ✓ | 403 ✓  |
+----------+--------+------+-------+-------+--------+
```

---

## 11. Test Automation — Why and How

### Manual vs Automated Testing

| Aspect | Manual Testing | Automated Testing |
|---|---|---|
| Speed | Slow (minutes per test) | Fast (milliseconds per test) |
| Accuracy | Human error possible | Always exact |
| Cost | High (human time) | High upfront, low ongoing |
| Repetition | Tedious and error-prone | Tireless |
| Coverage | Limited by time | Can run thousands of tests |
| Best For | Exploratory, usability | Regression, repetitive checks |

### The Automation Pyramid in Practice

```
For our framework (76 tests, 36 seconds):

17 Error/Edge Case tests    ← Verify failure handling
8  Pagination tests         ← Verify data navigation
16 User CRUD tests          ← Core business functionality
12 Login/Auth tests         ← Security & authentication
 3 JWT Helper tests         ← Framework internal tools (unit)
```

### Test Automation Principles

#### DRY — Don't Repeat Yourself
```python
# BAD — repeated code
def test_users_1():
    response = requests.get("https://dummyjson.com/users", headers={"Content-Type": "application/json"})
    assert response.status_code == 200

def test_users_2():
    response = requests.get("https://dummyjson.com/users", headers={"Content-Type": "application/json"})
    assert response.json()["total"] > 0

# GOOD — shared APIClient handles the repeated parts
def test_users_1(client):
    response = client.get("/users")
    assert_status_code(response, 200)

def test_users_2(client):
    response = client.get("/users")
    assert response.json()["total"] > 0
```

#### FIRST Principles for Good Tests
- **F**ast — Tests should run quickly
- **I**ndependent — Tests should not depend on each other
- **R**epeatable — Same result every run, regardless of environment
- **S**elf-validating — Tests should clearly pass or fail (no manual interpretation)
- **T**imely — Tests should be written alongside or before the code

#### AAA Pattern — Test Structure
Every test should have 3 sections:

```python
def test_create_user_first_name_matches(client):
    # ARRANGE — Set up the test data
    user_data = {"firstName": "John", "lastName": "Smith", "age": 25}

    # ACT — Perform the action being tested
    response = client.post("/users/add", json=user_data)

    # ASSERT — Verify the outcome
    assert response.json().get("firstName") == "John"
```

---

## 12. Python for Test Automation

### Why Python?

1. **Simple syntax** — Readable, close to English
2. **Rich ecosystem** — pytest, requests, selenium, playwright all have excellent Python support
3. **Industry standard** — Most test automation frameworks support Python
4. **Quick to write** — Less boilerplate than Java/C#
5. **Wide adoption** — Large community, tons of resources

### Python Concepts Used in Our Framework

#### Virtual Environments
```bash
# Why: Isolate project dependencies
# Without venv, all projects share one Python environment — conflicts!

python -m venv venv          # Create virtual environment
source venv/bin/activate     # Activate (Mac/Linux)
venv\Scripts\activate        # Activate (Windows)
pip install -r requirements.txt  # Install dependencies INTO venv
```

#### Type Hints (Python 3.5+)
```python
# Without type hints (harder to understand)
def login(client, username, password):
    ...

# With type hints (clear contract)
def login(client: APIClient, username: str, password: str) -> str:
    ...
```

#### Dataclasses and Classes
```python
class APIClient:
    def __init__(self, token: str | None = None):
        self.session = requests.Session()
        self.token = token
        # Sets up the reusable HTTP session
```

#### Decorators
```python
@pytest.mark.smoke          # Marks test as smoke test
@pytest.mark.parametrize    # Runs test with multiple inputs
@pytest.fixture             # Creates reusable test setup
```

#### f-strings
```python
url = f"{self.base_url}{endpoint}"
# f-strings are faster and more readable than .format() or % formatting
```

#### Context Managers
```python
with open("file.txt") as f:    # Automatically closes file
    data = f.read()
```

#### List Comprehensions
```python
# Traditional
ids = []
for user in all_users:
    ids.append(user["id"])

# List comprehension (Pythonic)
ids = [user["id"] for user in all_users]
```

#### Dictionary `.get()` Method
```python
# Dangerous — raises KeyError if key doesn't exist
name = response_body["name"]

# Safe — returns None (or default) if key missing
name = response_body.get("name")
name = response_body.get("name", "Unknown")  # with default
```

---

## 13. pytest — The Testing Framework

### What is pytest?

pytest is the most popular Python testing framework. It discovers and runs tests, provides fixtures, parametrisation, and plugins.

### Test Discovery Rules

pytest automatically finds tests by looking for:
- Files named `test_*.py` or `*_test.py`
- Classes named `Test*`
- Functions named `test_*`

```python
# pytest WILL find these:
tests/test_login.py
tests/test_users.py

class TestLoginSuccess:
    def test_login_returns_200(self):
        ...

# pytest WON'T find these:
tests/login_tests.py      ← wrong filename pattern
class LoginTests:          ← missing "Test" prefix
def check_login():         ← missing "test_" prefix
```

### Fixtures — Setup and Teardown

Fixtures are functions that provide **shared setup** for tests. They run before (and optionally after) each test.

```python
# BASIC FIXTURE
@pytest.fixture
def client():
    return APIClient()     # Creates a fresh client for each test

# SCOPED FIXTURE — reuse across multiple tests
@pytest.fixture(scope="module")   # Created once per module (file)
def client():
    return APIClient()

# Scopes:
# "function" (default) — new instance for each test
# "class"              — shared within a class
# "module"             — shared within a file
# "session"            — shared for entire test run

# FIXTURE WITH TEARDOWN
@pytest.fixture
def temp_user(client):
    # SETUP: Create a user for the test
    response = client.post("/users/add", json={"firstName": "Temp"})
    user_id = response.json()["id"]

    yield user_id           # Hand the user_id to the test

    # TEARDOWN: Runs after the test, even if it fails
    client.delete(f"/users/{user_id}")
```

### Parametrize — Running One Test with Multiple Inputs

```python
# Instead of writing 6 separate identical tests:
@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5, 6])
def test_users_are_retrievable_by_id(client, user_id):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
# This creates 6 test cases: test_users_are_retrievable_by_id[1]
#                                                             ...[2]... etc.

# Multiple parameters
@pytest.mark.parametrize("method,endpoint,expected_status", [
    ("GET",    "/users/1",   200),
    ("GET",    "/users/999", 404),
    ("DELETE", "/users/1",   200),
])
def test_endpoints(client, method, endpoint, expected_status):
    response = client.request(method, endpoint)
    assert response.status_code == expected_status
```

### Markers — Organising and Filtering Tests

```python
# Define custom markers in pytest.ini
[pytest]
markers =
    smoke: Quick sanity checks
    regression: Full regression suite
    auth: Authentication tests
    users: User management tests

# Apply markers in tests
@pytest.mark.smoke
@pytest.mark.auth
class TestLoginSuccess:
    def test_login_returns_200(self, client):
        ...

# Run specific markers from command line
pytest -m smoke              # Only smoke tests
pytest -m "auth and users"   # Auth AND users tests
pytest -m "not regression"   # Everything except regression
```

### pytest.ini — Configuration

```ini
[pytest]
testpaths = tests                     # Where to look for tests
addopts = --html=reports/report.html  # Always generate HTML report
          -v                          # Verbose output
          --tb=short                  # Short traceback on failure
log_cli = true                        # Show logs in console
markers =
    smoke: Smoke tests
    regression: Regression tests
    auth: Authentication tests
```

### conftest.py — Shared Fixtures

`conftest.py` is a special file that pytest automatically loads. Fixtures defined here are available to ALL test files without importing.

```python
# tests/conftest.py
@pytest.fixture(scope="session")
def api_client():
    """Shared client for entire test session."""
    return APIClient()

@pytest.fixture(scope="session")
def authenticated_client(api_client):
    """Client with valid auth token — logs in once for all tests."""
    response = api_client.post("/auth/login", json={
        "username": settings.LOGIN_USERNAME,
        "password": settings.LOGIN_PASSWORD
    })
    token = response.json()["accessToken"]
    api_client.set_token(token)
    return api_client
```

### Assertions in pytest

pytest rewrites `assert` statements to give detailed error messages:

```python
# Simple assert
assert response.status_code == 200
# If fails: AssertionError: assert 404 == 200

# With message
assert response.status_code == 200, f"Expected 200, got {response.status_code}"

# pytest.raises — asserting that exceptions occur
with pytest.raises(ValueError):
    int("not a number")

with pytest.raises(jwt.ExpiredSignatureError):
    decode_jwt_token(expired_token)
```

---

## 14. The requests Library

### What is requests?

The `requests` library is the most popular Python library for making HTTP requests. It wraps Python's built-in `urllib` with a much cleaner API.

```bash
pip install requests
```

### Basic Usage

```python
import requests

# GET request
response = requests.get("https://dummyjson.com/users/1")

# POST request with JSON body
response = requests.post(
    "https://dummyjson.com/auth/login",
    json={"username": "emilys", "password": "emilyspass"}
)

# The response object
print(response.status_code)     # 200
print(response.headers)         # {'Content-Type': 'application/json', ...}
print(response.text)            # Raw string body
print(response.json())          # Parsed Python dictionary
print(response.url)             # Final URL (after redirects)
print(response.elapsed)         # How long it took
```

### requests.Session

A Session object persists settings (headers, cookies, authentication) across multiple requests. More efficient because it reuses the underlying TCP connection.

```python
# Without Session — new connection every request (inefficient)
requests.get("https://api.example.com/users")
requests.get("https://api.example.com/products")

# With Session — reuses connection (efficient)
session = requests.Session()
session.headers.update({"Authorization": "Bearer token123"})
session.get("https://api.example.com/users")    # Token included automatically
session.get("https://api.example.com/products") # Token included automatically
```

### Our APIClient Class Explained

```python
class APIClient:
    def __init__(self, base_url=settings.BASE_URL, token=None):
        self.session = requests.Session()      # Reusable session
        self.base_url = base_url
        self.token = token

        # Set up retry logic — retry on server errors
        adapter = HTTPAdapter(max_retries=Retry(
            total=3,                           # Max 3 retries
            backoff_factor=0.3,                # Wait 0.3s, 0.6s, 1.2s between retries
            status_forcelist=[429, 500, 502, 503, 504]  # Retry on these codes
        ))
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"

        # Inject auth token if present
        headers = kwargs.pop("headers", {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        # Log the request
        log.info(f"→ {method} {url}")

        # Make the actual request
        response = self.session.request(method, url, headers=headers, **kwargs)

        # Log the response
        log.info(f"← {method} {url} [{response.status_code}]")

        return response
```

### Handling Responses Safely

```python
# DANGEROUS — crashes if response is not JSON
data = response.json()

# SAFER — check content type first
if "application/json" in response.headers.get("Content-Type", ""):
    data = response.json()
else:
    print(f"Non-JSON response: {response.text}")

# Or catch the exception
try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print(f"Could not parse JSON: {response.text}")
```

---

## 15. JSON Schema Validation

### What is JSON Schema?

JSON Schema is a vocabulary that allows you to **annotate and validate JSON documents**. It defines the structure, types, and constraints that a valid JSON document must satisfy.

Think of it as a **blueprint** or **contract** for your API responses.

### Why Validate Schemas?

A status code of 200 only tells you the request succeeded. It doesn't tell you:
- Were the right fields returned?
- Are the data types correct?
- Is the `id` actually a number and not a string?
- Is the `email` field present?

Schema validation catches **contract violations** — when the API returns the right status code but wrong data.

### Schema Definition Example

```python
USER_SCHEMA = {
    "type": "object",                    # The JSON value must be an object {}

    "required": ["id", "email", "firstName"],  # These keys MUST be present

    "properties": {
        "id": {
            "type": "integer",           # Must be a whole number
            "minimum": 1                 # Must be at least 1
        },
        "email": {
            "type": "string",            # Must be a string
            "format": "email"            # Must match email pattern
        },
        "firstName": {
            "type": "string",
            "minLength": 1               # Must not be empty string
        },
        "lastName": {
            "type": "string",
            "minLength": 1
        },
        "age": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "active": {
            "type": "boolean"            # Must be true or false
        },
        "tags": {
            "type": "array",             # Must be a list
            "items": {
                "type": "string"         # Each item must be a string
            }
        }
    },
    "additionalProperties": False        # No unexpected fields allowed
}
```

### Schema for Paginated Response (DummyJSON)

```python
USER_LIST_SCHEMA = {
    "type": "object",
    "required": ["users", "total", "skip", "limit"],
    "properties": {
        "users": {
            "type": "array",
            "items": USER_SCHEMA         # Each item must match USER_SCHEMA
        },
        "total": {"type": "integer", "minimum": 0},
        "skip":  {"type": "integer", "minimum": 0},
        "limit": {"type": "integer", "minimum": 1}
    }
}
```

### Running Validation

```python
import jsonschema

def validate_schema(instance, schema):
    try:
        jsonschema.validate(instance=instance, schema=schema)
        # No exception = validation passed
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")

# Usage in test
response = client.get("/users/1")
validate_schema(response.json(), USER_SCHEMA)
```

### Common Schema Validation Errors

```
"'id' is a required property"          ← Missing required field
"'abc' is not of type 'integer'"       ← Wrong type
"'email' does not match '^[^@]+@[^@]+$'" ← Format mismatch
"-1 is less than the minimum of 1"    ← Constraint violation
"Additional properties are not allowed" ← Unexpected field
```

---

## 16. JWT — JSON Web Tokens

*(Expanded technical deep-dive)*

### JWT in Our Framework

We use the `PyJWT` library:

```python
import jwt

# GENERATE a token (signs it with our secret key)
def generate_jwt_token(payload, secret="test_secret", expires_in=3600):
    payload = {
        **payload,
        "iat": int(time.time()),               # Issued at
        "exp": int(time.time()) + expires_in   # Expiry
    }
    return jwt.encode(payload, secret, algorithm="HS256")

# DECODE and VERIFY a token
def decode_jwt_token(token, secret="test_secret"):
    return jwt.decode(token, secret, algorithms=["HS256"])
    # Raises jwt.ExpiredSignatureError if token has expired
    # Raises jwt.InvalidTokenError if signature is invalid

# DECODE without verifying (for inspection)
def decode_jwt_unverified(token):
    return jwt.decode(token, options={"verify_signature": False})
```

### Token-Based Auth Flow in Tests

```python
def test_authenticated_request_with_token(client):
    # Step 1: Authenticate
    login_response = client.post("/auth/login", json={
        "username": "emilys",
        "password": "emilyspass"
    })
    assert login_response.status_code == 200

    # Step 2: Extract token
    token = login_response.json()["accessToken"]

    # Step 3: Use token on protected endpoint
    auth_client = APIClient(token=token)
    me_response = auth_client.get("/auth/me")
    assert me_response.status_code == 200
    assert "username" in me_response.json()
```

---

## 17. Our Framework — Architecture Deep Dive

### The 4-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: TESTS                                         │
│  test_login.py | test_users.py | test_pagination.py     │
│  test_error_cases.py                                    │
│  "What to test"                                         │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: HELPERS                                       │
│  utils/helpers.py                                       │
│  assert_status_code() | validate_schema() | get_all_pages() │
│  "How to assert"                                        │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: API CLIENT                                    │
│  utils/api_client.py                                    │
│  get() | post() | put() | patch() | delete()            │
│  "How to communicate"                                   │
├─────────────────────────────────────────────────────────┤
│  LAYER 1: CONFIG                                        │
│  config/settings.py | config/environment.py             │
│  BASE_URL | LOGIN_USERNAME | DEFAULT_TIMEOUT            │
│  "Where to connect and with what"                       │
└─────────────────────────────────────────────────────────┘
```

### Why Layers Matter

**Without layers (bad):**
```python
def test_login():
    response = requests.post(
        "https://dummyjson.com/auth/login",    # URL hardcoded everywhere
        json={"username": "emilys", "password": "emilyspass"},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    assert response.status_code == 200
    # If the URL changes, you update 76 tests
    # If you need to add retry logic, you update 76 tests
```

**With layers (good):**
```python
def test_login(client):
    response = client.post("/auth/login", json={...})
    assert_status_code(response, 200)
    # URL managed in config — change in 1 place
    # Retry logic in APIClient — change in 1 place
    # The test only cares about the business logic
```

### Data Flow: From Test to API and Back

```
test_login.py:
    client.post("/auth/login", json={...})
         ↓
    APIClient._request("POST", "/auth/login", json={...})
         ↓
    Constructs URL: "https://dummyjson.com/auth/login"
    Injects headers: Content-Type, Authorization (if token)
    Logs: "→ POST https://dummyjson.com/auth/login"
         ↓
    session.request("POST", url, json={...}, timeout=30)
         ↓
    [Network: HTTPS request travels to DummyJSON servers]
         ↓
    [DummyJSON processes: validates credentials, generates JWT]
         ↓
    [Network: HTTPS response travels back]
         ↓
    response.status_code = 200
    response.json() = {"accessToken": "eyJ...", "id": 1, ...}
    Logs: "← POST https://dummyjson.com/auth/login [200] 312ms"
         ↓
    Back in test: assert_status_code(response, 200)  ✅
                  validate_schema(response.json(), LOGIN_SUCCESS_SCHEMA) ✅
```

### How conftest.py Fixtures Flow

```python
# conftest.py
@pytest.fixture(scope="module")
def client():
    return APIClient()

# test_users.py
class TestGetUsersList:
    def test_get_users_returns_200(self, client):  # ← pytest injects this
        response = client.get("/users", params={"limit": 10})
        assert response.status_code == 200
    
    def test_get_users_returns_data(self, client):  # ← same instance (module scope)
        response = client.get("/users", params={"limit": 10})
        assert len(response.json()["users"]) > 0
```

pytest matches the parameter name `client` to the fixture named `client` and automatically provides it — this is called **dependency injection**.

### The .env Pattern — Secrets Management

```
# .env file (NEVER commit to git)
BASE_URL=https://dummyjson.com
LOGIN_USERNAME=emilys
LOGIN_PASSWORD=emilyspass
JWT_SECRET=my-super-secret-key

# .env.example file (commit this — shows what variables are needed)
BASE_URL=https://dummyjson.com
LOGIN_USERNAME=your-username-here
LOGIN_PASSWORD=your-password-here
JWT_SECRET=your-secret-here
```

```python
# settings.py
from dotenv import load_dotenv
load_dotenv()   # Reads .env file into environment variables

class Settings:
    BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")  # .env first, default if missing
```

This pattern means:
- Local developers use `.env` with test credentials
- CI/CD systems inject real secrets via environment variables
- No secrets are ever hardcoded or committed to source control

---

## 18. CI/CD — Automation in the Cloud

### What is CI/CD?

**CI = Continuous Integration**: Every time a developer pushes code, automated tests run immediately to catch issues.

**CD = Continuous Delivery/Deployment**: If tests pass, the code is automatically deployed to production.

```
Developer pushes code to GitHub
        ↓
GitHub Actions triggered automatically
        ↓
┌────────────────────────────────────┐
│  CI Pipeline:                      │
│  1. Checkout code                  │
│  2. Install Python + dependencies  │
│  3. Run linting (code quality)     │
│  4. Run pytest tests               │
│  5. Upload test report             │
└────────────────────────────────────┘
        ↓
Tests PASS → Code can be merged/deployed  ✅
Tests FAIL → Developer notified, must fix ❌
```

### Our GitHub Actions Workflow Explained

```yaml
# .github/workflows/ci.yml

name: API Test Automation CI

on:
  push:                    # Run on every push
    branches: [main, develop]
  pull_request:            # Run on every PR
    branches: [main]
  schedule:
    - cron: '0 6 * * *'   # Run every day at 6 AM (nightly regression)
  workflow_dispatch:        # Allow manual trigger from GitHub UI

jobs:
  pytest:
    runs-on: ubuntu-latest   # Run on a fresh Ubuntu virtual machine
    
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]   # Test on 2 operating systems!

    steps:
      - name: Checkout code
        uses: actions/checkout@v3           # Download the repository

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: python -m pytest --html=reports/report.html
        env:
          BASE_URL: ${{ secrets.BASE_URL }}   # Injected from GitHub Secrets
          LOGIN_USERNAME: ${{ secrets.LOGIN_USERNAME }}

      - name: Upload test report
        uses: actions/upload-artifact@v3
        with:
          name: pytest-report
          path: reports/report.html
          retention-days: 30                  # Keep report for 30 days
```

### Benefits of CI/CD for Testing

1. **Immediate feedback** — Know within minutes if your change broke something
2. **Consistency** — Tests run in the same environment every time
3. **Documentation** — Test history shows when bugs were introduced
4. **Confidence** — Merge/deploy with confidence knowing tests passed
5. **Prevention** — Bugs are caught before reaching production

---

## 19. BDD — Behaviour Driven Development

### What is BDD?

BDD is an approach where **tests are written in plain English** that all stakeholders (developers, testers, business analysts, product owners) can read and understand.

It bridges the gap between technical and non-technical team members.

### The Gherkin Language

BDD uses a syntax called **Gherkin** with keywords: `Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But`

```gherkin
Feature: User Authentication
  As a registered user
  I want to be able to log in
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given I have valid credentials
      | username | emilys      |
      | password | emilyspass  |
    When I POST to "/auth/login" with those credentials
    Then the response status code should be 200
    And the response should contain an "accessToken"
    And the token should be a valid JWT

  Scenario: Failed login with wrong password
    Given I have incorrect credentials
      | username | emilys      |
      | password | wrongpassword |
    When I POST to "/auth/login" with those credentials
    Then the response status code should be 400
    And the response should contain a "message" field
```

### Behave (Python BDD Framework)

```python
# steps/login_steps.py
from behave import given, when, then

@given('I have valid credentials')
def step_set_valid_credentials(context):
    context.credentials = {
        "username": "emilys",
        "password": "emilyspass"
    }

@when('I POST to "/auth/login" with those credentials')
def step_post_login(context):
    context.response = context.client.post(
        "/auth/login",
        json=context.credentials
    )

@then('the response status code should be {status_code:d}')
def step_check_status(context, status_code):
    assert context.response.status_code == status_code

@then('the response should contain an "{key}"')
def step_check_key(context, key):
    assert key in context.response.json()
```

### BDD vs Traditional Testing

| Aspect | Traditional (pytest) | BDD (Behave) |
|---|---|---|
| Audience | Developers/QA | All stakeholders |
| Language | Python code | Plain English |
| Readability | Technical | Business-friendly |
| Maintenance | Easier to refactor | More overhead |
| Best For | Unit/integration tests | Acceptance tests |

### When to Use BDD

Use BDD when:
- Business stakeholders want to define/review test scenarios
- You need living documentation that non-technical people can verify
- Acceptance criteria need to be directly testable

Don't use BDD when:
- Working in small dev teams without business stakeholders
- Testing complex technical edge cases (BDD overhead isn't worth it)
- You need fast execution (BDD has more overhead)

---

## 20. Design Patterns in Test Automation

### 1. Page Object Model (POM) — for UI; Equivalent is Client/Helper Pattern for API

In UI testing, POM means creating one class per page. For API testing, we create one class per domain:

```python
# api_client.py — The "page object" for API testing
class APIClient:
    """Encapsulates all HTTP communication."""
    def get(self, endpoint): ...
    def post(self, endpoint): ...

# Could extend to domain-specific clients:
class UserClient(APIClient):
    def get_user(self, user_id): return self.get(f"/users/{user_id}")
    def create_user(self, data): return self.post("/users/add", json=data)
    def delete_user(self, user_id): return self.delete(f"/users/{user_id}")
```

### 2. Factory Pattern — Creating Test Data

```python
# Instead of hardcoding test data everywhere:
class UserFactory:
    @staticmethod
    def create_valid_user():
        return {
            "firstName": f"Test_{int(time.time())}",
            "lastName": "User",
            "age": 25,
            "email": f"test_{int(time.time())}@test.com"
        }

    @staticmethod
    def create_minimal_user():
        return {"firstName": "Min"}

# Usage
user_data = UserFactory.create_valid_user()
response = client.post("/users/add", json=user_data)
```

### 3. Builder Pattern — Fluent Request Building

```python
class RequestBuilder:
    def __init__(self):
        self._data = {}

    def with_first_name(self, name):
        self._data["firstName"] = name
        return self  # Enables method chaining

    def with_age(self, age):
        self._data["age"] = age
        return self

    def build(self):
        return self._data

# Usage
user = (RequestBuilder()
    .with_first_name("John")
    .with_age(30)
    .build())
```

### 4. Singleton Pattern — Single Instance

```python
class APIClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# Always returns the same client object
client = APIClient.get_instance()
```

### 5. Strategy Pattern — Swappable Auth

```python
class TokenAuth:
    def apply(self, session, token):
        session.headers["Authorization"] = f"Bearer {token}"

class ApiKeyAuth:
    def apply(self, session, key):
        session.headers["X-API-Key"] = key

class APIClient:
    def set_auth_strategy(self, strategy, credential):
        strategy.apply(self.session, credential)
```

---

## 21. Interview Questions & Answers

### Beginner Level

**Q1: What is an API?**
> An API (Application Programming Interface) is a contract that defines how two software applications can communicate with each other. It specifies what requests can be made, how to make them, and what responses to expect. In REST APIs, this communication happens over HTTP.

**Q2: What is the difference between GET and POST?**
> GET is used to retrieve/read data. It has no request body, it's safe (read-only), and it's idempotent (calling it multiple times has the same effect). POST is used to create new resources. It has a request body containing the data to create, it's not safe, and it's not idempotent (calling it multiple times creates multiple resources).

**Q3: What is a REST API?**
> REST (Representational State Transfer) is an architectural style for designing APIs. Key principles: statelessness (each request contains all needed info), uniform interface (standard HTTP methods and status codes), client-server separation, and resource-based URLs (nouns not verbs). An API following these principles is called RESTful.

**Q4: What does HTTP 200 vs 201 vs 204 mean?**
> 200 OK is the standard success response for GET, PUT, PATCH. 201 Created is returned when a new resource has been created (POST). 204 No Content is returned for successful operations that don't return a body (often DELETE).

**Q5: What is the difference between authentication and authorization?**
> Authentication answers "Who are you?" — verifying identity (login with username/password). Authorization answers "What are you allowed to do?" — verifying permissions (can this user access this resource). You need authentication before authorization. A 401 status means not authenticated; 403 means authenticated but not authorized.

---

### Intermediate Level

**Q6: What is JSON Schema validation and why is it important?**
> JSON Schema is a vocabulary for validating the structure of JSON data. In API testing, it's important because a correct status code (200) doesn't guarantee the response body has the right structure, fields, and data types. Schema validation checks the contract — ensuring the API returns exactly what it promised. For example, if an `id` field should be an integer but the API returns a string, schema validation catches this even though the status code might be 200.

**Q7: Explain JWT and how it works.**
> JWT (JSON Web Token) is a self-contained token for authentication. It has three parts: Header (algorithm), Payload (user data and claims like expiry), and Signature (cryptographic proof of authenticity). The server signs the token with a secret key. When the client sends the token, the server verifies the signature without needing a database lookup (stateless). The payload contains claims like `exp` (expiry time) and `iat` (issued at).

**Q8: What is the difference between PUT and PATCH?**
> PUT replaces the entire resource. If you PUT `{"firstName": "John"}` on a user that also has `lastName`, `age`, and `email`, those other fields might be lost. PATCH partially updates — only the fields you send are changed. PATCH is more network-efficient (send only changed data) but requires the server to implement partial update logic.

**Q9: What are pytest fixtures and why are they used?**
> Fixtures are functions that provide shared setup/teardown for tests. They promote DRY (Don't Repeat Yourself) by creating test dependencies (like an API client, database connection, or test user) once and injecting them into multiple tests. Fixtures have scopes (function/class/module/session) controlling how often they're re-created. They also handle cleanup via `yield`, ensuring teardown happens even if a test fails.

**Q10: How do you test pagination in an API?**
> Test pagination by: (1) Verifying the response structure contains pagination metadata (total, skip/limit or page/per_page). (2) Checking that different pages return different data. (3) Confirming there are no duplicate records across pages. (4) Verifying that collecting all pages gives a total count matching the `total` field. (5) Testing boundary conditions — very large skip/page should return empty data, not an error.

**Q11: What is the difference between smoke testing and regression testing?**
> Smoke testing is a quick subset of tests run to check basic functionality — "Is the system alive?" Usually 10-20% of tests, runs in minutes, done on every build. Regression testing is a comprehensive suite run to ensure new changes haven't broken existing functionality — all tests, takes longer, usually run before release or on nightly builds.

**Q12: What is idempotency in REST APIs?**
> An operation is idempotent if making the same request multiple times produces the same result as making it once. GET, PUT, DELETE are idempotent. POST is not idempotent (calling POST /users multiple times creates multiple users). PATCH may or may not be idempotent depending on implementation. Idempotency is crucial for safe retry logic — if a network timeout occurs, you can safely retry idempotent requests.

---

### Advanced Level

**Q13: How do you handle test data management in API automation?**
> Several strategies: (1) Use the API itself to create test data in fixtures and clean up in teardown. (2) Use a dedicated test environment with seeded data. (3) Use factories/builders to generate unique test data (timestamps in usernames prevent conflicts). (4) Use test doubles/mocks for unit testing business logic without API calls. (5) For immutable data tests, use GET on existing resources; for mutable data tests, create fresh resources in setup and delete in teardown.

**Q14: What is the Page Object Model and its equivalent in API testing?**
> POM is a design pattern where each UI page has a corresponding class that encapsulates all interactions with that page. In API testing, the equivalent is having domain-specific client classes (UserClient, AuthClient, ProductClient) that encapsulate the API calls for each domain. This keeps tests clean (one line per action) and centralises endpoint URLs and request structures — when an endpoint changes, update one class instead of all tests.

**Q15: How do you test an API for security vulnerabilities?**
> Key security tests: (1) Authentication — endpoints requiring auth return 401 without valid token. (2) Authorization — users can't access other users' data (IDOR - Insecure Direct Object Reference). (3) Input validation — injection attacks (SQL injection via API params), oversized payloads. (4) Rate limiting — endpoints return 429 after too many requests. (5) Sensitive data exposure — passwords/secrets not returned in responses. (6) Token validation — expired/tampered tokens are rejected.

**Q16: Explain CI/CD in the context of test automation.**
> CI (Continuous Integration) means tests run automatically on every code push, immediately catching regressions. Our GitHub Actions workflow triggers on push/PR, sets up a clean environment, installs dependencies, runs pytest, and uploads the HTML report. CD (Continuous Deployment) extends this — if tests pass, code is automatically deployed. This creates a safety net: new code can only reach production if all tests pass, making releases faster and safer.

**Q17: What is the difference between mocking and stubbing?**
> Both are test doubles that replace real dependencies. A **stub** provides canned/fixed responses to calls made during the test — it doesn't verify anything. A **mock** is a stub that also records calls made to it and allows you to assert they were called correctly. Example: Stub = "When `get_user(1)` is called, return this fake user." Mock = "When `get_user(1)` is called, return this fake user AND verify it was called exactly once with argument 1."

**Q18: How do you handle flaky tests?**
> Flaky tests randomly pass or fail without code changes. Causes and solutions: (1) Timing issues → Add explicit waits/retries (our HTTPAdapter has retry logic). (2) Test order dependency → Use fresh fixtures, ensure test isolation. (3) Environment differences → Docker for consistent environments. (4) Third-party API instability → Consider mocking external APIs. (5) Shared state → Each test should create its own data and clean up after. (6) Identify patterns → Run flaky tests 10x to confirm flakiness, then fix root cause.

---

## 22. Real-World Scenarios & Troubleshooting

### Scenario 1: The API Changed — Schema Mismatch

**Situation**: Your test passes status code checks but schema validation starts failing.
```
AssertionError: Schema validation failed: 'user_name' is a required property
```

**What happened**: The API team renamed `username` to `user_name`. Status code is still 200, so naive tests wouldn't catch this. But schema validation caught it.

**Solution**: Update the schema to match the new contract, and notify API consumers.

---

### Scenario 2: Intermittent 429 Errors — Rate Limiting

**Situation**: Tests work in isolation but fail when run in parallel.
```
AssertionError: Expected HTTP 200, got 429.
```

**What happened**: Too many requests too quickly. The API is rate limiting your test suite.

**Solution**:
```python
# Option 1: Add delays
import time
time.sleep(0.1)  # 100ms between requests

# Option 2: HTTPAdapter with retry
Retry(status_forcelist=[429], backoff_factor=1)

# Option 3: Don't run too many tests in parallel
pytest -n 2  # Maximum 2 parallel workers
```

---

### Scenario 3: Tests Pass Locally, Fail in CI

**Situation**: All 76 tests pass on your Mac but fail in GitHub Actions.

**Common causes**:
1. **Environment variables** — Secrets not configured in GitHub
2. **Dependencies** — requirements.txt missing a package
3. **Timezone** — Date/time assertions fail on UTC servers
4. **Hardcoded paths** — `/Users/sumit/file.txt` doesn't exist in CI
5. **Python version** — Different Python version in CI

**Solution**: Check each systematically. Add verbose CI logging.

---

### Scenario 4: Authentication Token Expiry

**Situation**: Tests start passing but later tests fail with 401.

**What happened**: The access token expired mid-test-run.

**Solution**:
```python
@pytest.fixture(scope="session")
def authenticated_client():
    # Use refresh token to renew access token if needed
    client = APIClient()
    response = client.post("/auth/login", json={...})
    client.set_token(response.json()["accessToken"])
    return client

# Or: use short-lived access tokens but refresh as needed
```

---

### Scenario 5: Testing APIs Behind Authentication Wall

**Situation**: Production API requires OAuth 2.0 authentication with multiple steps.

**Solution**:
```python
@pytest.fixture(scope="session")
def oauth_token():
    # Step 1: Get auth code
    # Step 2: Exchange for token
    response = requests.post(
        "https://oauth.provider.com/token",
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "scope": "users:read"
        }
    )
    return response.json()["access_token"]
```

---

### Debugging Tips

```bash
# Run single test with maximum verbosity
python -m pytest tests/test_login.py::TestLoginSuccess::test_login_returns_200 -vvv

# Show print statements in output
python -m pytest -s

# Stop after first failure
python -m pytest -x

# Show the 5 slowest tests
python -m pytest --durations=5

# Run only tests matching a keyword
python -m pytest -k "login"
python -m pytest -k "not delete"

# Collect tests without running them
python -m pytest --collect-only

# Run with specific marker
python -m pytest -m smoke
```

---

## 23. Glossary of Terms

| Term | Definition |
|---|---|
| **API** | Application Programming Interface — a contract for software communication |
| **REST** | Representational State Transfer — architectural style for HTTP APIs |
| **HTTP** | HyperText Transfer Protocol — rules for web communication |
| **HTTPS** | HTTP + TLS encryption |
| **Endpoint** | A specific URL that performs a specific action (`/users/1`) |
| **Request** | A message sent from client to server |
| **Response** | A message sent from server back to client |
| **Status Code** | 3-digit number indicating the outcome of an HTTP request |
| **Header** | Key-value metadata attached to HTTP requests/responses |
| **Body** | The data payload of a request or response |
| **JSON** | JavaScript Object Notation — data exchange format |
| **JWT** | JSON Web Token — self-contained authentication token |
| **Authentication** | Verifying who you are |
| **Authorization** | Verifying what you can do |
| **Bearer Token** | Auth token sent in the Authorization header |
| **CRUD** | Create, Read, Update, Delete — basic data operations |
| **Idempotent** | Same request produces same result regardless of how many times called |
| **Fixture** | pytest concept: shared setup function for tests |
| **Schema** | A definition of the expected structure of data |
| **Schema Validation** | Verifying data matches its expected schema |
| **Parametrize** | Running one test with multiple different inputs |
| **Marker** | pytest label for categorising and filtering tests |
| **Mock** | A fake implementation that records calls and verifies behaviour |
| **Stub** | A fake implementation that returns pre-defined responses |
| **CI/CD** | Continuous Integration/Deployment — automated test and deploy pipelines |
| **Pagination** | Splitting large datasets across multiple pages |
| **Rate Limiting** | Restricting how many requests a client can make in a time period |
| **Retry Logic** | Automatically repeating failed requests |
| **Session** | A persistent HTTP connection that reuses settings |
| **AAA** | Arrange-Act-Assert — test structure pattern |
| **DRY** | Don't Repeat Yourself — code reuse principle |
| **BDD** | Behaviour Driven Development — plain English test scenarios |
| **Gherkin** | The Given/When/Then language used in BDD |
| **TDD** | Test Driven Development — write tests before code |
| **Regression** | A bug introduced by a new change breaking existing functionality |
| **Flaky Test** | A test that randomly passes or fails without code changes |
| **Smoke Test** | Quick test to verify basic system health |
| **SDLC** | Software Development Life Cycle |
| **conftest.py** | pytest special file containing shared fixtures |
| **requirements.txt** | File listing all Python package dependencies |
| **venv** | Python virtual environment — isolated package space |
| **dotenv** | Library that loads environment variables from a `.env` file |
| **Payload** | The data content of a request or response body |
| **Endpoint** | A specific URL + HTTP method combination that the API exposes |
| **Base URL** | The common prefix for all API endpoints (`https://dummyjson.com`) |
| **Path Parameter** | A variable embedded in the URL path (`/users/{id}`) |
| **Query Parameter** | A filter appended to the URL after `?` (`/users?limit=10`) |
| **Content-Type** | HTTP header declaring the format of the request/response body |
| **Accept** | HTTP header declaring what format the client wants in the response |
| **ISTQB** | International Software Testing Qualifications Board — industry standard |
| **Assertion** | A statement that checks a condition is true during testing |
| **Test Case** | A single test scenario with inputs, actions, and expected results |
| **Test Suite** | A collection of related test cases |
| **Test Coverage** | How much of the code/functionality is covered by tests |
| **Positive Testing** | Testing expected/valid inputs (happy path) |
| **Negative Testing** | Testing unexpected/invalid inputs (error scenarios) |
| **Boundary Testing** | Testing at the edges of valid ranges |
| **Integration Test** | Testing how multiple components work together |
| **Environment Variables** | Configuration values stored outside the code |
| **HTTPAdapter** | requests library class for configuring retry behaviour |

---

## Quick Reference Card

### HTTP Methods Cheat Sheet
```
GET    /users         → List all users
GET    /users/1       → Get user 1
POST   /users         → Create new user (body: user data)
PUT    /users/1       → Replace user 1 (body: complete user)
PATCH  /users/1       → Update user 1 partially (body: changed fields)
DELETE /users/1       → Delete user 1
```

### Status Code Cheat Sheet
```
200 OK          → GET/PUT/PATCH success
201 Created     → POST success (new resource)
204 No Content  → DELETE success (no body)
400 Bad Request → Invalid request data
401 Unauthorized → Not logged in
403 Forbidden   → Logged in but no permission
404 Not Found   → Resource doesn't exist
429 Too Many    → Rate limit exceeded
500 Server Error → Something crashed on the server
```

### pytest Command Cheat Sheet
```bash
python -m pytest                    # Run all tests
python -m pytest -v                 # Verbose output
python -m pytest -m smoke           # Smoke tests only
python -m pytest -k login           # Tests containing "login"
python -m pytest -x                 # Stop on first failure
python -m pytest --lf               # Run last failed tests only
python -m pytest -n 4               # Run in parallel (4 workers)
python -m pytest --collect-only     # Show tests without running
python -m pytest -s                 # Show print() output
```

### Our Framework Command Cheat Sheet
```bash
python -m pytest                    # All 76 tests
python -m pytest -m smoke           # Quick sanity (smoke tests)
python -m pytest -m auth            # Auth tests only
python -m pytest -m "users and not regression"  # Combined
python -m pytest tests/test_login.py  # One file only
python -m pytest tests/test_login.py::TestLoginSuccess  # One class
python -m pytest tests/test_login.py::TestLoginSuccess::test_login_returns_200  # One test

ENV=staging python -m pytest        # Test against staging environment
```

---

*Guide Version: 1.0 | Framework: Python + pytest + DummyJSON*
*Total Tests: 76 | Target API: https://dummyjson.com*


---

<p align="center">
Created with <span style="display:inline-block;animation:beat 1s infinite;">❤️</span> by 
<a href="https://www.linkedin.com/in/thesumitsuman/" target="_blank"><b>Sumit</b></a> • 
Knowledge shared for the <i>REST API Test Automation — Complete Guide</i>
</p>

<style>
@keyframes beat {
  0%,100% {transform: scale(1);}
  50% {transform: scale(1.25);}
}
</style>