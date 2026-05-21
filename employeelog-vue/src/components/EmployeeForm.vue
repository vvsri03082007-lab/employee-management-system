<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit">
      <div class="form-grid">
        <!-- Core Fields -->
        <div class="form-group">
          <label>Employee Name</label>
          <input type="text" v-model="employee.name" placeholder="John Doe" required />
        </div>
        <div class="form-group">
          <label>Corporate Email</label>
          <input type="email" v-model="employee.email" placeholder="john@company.com" required :disabled="role === 'manager'" />
        </div>
        <div class="form-group">
          <label>Department</label>
          <input type="text" v-model="employee.department" placeholder="Engineering" />
        </div>
        <div class="form-group">
          <label>Designation</label>
          <input type="text" v-model="employee.designation" placeholder="Senior Developer" required />
        </div>
        <div class="form-group">
          <label>Salary (Monthly)</label>
          <input type="number" v-model="employee.salary" placeholder="80000" required :disabled="role === 'manager'" />
        </div>
        <div class="form-group">
          <label>Phone Number</label>
          <input type="text" v-model="employee.phone" placeholder="+1234567890" required />
        </div>
      </div>

      <!-- Dynamic Custom Fields Section -->
      <div v-if="dynamicFields.length > 0" class="dynamic-section">
        <h3>Workspace Custom Fields</h3>
        <div class="form-grid">
          <div v-for="field in dynamicFields" :key="field.id" class="form-group">
            <label>{{ field.field_name }} <span v-if="field.required" class="required">*</span></label>
            
            <!-- Text field -->
            <input 
              v-if="field.field_type === 'text'" 
              type="text" 
              v-model="dynamic_data[field.id]" 
              :placeholder="`Enter ${field.field_name}`"
              :required="field.required"
            />
            
            <!-- Number field -->
            <input 
              v-if="field.field_type === 'number'" 
              type="number" 
              v-model="dynamic_data[field.id]" 
              :placeholder="`Enter number`"
              :required="field.required"
            />
            
            <!-- Date picker -->
            <input 
              v-if="field.field_type === 'date'" 
              type="date" 
              v-model="dynamic_data[field.id]" 
              :required="field.required"
            />

            <!-- Dropdown selector -->
            <select 
              v-if="field.field_type === 'dropdown'" 
              v-model="dynamic_data[field.id]" 
              :required="field.required"
            >
              <option value="" disabled selected>Select {{ field.field_name }}</option>
              <option 
                v-for="opt in parseOptions(field.options)" 
                :key="opt" 
                :value="opt"
              >
                {{ opt }}
              </option>
            </select>

            <!-- Checkbox toggle -->
            <div v-if="field.field_type === 'checkbox'" class="checkbox-container">
              <input 
                type="checkbox" 
                :id="`chk-${field.id}`" 
                v-model="dynamic_data[field.id]"
              />
              <span class="chk-label">Yes / Enable</span>
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary">
          {{ isEditing ? 'Save Changes' : 'Add Employee' }}
        </button>
        <button type="button" v-if="isEditing" class="btn btn-secondary" @click="cancelEdit">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "EmployeeForm",
  props: {
    dynamicFields: {
      type: Array,
      default: () => []
    },
    employeeToEdit: {
      type: Object,
      default: null
    },
    role: {
      type: String,
      default: 'admin'
    }
  },
  data() {
    return {
      employee: {
        name: '',
        email: '',
        department: '',
        designation: '',
        salary: '',
        phone: ''
      },
      dynamic_data: {}
    }
  },
  computed: {
    isEditing() {
      return !!this.employeeToEdit;
    }
  },
  watch: {
    employeeToEdit: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          // Pre-fill base fields
          this.employee = { ...newVal };
          
          // Pre-fill dynamic custom fields values
          const dynamicValues = {};
          if (newVal.dynamic_data) {
            newVal.dynamic_data.forEach(item => {
              const field = this.dynamicFields.find(f => f.id === item.dynamic_field);
              if (field && field.field_type === 'checkbox') {
                dynamicValues[item.dynamic_field] = item.value === 'true';
              } else {
                dynamicValues[item.dynamic_field] = item.value;
              }
            });
          }
          this.dynamic_data = dynamicValues;
        } else {
          this.resetForm();
        }
      }
    }
  },
  methods: {
    parseOptions(optionsStr) {
      if (!optionsStr) return [];
      return optionsStr.split(',').map(s => s.trim()).filter(Boolean);
    },
    handleSubmit() {
      // Package payload
      const processedDynamicData = {};
      this.dynamicFields.forEach(field => {
        let val = this.dynamic_data[field.id];
        if (field.field_type === 'checkbox') {
          val = val ? 'true' : 'false';
        }
        processedDynamicData[field.id] = val !== undefined && val !== null ? val : '';
      });

      const payload = {
        ...this.employee,
        dynamic_data: processedDynamicData
      };
      
      if (this.isEditing) {
        this.$emit('edit:employee', this.employee.id, payload);
      } else {
        this.$emit('add:employee', payload);
      }
      this.resetForm();
    },
    cancelEdit() {
      this.$emit('cancel:edit');
      this.resetForm();
    },
    resetForm() {
      this.employee = { name: '', email: '', department: '', designation: '', salary: '', phone: '' };
      this.dynamic_data = {};
    }
  }
}
</script>

<style scoped>
.form-container {
  margin-top: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.required {
  color: var(--danger);
}

.dynamic-section {
  border-top: 1.5px dashed var(--border-light);
  margin-top: 25px;
  padding-top: 20px;
}

.dynamic-section h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 15px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 48px; /* Alignment with inputs */
}

.checkbox-container input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: var(--primary);
  cursor: pointer;
  margin-bottom: 0;
}

.chk-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 25px;
  border-top: 1px solid var(--border-light);
  padding-top: 20px;
}
</style>