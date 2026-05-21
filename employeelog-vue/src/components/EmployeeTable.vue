<template>
  <div class="table-card">
    <div v-if="employees.length < 1" class="empty-table-container">
      <span class="empty-icon">👥</span>
      <p class="empty-table">No employees registered in this workspace yet.</p>
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Designation</th>
            <th>Salary</th>
            <th>Phone</th>
            
            <!-- Dynamic Headers -->
            <th v-for="field in dynamicFields" :key="field.id">
              {{ field.field_name }}
            </th>

            <th v-if="role === 'admin' || role === 'manager'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td class="font-bold">{{ employee.name }}</td>
            <td>{{ employee.email }}</td>
            <td>
              <span class="dept-badge">{{ employee.department || 'N/A' }}</span>
            </td>
            <td>{{ employee.designation }}</td>
            <td class="font-bold text-slate">₹{{ formatSalary(employee.salary) }}</td>
            <td>{{ employee.phone }}</td>

            <!-- Dynamic Data Cells -->
            <td v-for="field in dynamicFields" :key="field.id">
              <span v-if="field.field_type === 'checkbox'" :class="getCheckboxClass(employee, field.id)">
                {{ getCheckboxText(employee, field.id) }}
              </span>
              <span v-else>
                {{ getDynamicValue(employee, field.id) }}
              </span>
            </td>

            <!-- Actions -->
            <td v-if="role === 'admin' || role === 'manager'">
              <div class="actions-group">
                <button class="action-btn btn-edit" @click="$emit('edit:employee', employee)">
                  Edit
                </button>
                <button v-if="role === 'admin'" class="action-btn btn-delete" @click="confirmDelete(employee.id)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "EmployeeTable",
  props: {
    employees: {
      type: Array,
      default: () => []
    },
    dynamicFields: {
      type: Array,
      default: () => []
    },
    role: {
      type: String,
      default: 'employee'
    }
  },
  methods: {
    formatSalary(val) {
      if (!val) return '0';
      return Number(val).toLocaleString('en-IN');
    },
    getDynamicValue(employee, fieldId) {
      if (!employee.dynamic_data) return '-';
      const data = employee.dynamic_data.find(d => d.dynamic_field === fieldId);
      return data ? data.value : '-';
    },
    getCheckboxText(employee, fieldId) {
      const val = this.getDynamicValue(employee, fieldId);
      if (val === 'true') return 'Yes';
      if (val === 'false') return 'No';
      return '-';
    },
    getCheckboxClass(employee, fieldId) {
      const val = this.getDynamicValue(employee, fieldId);
      if (val === 'true') return 'chk-badge badge-active';
      if (val === 'false') return 'chk-badge badge-inactive';
      return '';
    },
    confirmDelete(id) {
      if (confirm("Are you sure you want to delete and soft-archive this employee? This will revoke their corporate account login immediately.")) {
        this.$emit('delete:employee', id)
      }
    }
  }
}
</script>

<style scoped>
.table-card {
  background: transparent;
  border-radius: 16px;
  overflow: hidden;
}

.font-bold {
  font-weight: 600;
  color: var(--text-main);
}

.text-slate {
  color: var(--text-muted);
}

.dept-badge {
  background: hsla(var(--primary-hsl), 0.08);
  color: var(--primary);
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid hsla(var(--primary-hsl), 0.1);
}

/* Custom Checkbox Badges */
.chk-badge {
  display: inline-flex;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.badge-active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.badge-inactive {
  background: rgba(244, 63, 94, 0.1);
  color: var(--danger);
  border: 1px solid rgba(244, 63, 94, 0.15);
}

/* Actions styling */
.actions-group {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit {
  background: hsla(var(--primary-hsl), 0.08);
  color: var(--primary);
  border: 1px solid hsla(var(--primary-hsl), 0.1);
}

.btn-edit:hover {
  background: var(--primary);
  color: white;
  box-shadow: 0 4px 12px var(--primary-glow);
}

.btn-delete {
  background: rgba(244, 63, 94, 0.08);
  color: var(--danger);
  border: 1px solid rgba(244, 63, 94, 0.1);
}

.btn-delete:hover {
  background: var(--danger);
  color: white;
  box-shadow: 0 4px 12px var(--danger-glow);
}

/* Empty State */
.empty-table-container {
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 15px;
}

.empty-table {
  color: var(--text-muted);
  font-size: 15px;
  font-weight: 500;
}
</style>