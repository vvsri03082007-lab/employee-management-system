# Employee Management System

A full stack Employee Management System built using Vue.js, Django REST Framework, and MySQL.

---

# Features

- Add Employees
- Edit Employee Details
- Delete Employees
- Store Deleted Employees History
- Employee Phone Number Support
- REST API Integration
- Responsive UI
- Full CRUD Operations

---

# Tech Stack

## Frontend
- Vue.js
- Axios
- CSS

## Backend
- Django
- Django REST Framework

## Database
- MySQL

---

# Project Structure

employee-management-system/
│
├── employeelog-django/
│   ├── employees/
│   ├── employeelog/
│   └── manage.py
│
├── employeelog-vue/
│   ├── src/
│   └── public/
│
└── README.md

---

# API Endpoints

## Current Employees

GET
/api/employees/

POST
/api/employees/

PUT
/api/employees/id/

DELETE
/api/employees/id/

---

## Deleted Employees

GET
/api/deleted-employees/

---

# Database Tables

## employees_employee
Stores current employees.

## employees_deletedemployee
Stores deleted employee records for history tracking.

---

# Installation

## Backend Setup

```bash
cd employeelog-django

pip install -r requirements.txt

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver
