# 🚀 WorkSphere HRMS — Modern Multi-Tenant SaaS Roster & Collaboration Cockpit

WorkSphere is a state-of-the-art, high-performance Human Resource Management System (HRMS) built with **Django REST Framework** on the backend and **Vue.js** on the frontend. The platform features an ultra-premium glassmorphism design system, real-time peer-to-peer workspace chat portals, and customizable dynamic schema extensions.

---

## ✨ Features Spotlight

### 1. 🌗 Premium Adaptive Light/Dark Design Engine
* **Fluid Global Theme Sync**: A persistent one-click theme switcher available on all screens—including a floating glassmorphic toggle directly on the authentication portal.
* **Modern Glassmorphic Interface**: Border highlights (`var(--border-light)`), harmonized custom HSL coordinates, premium Outfit typography, dynamic card translations, and custom scrollbar overrides.

### 2. 📊 Live Workspace Activity Feed & Compliance Audit
* **Real-time Session Feed**: A dynamic timeline grid tracking all administrator actions (adding staff, profile updates, archiving, custom field additions/deletions, or company branding modifications).
* **Color-Coded Timeline Bullets**: Glowing neons highlighting specific events:
  * 🟢 **Green** (`bullet-create`) — Additions & setups
  * 🟣 **Purple** (`bullet-update`) — Profile & branding updates
  * 🔴 **Rose** (`bullet-delete`) — Soft deletions & field drops
  * ⚪ **Slate** (`bullet-system`) — Workspace session initializations
* **Session compliance resets** with built-in clean-up confirmation checks.

### 3. 💬 Collaboration Portal & DM Stream
* **Glassmorphic Chat Viewports**: Clean Direct Messaging bubbles with glowing borders and metadata tags.
* **Teammate Directories**: Live grids showing teammate profiles, active heartbeats, and designations.
* **Broadcast Announcements**: System-wide announcements that publish updates instantly to all employee and manager feeds.

### 4. ⚡ High-Performance CSV Roster Exporter
* **Schema-Aware Compilation**: Download your entire staff roster in a single click using browser Blobs.
* **Custom Field Matching**: Dynamically reads and compiles all dynamic custom fields as separate CSV columns alongside core databases (Name, Email, Department, Designation, and phone numbers).

### 5. 🔍 Responsive Search & Department Filter
* **Instant Filters**: Case-insensitive filtering of staff rosters by Name, Email, or Designation.
* **Department Breakdowns**: Dynamic department stats cards with reactive HSL progress bars.

### 6. ⚙️ Dynamic Schema Builder (Custom Fields)
* **Custom DB Extensions**: Create custom attributes (Text, Options, required checkmarks, salary, tech stacks, or contact fields) on the fly without making manual database table migrations.

### 7. 📡 Real-Time Presence Heartbeats
* **Teammate Active Status**: Frontends push a heartbeat ping to `/api/presence/heartbeat/` every 10 seconds.
* **Automatic Eviction**: Teammates inactive for more than 30 seconds are automatically swept and rendered as "Offline" dynamically.

### 8. 🔒 Hardened OTP & Auth Normalization
* **Normalized Authentication**: Strict lowercase and white-space stripping on all credentials, resolving casing typos.
* **Developer Terminal Console Backend**: OTP passcodes log directly to the terminal stdout for instant checking.

---

## 🛠️ Installation & Setup

### 1. Backend REST API (Django)
Navigate to the backend directory:
```bash
cd employeelog-django
```

Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run database migrations:
```bash
python manage.py migrate
```

Start the API development server:
```bash
python manage.py runserver
```
> The API will be active at `http://127.0.0.1:8000/`.

#### 🔑 Helper Commands:
* **Reset Authentication & Database**: Purge all users, databases, active session cookies, and JWT caches back to a completely clean slate:
  ```bash
  python manage.py reset_auth
  ```

---

### 2. Frontend SPA (Vue.js 3)
Navigate to the frontend directory:
```bash
cd employeelog-vue
```

Install package dependencies:
```bash
npm install
```

Start the hot-reloading development server:
```bash
npm run serve
```
> The web app will run locally at `http://localhost:8080/`.

---

## 🎨 Technology Stack
* **Frontend**: Vue 3 SPA, Vue Router, HSL Color Coordination, Vanilla Glassmorphism CSS variables, Axios API client.
* **Backend**: Django, Django REST Framework, SimpleJWT (JSON Web Tokens), SQLite 3 Database.
