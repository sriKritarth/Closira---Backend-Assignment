# Closira Backend Assignment

A lightweight backend prototype for Closira’s enquiry-handling pipeline.

This project simulates how Closira can receive inbound customer enquiries from channels like WhatsApp, email, and phone calls, process them asynchronously, match them against predefined SOPs, schedule follow-ups, escalate unresolved enquiries, and expose enquiry history through REST APIs.

---

## 1. Project Overview

Closira is an AI-powered customer communication platform for small and medium businesses. The goal of this backend assignment was to build a simple REST API service that handles inbound enquiries and demonstrates backend fundamentals such as:

- REST API design
- Request validation
- Async background processing
- SOP matching logic
- Database persistence
- Follow-up scheduling
- Escalation handling
- Health checks
- API testability
- Clear engineering trade-off reasoning

This is not intended to be a production-ready system. It is a focused prototype built to show clean backend thinking, practical trade-offs, and a working enquiry workflow.

---

## 2. Tech Stack Used

| Technology | Purpose |
|---|---|
| Python | Core backend programming language |
| FastAPI | REST API framework |
| Pydantic | Request validation and schema definition |
| SQLite3 | Lightweight local database |
| FastAPI BackgroundTasks | Async-style background processing for enquiry SOP matching |
| Uvicorn | ASGI server for running the FastAPI app |
| `.http` file | Manual API testing through REST Client / VS Code |
| Pytest | Testing framework dependency |
| HTTPX | Test client dependency for API testing |
| python-json-logger | Added as a dependency for structured logging support, but logging implementation was not completed due to time constraints |

---

## 3. Why FastAPI?

FastAPI was chosen because it is simple, fast, and ideal for building clean REST APIs quickly.

Key reasons:

- Automatic OpenAPI documentation at `/docs`
- Built-in request validation using Pydantic
- Clear route structure
- Easy integration with background tasks
- Suitable for small prototypes as well as scalable production APIs
- Developer-friendly error handling and schema documentation

The assignment specifically required Python + FastAPI, so the implementation follows that requirement directly.

---

## 4. Why SQLite3 Instead of SQLAlchemy?

I used SQLite with direct SQL queries to keep the prototype lightweight, transparent, and easy to run locally.

For this assignment, SQLite was enough because:

- No external database setup is required
- The evaluator can clone and run the project quickly
- The schema is simple and easy to inspect
- Direct SQL makes the data flow transparent
- It keeps the prototype focused on backend workflow rather than database configuration

For a production version, I would use SQLAlchemy with PostgreSQL for stronger schema management, relationships, migrations, indexing, concurrency handling, and long-term scalability.

### Production Upgrade Path

| Current Prototype | Production Version |
|---|---|
| SQLite3 | PostgreSQL |
| Direct SQL queries | SQLAlchemy ORM / SQLModel |
| Manual schema creation | Alembic migrations |
| Local file database | Managed database instance |
| Simple relationship handling | Strong relational constraints and indexes |

---

## 5. Why FastAPI BackgroundTasks Instead of Celery?

I used FastAPI `BackgroundTasks` because this is a lightweight prototype.

The async processing required in this assignment is simple:

- Receive enquiry
- Return job ID immediately
- Process SOP matching in the background
- Update enquiry status
- Escalate if no SOP is matched

For this workflow, FastAPI BackgroundTasks are enough because:

- No Redis/RabbitMQ setup is required
- The project remains easy to run locally
- It avoids unnecessary infrastructure complexity
- It matches the prototype nature of the assignment
- It keeps the evaluator’s setup process simple

For production, I would use Celery or another proper job queue system.

### Production Upgrade Path

| Current Prototype | Production Version |
|---|---|
| FastAPI BackgroundTasks | Celery / RQ / Dramatiq |
| In-process background execution | Separate worker process |
| No message broker | Redis / RabbitMQ |
| Basic retry behavior | Retries, dead-letter queues, monitoring |
| Suitable for demo | Suitable for high-volume workloads |

---

## 6. Features Implemented

This backend implements the core enquiry-handling workflow required for the Closira backend assignment. The system accepts customer enquiries, processes them in the background, matches them with predefined SOPs, supports follow-up scheduling, handles escalation, and exposes enquiry history.

Each feature below maps directly to the assignment requirements and the implemented API endpoints.

---

### 6.1 Health Check

Endpoint:

```http
GET /health
```

### 6.2 Create New Enquiry

Endpoint:

```http
POST /enquiry
```

### 6.3 Async Background Processing and retrieving history

Endpoint:

```http
GET /enquiry/{enquiry_id}/history
```

### 6.4 Schedule Follow-up

Endpoint:

```http
POST /enquiry/{enquiry_id}/follow-up
```

### 6.5 Escalation Enquiry

Endpoint:

```http
POST /enquiry/{enquiry_id}/escalate
```