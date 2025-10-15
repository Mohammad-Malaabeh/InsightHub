InsightHub


A role‑based project, task, and content management app built with Django. Users can create projects and tasks, write tagged posts, and receive real‑time notifications. Managers and admins get reporting and user management features.

Screenshot/Logo


- Add 1–2 images here to show the dashboard or a signature page

- Example:
	- attachments/Screenshot_2025-02-16_180034.png

	- attachments/Screenshot_2025-04-08_003601.png


App Overview

InsightHub helps small teams organize their work:


- Staff users manage their own projects and tasks and write posts

- Managers see all projects/tasks and access reports

- Admins manage users, projects, and posts

- Optional real‑time notifications (Django Channels + Redis) and admin email alerts

Why I built it

A compact, full‑stack Django app to practice:

- Custom user models (email login, roles)

- Role‑based access control for views and templates

- Real‑time features with Channels

- CSS without a UI framework (responsive, mobile‑first)

Getting Started

Live Demo 


- URL: # missing

Planning Materials


- ERD: # missing

- User stories / tasks: # missing

Local Setup


	# clone
	git clone <repo-url>
	cd <repo-folder>
	
	# virtualenv
	python -m venv venv
	# Windows
	venv\Scripts\activate
	# macOS/Linux
	source venv/bin/activate
	
	# install
	pip install -r requirements.txt  # or pip install Django djangorestframework django-filter channels channels-redis redis python-dotenv Pillow
	
	# env
	cp .env.example .env  # create your .env from template
	# then edit .env and set DB/EMAIL/REDIS configs
	
	# database
	python manage.py migrate
	python manage.py createsuperuser
	
	# run Redis (dev)
	# macOS: brew services start redis
	# Ubuntu: sudo service redis-server start
	# Windows: use Memurai or WSL + redis-server
	
	# run server (dev)
	python manage.py runserver

Environment Variables (.env)


	DEBUG=True
	SECRET_KEY=change-me
	
	ALLOWED_HOSTS=127.0.0.1,localhost
	
	# DB (Postgres example)
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=insighthub_db
	DB_USER=postgres
	DB_PASSWORD=your_db_password
	DB_HOST=localhost
	DB_PORT=5432
	
	# Email
	EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
	DEFAULT_FROM_EMAIL=InsightHub <no-reply@example.com>
	ADMIN_ALERT_EMAILS=admin@example.com
	
	# Channels / Redis
	REDIS_HOST=127.0.0.1
	REDIS_PORT=6379

Features


- Authentication & Roles
	- Email login

	- Roles: Admin, Manager, Staff

	- Password reset flow


- Projects & Tasks
	- CRUD for projects and tasks

	- Task attachments, assignee

	- Staff see their own; managers/admins see all


- Posts
	- CRUD for posts

	- Tagging and likes


- Reporting
	- Manager/ Admin reports (project/task overview)


- Real‑time
	- Channels + Redis WebSocket notifications on CRUD events

	- Admin email alerts via signals


- UI
	- No CSS framework; responsive, mobile‑first

	- Small‑screen navbar with a pure‑CSS hamburger


Technologies Used


- Python, Django

- Django Channels, Redis

- Django REST Framework

- PostgreSQL (or SQLite for dev)

- python-dotenv

- Pillow (for image uploads)

- CSS (custom)


Attributions


- Django, Django Channels, DRF

- Redis/Memurai (Windows)

- Any articles, icons, or assets you used—list links here

Lessons Learned (Optional)


- Email as USERNAME_FIELD and implications for editing

- Role‑based access in views and templates

- Pure CSS hamburger for small screens

- Real‑time notifications with Channels/Redis

Next Steps


- DRF API with JWT

- Pagination and filters for lists

- Profile avatars and extended user fields

- Notifications UI (toasts/badges)

- CI/CD and containerization

Author


- Name: Mohammad Malabeh

- GitHub: Mohammad-Malaabeh

- Contact: malaabehmohamed@gmail.com

License

- License © 2025 Mohammad Malabeh