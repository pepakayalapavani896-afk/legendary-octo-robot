/**
 * GramSetu — Authentication & Role Manager
 */

// Citizen Registration
async function handleCitizenRegister(e) {
  e.preventDefault();
  const name = document.getElementById("regName").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const mobile = document.getElementById("regMobile").value.trim();
  const password = document.getElementById("regPassword").value;
  const village = document.getElementById("regVillage").value.trim();
  const preferred_language = document.getElementById("regLang").value;

  if (!name || !email || !mobile || !password) {
    showToast("Please fill in all required fields.", "warning");
    return;
  }

  try {
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, mobile, password, village, preferred_language })
    });
    const data = await res.json();

    if (res.ok && data.success) {
      STATE.token = data.token;
      STATE.user = data.user;
      localStorage.setItem("gramsetu_token", data.token);
      setLanguage(preferred_language);
      closeModal("citizenRegisterModal");
      updateNavUI();
      showToast(`Welcome ${name}! Account created successfully.`, "success");
      showSection("citizen-dashboard");
    } else {
      showToast(data.detail || "Registration failed.", "error");
    }
  } catch (err) {
    showToast("Network error during registration.", "error");
  }
}

// Citizen Login
async function handleCitizenLogin(e) {
  e.preventDefault();
  const identifier = document.getElementById("loginIdentifier").value.trim();
  const password = document.getElementById("loginPassword").value;

  if (!identifier || !password) {
    showToast("Please enter email/mobile and password.", "warning");
    return;
  }

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier, password })
    });
    const data = await res.json();

    if (res.ok && data.success) {
      STATE.token = data.token;
      STATE.user = data.user;
      localStorage.setItem("gramsetu_token", data.token);
      if (data.user.preferred_language) {
        setLanguage(data.user.preferred_language);
      }
      closeModal("citizenLoginModal");
      updateNavUI();
      showToast(`Welcome back, ${data.user.name}!`, "success");
      showSection("citizen-dashboard");
    } else {
      showToast(data.detail || "Invalid login credentials.", "error");
    }
  } catch (err) {
    showToast("Network error during login.", "error");
  }
}

// Authority Login
async function handleAuthorityLogin(e) {
  e.preventDefault();
  const identifier = document.getElementById("authIdentifier").value.trim();
  const password = document.getElementById("authPassword").value;

  if (!identifier || !password) {
    showToast("Please enter official ID and password.", "warning");
    return;
  }

  try {
    const res = await fetch("/api/auth/authority-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier, password })
    });
    const data = await res.json();

    if (res.ok && data.success) {
      STATE.token = data.token;
      STATE.user = data.user;
      localStorage.setItem("gramsetu_token", data.token);
      closeModal("authorityLoginModal");
      updateNavUI();
      showToast(`Welcome Officer ${data.user.name} (${data.user.department || "Admin"}).`, "success");
      showSection("authority-portal");
    } else {
      showToast(data.detail || "Authority verification failed.", "error");
    }
  } catch (err) {
    showToast("Network error during authority login.", "error");
  }
}

// Demo Account Quick Fill Helpers
function fillDemoCitizen(email, password, lang) {
  document.getElementById("loginIdentifier").value = email;
  document.getElementById("loginPassword").value = password;
  if (lang) setLanguage(lang);
}

function fillDemoAuthority(email, password) {
  document.getElementById("authIdentifier").value = email;
  document.getElementById("authPassword").value = password;
}

// Switch between Register & Login Modals
function switchToRegister() {
  closeModal("citizenLoginModal");
  openModal("citizenRegisterModal");
}

function switchToLogin() {
  closeModal("citizenRegisterModal");
  openModal("citizenLoginModal");
}
