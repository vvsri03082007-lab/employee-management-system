<template>
  <div class="collab-container">
    <!-- Sub-navigation Tabs -->
    <div class="collab-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeSubTab === 'chat' }" 
        @click="activeSubTab = 'chat'"
      >
        💬 Direct Messaging
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeSubTab === 'directory' }" 
        @click="activeSubTab = 'directory'"
      >
        📖 Coworker Directory
      </button>
      <button 
        v-if="userRole === 'admin'"
        class="tab-btn" 
        :class="{ active: activeSubTab === 'announcements' }" 
        @click="activeSubTab = 'announcements'"
      >
        📢 Broadcast Announcement
      </button>
    </div>

    <!-- SUB-TAB 1: DIRECT MESSAGING PORTAL -->
    <div v-if="activeSubTab === 'chat'" class="chat-portal card">
      <!-- Conversation Sidebar -->
      <div class="chat-sidebar">
        <div class="sidebar-header">
          <h3>Active Chats</h3>
          <span class="chats-count">{{ conversations.length }} chats</span>
        </div>
        
        <div v-if="conversations.length === 0" class="no-chats-placeholder">
          <p>No active conversations.</p>
          <button class="btn btn-primary btn-sm" style="margin-top: 10px;" @click="activeSubTab = 'directory'">
            Find Coworkers
          </button>
        </div>

        <ul v-else class="chats-list">
          <li 
            v-for="conv in conversations" 
            :key="conv.id" 
            class="chat-list-item"
            :class="{ active: selectedConversation && selectedConversation.id === conv.id }"
            @click="selectConversation(conv)"
          >
            <div class="chat-avatar-wrapper">
              <img 
                v-if="getChatPartner(conv).profile_picture" 
                :src="getChatPartner(conv).profile_picture" 
                class="chat-partner-avatar" 
                alt="Avatar" 
              />
              <div 
                v-else 
                class="chat-partner-avatar" 
                style="display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white;"
              >
                {{ getInitials(getChatPartner(conv).name) }}
              </div>
              <span class="presence-indicator" :class="{ online: getChatPartner(conv).is_online }"></span>
            </div>
            <div class="chat-item-details">
              <div class="chat-item-row">
                <span class="chat-partner-name">
                  {{ getChatPartner(conv).name }}
                  <span v-if="getChatPartner(conv).status_emoji" class="partner-status-emoji" :title="getChatPartner(conv).custom_status">
                    {{ getChatPartner(conv).status_emoji }}
                  </span>
                </span>
                <span class="chat-time">{{ formatTime(conv.updated_at) }}</span>
              </div>
              <div class="chat-item-row" style="margin-top: 4px;">
                <span class="chat-preview">
                  {{ conv.last_message ? conv.last_message.content : 'No messages yet' }}
                </span>
                <span v-if="conv.unread_count > 0" class="chat-unread-badge">
                  {{ conv.unread_count }}
                </span>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Chat Conversation Window -->
      <div class="chat-window">
        <div v-if="!selectedConversation" class="no-selected-chat">
          <div class="empty-state-icon">💬</div>
          <h2>Select a Coworker</h2>
          <p>Start a secure conversation with any teammate inside your company workspace.</p>
        </div>

        <div v-else class="active-chat-container">
          <!-- Chat Window Header -->
          <div class="chat-window-header">
            <div class="header-avatar-wrapper">
              <img 
                v-if="selectedPartner.profile_picture" 
                :src="selectedPartner.profile_picture" 
                class="window-partner-avatar" 
              />
              <div 
                v-else 
                class="window-partner-avatar" 
                style="display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white;"
              >
                {{ getInitials(selectedPartner.name) }}
              </div>
              <span class="presence-indicator" :class="{ online: selectedPartner.is_online }"></span>
            </div>
            <div class="header-partner-info">
              <h3 style="display: flex; align-items: center; gap: 6px;">
                {{ selectedPartner.name }}
                <span v-if="selectedPartner.status_emoji" class="header-status-emoji" :title="selectedPartner.custom_status" style="font-size: 16px;">
                  {{ selectedPartner.status_emoji }}
                </span>
              </h3>
              <p style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                {{ selectedPartner.designation }} &bull; <span class="dept-badge">{{ selectedPartner.department }}</span>
                <span v-if="selectedPartner.custom_status" class="header-status-text" style="font-style: italic; opacity: 0.85;">
                  &bull; "{{ selectedPartner.custom_status }}"
                </span>
              </p>
            </div>
            <div class="header-status">
              <span class="status-text" :class="{ online: selectedPartner.is_online }">
                {{ selectedPartner.is_online ? 'Online now' : 'Offline' }}
              </span>
            </div>
          </div>

          <!-- Messages Scroller -->
          <div class="messages-scroller" ref="messagesContainer">
            <div v-if="messages.length === 0" class="empty-chat-state">
              <p>This is the beginning of your direct message history. Message logs are fully isolated and secure.</p>
            </div>
            <div 
              v-for="msg in messages" 
              :key="msg.id" 
              class="message-bubble-wrapper"
              :class="{ 'sent': msg.sender_email === myEmail, 'received': msg.sender_email !== myEmail }"
            >
              <div class="bubble-body">
                <div class="bubble-content-row">
                  <p class="bubble-text">{{ msg.content }}</p>
                  <button 
                    v-if="msg.sender_email === myEmail"
                    class="delete-msg-btn"
                    title="Delete message"
                    @click="deleteMessage(msg.id)"
                  >
                    &times;
                  </button>
                </div>
                <div class="bubble-meta">
                  <span class="msg-time">{{ formatFullTime(msg.created_at) }}</span>
                  <span v-if="msg.sender_email === myEmail" class="seen-indicator">
                    {{ msg.is_seen ? '✓✓ Seen' : '✓ Sent' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Message Input -->
          <form @submit.prevent="sendMessage" class="message-input-area">
            <input 
              type="text" 
              placeholder="Type a secure message..." 
              v-model="newMessageText"
              class="input msg-input-box"
              required 
            />
            <button type="submit" class="btn btn-primary send-msg-btn" :disabled="sendingMessage">
              {{ sendingMessage ? 'Sending...' : 'Send 🚀' }}
            </button>
          </form>
        </div>
      </div>
    </div>

    <!-- SUB-TAB 2: COWORKER DIRECTORY -->
    <div v-if="activeSubTab === 'directory'" class="directory-portal card">
      <div class="dir-header">
        <div>
          <h2>Corporate Teammates Directory</h2>
          <p>Search and directly communicate with coworkers inside your company tenant.</p>
        </div>
        <input 
          type="text" 
          placeholder="Search teammates by name, designation, or department..." 
          v-model="dirSearchQuery" 
          class="input dir-search-box"
        />
      </div>

      <div v-if="filteredCoworkers.length === 0" class="no-results-placeholder">
        <p>No active teammates match your query.</p>
      </div>

      <div v-else class="dir-grid">
        <div v-for="user in filteredCoworkers" :key="user.id" class="dir-card">
          <div class="dir-card-avatar-wrapper">
            <img 
              v-if="user.profile_picture" 
              :src="user.profile_picture" 
              class="dir-card-avatar" 
            />
            <div 
              v-else 
              class="dir-card-avatar" 
              style="display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; background: linear-gradient(135deg, #94a3b8, #64748b); color: white;"
            >
              {{ getInitials(user.name) }}
            </div>
            <span class="presence-indicator" :class="{ online: user.is_online }"></span>
          </div>
          <h3 style="display: flex; align-items: center; justify-content: center; gap: 6px;">
            {{ user.name }}
            <span v-if="user.status_emoji" class="dir-status-emoji" :title="user.custom_status" style="font-size: 16px;">
              {{ user.status_emoji }}
            </span>
          </h3>
          <p class="dir-card-title">{{ user.designation }}</p>
          <p v-if="user.custom_status" class="dir-custom-status" style="font-size: 13px; font-style: italic; opacity: 0.85; margin: -5px 0 12px 0;">
            "{{ user.custom_status }}"
          </p>
          <div class="dir-card-badges">
            <span class="dept-badge">{{ user.department }}</span>
            <span class="badge" :class="'badge-' + user.role">{{ user.role }}</span>
          </div>
          <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 15px 0;" />
          <div class="dir-card-contact">
            <span>📧 {{ user.email }}</span>
            <span v-if="user.is_online" class="online-indicator">● Active now</span>
            <span v-else class="offline-indicator">Last active: {{ formatTime(user.last_seen) }}</span>
          </div>
          <button class="btn btn-primary btn-sm dm-trigger-btn" @click="startDirectMessage(user)">
            💬 Direct Message
          </button>
        </div>
      </div>
    </div>

    <!-- SUB-TAB 3: BROADCAST ANNOUNCEMENTS -->
    <div v-if="activeSubTab === 'announcements' && userRole === 'admin'" class="announcements-portal card">
      <h2>📢 Dispatch Company-Wide Announcement</h2>
      <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">
        Broadcast critical information to all employee and manager dashboards in your company tenant instantly.
      </p>

      <form @submit.prevent="broadcastAnnouncement" class="announcement-form">
        <div class="form-group">
          <label>Announcement Title</label>
          <input 
            type="text" 
            v-model="announcement.title" 
            placeholder="e.g., Annual Workspace Review or Server Maintenance" 
            required 
            class="input"
          />
        </div>
        <div class="form-group" style="margin-top: 15px;">
          <label>Detailed Message</label>
          <textarea 
            v-model="announcement.description" 
            placeholder="Provide a comprehensive explanation..." 
            rows="5"
            required
            class="input text-area"
          ></textarea>
        </div>
        <button type="submit" class="btn btn-success" :disabled="sendingAnnouncement" style="margin-top: 20px;">
          {{ sendingAnnouncement ? 'Broadcasting...' : '📢 Broadcast Instantly' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { api } from '../api'

export default {
  name: 'CollaborationPortal',
  data() {
    return {
      activeSubTab: 'chat',
      userRole: localStorage.getItem('role') || 'employee',
      myEmail: (localStorage.getItem('username') || '') + '@', // prefix approximation
      conversations: [],
      selectedConversation: null,
      messages: [],
      newMessageText: '',
      sendingMessage: false,
      coworkers: [],
      dirSearchQuery: '',
      announcement: {
        title: '',
        description: ''
      },
      sendingAnnouncement: false,
      pollingInterval: null
    }
  },
  computed: {
    selectedPartner() {
      if (!this.selectedConversation) return null;
      return this.getChatPartner(this.selectedConversation);
    },
    filteredCoworkers() {
      const q = this.dirSearchQuery.toLowerCase().trim();
      if (!q) return this.coworkers;
      return this.coworkers.filter(user => 
        user.name.toLowerCase().includes(q) ||
        user.email.toLowerCase().includes(q) ||
        user.designation.toLowerCase().includes(q) ||
        user.department.toLowerCase().includes(q)
      );
    }
  },
  async mounted() {
    // Attempt exact email setup
    const username = localStorage.getItem('username') || '';
    if (username.includes('@')) {
      this.myEmail = username.toLowerCase();
    } else {
      this.myEmail = username.toLowerCase() + '@';
    }
    
    await this.fetchCoworkers();
    await this.fetchConversations();
    
    // Heartbeat presence instantly
    this.sendHeartbeat();
    
    // Polling setup for active collaboration
    this.pollingInterval = setInterval(async () => {
      await this.sendHeartbeat();
      await this.fetchConversations();
      if (this.selectedConversation) {
        await this.fetchMessages(this.selectedConversation.id, false); // Fetch without resetting scroll
      }
    }, 4000);
  },
  unmounted() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }
  },
  methods: {
    async fetchCoworkers() {
      try {
        const res = await api.get('coworkers/');
        this.coworkers = res.data;
      } catch (err) {
        console.error("Failed to load directory coworkers:", err);
      }
    },
    async fetchConversations() {
      try {
        const res = await api.get('conversations/');
        this.conversations = res.data;
      } catch (err) {
        console.error("Failed to load conversations:", err);
      }
    },
    async fetchMessages(convId, autoScroll = true) {
      try {
        const res = await api.get(`conversations/${convId}/messages/`);
        this.messages = res.data;
        if (autoScroll) {
          this.scrollChatToBottom();
        }
      } catch (err) {
        console.error("Failed to load message history:", err);
      }
    },
    async selectConversation(conv) {
      this.selectedConversation = conv;
      await this.fetchMessages(conv.id, true);
    },
    async startDirectMessage(coworker) {
      try {
        const res = await api.post('conversations/', { recipient_id: coworker.id });
        const conversation = res.data;
        await this.fetchConversations();
        
        // Find matched conversation object and select it
        const match = this.conversations.find(c => c.id === conversation.id) || conversation;
        await this.selectConversation(match);
        
        // Switch tab to DM
        this.activeSubTab = 'chat';
      } catch (err) {
        console.error("Failed to initialize conversation:", err);
        alert("Failed to start conversation. Please check coworker isolation policies.");
      }
    },
    async sendMessage() {
      if (!this.newMessageText.trim() || !this.selectedConversation) return;
      this.sendingMessage = true;
      try {
        await api.post(`conversations/${this.selectedConversation.id}/messages/`, {
          content: this.newMessageText
        });
        this.newMessageText = '';
        await this.fetchMessages(this.selectedConversation.id, true);
        await this.fetchConversations();
      } catch (err) {
        console.error("Failed to dispatch message:", err);
        alert("Message dispatch failed. Access forbidden.");
      } finally {
        this.sendingMessage = false;
      }
    },
    async deleteMessage(msgId) {
      if (!confirm("Are you sure you want to permanently delete this message?")) return;
      try {
        await api.delete(`messages/${msgId}/`);
        if (this.selectedConversation) {
          await this.fetchMessages(this.selectedConversation.id, false);
        }
      } catch (err) {
        console.error("Failed to delete message:", err);
        alert("Message deletion denied.");
      }
    },
    async broadcastAnnouncement() {
      if (!this.announcement.title.trim() || !this.announcement.description.trim()) return;
      this.sendingAnnouncement = true;
      try {
        await api.post('announcements/', this.announcement);
        this.announcement = { title: '', description: '' };
        alert("📢 Announcement successfully broadcast to all company tenants!");
      } catch (err) {
        console.error(err);
        alert("Failed to broadcast announcement.");
      } finally {
        this.sendingAnnouncement = false;
      }
    },
    async sendHeartbeat() {
      try {
        await api.post('presence/heartbeat/');
      } catch (err) {
        console.warn("Heartbeat update omitted:", err);
      }
    },
    getChatPartner(conv) {
      // Return the participant who is not me
      const partner = conv.participants.find(p => !p.email.toLowerCase().startsWith(this.myEmail.toLowerCase()) && p.email.toLowerCase() !== this.myEmail.toLowerCase());
      return partner || conv.participants[0] || {};
    },
    scrollChatToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    },
    formatTime(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    formatFullTime(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    getInitials(name) {
      if (!name) return 'US';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
  }
}
</script>

<style scoped>
.collab-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

/* Tab buttons */
.collab-tabs {
  display: flex;
  gap: 12px;
  background: var(--glass-bg);
  padding: 8px;
  border-radius: 14px;
  align-self: flex-start;
  border: 1px solid var(--border-light);
}

.tab-btn {
  padding: 10px 18px;
  border: none;
  border-radius: 10px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: var(--primary);
  background: hsla(var(--primary-hsl), 0.05);
}

.tab-btn.active {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  color: white;
  box-shadow: 0 4px 12px var(--primary-glow);
}

/* Chat Portal Card */
.chat-portal {
  display: flex;
  height: 600px;
  padding: 0 !important;
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.chat-sidebar {
  width: 320px;
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.08);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
}

.chats-count {
  font-size: 11px;
  background: hsla(var(--primary-hsl), 0.1);
  color: var(--primary);
  padding: 3px 8px;
  border-radius: 9999px;
  font-weight: 700;
}

.no-chats-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: var(--text-muted);
  text-align: center;
}

.chats-list {
  flex: 1;
  overflow-y: auto;
  list-style: none;
}

.chat-list-item {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chat-list-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.chat-list-item.active {
  background: hsla(var(--primary-hsl), 0.05);
  border-left: 4px solid var(--primary);
}

.chat-avatar-wrapper {
  position: relative;
  width: 44px;
  height: 44px;
}

.chat-partner-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  background: var(--border-light);
}

.presence-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--text-muted);
  border: 2px solid var(--bg-main);
}

.presence-indicator.online {
  background: #10b981;
}

.chat-item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-partner-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-main);
}

.chat-time {
  font-size: 11px;
  color: var(--text-muted);
}

.chat-preview {
  font-size: 12px;
  color: var(--text-muted);
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  max-width: 160px;
}

.chat-unread-badge {
  background: var(--danger);
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 9999px;
  min-width: 18px;
  text-align: center;
}

/* Chat Window */
.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.no-selected-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: var(--text-muted);
  text-align: center;
  background: transparent;
}

.empty-state-icon {
  font-size: 54px;
  margin-bottom: 20px;
}

.active-chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: transparent;
}

.chat-window-header {
  padding: 16px 25px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-avatar-wrapper {
  position: relative;
  width: 48px;
  height: 48px;
}

.window-partner-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  background: var(--border-light);
}

.header-partner-info h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
}

.header-partner-info p {
  font-size: 12px;
  color: var(--text-muted);
}

.header-status {
  margin-left: auto;
}

.status-text {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  background: var(--border-light);
  padding: 4px 10px;
  border-radius: 6px;
}

.status-text.online {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.messages-scroller {
  flex: 1;
  padding: 25px;
  overflow-y: auto;
  background: rgba(15, 23, 42, 0.05);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.empty-chat-state {
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  padding: 30px;
  max-width: 400px;
  margin: 0 auto;
}

.message-bubble-wrapper {
  display: flex;
  width: 100%;
}

.message-bubble-wrapper.sent {
  justify-content: flex-end;
}

.message-bubble-wrapper.received {
  justify-content: flex-start;
}

.bubble-body {
  max-width: 65%;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bubble-content-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bubble-text {
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  word-break: break-word;
}

.sent .bubble-text {
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  color: white;
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 10px var(--primary-glow);
}

.received .bubble-text {
  background: var(--glass-bg);
  color: var(--text-main);
  border-bottom-left-radius: 4px;
  border: 1px solid var(--border-light);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
}

.delete-msg-btn {
  background: transparent;
  border: none;
  color: var(--danger);
  font-size: 18px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
  padding: 0 4px;
}

.bubble-content-row:hover .delete-msg-btn {
  opacity: 1;
}

.bubble-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 10px;
  color: var(--text-muted);
  font-weight: 600;
  padding: 0 4px;
}

.sent .bubble-meta {
  justify-content: flex-end;
}

.seen-indicator {
  color: var(--primary);
}

/* Message Input Box */
.message-input-area {
  padding: 16px 20px;
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: 12px;
  align-items: center;
}

.msg-input-box {
  flex: 1;
  margin-bottom: 0 !important;
}

.send-msg-btn {
  flex-shrink: 0;
  height: 48px;
}

/* Directory Portal Card */
.dir-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.dir-search-box {
  width: 350px;
  margin-bottom: 0 !important;
}

.no-results-placeholder {
  text-align: center;
  color: var(--text-muted);
  padding: 50px 0;
}

.dir-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.dir-card {
  background: var(--glass-bg);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  padding: 25px;
  text-align: center;
  transition: all 0.3s ease;
}

.dir-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: var(--primary);
}

.dir-card-avatar-wrapper {
  position: relative;
  width: 68px;
  height: 68px;
  margin: 0 auto 15px;
}

.dir-card-avatar {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: var(--border-light);
  object-fit: cover;
  border: 2px solid var(--border-light);
}

.dir-card h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}

.dir-card-title {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 12px;
}

.dir-card-badges {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.dir-card-contact {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: center;
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 20px;
}

.online-indicator {
  color: #10b981;
  font-weight: 700;
  font-size: 11px;
}

.offline-indicator {
  color: var(--text-muted);
  font-size: 11px;
}

.dm-trigger-btn {
  width: 100%;
}

/* Announcement Form styling */
.announcement-form {
  display: flex;
  flex-direction: column;
  max-width: 600px;
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
}

.text-area {
  resize: vertical;
  line-height: 1.5;
}
</style>
