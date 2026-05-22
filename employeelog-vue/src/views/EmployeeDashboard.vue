<template>
  <div class="dashboard-layout">
    <!-- Sidebar Navigation -->
    <div class="sidebar">
      <div class="sidebar-brand">
        <span class="logo-dot"></span>
        WorkSpace HRMS
      </div>
      <ul class="sidebar-menu">
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'profile' }"
          @click="currentTab = 'profile'"
        >
          🪪 My Profile
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'directory' }"
          @click="currentTab = 'directory'"
        >
          📖 Directory
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'collaboration' }"
          @click="currentTab = 'collaboration'"
        >
          💬 Chat & Teammates
        </li>
      </ul>

      <div style="margin-top: auto; padding-top: 20px; border-top: 1px solid rgba(226,232,240,0.6)">
        <button 
          class="btn btn-secondary" 
          style="width: 100%; margin-bottom: 12px; font-size: 13px; padding: 10px 15px; border-radius: 10px;" 
          @click="toggleTheme"
        >
          {{ isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode' }}
        </button>
        <p style="font-size: 12px; color: #94a3b8; margin-bottom: 10px;">Logged in as employee</p>
        <button class="btn btn-danger" style="width: 100%" @click="logout">Sign Out</button>
      </div>
    </div>

    <!-- Main Content Panel -->
    <div class="main-content">
      <div class="header" style="margin-bottom: 35px; display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 100;">
        <div>
          <span class="badge badge-employee">Employee Portal</span>
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

      <!-- TAB 1: GORGEOUS DIGITAL CORPORATE ID CARD -->
      <div v-if="currentTab === 'profile'">
        <div class="profile-card-container">
          <div class="id-card">
            <div class="id-card-header">
              <span class="logo-dot"></span>
              <h3>{{ companyName }} CORPORATE ID</h3>
            </div>
            
            <div class="id-card-body">
              <div class="id-avatar-wrapper" style="position: relative; margin: 0 auto 15px; width: 80px; height: 80px;">
                <img 
                  v-if="profilePicture" 
                  :src="profilePicture" 
                  class="id-avatar" 
                  style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.1);" 
                />
                <div 
                  v-else 
                  class="avatar-placeholder" 
                  style="margin: 0; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white;"
                >
                  {{ getInitials(myRecord.name) }}
                </div>
              </div>
              <div class="id-card-info">
                <h2>{{ myRecord.name || 'Loading Name...' }}</h2>
                <p class="id-designation">{{ myRecord.designation || 'Specialist' }}</p>
                <span class="badge badge-employee" style="margin-top: 5px;">{{ myRecord.department || 'Staff' }}</span>
              </div>
            </div>

            <div class="id-card-footer">
              <div class="id-footer-item">
                <span class="label">ID Number</span>
                <span class="value">#000{{ myRecord.id || 'N/A' }}</span>
              </div>
              <div class="id-footer-item">
                <span class="label">Email Contact</span>
                <span class="value">{{ myRecord.email || 'N/A' }}</span>
              </div>
              <div class="id-footer-item">
                <span class="label">Phone</span>
                <span class="value">{{ myRecord.phone || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <!-- Extended Corporate Metadata Card -->
          <div class="card ext-profile-card">
            <h2>Detailed Employment Parameters</h2>
            <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">Verified secure workspace parameters stored for your employee registry.</p>
            
            <div class="metadata-grid">
              <div class="meta-item">
                <span class="lbl">Salary Bracket (Confidential)</span>
                <span class="val salary-val">₹{{ Number(myRecord.salary || 0).toLocaleString('en-IN') }} / month</span>
              </div>
              
              <!-- Render Dynamic Fields and Values of employee -->
              <div v-for="field in dynamicFields" :key="field.id" class="meta-item">
                <span class="lbl">{{ field.field_name }}</span>
                <span class="val" v-if="field.field_type === 'checkbox'">
                  <span :class="getCheckboxClass(field.id)">
                    {{ getCheckboxText(field.id) }}
                  </span>
                </span>
                <span class="val" v-else>
                  {{ getDynamicValue(field.id) }}
                </span>
              </div>
            </div>

            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;" />

            <h3 style="font-size: 16px; font-weight: 700; color: #1e293b;">Workspace Profile Photo</h3>
            <p style="color: #64748b; font-size: 13px; margin: 5px 0 15px 0;">Upload a professional corporate photo directly from your computer to represent you in the company channels.</p>
            
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

            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;" />

            <!-- Employee Custom Status Card Section -->
            <h3 style="font-size: 16px; font-weight: 700; color: #1e293b;">Custom Workspace Status</h3>
            <p style="color: #64748b; font-size: 13px; margin: 5px 0 15px 0;">
              Share your current mood or status with coworkers in this tenant workspace.
            </p>

            <div style="display: flex; flex-direction: column; gap: 20px;">
              <!-- Current status display -->
              <div v-if="customStatus || statusEmoji" style="display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 12px 18px; border-radius: 12px; border: 1px solid #e2e8f0;">
                <span style="font-size: 24px;">{{ statusEmoji }}</span>
                <div>
                  <p style="font-size: 11px; color: #64748b; font-weight: 500; text-transform: uppercase;">Current Status</p>
                  <p style="font-size: 15px; font-weight: 600; color: #1e293b;">"{{ customStatus }}"</p>
                </div>
              </div>

              <!-- Custom status inputs -->
              <div class="form-grid" style="grid-template-columns: 80px 1fr; gap: 15px; align-items: flex-end; margin-top: 0;">
                <div class="form-group" style="margin-top: 0;">
                  <label>Emoji</label>
                  <select v-model="statusEmojiInput" class="input" style="margin-bottom: 0; text-align: center; font-size: 18px;">
                    <option value="">None</option>
                    <option value="💻">💻</option>
                    <option value="🥪">🥪</option>
                    <option value="🗓️">🗓️</option>
                    <option value="🏠">🏠</option>
                    <option value="☕">☕</option>
                    <option value="🚀">🚀</option>
                    <option value="🤒">🤒</option>
                    <option value="🎉">🎉</option>
                  </select>
                </div>
                <div class="form-group" style="margin-top: 0;">
                  <label>Status message</label>
                  <input 
                    type="text" 
                    v-model="customStatusInput" 
                    placeholder="What's your current status?" 
                    class="input"
                    style="margin-bottom: 0;"
                  />
                </div>
              </div>

              <!-- Presets -->
              <div>
                <p style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Quick Presets</p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                  <button 
                    type="button"
                    class="btn btn-secondary btn-sm" 
                    style="font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 8px;"
                    @click="applyPreset('💻', 'Focused')"
                  >
                    💻 Focused
                  </button>
                  <button 
                    type="button"
                    class="btn btn-secondary btn-sm" 
                    style="font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 8px;"
                    @click="applyPreset('🥪', 'Out for Lunch')"
                  >
                    🥪 Out for Lunch
                  </button>
                  <button 
                    type="button"
                    class="btn btn-secondary btn-sm" 
                    style="font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 8px;"
                    @click="applyPreset('🗓️', 'In a Meeting')"
                  >
                    🗓️ In a Meeting
                  </button>
                  <button 
                    type="button"
                    class="btn btn-secondary btn-sm" 
                    style="font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 8px;"
                    @click="applyPreset('🏠', 'Working Remotely')"
                  >
                    🏠 Working Remotely
                  </button>
                  <button 
                    type="button"
                    class="btn btn-secondary btn-sm" 
                    style="font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 8px;"
                    @click="applyPreset('☕', 'Coffee Break')"
                  >
                    ☕ Coffee Break
                  </button>
                </div>
              </div>

              <!-- Actions -->
              <div style="display: flex; gap: 10px;">
                <button 
                  type="button"
                  @click="updateStatus" 
                  class="btn btn-primary"
                  :disabled="savingStatus"
                  style="height: 40px; padding: 0 20px; font-weight: 600;"
                >
                  {{ savingStatus ? 'Saving...' : '🚀 Save Status' }}
                </button>
                <button 
                  v-if="customStatus || statusEmoji"
                  type="button"
                  @click="clearStatus" 
                  class="btn btn-danger"
                  :disabled="savingStatus"
                  style="height: 40px; padding: 0 20px; font-weight: 600;"
                >
                  Clear Status
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: SEARCHABLE DIRECTORY -->
      <div v-if="currentTab === 'directory'">
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; flex-wrap: wrap; gap: 15px;">
            <div>
              <h2>Workspace Teammates Directory</h2>
              <p style="color: #64748b; font-size: 14px; margin-top: 5px;">Interact and collaborate with colleagues in the {{ companyName }} tenant.</p>
            </div>
            <input 
              type="text" 
              placeholder="Search by name, department, or title..." 
              v-model="searchQuery" 
              class="input"
              style="width: 320px; margin-bottom: 0;"
            />
          </div>

          <div v-if="filteredEmployees.length === 0" style="text-align: center; color: #94a3b8; padding: 40px 0;">No active staff records match your query.</div>

          <div v-else class="directory-grid">
            <div v-for="emp in filteredEmployees" :key="emp.id" class="directory-card">
              <div class="dir-avatar-wrapper" style="position: relative; margin: 0 auto 12px; width: 64px; height: 64px;">
                <img 
                  v-if="emp.profile_picture" 
                  :src="emp.profile_picture" 
                  class="dir-avatar" 
                  style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover; border: 2px solid #e2e8f0; margin: 0;" 
                />
                <div 
                  v-else 
                  class="dir-avatar" 
                  style="width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white; margin: 0;"
                >
                  {{ getInitials(emp.name) }}
                </div>
              </div>
              <h3>{{ emp.name }}</h3>
              <p class="dir-title">{{ emp.designation }}</p>
              <div class="dir-badges">
                <span class="dept-badge">{{ emp.department || 'N/A' }}</span>
              </div>
              <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 15px 0;" />
              <div class="dir-contact">
                <span>📧 {{ emp.email }}</span>
                <span>📞 {{ emp.phone }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: COLLABORATION PORTAL -->
      <div v-if="currentTab === 'collaboration'">
        <CollaborationPortal />
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../api'
import CollaborationPortal from './CollaborationPortal.vue'

export default {
  name: 'EmployeeDashboard',
  components: {
    CollaborationPortal
  },
  data() {
    return {
      currentTab: 'profile',
      notifications: [],
      showNotificationsDropdown: false,
      notificationInterval: null,
      presenceInterval: null,
      companyName: localStorage.getItem('company_name') || 'Company',
      username: localStorage.getItem('username') || 'employee',
      employees: [],
      dynamicFields: [],
      searchQuery: '',
      myRecord: {
        id: null,
        name: '',
        email: '',
        department: '',
        designation: '',
        salary: 0,
        phone: '',
        dynamic_data: []
      },
      profilePicture: '',
      profilePictureInput: '',
      savingProfilePicture: false,
      uploadFileName: '',
      customStatus: '',
      customStatusInput: '',
      statusEmoji: '',
      statusEmojiInput: '',
      savingStatus: false,
      isDarkMode: false
    }
  },
  computed: {
    filteredEmployees() {
      const q = this.searchQuery.toLowerCase().trim();
      if (!q) return this.employees;
      return this.employees.filter(emp => 
        emp.name.toLowerCase().includes(q) || 
        (emp.department && emp.department.toLowerCase().includes(q)) || 
        emp.designation.toLowerCase().includes(q)
      );
    },
    unreadNotificationsCount() {
      return this.notifications.filter(n => !n.is_read).length;
    }
  },
  async mounted() {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'dark') {
      this.isDarkMode = true
      document.body.classList.add('dark-theme')
    } else {
      this.isDarkMode = false
      document.body.classList.remove('dark-theme')
    }

    await this.fetchFields()
    await this.fetchEmployees()
    this.extractMyRecord()
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
        console.error(err)
      }
    },
    async fetchEmployees() {
      try {
        const res = await api.get('employees/')
        this.employees = res.data
      } catch (err) {
        console.error(err)
      }
    },
    extractMyRecord() {
      // Access token details return username/email. Let's find the matching record in company list
      const email = localStorage.getItem('username') + '@'; // Username matches email prefix.
      const match = this.employees.find(emp => emp.email.toLowerCase().startsWith(email.toLowerCase()) || emp.email.toLowerCase() === localStorage.getItem('username').toLowerCase());
      if (match) {
        this.myRecord = match;
      } else if (this.employees.length > 0) {
        // Fallback to first employee record for simulation if match not direct
        this.myRecord = this.employees[0];
      }
    },
    getInitials(name) {
      if (!name) return 'EP';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },
    getDynamicValue(fieldId) {
      if (!this.myRecord.dynamic_data) return 'Unspecified';
      const data = this.myRecord.dynamic_data.find(d => d.dynamic_field === fieldId);
      return data ? data.value : 'Unspecified';
    },
    getCheckboxText(fieldId) {
      const val = this.getDynamicValue(fieldId);
      if (val === 'true') return 'Enabled';
      if (val === 'false') return 'Disabled';
      return 'Unspecified';
    },
    getCheckboxClass(fieldId) {
      const val = this.getDynamicValue(fieldId);
      if (val === 'true') return 'badge-active';
      if (val === 'false') return 'badge-inactive';
      return '';
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
      } else {
        document.body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
      }
    },
    async fetchUserProfile() {
      try {
        const res = await api.get('profile/')
        this.profilePicture = res.data.profile_picture
        this.profilePictureInput = res.data.profile_picture
        this.customStatus = res.data.custom_status || ''
        this.customStatusInput = res.data.custom_status || ''
        this.statusEmoji = res.data.status_emoji || ''
        this.statusEmojiInput = res.data.status_emoji || ''
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
    applyPreset(emoji, text) {
      this.statusEmojiInput = emoji;
      this.customStatusInput = text;
    },
    async updateStatus() {
      this.savingStatus = true;
      try {
        const res = await api.put('profile/', {
          custom_status: this.customStatusInput,
          status_emoji: this.statusEmojiInput
        });
        this.customStatus = res.data.custom_status || '';
        this.statusEmoji = res.data.status_emoji || '';
        this.customStatusInput = res.data.custom_status || '';
        this.statusEmojiInput = res.data.status_emoji || '';
        alert("Status updated successfully!");
      } catch (err) {
        console.error("Failed to update status:", err);
        alert("Failed to update status.");
      } finally {
        this.savingStatus = false;
      }
    },
    async clearStatus() {
      this.savingStatus = true;
      try {
        await api.put('profile/', {
          custom_status: '',
          status_emoji: ''
        });
        this.customStatus = '';
        this.statusEmoji = '';
        this.customStatusInput = '';
        this.statusEmojiInput = '';
        alert("Status cleared successfully!");
      } catch (err) {
        console.error("Failed to clear status:", err);
        alert("Failed to clear status.");
      } finally {
        this.savingStatus = false;
      }
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
/* Profile and ID card layout */
.profile-card-container {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
}

.id-card {
  width: 380px;
  background: linear-gradient(135deg, #1e1b4b, #312e81);
  color: white;
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 20px 40px rgba(49, 46, 129, 0.25);
  display: flex;
  flex-direction: column;
  height: 480px;
  position: relative;
  overflow: hidden;
}

.id-card::before {
  content: '';
  position: absolute;
  top: -10%;
  right: -10%;
  width: 150px;
  height: 150px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 50%;
}

.id-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1.5px solid rgba(255,255,255,0.15);
  padding-bottom: 15px;
  margin-bottom: 25px;
}

.id-card-header h3 {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #cbd5e1;
}

.id-card-body {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
}

.avatar-placeholder {
  width: 90px;
  height: 90px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 700;
  box-shadow: 0 0 0 4px rgba(255,255,255,0.1);
}

.id-card-info h2 {
  font-size: 22px;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.id-designation {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 500;
}

.id-card-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: rgba(255,255,255,0.05);
  padding: 20px;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.05);
}

.id-footer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.id-footer-item .label {
  font-size: 10px;
  color: #94a3b8;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.id-footer-item .value {
  font-size: 13px;
  color: #e2e8f0;
  font-weight: 600;
}

.ext-profile-card {
  flex: 1;
  min-width: 320px;
}

.metadata-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.meta-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 16px 20px;
  border-radius: 12px;
}

.meta-item .lbl {
  display: block;
  font-size: 11px;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 5px;
  letter-spacing: 0.5px;
}

.meta-item .val {
  display: block;
  font-size: 15px;
  color: #1e293b;
  font-weight: 600;
}

.salary-val {
  color: #059669 !important;
  font-weight: 700 !important;
}

.badge-active {
  color: #059669;
  font-weight: 700;
}

.badge-inactive {
  color: #dc2626;
  font-weight: 700;
}

/* Directory view grid */
.directory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
}

.directory-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 25px;
  text-align: center;
  transition: all 0.3s ease;
}

.directory-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  border-color: #cbd5e1;
}

.dir-avatar {
  width: 64px;
  height: 64px;
  background: #f1f5f9;
  color: #475569;
  font-size: 20px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 0 auto 15px;
}

.directory-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.dir-title {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
  margin-bottom: 12px;
}

.dept-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.dir-contact {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
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
