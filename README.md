# Reserva App Documentation

## Project Overview

The **Reserva App** is a web-based application designed to streamline the process of reserving rooms for various purposes, such as meetings, classes, or events. Developed using Python and the Flask framework, this project serves as a practical example of backend web development and multi-page application design.

---

## Key Features

### User Roles

1. **Administrator**:
   - Login.
   - Reserve rooms.
   - View all reservations.
   - Cancel reservations.
   - Manage room details.
   - Logout.

2. **Professor**:
   - Register an account.
   - Login.
   - Reserve rooms.
   - View personal reservations.
   - Cancel own reservations.
   - Logout.

### Data Models

- **User**:
  - ID
  - Name
  - Email
  - Password (hashed for security)
  - Active status
  - Admin status

- **Room**:
  - ID
  - Capacity
  - Active status
  - Type (e.g., conference, lecture)
  - Description

- **Reservation**:
  - ID
  - User ID
  - Room ID
  - Start datetime
  - End datetime
  - Active status

---

## Technical Implementation

### Backend
- Built using Python with the Flask framework.
- Database managed with SQLite.
- Implements the Model-View-Controller (MVC) architectural pattern.

### Frontend
- Jinja2 templating engine for rendering dynamic HTML templates.
- Responsive user interface designed with HTML5 and CSS3.

### Authentication & Authorization
- Secure user registration and login functionalities.
- Password hashing for secure storage.
- Role-based access control (RBAC) to differentiate functionalities between administrators and professors.

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- [Poetry](https://python-poetry.org/)
- SQLite

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/reserva-de-salas/reserva-app.git
   cd reserva-app
   ```

2. **Install Dependencies:**
   ```bash
   poetry install
   ```

3. **Set Up the Database:**
   - Use the provided SQL script to initialize the database:
     ```bash
     sqlite3 database.db < banco.sql
     ```

4. **Run the Application:**
   - Start the Flask application using Poetry:
     ```bash
     poetry run flask run
     ```

---

## CSV Files

The project includes some CSV files that were previously used before the database implementation. These files have been retained for testing purposes but do not play an active role in the current functionality of the application.

---

## Educational Value

This project provides hands-on experience with:

- **Flask Application Development**:
  - Organizing routes, templates, and static files.

- **Database Management**:
  - Implementing CRUD operations with SQLite.

- **Authentication**:
  - Managing user sessions and securing endpoints.

- **Role-Based Access Control**:
  - Differentiating functionalities based on user roles.

---

## Conclusion

The **Reserva App** is a fully functional room reservation system and a practical example of web application design and development using Python and Flask. It offers valuable insights into backend development, user management, and role-based access control.

For more information, access the [GitHub repository](https://github.com/reserva-de-salas/reserva-app).
