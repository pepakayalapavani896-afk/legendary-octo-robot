/**
 * GramSetu — Global Application Controller & State
 */

const STATE = {
  user: null,
  token: localStorage.getItem("gramsetu_token") || null,
  activeSection: "home",
  notifications: [],
  unreadNotifsCount: 0
};

// Global Toast System
function showToast(message, type = "info", duration = 4000) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  
  let icon = "ℹ️";
  if (type === "success") icon = "✅";
  if (type === "error") icon = "⚠️";
  if (type === "warning") icon = "🔔";

  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Router & Section Switcher
function showSection(sectionId) {
  // Role Protection Guard
  if (sectionId === "authority-portal") {
    if (!STATE.user || (STATE.user.role !== "authority" && STATE.user.role !== "admin")) {
      showToast(t("demoAccountNotice") || "Authority credentials required.", "error");
      openModal("authorityLoginModal");
      return;
    }
  }

  if (sectionId === "report" || sectionId === "citizen-dashboard" || sectionId === "my-complaints") {
    if (!STATE.token || !STATE.user) {
      showToast(t("demoAccountNotice") || "Please login as a Citizen first.", "warning");
      openModal("citizenLoginModal");
      return;
    }
  }

  // Update DOM active sections
  document.querySelectorAll(".page-section").forEach(sec => {
    sec.classList.remove("active");
  });

  const target = document.getElementById(sectionId);
  if (target) {
    target.classList.add("active");
    STATE.activeSection = sectionId;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Update nav links active styling
  document.querySelectorAll(".nav-link").forEach(link => {
    if (link.getAttribute("data-section") === sectionId) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });

  // Trigger section-specific loaders
  if (sectionId === "map") {
    if (window.initProblemMap) window.initProblemMap();
  } else if (sectionId === "authority-portal") {
    if (window.loadAuthorityDashboard) window.loadAuthorityDashboard();
  } else if (sectionId === "my-complaints") {
    if (window.loadMyComplaints) window.loadMyComplaints();
  } else if (sectionId === "report") {
    if (window.initReportWizard) window.initReportWizard();
  } else if (sectionId === "citizen-dashboard") {
    if (window.loadCitizenDashboard) window.loadCitizenDashboard();
  }
}

// Modal Control Helpers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("active");
    document.body.style.overflow = "hidden";
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("active");
    document.body.style.overflow = "auto";
  }
}

// Fetch Current Profile
async function checkAuthSession() {
  if (!STATE.token) {
    updateNavUI();
    return;
  }

  try {
    const res = await fetch("/api/auth/me", {
      headers: { "Authorization": `Bearer ${STATE.token}` }
    });
    if (res.ok) {
      const data = await res.json();
      STATE.user = data.user;
      if (STATE.user.preferred_language) {
        setLanguage(STATE.user.preferred_language);
      }
    } else {
      // Token expired or invalid
      logout(false);
    }
  } catch (err) {
    console.error("Auth check failed:", err);
  } finally {
    updateNavUI();
  }
}

function updateNavUI() {
  const guestGroup = document.getElementById("navGuestGroup");
  const userGroup = document.getElementById("navUserGroup");
  const userNameEl = document.getElementById("navUserName");
  const userRoleEl = document.getElementById("navUserRole");
  const navMyComplaintsLink = document.getElementById("navMyComplaintsLink");
  const navAuthorityLink = document.getElementById("navAuthorityLink");

  if (STATE.user && STATE.token) {
    if (guestGroup) guestGroup.style.display = "none";
    if (userGroup) userGroup.style.display = "flex";
    if (userNameEl) userNameEl.textContent = STATE.user.name;
    if (userRoleEl) {
      userRoleEl.textContent = STATE.user.role === "authority" 
        ? `🏛️ ${STATE.user.department || "Officer"}` 
        : `👤 ${STATE.user.village || "Citizen"}`;
    }

    if (STATE.user.role === "authority" || STATE.user.role === "admin") {
      if (navAuthorityLink) navAuthorityLink.style.display = "flex";
      if (navMyComplaintsLink) navMyComplaintsLink.style.display = "none";
    } else {
      if (navAuthorityLink) navAuthorityLink.style.display = "none";
      if (navMyComplaintsLink) navMyComplaintsLink.style.display = "flex";
    }
    fetchNotifications();
  } else {
    if (guestGroup) guestGroup.style.display = "flex";
    if (userGroup) userGroup.style.display = "none";
    if (navMyComplaintsLink) navMyComplaintsLink.style.display = "none";
    if (navAuthorityLink) navAuthorityLink.style.display = "flex";
  }
}

function logout(showMsg = true) {
  STATE.token = null;
  STATE.user = null;
  localStorage.removeItem("gramsetu_token");
  updateNavUI();
  showSection("home");
  if (showMsg) showToast("Logged out successfully.", "info");
}

// Notifications System
async function fetchNotifications() {
  if (!STATE.token) return;
  try {
    const res = await fetch("/api/notifications", {
      headers: { "Authorization": `Bearer ${STATE.token}` }
    });
    if (res.ok) {
      const data = await res.json();
      STATE.notifications = data.notifications || [];
      STATE.unreadNotifsCount = STATE.notifications.filter(n => !n.is_read).length;
      renderNotificationBadge();
    }
  } catch (err) {
    console.error("Notifications fetch error:", err);
  }
}

function renderNotificationBadge() {
  const badge = document.getElementById("notifBadge");
  if (badge) {
    if (STATE.unreadNotifsCount > 0) {
      badge.textContent = STATE.unreadNotifsCount;
      badge.style.display = "inline-flex";
    } else {
      badge.style.display = "none";
    }
  }
}

function openNotificationsModal() {
  const list = document.getElementById("notifsListContainer");
  if (!list) return;

  if (STATE.notifications.length === 0) {
    list.innerHTML = `<div style="text-align:center; padding: 2rem; color: #94A3B8;">No notifications yet.</div>`;
  } else {
    list.innerHTML = STATE.notifications.map(n => {
      let title = n[`title_${CURRENT_LANG}`] || n.title_en;
      let msg = n[`message_${CURRENT_LANG}`] || n.message_en;
      return `
        <div style="background: ${n.is_read ? '#F8FAFC' : '#EFF6FF'}; border-left: 4px solid ${n.is_read ? '#CBD5E1' : '#2563EB'}; padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem;">
          <div style="font-weight: 700; color: #0B2239; margin-bottom: 0.25rem;">${title}</div>
          <div style="font-size: 0.88rem; color: #475569;">${msg}</div>
          <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.35rem;">📅 ${new Date(n.created_at).toLocaleString()}</div>
        </div>
      `;
    }).join("");
  }

  openModal("notificationsModal");

  // Mark all as read
  if (STATE.unreadNotifsCount > 0) {
    fetch("/api/notifications/read-all", {
      method: "POST",
      headers: { "Authorization": `Bearer ${STATE.token}` }
    }).then(() => {
      STATE.unreadNotifsCount = 0;
      renderNotificationBadge();
    });
  }
}

// App Initialization
document.addEventListener("DOMContentLoaded", () => {
  applyTranslations();
  checkAuthSession();

  // Language buttons
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const lang = e.currentTarget.getAttribute("data-lang");
      setLanguage(lang);
    });
  });

  // Periodic notifications check
  setInterval(fetchNotifications, 15000);
});
