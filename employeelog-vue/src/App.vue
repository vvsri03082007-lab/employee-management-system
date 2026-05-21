<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
  /* Premium Palette */
  --primary-hsl: 243, 75%, 59%;
  --primary: hsl(var(--primary-hsl));
  --primary-hover: hsl(243, 75%, 54%);
  --primary-glow: hsla(var(--primary-hsl), 0.18);
  
  --secondary: #6366f1;
  --success: #10b981;
  --success-glow: rgba(16, 185, 129, 0.18);
  --danger: #f43f5e;
  --danger-glow: rgba(244, 63, 94, 0.18);
  
  --text-main: #0f172a;
  --text-muted: #64748b;
  --bg-main: #f8fafc;
  --border-light: rgba(226, 232, 240, 0.8);
  
  /* Glassmorphism Variables */
  --glass-bg: rgba(255, 255, 255, 0.75);
  --glass-border: rgba(255, 255, 255, 0.8);
  --glass-blur: 20px;
}

body.dark-theme {
  --bg-main: #0b0f19;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --border-light: rgba(51, 65, 85, 0.4);
  --glass-bg: rgba(15, 23, 42, 0.85);
  --glass-border: rgba(255, 255, 255, 0.05);
  --primary-glow: rgba(129, 140, 248, 0.25);
}

body.dark-theme .card {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(255, 255, 255, 0.06);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

body.dark-theme .card:hover {
  background: rgba(15, 23, 42, 0.75);
  border-color: rgba(255, 255, 255, 0.12);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.45);
}

body.dark-theme .analytics-card {
  background: rgba(15, 23, 42, 0.6);
  border-color: rgba(255, 255, 255, 0.06);
}

body.dark-theme .analytics-card:hover {
  border-color: rgba(129, 140, 248, 0.3);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
}

body.dark-theme table {
  background: #111827;
}

body.dark-theme thead {
  background: #1f2937;
  border-bottom-color: #374151;
}

body.dark-theme th {
  color: #94a3b8;
}

body.dark-theme td {
  border-bottom-color: #1f2937;
  color: #e5e7eb;
}

body.dark-theme tr:hover td {
  background-color: #1f2937;
}

body.dark-theme .input, body.dark-theme input, body.dark-theme select {
  background: #111827;
  border-color: #374151;
  color: #f8fafc;
}

body.dark-theme .input:focus, body.dark-theme input:focus, body.dark-theme select:focus {
  background: #1f2937;
  border-color: var(--primary);
}

body.dark-theme h1, body.dark-theme h2, body.dark-theme h3, body.dark-theme h4 {
  color: #f8fafc;
}

body.dark-theme .btn-secondary {
  background: #1f2937;
  color: #94a3b8;
}

body.dark-theme .btn-secondary:hover {
  background: #374151;
  color: #f8fafc;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 9999px;
  border: 2px solid #f1f5f9;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

body {
  background: radial-gradient(circle at 0% 0%, hsla(var(--primary-hsl), 0.08) 0%, transparent 40%),
              radial-gradient(circle at 100% 100%, hsla(271, 76%, 53%, 0.08) 0%, transparent 45%),
              var(--bg-main);
  font-family: 'Outfit', sans-serif;
  color: var(--text-main);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
}

/* Dashboard Core Layout */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* Premium Glassmorphic Sidebar */
.sidebar {
  width: 290px;
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border-right: 1px solid var(--border-light);
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 1000;
  box-shadow: 4px 0 30px rgba(0, 0, 0, 0.02);
}

.sidebar-brand {
  font-size: 24px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  letter-spacing: -0.5px;
}

.sidebar-brand .logo-dot {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, var(--primary), #a855f7);
  border-radius: 50%;
  box-shadow: 0 0 15px var(--primary-glow);
  display: inline-block;
  animation: logo-pulse 2s infinite ease-in-out;
}

@keyframes logo-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.sidebar-menu {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar-item {
  padding: 15px 20px;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 600;
  color: var(--text-muted);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
  overflow: hidden;
}

.sidebar-item:hover {
  background: rgba(79, 70, 229, 0.04);
  color: var(--primary);
  transform: translateX(6px);
}

.sidebar-item.active {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  color: white;
  box-shadow: 0 10px 25px -5px var(--primary-glow);
}

.sidebar-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 25%;
  height: 50%;
  width: 4px;
  background: white;
  border-radius: 0 4px 4px 0;
}

.main-content {
  margin-left: 290px;
  flex: 1;
  padding: 50px;
  max-width: 1600px;
  animation: main-slide 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes main-slide {
  from { transform: translateY(15px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Premium Card Designs */
.card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  padding: 35px;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.04),
              0 1px 2px rgba(0, 0, 0, 0.02);
  margin-bottom: 35px;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 45px rgba(31, 38, 135, 0.07);
  border-color: rgba(255, 255, 255, 0.95);
  background: rgba(255, 255, 255, 0.85);
}

/* Typography Overrides */
h1, h2, h3, h4 {
  color: var(--text-main);
  font-weight: 800;
  letter-spacing: -0.02em;
}

h2 {
  font-size: 22px;
  margin-bottom: 8px;
}

/* Premium Inputs */
.input, input[type="text"], input[type="email"], input[type="password"], input[type="number"], input[type="date"], select {
  width: 100%;
  padding: 15px 20px;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  font-family: inherit;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-main);
  outline: none;
  background: #f8fafc;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  margin-bottom: 18px;
}

.input:focus, input:focus, select:focus {
  border-color: var(--primary);
  background: white;
  box-shadow: 0 0 0 4px var(--primary-glow);
}

/* Modern Hover Interactive Buttons */
.btn {
  padding: 15px 26px;
  border: none;
  border-radius: 14px;
  font-family: inherit;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  color: white;
  box-shadow: 0 6px 18px var(--primary-glow);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px var(--primary-glow);
  filter: brightness(1.05);
}

.btn-success {
  background: linear-gradient(135deg, var(--success), #059669);
  color: white;
  box-shadow: 0 6px 18px var(--success-glow);
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px var(--success-glow);
  filter: brightness(1.05);
}

.btn-danger {
  background: linear-gradient(135deg, var(--danger), #e11d48);
  color: white;
  box-shadow: 0 6px 18px var(--danger-glow);
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px var(--danger-glow);
  filter: brightness(1.05);
}

.btn-secondary {
  background: #f1f5f9;
  color: var(--text-muted);
}

.btn-secondary:hover {
  background: #e2e8f0;
  color: var(--text-main);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(1px);
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* Premium Roster Tables */
.table-container {
  overflow-x: auto;
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.6);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01);
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

th {
  padding: 18px 24px;
  font-weight: 700;
  text-align: left;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
}

td {
  padding: 18px 24px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background-color: #f8fafc;
}

/* Badges / Status Labels */
.badge {
  display: inline-flex;
  padding: 5px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-admin {
  background: rgba(79, 70, 229, 0.08);
  color: var(--primary);
  border: 1px solid rgba(79, 70, 229, 0.15);
}

.badge-manager {
  background: rgba(16, 185, 129, 0.08);
  color: var(--success);
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.badge-employee {
  background: rgba(100, 116, 139, 0.08);
  color: var(--text-muted);
  border: 1px solid rgba(100, 116, 139, 0.15);
}

/* Modern Analytics Grid */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 25px;
  margin-bottom: 35px;
}

.analytics-card {
  background: white;
  padding: 28px;
  border-radius: 22px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
  border: 1px solid rgba(226, 232, 240, 0.6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.analytics-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.04);
  border-color: rgba(79, 70, 229, 0.15);
}

.analytics-info h3 {
  font-size: 13px;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 8px;
  letter-spacing: 0.8px;
  font-weight: 700;
}

.analytics-info .value {
  font-size: 32px;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.03em;
}

.analytics-icon {
  width: 58px;
  height: 58px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  transition: transform 0.3s ease;
}

.analytics-card:hover .analytics-icon {
  transform: scale(1.1) rotate(5deg);
}

/* Forms Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Trend Badges */
.trend-badge {
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 8px;
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: fit-content;
}
.trend-badge.positive {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.15);
}
.trend-badge.neutral {
  background: hsla(var(--primary-hsl), 0.1);
  color: var(--primary);
  border: 1px solid hsla(var(--primary-hsl), 0.15);
}
.trend-badge.negative {
  background: rgba(244, 63, 94, 0.1);
  color: var(--danger);
  border: 1px solid rgba(244, 63, 94, 0.15);
}
</style>