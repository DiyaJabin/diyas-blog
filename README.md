# Diya's Blog

A full-stack Flask blog application built as part of my Python learning journey.  
The project started as a course-based Flask blog application and was extended/deployed with a production-style setup using Vercel and PostgreSQL.

## Live Demo

[View the deployed site](https://diyas-blog.vercel.app)

## About the Project

Diya's Blog is a Flask-based blog website where users can register, log in, read blog posts, comment on posts, and where an admin user can create, edit, and delete blog posts.

While the base project was developed as part of a Python course, I independently worked through the deployment process, environment variable setup, database migration from SQLite to PostgreSQL, and debugging production issues on Vercel.

## Features

- User registration and login
- Password hashing using Werkzeug
- User session management with Flask-Login
- Admin-only post creation, editing, and deletion
- Blog post detail pages
- Comment system for logged-in users
- Contact form with email support
- Gravatar profile image support
- PostgreSQL database integration
- Deployed on Vercel

## Tech Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-CKEditor
- Bootstrap-Flask
- Werkzeug

### Database

- PostgreSQL
- Neon Database

### Deployment

- Vercel
- Environment Variables
- GitHub

## Project Structure

```text
diyas-blog/
│
├── static/
├── templates/
├── forms.py
├── server.py
├── requirements.txt
├── vercel.json
├── README.md
└── .gitignore