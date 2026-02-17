# Homey - Property Management Information System (PMIS)

## Overview
Homey is a Django-based PMIS following the MVT architecture. It enables property owners, managers, and tenants to manage properties, leases, maintenance requests, payments (future), and notifications.

## Tech Stack
- Backend: Django (LTS)
- Frontend: Django Templates + Bootstrap 5
- Database: SQLite for development (PostgreSQL ready)
- Auth: Django Auth + Custom User model
- Notifications: Django signals + Email (console) + In-app

## Key Apps
- accounts: Custom User model with roles
- properties: Property and Unit models
- tenants: Tenant profile and lease data
- maintenance: Maintenance Request flow
- notifications: In-app notifications
- dashboard: Role-based dashboards

## Installation
1. Create virtual environment and install dependencies
2. Configure `.env` (SECRET_KEY, DEBUG, DATABASE_URL) if needed
3. Run migrations: `python manage.py makemigrations && python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## Environment
- DEBUG toggled in `settings.py`
- Static/Media configured
- Email backend: console for development

## User Roles
- Admin: full control via admin
- Owner: manage properties, view tenants, track metrics
- Manager: handle assigned properties and maintenance
- Tenant: view lease, submit requests, receive alerts

## Features
- Authentication: login, logout, registration, password reset
- Property management: CRUD (via admin), units, status
- Tenant management: assignment to unit/property, leases
- Maintenance: tenant submission, manager/owner updates, notifications
- Notifications: dashboard list, mark read
- Dashboards: role-based summaries and tables

## ER Diagram (text)
- User 1..* Property (owner)
- User 1..* Property (manager, optional)
- Property 1..* Unit
- User 1..1 Tenant
- Tenant ..1 Unit (optional)
- Tenant ..1 Property
- MaintenanceRequest ..1 Property, ..1 User(tenant), ..0..1 Unit
- Notification ..1 User

## Architecture
- Models in respective apps
- Views and URLconfs per app
- Signals for MaintenanceRequest status lifecycle
- Templates under `templates/` with Bootstrap UI

## Testing
- Recommended: Django TestCase for models and views
- Quick check: `python manage.py check`

## Security
- Role-based access decorator
- CSRF protection enabled
- Media and static handling with DEBUG separation

