<template>
  <div class="dashboard-layout">
    <!-- Sidebar Navigation -->
    <div class="sidebar">
      <div class="sidebar-brand">
        <span class="logo-dot"></span>
       WorkSphere HRMS
      </div>
      <ul class="sidebar-menu">
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'analytics' }"
          @click="currentTab = 'analytics'"
        >
          📊 Dashboard
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'employees' }"
          @click="currentTab = 'employees'"
        >
          👥 Team Roster
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'collaboration' }"
          @click="currentTab = 'collaboration'"
        >
          💬 Chat & Teammates
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'settings' }"
          @click="currentTab = 'settings'"
        >
          🔧 Settings
        </li>
      </ul>

      <div style="margin-top: auto; padding-top: 20px; border-top: 1px solid rgba(226,232,240,0.6)">
        <p style="font-size: 12px; color: #94a3b8; margin-bottom: 10px;">Logged in as manager</p>
        <button class="btn btn-danger" style="width: 100%" @click="logout">Sign Out</button>
      </div>
    </div>

    <!-- Main Content Panel -->
    <div class="main-content">
      <div class="header" style="margin-bottom: 35px; display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 100;">
        <div>
          <span class="badge badge-manager">Company Manager</span>
          <h1 style="font-size: 32px; font-weight: 800; margin-top: 6px; color: #0f172a;">
            {{ companyName }} Workspace
          </h1>
        </div>
        
        <!-- Notifications Dropdown -->
        <div class="header-actions" style="display: flex; align-items: center; gap: 20px;">
          <div class="notif-wrapper" style="position: relative;">
            <button class="notif-btn" @click="showNotificationsDropdown = !showNotificationsDropdown">
              🔔
              <span v-if="unreadNotificationsCount > 0" class="notif-badge">
                {{ unreadNotificationsCount }}
              </span>
            </button>
            
            <div v-if="showNotificationsDropdown" class="notif-dropdown">
              <div class="notif-header">
                <h4>Workspace Alerts</h4>
                <button class="mark-all-btn" @click="markAllNotificationsRead">Mark all as read</button>
              </div>
              <div v-if="notifications.length === 0" class="notif-empty">
                No new notifications.
              </div>
              <ul v-else class="notif-list">
                <li 
                  v-for="n in notifications.slice(0, 5)" 
                  :key="n.id" 
                  class="notif-item"
                  :class="{ unread: !n.is_read }"
                  @click="markNotificationRead(n)"
                >
                  <p class="notif-title">{{ n.title }}</p>
                  <p class="notif-desc">{{ n.description }}</p>
                  <span class="notif-time">{{ formatDate(n.created_at) }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div style="text-align: right">
            <p style="font-size: 14px; color: #64748b; font-weight: 500;">Corporate Domain</p>
            <p style="font-size: 15px; color: #1e293b; font-weight: 600;">{{ username }}@domain</p>
          </div>
        </div>
      </div>

      <!-- TAB 1: DASHBOARD METRICS -->
      <div v-if="currentTab === 'analytics'">
        <div class="analytics-grid">
          <div class="analytics-card">
            <div class="analytics-info">
              <h3>Active Colleagues</h3>
              <div class="value">{{ employees.length }}</div>
            </div>
            <div class="analytics-icon" style="background: rgba(16, 185, 129, 0.1); color: #10b981;">👥</div>
          </div>
          <div class="analytics-card">
            <div class="analytics-info">
              <h3>Custom parameters</h3>
              <div class="value">{{ dynamicFields.length }}</div>
            </div>
            <div class="analytics-icon" style="background: rgba(79, 70, 229, 0.1); color: #4f46e5;">⚙️</div>
          </div>
        </div>

        <div class="card">
          <h2>Department Roster Breakdown</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">Staff volume and allocations inside corporate departments.</p>
          <div v-if="employees.length === 0" style="text-align: center; color: #94a3b8; padding: 40px 0;">No active staff records available.</div>
          <div v-else class="dept-list">
            <div v-for="(count, dept) in departmentBreakdown" :key="dept" class="dept-item">
              <span class="dept-name">{{ dept }}</span>
              <div class="dept-bar-container">
                <div class="dept-bar" :style="{ width: `${(count / employees.length) * 100}%` }"></div>
              </div>
              <span class="dept-count">{{ count }} ({{ Math.round((count / employees.length) * 100) }}%)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: TEAM ROSTER EDITING -->
      <div v-if="currentTab === 'employees'">
        <div v-if="employeeToEdit" class="card">
          <h2>Edit Corporate Record</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">
            Modify contact and department details. Note: salary and registry email configurations are protected and cannot be changed by managers.
          </p>
          <EmployeeForm 
            :dynamicFields="dynamicFields" 
            :employeeToEdit="employeeToEdit"
            role="manager"
            @edit:employee="updateEmployee"
            @cancel:edit="cancelEdit"
          />
        </div>

        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h2>Team Staff Directory</h2>
            <span class="badge badge-manager">{{ employees.length }} Active Colleagues</span>
          </div>
          <EmployeeTable
            :employees="employees"
            :dynamicFields="dynamicFields"
            role="manager"
            @edit:employee="selectEmployeeForEdit"
          />
        </div>
      </div>

      <!-- TAB 3: COLLABORATION PORTAL -->
      <div v-if="currentTab === 'collaboration'">
        <CollaborationPortal />
      </div>

      <!-- TAB 4: SETTINGS -->
      <div v-if="currentTab === 'settings'">
        <div class="card">
          <h2>Manager Avatar & Profile Photo</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">
            Specify a custom image URL to update your manager profile picture across workspace channels and coworker lists.
          </p>

          <div style="display: flex; gap: 25px; align-items: center; margin-bottom: 25px;">
            <img 
              v-if="profilePicture" 
              :src="profilePicture" 
              class="manager-avatar" 
              style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);" 
            />
            <div 
              v-else 
              class="avatar-placeholder" 
              style="width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white;"
            >
              MG
            </div>
            <div>
              <p style="font-weight: 600; color: #1e293b; font-size: 16px;">{{ username }} (Workspace Manager)</p>
              <p style="color: #64748b; font-size: 13px;">Corporate Manager Account</p>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 15px; align-items: flex-start; margin-top: 15px;">
            <div style="display: flex; align-items: center; gap: 12px; width: 100%;">
              <label 
                class="btn btn-primary" 
                style="cursor: pointer; display: inline-flex; align-items: center; gap: 8px; margin: 0; height: 40px; padding: 0 20px; font-weight: 600;"
              >
                📁 Choose Photo File
                <input 
                  type="file" 
                  accept="image/*" 
                  @change="handlePhotoUpload" 
                  style="display: none;" 
                />
              </label>
              <span style="color: #64748b; font-size: 13px; word-break: break-all;">
                {{ uploadFileName || 'No file chosen' }}
              </span>
            </div>
            
            <button 
              v-if="profilePictureInput" 
              @click="updateProfilePicture" 
              class="btn btn-success" 
              :disabled="savingProfilePicture" 
              style="height: 40px; padding: 0 20px; font-weight: 600;"
            >
              {{ savingProfilePicture ? 'Uploading photo...' : '🚀 Save Uploaded Photo' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../api'
import EmployeeForm from '../components/EmployeeForm.vue'
import EmployeeTable from '../components/EmployeeTable.vue'
import CollaborationPortal from './CollaborationPortal.vue'

export default {
  name: 'ManagerDashboard',
  components: {
    EmployeeForm,
    EmployeeTable,
    CollaborationPortal
  },
  data() {
    return {
      currentTab: 'analytics',
      notifications: [],
      showNotificationsDropdown: false,
      notificationInterval: null,
      presenceInterval: null,
      companyName: localStorage.getItem('company_name') || 'Company',
      username: localStorage.getItem('username') || 'manager',
      employees: [],
      dynamicFields: [],
      employeeToEdit: null,
      profilePicture: '',
      profilePictureInput: '',
      savingProfilePicture: false,
      uploadFileName: ''
    }
  },
  computed: {
    departmentBreakdown() {
      const depts = {};
      this.employees.forEach(emp => {
        const d = emp.department || 'Unassigned';
        depts[d] = (depts[d] || 0) + 1;
      });
      return depts;
    },
    unreadNotificationsCount() {
      return this.notifications.filter(n => !n.is_read).length;
    }
  },
  async mounted() {
    await this.fetchFields()
    await this.fetchEmployees()
    await this.fetchNotifications()
    await this.fetchUserProfile()
    
    await this.updatePresence()
    this.notificationInterval = setInterval(this.fetchNotifications, 5000)
    this.presenceInterval = setInterval(this.updatePresence, 10000)
  },
  unmounted() {
    if (this.notificationInterval) clearInterval(this.notificationInterval)
    if (this.presenceInterval) clearInterval(this.presenceInterval)
  },
  methods: {
    async fetchFields() {
      try {
        const res = await api.get('dynamic-fields/')
        this.dynamicFields = res.data
      } catch (err) {
        console.error("Failed to load custom fields:", err)
      }
    },
    async fetchEmployees() {
      try {
        const res = await api.get('employees/')
        this.employees = res.data
      } catch (err) {
        console.error("Failed to load employees:", err)
      }
    },
    selectEmployeeForEdit(employee) {
      this.employeeToEdit = employee;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    async updateEmployee(id, employeeData) {
      try {
        // Enforce managers cannot update salary from api side (backend permissions check anyway)
        await api.put(`employees/${id}/`, employeeData)
        this.employeeToEdit = null;
        await this.fetchEmployees()
        alert("Employee updated successfully!")
      } catch (err) {
        console.error(err)
        alert("Failed to save changes. Make sure you haven't altered protected fields.");
      }
    },
    cancelEdit() {
      this.employeeToEdit = null;
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    },
    async fetchUserProfile() {
      try {
        const res = await api.get('profile/')
        this.profilePicture = res.data.profile_picture
        this.profilePictureInput = res.data.profile_picture
      } catch (err) {
        console.warn("Could not fetch user profile details")
      }
    },
    async updateProfilePicture() {
      if (!this.profilePictureInput.trim()) return;
      this.savingProfilePicture = true
      try {
        const res = await api.put('profile/', { profile_picture: this.profilePictureInput })
        this.profilePicture = res.data.profile_picture
        this.profilePictureInput = res.data.profile_picture
        this.uploadFileName = ''
        alert("Profile photo updated successfully!")
      } catch (err) {
        console.error("Failed to update profile photo:", err)
        alert("Failed to update profile photo.")
      } finally {
        this.savingProfilePicture = false
      }
    },
    handlePhotoUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.uploadFileName = file.name;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.profilePictureInput = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    async fetchNotifications() {
      try {
        const res = await api.get('notifications/')
        this.notifications = res.data
      } catch (err) {
        console.warn("Notifications load skipped")
      }
    },
    async markNotificationRead(notif) {
      try {
        await api.post(`notifications/${notif.id}/mark-read/`)
        await this.fetchNotifications()
        this.showNotificationsDropdown = false
        if (notif.notification_type === 'message') {
          this.currentTab = 'collaboration'
        }
      } catch (err) {
        console.error(err)
      }
    },
    async markAllNotificationsRead() {
      try {
        await api.post('notifications/mark-all-read/')
        await this.fetchNotifications()
      } catch (err) {
        console.error(err)
      }
    },
    async updatePresence() {
      try {
        await api.post('presence/heartbeat/')
      } catch (err) {
        console.warn("Presence heartbeat skipped")
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      return new Date(dateStr).toLocaleString();
    }
  }
}
</script>

<style scoped>
/* Analytics Dept styling */
.dept-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.dept-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.dept-name {
  width: 140px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.dept-bar-container {
  flex: 1;
  height: 10px;
  background: #f1f5f9;
  border-radius: 9999px;
  overflow: hidden;
}

.dept-bar {
  height: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 9999px;
}

.dept-count {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  width: 90px;
  text-align: right;
}

/* Premium Notification dropdown classes */
.notif-btn {
  background: white;
  border: 1px solid #e2e8f0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
}

.notif-btn:hover {
  transform: scale(1.05);
  border-color: #cbd5e1;
}

.notif-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white;
}

.notif-dropdown {
  position: absolute;
  top: 55px;
  right: 0;
  width: 320px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.notif-header {
  padding: 14px 18px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.notif-header h4 {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
}

.mark-all-btn {
  background: transparent;
  border: none;
  color: #4f46e5;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}

.notif-empty {
  padding: 30px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

.notif-list {
  list-style: none;
  max-height: 250px;
  overflow-y: auto;
}

.notif-item {
  padding: 14px 18px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.2s ease;
}

.notif-item:last-child {
  border-bottom: none;
}

.notif-item:hover {
  background: #f8fafc;
}

.notif-item.unread {
  background: rgba(79, 70, 229, 0.03);
}

.notif-title {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
}

.notif-desc {
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.notif-time {
  font-size: 10px;
  color: #94a3b8;
  display: block;
  margin-top: 6px;
}
</style>
