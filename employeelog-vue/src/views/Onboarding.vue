<template>
  <div class="auth-container">
    <div class="auth-card card">
      <!-- Title & Branding -->
      <div class="branding">
        <span class="logo-dot"></span>
        <h1>WorkSphere HRMS</h1>
      </div>

      <!-- STEP 1: Enter Company Email -->
      <div v-if="step === 1" class="onboard-step">
        <h2>Initialize Workspace</h2>
        <p class="subtitle">Enter your company email to generate your isolated database and admin console.</p>

        <form @submit.prevent="requestVerification">
          <input 
            type="email" 
            placeholder="admin@company.com" 
            v-model="email" 
            class="input" 
            required 
            :disabled="loading"
          />
          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Checking Email...' : 'Generate Verification Code' }}
          </button>
        </form>

        <p class="footer-link">
          Already have a workspace? <router-link to="/login">Sign In</router-link>
        </p>
      </div>

      <!-- STEP 2: Enter Verification Code -->
      <div v-if="step === 2" class="onboard-step">
        <h2>Verify Email Domain</h2>
        <p class="subtitle">We have sent a security code to <strong>{{ email }}</strong>. Please check your inbox (and spam folder).</p>

        <form @submit.prevent="verifyCode">
          <input 
            type="text" 
            placeholder="Enter 6-Digit Code" 
            v-model="code" 
            class="input text-center code-input" 
            maxlength="6"
            required 
            :disabled="loading"
          />
          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Verifying...' : 'Verify & Setup Workspace' }}
          </button>
        </form>

        <button @click="step = 1" class="btn btn-secondary w-full mt-10" :disabled="loading">
          Back
        </button>
      </div>

      <!-- STEP 3: Setup Success Credentials -->
      <div v-if="step === 3" class="onboard-step">
        <div class="success-icon">✓</div>
        <h2>Workspace Initialized!</h2>
        <p class="subtitle">Your SaaS environment has been successfully built. Copy these temporary credentials safely.</p>

        <div class="credentials-card">
          <div class="cred-item">
            <span class="label">Company Workspace</span>
            <span class="value">{{ companyData.company_name }}</span>
          </div>
          <div class="cred-item">
            <span class="label">Admin Username</span>
            <span class="value">{{ companyData.admin_email }}</span>
          </div>
          <div class="cred-item">
            <span class="label">Temporary Password</span>
            <span class="value password-value">{{ companyData.admin_password }}</span>
          </div>
        </div>

        <button class="btn btn-success w-full" @click="goToLogin">
          Go to Sign In
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from '../api'

export default {
  name: 'OnboardingView',
  data() {
    return {
      email: '',
      code: '',
      step: 1,
      loading: false,
      companyData: null
    }
  },
  methods: {
    async requestVerification() {
      if (!this.email) return
      this.loading = true
      try {
        await api.post('request-otp/', { email: this.email, purpose: 'onboard' })
        this.step = 2
      } catch (err) {
        alert(err.response?.data?.error || "Workspace verification request failed.");
      } finally {
        this.loading = false
      }
    },
    async verifyCode() {
      if (!this.code) return
      this.loading = true
      try {
        const response = await api.post('verify-otp/', { 
          email: this.email,
          otp: this.code,
          purpose: 'onboard'
        })
        this.companyData = response.data
        this.step = 3
      } catch (err) {
        alert(err.response?.data?.error || "Verification failed. Please check the code.");
      } finally {
        this.loading = false
      }
    },
    goToLogin() {
      this.$router.push('/login')
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
  background: radial-gradient(circle at 10% 20%, rgb(240, 243, 248) 0%, rgb(220, 228, 240) 90.1%);
}

.auth-card {
  width: 440px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 20px 50px rgba(79, 70, 229, 0.1);
  text-align: center;
}

.branding {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 30px;
}

.branding h1 {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-dot {
  width: 10px;
  height: 10px;
  background: #7c3aed;
  border-radius: 50%;
  box-shadow: 0 0 10px #7c3aed;
}

.onboard-step h2 {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 10px;
}

.subtitle {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 25px;
}

.w-full {
  width: 100%;
}

.mt-10 {
  margin-top: 10px;
}

.text-center {
  text-align: center;
}

.code-input {
  letter-spacing: 4px;
  font-size: 20px;
  font-weight: 700;
}

.footer-link {
  font-size: 13px;
  color: #64748b;
  margin-top: 20px;
}

.footer-link a {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  font-size: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 0 auto 20px;
  font-weight: bold;
  animation: scaleUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.credentials-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  text-align: left;
  margin-bottom: 25px;
}

.cred-item {
  margin-bottom: 12px;
}

.cred-item:last-child {
  margin-bottom: 0;
}

.cred-item .label {
  display: block;
  font-size: 11px;
  color: #94a3b8;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 3px;
}

.cred-item .value {
  display: block;
  font-size: 15px;
  color: #1e293b;
  font-weight: 600;
}

.cred-item .password-value {
  color: #4f46e5;
  font-family: monospace;
  font-size: 16px;
  background: rgba(79, 70, 229, 0.05);
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;
}

@keyframes scaleUp {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>
