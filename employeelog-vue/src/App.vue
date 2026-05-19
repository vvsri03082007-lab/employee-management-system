<template>
  <div id="app">

    <div class="container">

      <div class="header">
        <h1>Employee Management System</h1>
        <p>Vue + Django + MySQL Full Stack Application</p>
      </div>

      <div class="card">
        <EmployeeForm @add:employee="addEmployee" />
      </div>

      <div class="card">
        <EmployeeTable
          :employees="employees"
          @delete:employee="deleteEmployee"
          @edit:employee="editEmployee"
        />
      </div>

    </div>

  </div>
</template>

<script>
import EmployeeForm from './components/EmployeeForm.vue'
import EmployeeTable from './components/EmployeeTable.vue'

const API_URL = 'https://employee-management-api-ldzb.onrender.com/api/employees/'

export default {

  name: 'App',

  components: {
    EmployeeTable,
    EmployeeForm
  },

  data() {
    return {
      employees: []
    }
  },

  methods: {

    async addEmployee(employee) {

      const response = await fetch(
        API_URL,
        {
          method: 'POST',
          body: JSON.stringify(employee),
          headers: {
            'Content-type': 'application/json; charset=UTF-8'
          }
        }
      )

      const data = await response.json()

      this.employees = [...this.employees, data]
    },

    async deleteEmployee(id) {

      await fetch(
        API_URL + id + '/',
        {
          method: 'DELETE'
        }
      )

      this.employees = this.employees.filter((employee) => {
        return employee.id !== id
      })

    },

    async editEmployee(id, updatedEmployee) {

      const response = await fetch(
        API_URL + id + '/',
        {
          method: 'PUT',
          body: JSON.stringify(updatedEmployee),
          headers: {
            'Content-type': 'application/json; charset=UTF-8'
          }
        }
      )

      const data = await response.json()

      this.employees = this.employees.map((employee) => {
        return employee.id === id ? data : employee
      })

    },

    async getEmployees() {

      const response = await fetch(API_URL)

      const data = await response.json()

      this.employees = data

    }

  },

  mounted() {
    this.getEmployees()
  }

}
</script>

<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #f4f7fb;
  font-family: Arial, Helvetica, sans-serif;
}

.container {
  max-width: 1000px;
  margin: 40px auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #1e293b;
  font-size: 40px;
  margin-bottom: 10px;
}

.header p {
  color: #64748b;
}

.card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

</style>