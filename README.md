# Identity and Profile Management API

A Django-based web application and REST API for managing user identity fragments in a clear, privacy-aware, and user-controlled way.

This project was built around the idea that identity is not static. Instead of treating identity as a single fixed profile, the system allows a user to manage multiple identity fragments linked to one main account. These fragments can represent different contexts such as professional, social, or platform-specific identities.

## Features

- User registration, login, and logout
- Dashboard for managing identity fragments
- Create, read, update, and delete identity records
- Avatar support through image URLs
- Visibility control for API exposure
- OAuth 2.0 protected API access
- REST API built with Django REST Framework
- PostgreSQL database backend

## Tech Stack

- Python
- Django
- Django REST Framework
- Django OAuth Toolkit
- PostgreSQL

## Project Structure

```text
ipmgr/
├── manage.py
├── requirements.txt
├── ipmgr/
├── accounts/
├── identities/
├── templates/
└── static/
```

## Prerequisites

Make sure you have installed:

- Python 3.10 or newer
- PostgreSQL
- pip
- virtualenv (recommended)

## 1. Clone the repository

```bash
mkdir ipmgr
cd ipmgr
git clone https://github.com/jamda/fp-wd-ipmgr
```

## 2. Create and activate a virtual environment

### On Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure PostgreSQL

Create a PostgreSQL database for the project.

Example:

```sql
CREATE DATABASE ipmgr_db;
CREATE USER ipmgr_user WITH PASSWORD 'your_password';
ALTER ROLE ipmgr_user SET client_encoding TO 'utf8';
ALTER ROLE ipmgr_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ipmgr_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ipmgr_db TO ipmgr_user;
```

## 5. Update database settings

Open your Django settings file and configure the database section.

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ipmgr_db',
        'USER': 'ipmgr_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Create a superuser

```bash
python manage.py createsuperuser
```

## 8. Start the development server

```bash
python manage.py runserver
```

The application should now be available at:

```text
http://127.0.0.1:8000/
```

## OAuth 2.0 setup

This project uses Django OAuth Toolkit for API authentication.

After starting the server, create an OAuth application.

### Option A: through Django admin

Go to:

```text
http://127.0.0.1:8000/admin/
```

Log in with your superuser account, then create a new OAuth2 application.

Suggested configuration:

- Client type: Confidential
- Authorization grant type: Resource owner password-based or Authorization code, depending on your setup
- Redirect URIs: leave blank for password grant, or set one if needed

### Option B: through shell if required

```bash
python manage.py shell
```

Then create an application manually if your project supports it.

## Getting an access token

Example request:

```bash
curl -X POST http://127.0.0.1:8000/oauth/get-token/ \
  -d "grant_type=password" \
  -d "username=your_username" \
  -d "password=your_password" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret"
```

If successful, this returns an access token that can be used to query the API.

## Example API usage

### List visible identities

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/identities/
```

### Create an identity

```bash
curl -X POST http://127.0.0.1:8000/api/identities/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Marc",
    "last_name": "Dubois",
    "nickname": "MDubois",
    "email": "marc@example.com",
    "context": "Professional",
    "avatar_url": "https://example.com/avatar.jpg",
    "is_visible_in_api": true
  }'
```

### Retrieve an identity by ID

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/identities/1/
```

### Update an identity

```bash
curl -X PUT http://127.0.0.1:8000/api/identities/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Marc",
    "last_name": "Dubois",
    "nickname": "MarcD",
    "email": "marc@example.com",
    "context": "Professional",
    "avatar_url": "https://example.com/avatar.jpg",
    "is_visible_in_api": true
  }'
```

### Delete an identity

```bash
curl -X DELETE http://127.0.0.1:8000/api/identities/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Admin access

The Django admin panel is available at:

```text
http://127.0.0.1:8000/admin/
```

## Notes

- Make sure PostgreSQL is running before starting the Django server.
- OAuth access is required for protected API routes.
- Only identity records marked as visible in the API are exposed through the authenticated API endpoints.
- The web interface and API are designed to complement each other: the interface supports direct user management, while the API simulates third-party access.

## Troubleshooting

### Database connection error

Check that:

- PostgreSQL is running
- database name, username, and password are correct
- the PostgreSQL port is correct

### Migration issues

Try:

```bash
python manage.py makemigrations
python manage.py migrate
```

### OAuth token not working

Check that:

- the OAuth application was created correctly
- the client ID and client secret are correct
- the username and password are correct
- the Authorization header uses the format:

```text
Bearer YOUR_ACCESS_TOKEN
```

## License

This project is for academic and demonstration purposes.
