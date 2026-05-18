<template>
  <div id="employee-table">

    <h1 class="title">Employee Management System</h1>

    <p
      v-if="employees.length < 1"
      class="empty-table"
    >
      No Employees Added
    </p>

    <table v-else>

      <thead>

        <tr>
          <th>S.No</th>
          <th>Name</th>
          <th>Email</th>
          <th>Designation</th>
          <th>Salary</th>
          <th>Actions</th>
        </tr>

      </thead>

      <tbody>

        <tr
          v-for="(employee, index) in employees"
          :key="employee.id"
        >

          <!-- SERIAL NUMBER -->

          <td>
            {{ index + 1 }}
          </td>

          <!-- NAME -->

          <td v-if="editing === employee.id">

            <input
              type="text"
              v-model="employee.name"
            />

          </td>

          <td v-else>
            {{ employee.name }}
          </td>

          <!-- EMAIL -->

          <td v-if="editing === employee.id">

            <input
              type="email"
              v-model="employee.email"
            />

          </td>

          <td v-else>
            {{ employee.email }}
          </td>

          <!-- DESIGNATION -->

          <td v-if="editing === employee.id">

            <input
              type="text"
              v-model="employee.designation"
            />

          </td>

          <td v-else>
            {{ employee.designation }}
          </td>

          <!-- SALARY -->

          <td v-if="editing === employee.id">

            <input
              type="number"
              v-model="employee.salary"
            />

          </td>

          <td v-else>
            ₹{{ employee.salary }}
          </td>

          <!-- ACTIONS -->

          <td v-if="editing === employee.id">

            <button
              class="save-btn"
              @click="editEmployee(employee)"
            >
              Save
            </button>

            <button
              class="cancel-btn"
              @click="cancelEdit(employee)"
            >
              Cancel
            </button>

          </td>

          <td v-else>

            <button
              class="edit-btn"
              @click="editMode(employee)"
            >
              Edit
            </button>

            <button
              class="delete-btn"
              @click="confirmDelete(employee.id)"
            >
              Delete
            </button>

          </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script>
export default {

  name: "EmployeeTable",

  props: {
    employees: Array
  },

  data() {

    return {

      editing: null,

      cachedEmployee: null

    }

  },

  methods: {

    editMode(employee) {

      this.editing = employee.id

      this.cachedEmployee = Object.assign({}, employee)

    },

    editEmployee(employee) {

      if (
        employee.name === '' ||
        employee.email === '' ||
        employee.designation === '' ||
        employee.salary === ''
      ) {

        alert("Please fill all fields")

        return

      }

      this.$emit('edit:employee', employee.id, employee)

      alert("Employee Updated Successfully")

      this.editing = null

    },

    cancelEdit(employee) {

      Object.assign(employee, this.cachedEmployee)

      this.editing = null

    },

    confirmDelete(id) {

      const confirmed = confirm(
        "Are you sure you want to delete this employee?"
      )

      if (confirmed) {

        this.$emit('delete:employee', id)

        alert("Employee Deleted Successfully")

      }

    }

  }

}
</script>

<style scoped>

body {
  background: #f3f4f6;
  font-family: Arial, Helvetica, sans-serif;
}

#employee-table {
  margin-top: 30px;
}

.title {
  text-align: center;
  margin-bottom: 25px;
  color: #4338ca;
  font-size: 34px;
}

.empty-table {
  text-align: center;
  color: red;
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

thead {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
}

th {
  padding: 18px;
  text-align: center;
  font-size: 15px;
}

td {
  padding: 18px;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
  font-size: 14px;
}

tr:hover {
  background-color: #f9fafb;
  transition: 0.3s;
}

input {
  width: 90%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  outline: none;
}

input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 5px rgba(79, 70, 229, 0.4);
}

button {
  border: none;
  padding: 10px 14px;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  margin-right: 8px;
  transition: 0.3s;
  font-size: 13px;
}

.edit-btn {
  background: #2563eb;
}

.edit-btn:hover {
  background: #1d4ed8;
}

.delete-btn {
  background: #dc2626;
}

.delete-btn:hover {
  background: #b91c1c;
}

.save-btn {
  background: #16a34a;
}

.save-btn:hover {
  background: #15803d;
}

.cancel-btn {
  background: #6b7280;
}

.cancel-btn:hover {
  background: #4b5563;
}

</style>