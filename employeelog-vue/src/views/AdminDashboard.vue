<template>
  <div class="dashboard-layout">
    <!-- Sidebar Navigation -->
    <div class="sidebar">
      <div class="sidebar-brand" style="flex-direction: column; gap: 12px; margin-bottom: 35px;">
        <img 
          v-if="settings.company_logo" 
          :src="settings.company_logo" 
          alt="Company Logo" 
          style="max-height: 48px; max-width: 180px; object-fit: contain; border-radius: 8px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.05));"
        />
        <div style="display: flex; align-items: center; gap: 8px;">
          <span class="logo-dot"></span>
          <span>WorkSphere HRMS</span>
        </div>
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
          👥 Employees
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'fields' }"
          @click="currentTab = 'fields'"
        >
          ⚙️ Custom Fields
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'deleted' }"
          @click="currentTab = 'deleted'"
        >
          🗑️ Deleted Archive
        </li>
        <li 
          class="sidebar-item" 
          :class="{ active: currentTab === 'settings' }"
          @click="currentTab = 'settings'"
        >
          🔧 Settings
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
        <p style="font-size: 12px; color: #94a3b8; margin-bottom: 10px;">Logged in as admin</p>
        <button class="btn btn-danger" style="width: 100%" @click="logout">Sign Out</button>
      </div>
    </div>

    <!-- Main Content Panel -->
    <div class="main-content">
      <div class="header" style="margin-bottom: 35px; display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 100;">
        <div style="display: flex; align-items: center; gap: 18px;">
          <img 
            v-if="settings.company_logo" 
            :src="settings.company_logo" 
            alt="Workspace Logo"
            style="width: 58px; height: 58px; object-fit: cover; border-radius: 16px; border: 2px solid white; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.08);"
          />
          <div>
            <span class="badge badge-admin">Company Administrator</span>
            <h1 style="font-size: 32px; font-weight: 800; margin-top: 6px; color: var(--text-main);">
              {{ companyName }} Workspace
            </h1>
          </div>
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
            <p style="font-size: 14px; color: var(--text-muted); font-weight: 500;">Corporate Domain</p>
            <p style="font-size: 15px; color: var(--text-main); font-weight: 600;">{{ username }}@domain</p>
          </div>
        </div>
      </div>

      <!-- TAB 1: ANALYTICS DASHBOARD -->
      <div v-if="currentTab === 'analytics'">
        <div class="analytics-grid">
          <div class="analytics-card">
            <div class="analytics-info">
              <h3>Active Employees</h3>
              <div class="value">{{ employees.length }}</div>
              <span class="trend-badge positive">↑ Live</span>
            </div>
            <div class="analytics-icon" style="background: rgba(79, 70, 229, 0.1); color: #4f46e5;">👥</div>
          </div>
          <div class="analytics-card">
            <div class="analytics-info">
              <h3>Dynamic Fields</h3>
              <div class="value">{{ dynamicFields.length }}</div>
              <span class="trend-badge neutral">Active Schema</span>
            </div>
            <div class="analytics-icon" style="background: rgba(16, 185, 129, 0.1); color: #10b981;">⚙️</div>
          </div>
          <div class="analytics-card">
            <div class="analytics-info">
              <h3>Soft Deleted</h3>
              <div class="value">{{ deletedEmployees.length }}</div>
              <span class="trend-badge negative">Archived Logs</span>
            </div>
            <div class="analytics-icon" style="background: rgba(239, 68, 68, 0.1); color: #ef4444;">🗑️</div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px; margin-top: 30px;">
          <!-- Column 1: Department distribution -->
          <div class="card" style="margin-top: 0;">
            <h2>Department Distribution</h2>
            <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px;">Breakdown of your workforce across operational departments.</p>
            <div v-if="employees.length === 0" style="text-align: center; color: var(--text-muted); padding: 40px 0;">No active staff records available.</div>
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

          <!-- Column 2: Live Activity Feed -->
          <div class="card" style="margin-top: 0; display: flex; flex-direction: column;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
              <h2>Workspace Activity Feed</h2>
              <button @click="clearActivityLogs" style="background: transparent; border: none; color: var(--danger); font-size: 12px; font-weight: 600; cursor: pointer;">
                Clear Logs
              </button>
            </div>
            <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 20px;">Real-time compliance audit stream of admin events.</p>
            
            <div style="flex: 1; max-height: 250px; overflow-y: auto; padding-right: 5px;">
              <div v-if="activityLogs.length === 0" style="text-align: center; color: var(--text-muted); padding: 40px 0;">No activities logged yet.</div>
              <div v-else style="display: flex; flex-direction: column; gap: 15px; position: relative; padding-left: 20px; border-left: 2px solid var(--border-light); margin-left: 10px;">
                <div v-for="log in activityLogs" :key="log.id" style="position: relative;">
                  <!-- Timeline Bullet -->
                  <span 
                    :class="'bullet-' + log.type"
                    style="position: absolute; left: -26px; top: 5px; width: 10px; height: 10px; border-radius: 50%; border: 2px solid var(--bg-main);"
                  ></span>
                  
                  <div style="display: flex; flex-direction: column; gap: 2px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <span style="font-size: 14px;">{{ log.icon }}</span>
                      <span style="font-size: 13.5px; font-weight: 600; color: var(--text-main);">{{ log.text }}</span>
                    </div>
                    <span style="font-size: 11px; color: var(--text-muted); font-weight: 500; margin-left: 22px;">{{ formatActivityTime(log.timestamp) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: ACTIVE EMPLOYEES CRUD -->
      <div v-if="currentTab === 'employees'">
        <div class="card">
          <h2>{{ employeeToEdit ? 'Edit Employee Details' : 'Add New Employee' }}</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">
            {{ employeeToEdit ? 'Modify active fields and custom parameters for this account.' : 'Create a brand new corporate profile and generate credentials automatically.' }}
          </p>
          <EmployeeForm 
            :dynamicFields="dynamicFields" 
            :employeeToEdit="employeeToEdit"
            @add:employee="addEmployee" 
            @edit:employee="updateEmployee"
            @cancel:edit="cancelEdit"
          />
        </div>

        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
            <h2>Corporate Staff Directory</h2>
            <span class="badge badge-admin">{{ filteredEmployees.length }} Filtered Users</span>
          </div>

          <!-- Real-Time Search & Filters -->
          <div style="display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 250px; position: relative;">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="🔍 Search by name, email, or designation..." 
                class="input" 
                style="margin-bottom: 0; padding-left: 18px;"
              />
            </div>
            
            <div style="width: 220px;">
              <select v-model="selectedDepartment" class="input" style="margin-bottom: 0;">
                <option value="">All Departments</option>
                <option v-for="dept in uniqueDepartments" :key="dept" :value="dept">{{ dept }}</option>
              </select>
            </div>

            <button class="btn btn-secondary" @click="exportToCSV" style="height: 48px; font-size: 14px; font-weight: 600;">
              📥 Export CSV
            </button>
          </div>

          <EmployeeTable
            :employees="filteredEmployees"
            :dynamicFields="dynamicFields"
            role="admin"
            @edit:employee="selectEmployeeForEdit"
            @delete:employee="deleteEmployee"
          />
        </div>
      </div>

      <!-- TAB 3: DYNAMIC FIELDS BUILDER -->
      <div v-if="currentTab === 'fields'">
        <div class="card">
          <h2>Dynamic Schema Builder</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
            Create and enforce custom data parameters (e.g. shifts, branch code, subject details) across all employee forms dynamically without modifying database schemas.
          </p>

          <div style="display: flex; flex-direction: column; gap: 15px; margin-bottom: 25px;">
            <div class="form-grid">
              <div class="form-group">
                <label>Field Name</label>
                <input type="text" v-model="newField.field_name" placeholder="e.g. Tech Stack" class="input" style="margin-bottom: 0;" />
              </div>
              <div class="form-group">
                <label>Field Type</label>
                <select v-model="newField.field_type" class="input" style="margin-bottom: 0;">
                  <option value="text">Text Field</option>
                  <option value="number">Number Field</option>
                  <option value="date">Date Picker</option>
                  <option value="dropdown">Dropdown Selector</option>
                  <option value="checkbox">Checkbox Toggle</option>
                </select>
              </div>
            </div>

            <!-- Optional Comma-Separated Options for Dropdown -->
            <div v-if="newField.field_type === 'dropdown'" class="form-group">
              <label>Dropdown Options (Comma-Separated)</label>
              <input type="text" v-model="newField.options" placeholder="e.g. Vue, React, Angular" class="input" style="margin-bottom: 0;" />
            </div>

            <div style="display: flex; gap: 10px; align-items: center;">
              <input type="checkbox" id="field-required" v-model="newField.required" style="width: 18px; height: 18px; margin-bottom: 0; accent-color: #4f46e5;" />
              <label for="field-required" style="font-size: 14px; font-weight: 600; color: #475569; cursor: pointer;">Required Field</label>
            </div>

            <button class="btn btn-primary" style="align-self: flex-start;" @click="addField">
              Create Custom Field
            </button>
          </div>

          <hr style="border: 0; border-top: 1px solid #f1f5f9; margin-bottom: 25px;" />

          <h3>Active Custom Fields Schema</h3>
          <ul class="fields-list">
            <li v-for="field in dynamicFields" :key="field.id" class="field-item">
              <div class="field-info">
                <span class="field-title">{{ field.field_name }}</span>
                <span class="field-meta">Type: <strong>{{ field.field_type }}</strong></span>
                <span v-if="field.required" class="field-req">Required</span>
                <span v-if="field.options" class="field-opt-list">Options: ({{ field.options }})</span>
              </div>
              <button class="btn btn-danger btn-sm" @click="deleteField(field.id)">
                Remove Field
              </button>
            </li>
          </ul>
        </div>
      </div>

      <!-- TAB 4: DELETED ARCHIVE LOG -->
      <div v-if="currentTab === 'deleted'">
        <div class="card">
          <h2>Soft Deleted Employee Archive</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 20px;">
            Archived logs of deleted company employees for audit and compliance. Their user login rights are revoked immediately, but history remains company-isolated.
          </p>

          <div v-if="deletedEmployees.length === 0" style="text-align: center; color: #94a3b8; padding: 50px 0;">No archived logs registered in this workspace.</div>
          
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
                  <th>Archived Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="emp in deletedEmployees" :key="emp.id">
                  <td style="font-weight: 600">{{ emp.name }}</td>
                  <td>{{ emp.email }}</td>
                  <td><span class="dept-badge">{{ emp.department || 'N/A' }}</span></td>
                  <td>{{ emp.designation }}</td>
                  <td>₹{{ Number(emp.salary).toLocaleString('en-IN') }}</td>
                  <td>{{ emp.phone }}</td>
                  <td style="color: #ef4444; font-size: 13px; font-weight: 600;">
                    {{ formatDate(emp.deleted_at) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB 5: COMPANY SETTINGS -->
      <div v-if="currentTab === 'settings'">
        <div class="card">
          <h2>Company Profile & Branding</h2>
          <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">Update your corporate workspace name, branding assets, and parameters.</p>

          <form @submit.prevent="updateSettings">
            <div class="form-grid">
              <div class="form-group">
                <label>Company Workspace Name</label>
                <input type="text" v-model="settings.company_name" required />
              </div>
              <div class="form-group">
                <label>Company Logo URL</label>
                <input type="text" v-model="settings.company_logo" placeholder="https://example.com/logo.png" />
              </div>
            </div>
            
            <button type="submit" class="btn btn-success" :disabled="savingSettings">
              {{ savingSettings ? 'Saving Changes...' : 'Save Workspace Settings' }}
            </button>
          </form>
        </div>

        <!-- Danger Zone Card -->
        <div class="card" style="margin-top: 30px; border: 1px solid #fee2e2; background-color: #fef2f2; padding: 25px; border-radius: 12px; transition: all 0.3s ease;">
          <h2 style="color: #991b1b; font-size: 18px; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
            ⚠️ Danger Zone (Highly Secure)
          </h2>
          
          <!-- Step 1: Initial state (Requesting Deletion) -->
          <div v-if="deleteStep === 1">
            <p style="color: #b91c1c; font-size: 14px; margin-bottom: 20px; line-height: 1.5;">
              Permanently delete this workspace and all associated coworker records, custom metadata, and channels. 
              To prevent accidental deletion, **we will send a secure 6-digit verification code to your administrator Gmail.**
            </p>
            <button 
              @click="initiateDeleteWorkspace" 
              class="btn btn-danger" 
              type="button" 
              :disabled="requestingDeleteOtp"
              style="font-weight: 600; background-color: #dc2626; border-color: #dc2626; padding: 10px 20px;"
            >
              {{ requestingDeleteOtp ? 'Sending Deletion OTP...' : 'Request Deletion OTP' }}
            </button>
          </div>

          <!-- Step 2: Verification state -->
          <div v-else-if="deleteStep === 2">
            <div style="background-color: #fee2e2; border-left: 4px solid #ef4444; padding: 12px; margin-bottom: 20px; border-radius: 4px;">
              <p style="color: #991b1b; font-size: 13px; font-weight: 600; margin: 0;">
                🔒 A 6-digit secure deletion verification OTP has been sent to your Gmail inbox!
              </p>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 15px; margin-bottom: 20px;">
              <div style="display: flex; flex-direction: column; gap: 6px;">
                <label style="color: #991b1b; font-size: 13px; font-weight: 600;">Type the Workspace Name to confirm ("{{ companyName }}")</label>
                <input 
                  type="text" 
                  v-model="deleteNameConfirm" 
                  placeholder="Type workspace name exactly" 
                  style="padding: 10px; border: 1px solid #fca5a5; border-radius: 6px; font-size: 14px; color: #7f1d1d; outline: none; background-color: white;" 
                />
              </div>
              
              <div style="display: flex; flex-direction: column; gap: 6px;">
                <label style="color: #991b1b; font-size: 13px; font-weight: 600;">6-Digit Gmail Verification OTP</label>
                <input 
                  type="text" 
                  v-model="deleteOtp" 
                  maxlength="6" 
                  placeholder="Enter 6-digit code" 
                  style="padding: 10px; border: 1px solid #fca5a5; border-radius: 6px; font-size: 14px; color: #7f1d1d; letter-spacing: 2px; font-weight: bold; text-align: center; outline: none; background-color: white;" 
                />
              </div>
            </div>

            <div style="display: flex; gap: 10px; align-items: center;">
              <button 
                @click="submitDeleteWorkspace" 
                class="btn btn-danger" 
                type="button" 
                :disabled="deletingWorkspace"
                style="font-weight: 600; background-color: #b91c1c; border-color: #b91c1c;"
              >
                {{ deletingWorkspace ? 'Permanently Deleting...' : 'Confirm Permanent Deletion' }}
              </button>
              
              <button 
                @click="resetDeleteFlow" 
                class="btn btn-secondary" 
                type="button" 
                style="font-weight: 600; background-color: #e2e8f0; border-color: #cbd5e1; color: #475569;"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>

        <!-- Administrator Avatar Card -->
        <div class="card" style="margin-top: 30px;">
          <h2>Administrator Avatar & Profile Photo</h2>
          <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 25px;">
            Specify a custom image URL to update your administrator profile picture across workspace channels and coworker lists.
          </p>

          <div style="display: flex; gap: 25px; align-items: center; margin-bottom: 25px;">
            <img 
              v-if="profilePicture" 
              :src="profilePicture" 
              class="admin-avatar" 
              style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);" 
            />
            <div 
              v-else 
              class="avatar-placeholder" 
              style="width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white;"
            >
              AD
            </div>
            <div>
              <p style="font-weight: 600; color: var(--text-main); font-size: 16px;">{{ username }} (Workspace Owner)</p>
              <p style="color: var(--text-muted); font-size: 13px;">Corporate Administrator Account</p>
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

        <!-- Administrator Custom Status Card -->
        <div class="card" style="margin-top: 30px;">
          <h2>Custom Workspace Status</h2>
          <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 25px;">
            Share your current mood or status with coworkers in this tenant workspace.
          </p>

          <div style="display: flex; flex-direction: column; gap: 20px;">
            <!-- Current status display -->
            <div v-if="customStatus || statusEmoji" style="display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 12px 18px; border-radius: 12px; border: 1px solid var(--border-light);">
              <span style="font-size: 24px;">{{ statusEmoji }}</span>
              <div>
                <p style="font-size: 11px; color: var(--text-muted); font-weight: 500; text-transform: uppercase;">Current Status</p>
                <p style="font-size: 15px; font-weight: 600; color: var(--text-main);">"{{ customStatus }}"</p>
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
              <p style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">Quick Presets</p>
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

      <!-- TAB 6: COLLABORATION PORTAL -->
      <div v-if="currentTab === 'collaboration'">
        <CollaborationPortal />
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
  name: 'AdminDashboard',
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
      username: localStorage.getItem('username') || 'admin',
      employees: [],
      deletedEmployees: [],
      dynamicFields: [],
      employeeToEdit: null,
      savingSettings: false,
      deleteStep: 1,
      deleteOtp: '',
      deleteNameConfirm: '',
      requestingDeleteOtp: false,
      deletingWorkspace: false,
      newField: {
        field_name: '',
        field_type: 'text',
        options: '',
        required: false
      },
      settings: {
        id: null,
        company_name: '',
        company_logo: ''
      },
      profilePicture: '',
      profilePictureInput: '',
      savingProfilePicture: false,
      uploadFileName: '',
      searchQuery: '',
      selectedDepartment: '',
      isDarkMode: false,
      activityLogs: [],
      customStatus: '',
      customStatusInput: '',
      statusEmoji: '',
      statusEmojiInput: '',
      savingStatus: false
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
    },
    uniqueDepartments() {
      const depts = new Set();
      this.employees.forEach(emp => {
        if (emp.department) depts.add(emp.department);
      });
      return Array.from(depts);
    },
    filteredEmployees() {
      return this.employees.filter(emp => {
        const matchesSearch = 
          !this.searchQuery ||
          emp.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          emp.email.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          emp.designation.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        const matchesDept = 
          !this.selectedDepartment || 
          emp.department === this.selectedDepartment;
          
        return matchesSearch && matchesDept;
      });
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
    
    const savedLogs = localStorage.getItem(`activity_logs_${this.companyName}`);
    if (savedLogs) {
      try {
        this.activityLogs = JSON.parse(savedLogs).map(l => ({ ...l, timestamp: new Date(l.timestamp) }));
      } catch (e) {
        this.activityLogs = [];
      }
    }
    if (this.activityLogs.length === 0) {
      this.logActivity('system', '🚀', 'Workspace initialized.');
    }
    
    await this.fetchFields()
    await this.fetchEmployees()
    await this.fetchDeleted()
    await this.fetchCompanySettings()
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
        console.error("Failed to fetch dynamic fields schema:", err)
      }
    },
    async fetchEmployees() {
      try {
        const res = await api.get('employees/')
        this.employees = res.data
      } catch (err) {
        console.error("Failed to fetch active employees roster:", err)
      }
    },
    async fetchDeleted() {
      try {
        const res = await api.get('deleted-employees/')
        this.deletedEmployees = res.data
      } catch (err) {
        console.error("Failed to fetch archived deleted log:", err)
      }
    },
    async fetchCompanySettings() {
      try {
        const res = await api.get('companies/')
        if (res.data && res.data.length > 0) {
          const c = res.data[0];
          this.settings.id = c.id;
          this.settings.company_name = c.company_name;
          this.settings.company_logo = c.company_logo || '';
        }
      } catch (err) {
        console.error("Failed to fetch company profile settings:", err)
      }
    },
    async addField() {
      if (!this.newField.field_name) return
      try {
        const fieldName = this.newField.field_name;
        await api.post('dynamic-fields/', this.newField)
        this.logActivity('create', '⚙️', `Added custom dynamic field schema: ${fieldName}`);
        this.newField = { field_name: '', field_type: 'text', options: '', required: false }
        await this.fetchFields()
        alert("Custom Field Schema added successfully!")
      } catch (err) {
        console.error(err)
        alert("Failed to build custom field.")
      }
    },
    async deleteField(id) {
      if (!confirm("Are you sure you want to delete this custom field? This will delete all employee values associated with it!")) return
      try {
        const field = this.dynamicFields.find(f => f.id === id);
        const fieldName = field ? field.field_name : 'Custom Field';
        await api.delete(`dynamic-fields/${id}/`)
        await this.fetchFields()
        await this.fetchEmployees()
        this.logActivity('delete', '⚙️', `Removed custom field schema: ${fieldName}`);
      } catch (err) {
        console.error(err)
      }
    },
    async addEmployee(employeeData) {
      try {
        await api.post('employees/', employeeData)
        await this.fetchEmployees()
        this.logActivity('create', '👥', `Added new employee: ${employeeData.name}`);
        alert("Employee created and corporate account email registered!")
      } catch (err) {
        console.error(err)
        alert("Failed to add employee: " + (err.response?.data?.email || "Check credentials."));
      }
    },
    selectEmployeeForEdit(employee) {
      this.employeeToEdit = employee;
      // Scroll smoothly to form
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    async updateEmployee(id, employeeData) {
      try {
        await api.put(`employees/${id}/`, employeeData)
        this.employeeToEdit = null;
        await this.fetchEmployees()
        this.logActivity('update', '✏️', `Updated profile details for employee: ${employeeData.name}`);
        alert("Employee updated successfully!")
      } catch (err) {
        console.error(err)
        alert("Failed to save changes.");
      }
    },
    cancelEdit() {
      this.employeeToEdit = null;
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
    logActivity(type, icon, text) {
      const newLog = {
        id: Date.now() + Math.random(),
        type, // 'create', 'update', 'delete', 'system'
        icon,
        text,
        timestamp: new Date()
      };
      this.activityLogs.unshift(newLog);
      localStorage.setItem(`activity_logs_${this.companyName}`, JSON.stringify(this.activityLogs.slice(0, 50)));
    },
    clearActivityLogs() {
      if (confirm("Are you sure you want to clear your session compliance audit logs?")) {
        this.activityLogs = [];
        localStorage.removeItem(`activity_logs_${this.companyName}`);
        this.logActivity('system', '🧹', 'Compliance logs cleared by administrator.');
      }
    },
    formatActivityTime(timestamp) {
      if (!timestamp) return '';
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    },
    exportToCSV() {
      if (this.filteredEmployees.length === 0) {
        alert("No employee records found to export.");
        return;
      }
      
      const coreHeaders = ['Name', 'Email', 'Department', 'Designation', 'Salary', 'Phone'];
      const dynamicHeaders = this.dynamicFields.map(f => f.field_name);
      const headers = [...coreHeaders, ...dynamicHeaders];
      
      const rows = this.filteredEmployees.map(emp => {
        const coreValues = [
          emp.name,
          emp.email,
          emp.department || 'N/A',
          emp.designation,
          emp.salary,
          emp.phone
        ];
        
        const dynamicValues = this.dynamicFields.map(f => {
          const dynamicData = emp.dynamic_data?.find(d => d.dynamic_field === f.id);
          return dynamicData ? dynamicData.value : '';
        });
        
        return [...coreValues, ...dynamicValues].map(val => `"${String(val !== null && val !== undefined ? val : '').replace(/"/g, '""')}"`);
      });
      
      const csvContent = headers.join(',') + '\n' + rows.map(r => r.join(',')).join('\n');
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement("a");
      const url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", `Worksphere_Roster_${this.companyName.replace(/ /g, '_')}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    async deleteEmployee(id) {
      try {
        const emp = this.employees.find(e => e.id === id);
        const empName = emp ? emp.name : 'Employee';
        await api.delete(`employees/${id}/`)
        await this.fetchEmployees()
        await this.fetchDeleted()
        this.logActivity('delete', '🗑️', `Soft-deleted and archived employee: ${empName}`);
      } catch (err) {
        console.error(err)
      }
    },
    async updateSettings() {
      if (!this.settings.id) return;
      this.savingSettings = true;
      try {
        await api.put(`companies/${this.settings.id}/`, {
          company_name: this.settings.company_name,
          company_logo: this.settings.company_logo,
          company_email: this.settings.company_name.toLowerCase().replace(/ /g, '') + '@domain.com' // Safe email mock update
        });
        localStorage.setItem('company_name', this.settings.company_name);
        this.companyName = this.settings.company_name;
        this.logActivity('update', '🔧', `Branding updated: ${this.companyName}`);
        alert("Workspace profile updated successfully!");
      } catch (err) {
        console.error(err);
        alert("Failed to save profile changes.");
      } finally {
        this.savingSettings = false;
      }
    },
    async initiateDeleteWorkspace() {
      this.requestingDeleteOtp = true;
      try {
        const adminEmail = localStorage.getItem('email') || '';
        await api.post('companies/request-delete-otp/', {
          email: adminEmail,
          purpose: 'delete_workspace'
        });
        this.deleteStep = 2;
        alert("A 6-digit secure deletion verification code has been successfully sent to your Gmail inbox!");
      } catch (err) {
        console.error(err);
        alert(err.response?.data?.error || "Failed to request deletion code. Please check your network and settings.");
      } finally {
        this.requestingDeleteOtp = false;
      }
    },
    async submitDeleteWorkspace() {
      if (this.deleteNameConfirm !== this.companyName) {
        alert("Workspace name mismatch! Please type the exact name to confirm.");
        return;
      }
      if (!this.deleteOtp || this.deleteOtp.length !== 6) {
        alert("Please enter a valid 6-digit verification code.");
        return;
      }
      
      this.deletingWorkspace = true;
      try {
        await api.post('companies/confirm-delete/', {
          otp: this.deleteOtp
        });
        alert("Your corporate workspace has been successfully and permanently deleted.");
        this.logout();
      } catch (err) {
        console.error(err);
        alert(err.response?.data?.error || "Invalid or expired deletion verification code.");
      } finally {
        this.deletingWorkspace = false;
      }
    },
    resetDeleteFlow() {
      this.deleteStep = 1;
      this.deleteOtp = '';
      this.deleteNameConfirm = '';
      this.requestingDeleteOtp = false;
      this.deletingWorkspace = false;
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      return new Date(dateStr).toLocaleString();
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
    }
  }
}
</script>

<style scoped>
.bullet-create { background: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
.bullet-update { background: var(--primary); box-shadow: 0 0 8px var(--primary-glow); }
.bullet-delete { background: var(--danger); box-shadow: 0 0 8px var(--danger-glow); }
.bullet-system { background: #94a3b8; box-shadow: 0 0 8px rgba(148, 163, 184, 0.4); }

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
}

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
  color: var(--text-main);
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.dept-bar-container {
  flex: 1;
  height: 10px;
  background: var(--border-light);
  border-radius: 9999px;
  overflow: hidden;
}

.dept-bar {
  height: 100%;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 9999px;
}

.dept-count {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  width: 90px;
  text-align: right;
}

/* Custom Field Builder items */
.fields-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field-item {
  background: var(--glass-bg);
  padding: 16px 20px;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
}

.field-item:hover {
  border-color: var(--primary);
}

.field-info {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.field-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-main);
}

.field-meta {
  font-size: 13px;
  color: var(--text-muted);
}

.field-req {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}

.field-opt-list {
  font-size: 12px;
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.05);
  padding: 2px 8px;
  border-radius: 6px;
  font-family: monospace;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
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
