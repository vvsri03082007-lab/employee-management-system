<template>

  <div class="form-container">

    <h2>Add Employee</h2>

    <form @submit.prevent="handleSubmit">

      <input
        type="text"
        v-model="employee.name"
        placeholder="Enter Employee Name"
      />

      <input
        type="email"
        v-model="employee.email"
        placeholder="Enter Employee Email"
      />

      <input
        type="text"
        v-model="employee.designation"
        placeholder="Enter Designation"
      />

      <input
        type="number"
        v-model="employee.salary"
        placeholder="Enter Salary"
      />

      <input
        type="number"
        v-model="employee.phone"
        placeholder="Enter Phone Number"
      />

      <button>Add Employee</button>

    </form>

  </div>

</template>

<script>
export default {

  name: "EmployeeForm",

  data() {

    return {

      employee: {

        name: '',
        email: '',
        designation: '',
        salary: '',
        phone: ''

      }

    }

  },

  methods: {

    handleSubmit() {

      if (
        this.employee.name === '' ||
        this.employee.email === '' ||
        this.employee.designation === '' ||
        this.employee.salary === '' ||
        this.employee.phone === ''
      ) {

        alert("Please fill all fields")

        return

      }

      this.$emit('add:employee', this.employee)

      alert("Employee Added Successfully")

      this.employee = {

        name: '',
        email: '',
        designation: '',
        salary: '',
        phone: ''

      }

    }

  }

}
</script>

<style scoped>

.form-container {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

h2 {
  text-align: center;
  color: #4338ca;
  margin-bottom: 25px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

input {
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  font-size: 15px;
  outline: none;
}

input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 5px rgba(79,70,229,0.4);
}

button {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  transition: 0.3s;
}

button:hover {
  transform: scale(1.02);
}

</style>