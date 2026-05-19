\# Day 69 – Advanced Flask Blog Website



Course project from a Udemy Python course.



This project is an advanced blog website built with Flask that combines authentication, database relationships, commenting, admin authorization, and email functionality.



The project expands on previous Flask concepts by implementing a more complete multi-user blogging system.



\## Features

\- User registration and login

\- Password hashing and salting

\- User session management with Flask-Login

\- Create, edit, and delete blog posts

\- Rich text blog editor using CKEditor

\- Comment system for logged-in users

\- Admin-only routes for managing posts

\- Contact form with email sending

\- Flash messages for authentication feedback

\- User avatars using Gravatar

\- Database relationships using SQLAlchemy ORM



\## Database Relationships

\- One user can create many blog posts

\- One user can write many comments

\- One blog post can contain many comments



\## Tech Used

\- Python

\- Flask

\- Flask-Login

\- Flask-WTF

\- Flask-Bootstrap

\- Flask-CKEditor

\- SQLite

\- SQLAlchemy

\- Jinja2

\- HTML/CSS

\- SMTP (Email Sending)



\## Run

1\. Install dependencies:

&#x20;  pip install flask flask-login flask-wtf flask-bootstrap flask-ckeditor flask-sqlalchemy python-dotenv



2\. Create a `.env` file:

&#x20;  SECRET\_KEY=your\_secret\_key

&#x20;  MY\_EMAIL=your\_email

&#x20;  PASSWORD=your\_email\_password



3\. Run the app:

&#x20;  python main.py



4\. Open in browser:

&#x20;  http://127.0.0.1:5002

