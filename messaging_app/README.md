# Messaging API

A robust and scalable RESTful API built with Django and Django REST Framework for managing user messaging conversations and messages. This project demonstrates best practices in API development including model design, serializers, viewsets, and clean URL routing.

---

## Overview

This project implements a messaging system backend API that allows users to create conversations, send messages, and manage user roles and profiles. It follows Django's best practices for project structure and RESTful API design.

---

## Features

* User management with roles (`guest`, `host`, `admin`)
* Conversations with multiple participants
* Sending and retrieving messages within conversations
* UUID primary keys for all models
* Timestamp fields with automatic creation times
* Nested serialization for conversations including messages

---

## Tech Stack

* Python 3.11+
* Django 4.x
* Django REST Framework
* SQLite (default, configurable to other databases)
* `django-environ` for environment variables (optional)

---

## Setup and Installation

### Prerequisites

* Python 3.11+ installed
* `venv` for virtual environments

### Steps

## Setup and Installation

You can run the project either **locally using a Python virtual environment (venv)** or **inside Docker containers**.

---

### Option 1: Local Setup (venv)

#### Prerequisites

* Python 3.11+ installed
* `venv` for virtual environments

#### Steps

```bash
# Clone the repo
git clone https://github.com/yourusername/messaging_api.git
cd messaging_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables if needed (optional)
# For example, create a `.env` file

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

### Option 2: Docker Setup

#### Prerequisites

* Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
* Docker Compose installed
* A `.env` file placed one directory above the project root with content similar to:

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=messagingdb
MYSQL_USER=your_db_user
MYSQL_PASSWORD=your_db_password
DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

#### Steps

```bash
# Clone the repo
git clone https://github.com/yourusername/messaging_api.git
cd messaging_api

# Build and start containers (adjust path to .env if needed)
docker compose --env-file ../.env up --build

# Run migrations inside the Django container
docker compose exec web python manage.py migrate

# (Optional) Create superuser inside the container
docker compose exec web python manage.py createsuperuser

# Access the app at http://localhost:8000/
```

---

## Project Structure

```
messaging_app/
├── chats/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── messaging_app/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

---

## Models

### User

* UUID primary key (`user_id`)
* `first_name`, `last_name`, `email` (unique)
* `phone_number` (optional)
* `role` (`guest`, `host`, `admin`)
* `created_at` timestamp

### Conversation

* UUID primary key (`conversation_id`)
* `participants` (many-to-many relationship with `User`)
* `created_at` timestamp

### Message

* UUID primary key (`message_id`)
* `sender` (foreign key to `User`)
* `conversation` (foreign key to `Conversation`)
* `message_body` (text)
* `sent_at` timestamp

---

## Serializers

* **UserSerializer:** Serializes user details, used nested inside other serializers.
* **ConversationSerializer:** Serializes conversations including nested participant users and nested messages.
* **ConversationCreateSerializer:** Used when creating or updating conversations; accepts participant IDs to establish many-to-many relationships.
* **MessageSerializer:** Serializes messages including sender details.
* **MessageCreateSerializer:** Used to create or update messages.

---

## Views (Viewsets)

* **ConversationViewSet:** Handles CRUD operations on conversations. Uses different serializers for listing (`ConversationSerializer`) and creating/updating (`ConversationCreateSerializer`).
* **MessageViewSet:** Handles CRUD operations on messages. Uses different serializers for listing (`MessageSerializer`) and creating/updating (`MessageCreateSerializer`).
* Both viewsets use `AllowAny` permissions for simplicity but can be customized for authentication.

---

## API Endpoints

| Method | Endpoint                   | Description                   |
| ------ | -------------------------- | ----------------------------- |
| GET    | `/api/conversations/`      | List all conversations        |
| POST   | `/api/conversations/`      | Create a new conversation     |
| GET    | `/api/conversations/{id}/` | Retrieve conversation details |
| GET    | `/api/messages/`           | List all messages             |
| POST   | `/api/messages/`           | Send a new message            |
| GET    | `/api/messages/{id}/`      | Retrieve message details      |

---

## Testing

Run the Django test suite:

```bash
python manage.py test
```


### Accessing the API via Browsable Interface (Session Auth)

1. Open your browser and go to your API root, e.g.,
   `http://127.0.0.1:8000/api/`

2. You should see the **DRF browsable API interface** with a **Login** button on the top right.

3. Click **Login** and enter your user credentials (created via `createsuperuser` or your app's users).

4. Once logged in, you can interact with the API endpoints using the browser — GET, POST, etc. — with session-based authentication automatically applied.

---

### Accessing the API Programmatically (JWT Token Auth)

1. Obtain a JWT token by sending a POST request to:
   `http://127.0.0.1:8000/api/token/`
   with JSON payload:

   ```json
   {
     "email": "your_email@example.com",
     "password": "your_password"
   }
   ```

2. You will receive a response like:

   ```json
   {
     "refresh": "your_refresh_token_here",
     "access": "your_access_token_here"
   }
   ```

3. Use the `access` token to authorize subsequent API requests by adding this HTTP header:

   ```
   Authorization: Bearer your_access_token_here
   ```

4. Example with `curl` to list conversations:

   ```bash
   curl -H "Authorization: Bearer your_access_token_here" http://127.0.0.1:8000/api/conversations/
   ```

---

### Summary

| Access Method          | How to Access                                                          | Authentication Used              |
| ---------------------- | ---------------------------------------------------------------------- | -------------------------------- |
| **Browser / UI**       | Visit `/api/` and login                                                | Session Authentication (cookies) |
| **Programmatic (API)** | Use `/api/token/` to get JWT token and pass it in Authorization header | JWT Token Authentication         |

---

If you’re seeing errors, make sure:

* You have users created with correct credentials.
* Your URLs include both `api-auth/` and JWT token endpoints.
* Your `REST_FRAMEWORK` settings include `SessionAuthentication` and `JWTAuthentication`.

---


Got it! Here's your README updated to **clearly show two setup options side-by-side** — using either **venv (local Python environment)** or **Docker** — so users can pick whichever suits them.

---

# Messaging API

A robust and scalable RESTful API built with Django and Django REST Framework for managing user messaging conversations and messages. This project demonstrates best practices in API development including model design, serializers, viewsets, and clean URL routing.

---

## Overview

This project implements a messaging system backend API that allows users to create conversations, send messages, and manage user roles and profiles. It follows Django's best practices for project structure and RESTful API design.

---

## Features

* User management with roles (`guest`, `host`, `admin`)
* Conversations with multiple participants
* Sending and retrieving messages within conversations
* UUID primary keys for all models
* Timestamp fields with automatic creation times
* Nested serialization for conversations including messages

---

## Tech Stack

* Python 3.11+
* Django 5.2.4
* Django REST Framework
* MySQL 8 (configurable; SQLite default for local dev)
* Docker & Docker Compose (optional)
* `django-environ` for environment variables

---



