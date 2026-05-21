<template>
  <div class="auth-container">
    <!-- Floating Theme Switcher top right -->
    <div style="position: absolute; top: 25px; right: 25px; z-index: 999;">
      <button 
        class="btn-theme-toggle" 
        @click="toggleTheme"
        style="background: var(--glass-bg); border: 1px solid var(--border-light); color: var(--text-main); padding: 8px 16px; border-radius: 9999px; font-size: 13px; font-weight: 600; cursor: pointer; backdrop-filter: blur(10px); display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); transition: all 0.3s ease;"
      >
        {{ isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode' }}
      </button>
    </div>

    <div class="auth-card card animate-fade-in">
      <div class="branding">
        <span class="logo-dot"></span>
        <h1>WorkSphere HRMS</h1>
      </div>

      <!-- STEP 1: Enter Corporate Email -->
      <div v-if="step === 1" class="auth-step">
        <h2>Sign In</h2>
        <p class="subtitle">Enter your company email to request a secure entry passcode or reset your access.</p>

        <form @submit.prevent="handleEmailSubmit">
          <input
            type="email"
            placeholder="Corporate Email"
            v-model="email"
            class="input"
            required
            :disabled="loading"
          />

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Checking Account...' : 'Receive Verification OTP' }}
          </button>
        </form>

        <div class="helper-links">
          <a href="#" @click.prevent="requestPasswordReset" class="forgot-link">Forgot Password?</a>
          <router-link to="/onboard" class="onboard-link">Register Workspace</router-link>
        </div>
      </div>

      <!-- STEP 2: Enter Verification OTP -->
      <div v-if="step === 2" class="auth-step">
        <h2>OTP Verification</h2>
        <p class="subtitle">We have dispatched a 6-digit one-time password to <strong>{{ email }}</strong>.</p>

        <form @submit.prevent="handleOTPSubmit">
          <input
            type="text"
            placeholder="Enter 6-Digit OTP"
            v-model="otp"
            class="input text-center otp-input"
            maxlength="6"
            required
            :disabled="loading"
          />

          <button type="submit" class="btn btn-success w-full" :disabled="loading">
            {{ loading ? 'Authenticating...' : 'Verify & Sign In' }}
          </button>
        </form>

        <div class="helper-links">
          <a href="#" @click.prevent="resendOTP('login')" class="resend-link" :class="{ disabled: resendLoading }">
            {{ resendLoading ? 'Resending...' : 'Resend Verification Code' }}
          </a>
          <a href="#" @click.prevent="step = 1" class="back-link">Back</a>
        </div>
      </div>

      <!-- STEP 3: Password Recovery / Reset -->
      <div v-if="step === 3" class="auth-step">
        <h2>Recover Password</h2>
        <p class="subtitle">Enter the recovery OTP sent to <strong>{{ email }}</strong> and set a new password.</p>

        <form @submit.prevent="handlePasswordResetSubmit">
          <input
            type="text"
            placeholder="6-Digit Reset OTP"
            v-model="otp"
            class="input text-center otp-input"
            maxlength="6"
            required
            :disabled="loading"
          />

          <input
            type="password"
            placeholder="New Corporate Password"
            v-model="newPassword"
            class="input"
            required
            :disabled="loading"
          />

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Resetting Password...' : 'Save & Update Password' }}
          </button>
        </form>

        <div class="helper-links">
          <a href="#" @click.prevent="resendOTP('reset')" class="resend-link" :class="{ disabled: resendLoading }">
            {{ resendLoading ? 'Resending...' : 'Resend Recovery OTP' }}
          </a>
          <a href="#" @click.prevent="step = 1" class="back-link">Back</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../api'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      otp: '',
      newPassword: '',
      step: 1,
      loading: false,
      resendLoading: false,
      isDarkMode: false
    }
  },
  mounted() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      this.isDarkMode = true;
      document.body.classList.add('dark-theme');
    } else {
      this.isDarkMode = false;
      document.body.classList.remove('dark-theme');
    }
  },
  methods: {
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
    async handleEmailSubmit() {
      if (!this.email) return
      this.loading = true
      try {
        await api.post("request-otp/", {
          email: this.email,
          purpose: 'login'
        });
        this.otp = '';
        this.step = 2;
      } catch (error) {
        alert(error.response?.data?.error || "Account check failed. Ensure your email exists.");
      } finally {
        this.loading = false
      }
    },
    async handleOTPSubmit() {
      if (!this.otp) return
      this.loading = true
      try {
        const response = await api.post("verify-otp/", {
          email: this.email,
          otp: this.otp,
          purpose: 'login'
        });

        // Store JWT payload values securely
        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);
        localStorage.setItem("role", response.data.role);
        localStorage.setItem("company_name", response.data.company_name);
        localStorage.setItem("username", response.data.username || this.email.split('@')[0]);

        // Redirect based on exact role permissions
        const role = response.data.role;
        if (role === 'admin') {
          this.$router.push('/admin');
        } else if (role === 'manager') {
          this.$router.push('/manager');
        } else {
          this.$router.push('/employee');
        }
      } catch (error) {
        alert(error.response?.data?.error || "Authentication failed. Double check your code.");
      } finally {
        this.loading = false
      }
    },
    async requestPasswordReset() {
      if (!this.email) {
        alert("Please input your corporate email address above first.");
        return;
      }
      this.loading = true;
      try {
        await api.post("request-otp/", {
          email: this.email,
          purpose: 'reset'
        });
        this.otp = '';
        this.newPassword = '';
        this.step = 3;
      } catch (error) {
        alert(error.response?.data?.error || "Reset request failed.");
      } finally {
        this.loading = false
      }
    },
    async handlePasswordResetSubmit() {
      if (!this.otp || !this.newPassword) return;
      this.loading = true;
      try {
        const response = await api.post("verify-otp/", {
          email: this.email,
          otp: this.otp,
          purpose: 'reset',
          new_password: this.newPassword
        });
        alert(response.data.message || "Password updated successfully!");
        this.step = 1;
      } catch (error) {
        alert(error.response?.data?.error || "Reset verification failed.");
      } finally {
        this.loading = false
      }
    },
    async resendOTP(purpose) {
      if (this.resendLoading) return;
      this.resendLoading = true;
      try {
        await api.post("request-otp/", {
          email: this.email,
          purpose: purpose
        });
        alert("A fresh one-time verification code has been dispatched.");
      } catch (error) {
        alert(error.response?.data?.error || "Resend failed.");
      } finally {
        this.resendLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--bg-main);
  transition: background 0.3s ease;
}

.auth-card {
  width: 420px;
  padding: 40px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-light);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.branding {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 25px;
}

.branding h1 {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-dot {
  width: 10px;
  height: 10px;
  background: var(--primary);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--primary);
}

h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 8px;
}

.subtitle {
  color: var(--text-muted);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 25px;
}

.w-full {
  width: 100%;
}

.otp-input {
  letter-spacing: 5px;
  font-size: 22px;
  font-weight: 700;
}

.helper-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  font-size: 13px;
}

.helper-links a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.2s ease;
}

.helper-links a:hover {
  opacity: 0.8;
}

.resend-link.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.back-link {
  color: var(--text-muted) !important;
}

.animate-fade-in {
  animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeIn {
  from { transform: translateY(10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
