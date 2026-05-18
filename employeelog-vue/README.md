## Database Structure

The project uses two separate database tables to manage employee records efficiently.

### Current Employees Table
This table stores all active employees currently working in the organization.

Fields:
- Employee ID
- Name
- Email
- Designation
- Salary

Operations supported:
- Add employee
- Edit employee
- Delete employee

### Deleted Employees Table
Whenever an employee is deleted from the system, the employee details are not permanently removed.

Instead, the deleted employee data is transferred and stored in a separate Deleted Employees table for record maintenance and tracking purposes.

Fields stored:
- Employee ID
- Name
- Email
- Designation
- Salary
- Deleted Time (optional)

This approach helps maintain:
- Employee history
- Data safety
- Record tracking
- Audit management

## Workflow

1. Employee is added using the Vue.js frontend.
2. Data is stored in MySQL through Django REST API.
3. Active employee records remain in the Current Employees table.
4. Deleted employee records move automatically to the Deleted Employees table.
5. Vue.js frontend updates dynamically after every CRUD operation.
