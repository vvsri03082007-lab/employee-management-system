# Employee Management System

A full-stack Employee Management System developed using Vue.js, Django REST Framework, and MySQL.

---

# Technologies Used

## Frontend
- Vue.js

## Backend
- Django
- Django REST Framework

## Database
- MySQL

---

# Features

- Add Employees
- Edit Employee Details
- Delete Employees
- Professional UI Design
- Real-time API Integration
- MySQL Database Connectivity
- Deleted Employee History Storage

---

# Database Structure

The project uses two separate database tables for better employee management and tracking.

## 1. Current Employees Table

This table stores all employees currently working in the organization.

### Fields
- Employee ID
- Name
- Email
- Designation
- Salary

### Operations
- Add Employee
- Edit Employee
- Delete Employee

---

## 2. Deleted Employees Table

When an employee is deleted from the system, the employee details are not permanently removed.

Instead, the deleted employee information is transferred automatically into a separate Deleted Employees table.

### Stored Details
- Employee ID
- Name
- Email
- Designation
- Salary

### Purpose
- Maintain employee history
- Record tracking
- Audit management
- Data safety

---

# Project Workflow

1. User enters employee details using the Vue.js frontend.
2. Vue.js sends requests to Django REST API.
3. Django processes the data and stores it in MySQL.
4. Current employees are stored in the Current Employees table.
5. Deleted employee records move automatically to the Deleted Employees table.
6. The frontend updates dynamically after every CRUD operation.

---

# Project Structure

employee-management-system/

│

├── employeelog django → Django Backend

│

├── employee vue → Vue.js Frontend

---

# How to Run the Project

## Backend

```bash
cd "employeelog django"
python3 manage.py runserver
