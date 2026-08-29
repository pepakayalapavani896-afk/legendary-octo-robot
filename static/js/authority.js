/**
 * GramSetu — Authority Command Center & Citizen Grievance Tracker
 */

let CURRENT_INSPECTING_COMPLAINT_ID = null;

// ==========================================
// 1. Citizen "My Complaints" & Timeline
// ==========================================
async function loadMyComplaints() {
  const container = document.getElementById("myComplaintsContainer");
  if (!container || !STATE.token) return;

  container.innerHTML = `<div style="text-align:center; padding: 2rem; color: #64748B;">${t("loading")}</div>`;

  try {
    const res = await fetch("/api/complaints/my", {
      headers: { "Authorization": `Bearer ${STATE.token}` }
    });
    const data = await res.json();

    if (res.ok && data.complaints) {
      renderMyComplaintsList(data.complaints);
    } else {
      container.innerHTML = `<div style="text-align:center; padding: 2rem; color: #EF4444;">Failed to load complaints.</div>`;
    }
  } catch (err) {
    container.innerHTML = `<div style="text-align:center; padding: 2rem; color: #EF4444;">Network error loading complaints.</div>`;
  }
}

function renderMyComplaintsList(complaints) {
  const container = document.getElementById("myComplaintsContainer");
  if (!container) return;

  if (complaints.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding: 3rem; background: #FFFFFF; border-radius: 12px; border: 1px solid #E2E8F0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📋</div>
        <h3 style="color: #0B2239; margin-bottom: 0.5rem;">No Grievances Submitted Yet</h3>
        <p style="color: #64748B; margin-bottom: 1.5rem;">You haven't reported any infrastructure issues yet.</p>
        <button class="btn btn-accent" onclick="showSection('report')">📸 Report a Problem Now</button>
      </div>
    `;
    return;
  }

  container.innerHTML = complaints.map(c => {
    // Stepper State Logic
    const steps = ["Submitted", "Under Review", "Assigned", "In Progress", "Resolved"];
    const currentIdx = steps.indexOf(c.status);

    let stepperHtml = `
      <div class="timeline-stepper">
        <div class="timeline-step ${currentIdx >= 0 ? 'completed' : ''}">
          <div class="timeline-circle">1</div>
          <span class="timeline-label">Submitted</span>
        </div>
        <div class="timeline-step ${currentIdx >= 1 ? 'completed' : ''}">
          <div class="timeline-circle">2</div>
          <span class="timeline-label">AI Review</span>
        </div>
        <div class="timeline-step ${currentIdx >= 2 ? 'completed' : ''}">
          <div class="timeline-circle">3</div>
          <span class="timeline-label">Assigned</span>
        </div>
        <div class="timeline-step ${currentIdx >= 3 ? 'completed' : ''}">
          <div class="timeline-circle">4</div>
          <span class="timeline-label">In Progress</span>
        </div>
        <div class="timeline-step ${currentIdx >= 4 ? 'completed' : ''}">
          <div class="timeline-circle">5</div>
          <span class="timeline-label">Resolved</span>
        </div>
      </div>
    `;

    // Photo Display Rule
    let photoDisplay = "";
    if (c.image_url) {
      photoDisplay = `
        <div style="width: 140px; height: 110px; border-radius: 8px; overflow: hidden; flex-shrink: 0; border: 1px solid #E2E8F0;">
          <img src="${c.image_url}" alt="Citizen Uploaded Evidence" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
      `;
    } else if (c.is_demo) {
      photoDisplay = `
        <div style="width: 140px; height: 110px; border-radius: 8px; background: #F1F5F9; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 0.72rem; color: #64748B; font-weight: bold; border: 1px dashed #CBD5E1; padding: 4px;">
          DEMO DATA (Prototype)
        </div>
      `;
    } else {
      photoDisplay = `
        <div style="width: 140px; height: 110px; border-radius: 8px; background: #F8FAFC; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 0.72rem; color: #94A3B8; border: 1px dashed #CBD5E1; padding: 4px;">
          No Photo Evidence
        </div>
      `;
    }

    return `
      <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.75rem; border-bottom: 1px solid #F1F5F9; padding-bottom: 0.75rem; margin-bottom: 1rem;">
          <div>
            <span style="font-weight: 800; font-size: 1.1rem; color: #0B2239;">#${c.complaint_id}</span>
            <span style="font-size: 0.8rem; color: #64748B; margin-left: 0.5rem;">📅 ${new Date(c.created_at).toLocaleDateString()}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="priority-tag priority-${c.priority.toLowerCase()}">${c.priority}</span>
            <span class="status-tag status-${c.status.toLowerCase().replace(' ', '-')}">${c.status}</span>
          </div>
        </div>

        <div style="display: flex; gap: 1.25rem; flex-wrap: wrap;">
          ${photoDisplay}
          <div style="flex: 1; min-width: 240px;">
            <div style="font-weight: 700; color: #1E3A8A; font-size: 1rem; margin-bottom: 0.35rem;">
              🏷️ ${c.category} &rarr; <span style="font-size: 0.88rem; color: #475569;">${c.department}</span>
            </div>
            <p style="font-size: 0.92rem; color: #334155; margin-bottom: 0.5rem; line-height: 1.5;">
              ${c.description}
            </p>
            <div style="font-size: 0.82rem; color: #64748B;">
              📍 <strong>${c.location_name}</strong>
            </div>

            ${c.resolution_notes ? `
              <div style="margin-top: 0.75rem; background: #F0FDF4; border-left: 4px solid #10B981; padding: 0.6rem 0.85rem; border-radius: 6px; font-size: 0.85rem; color: #065F46;">
                <strong>Resolution Note:</strong> ${c.resolution_notes}
              </div>
            ` : ''}
          </div>
        </div>

        ${stepperHtml}
      </div>
    `;
  }).join("");
}

// ==========================================
// 2. Authority Portal & Inspection
// ==========================================
async function loadAuthorityDashboard() {
  if (!STATE.token || (STATE.user.role !== "authority" && STATE.user.role !== "admin")) {
    showToast("Authority access restricted.", "error");
    return;
  }

  await loadAuthorityStats();
  await loadAuthorityComplaintsTable();
}

async function loadAuthorityStats() {
  try {
    const res = await fetch("/api/authority/stats", {
      headers: { "Authorization": `Bearer ${STATE.token}` }
    });
    const data = await res.json();

    if (res.ok && data.success) {
      const s = data.stats;
      document.getElementById("authStatTotal").textContent = s.total;
      document.getElementById("authStatPending").textContent = s.pending;
      document.getElementById("authStatInProgress").textContent = s.in_progress;
      document.getElementById("authStatResolved").textContent = s.resolved;
      document.getElementById("authStatHighPriority").textContent = s.high_priority;
      document.getElementById("authStatHotspots").textContent = s.hotspots_count;

      renderCategoryBreakdownList(data.category_breakdown);
    }
  } catch (err) {
    console.error("Authority stats error:", err);
  }
}

function renderCategoryBreakdownList(categories) {
  const container = document.getElementById("categoryBreakdownContainer");
  if (!container || !categories) return;

  const total = categories.reduce((acc, c) => acc + c.count, 0) || 1;

  container.innerHTML = categories.map(cat => {
    const pct = Math.round((cat.count / total) * 100);
    return `
      <div style="margin-bottom: 0.85rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.25rem;">
          <span style="color: #0B2239;">${cat.category}</span>
          <span style="color: #64748B;">${cat.count} (${pct}%)</span>
        </div>
        <div style="width: 100%; height: 8px; background: #E2E8F0; border-radius: 99px; overflow: hidden;">
          <div style="width: ${pct}%; height: 100%; background: linear-gradient(90deg, #1E40AF, #3B82F6); border-radius: 99px;"></div>
        </div>
      </div>
    `;
  }).join("");
}

async function loadAuthorityComplaintsTable() {
  const tableBody = document.getElementById("authorityTableBody");
  if (!tableBody) return;

  const statusFilter = document.getElementById("authFilterStatus") ? document.getElementById("authFilterStatus").value : "all";
  const catFilter = document.getElementById("authFilterCategory") ? document.getElementById("authFilterCategory").value : "all";
  const priorityFilter = document.getElementById("authFilterPriority") ? document.getElementById("authFilterPriority").value : "all";
  const search = document.getElementById("authSearchInput") ? document.getElementById("authSearchInput").value.trim() : "";

  tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2rem; color: #64748B;">${t("loading")}</td></tr>`;

  try {
    let url = `/api/authority/complaints?status_filter=${statusFilter}&category_filter=${catFilter}&priority_filter=${priorityFilter}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;

    const res = await fetch(url, {
      headers: { "Authorization": `Bearer ${STATE.token}` }
    });
    const data = await res.json();

    if (res.ok && data.complaints) {
      renderAuthorityTableRows(data.complaints);
    } else {
      tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color: #EF4444; padding: 1.5rem;">Failed to load complaints.</td></tr>`;
    }
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color: #EF4444; padding: 1.5rem;">Network error.</td></tr>`;
  }
}

function renderAuthorityTableRows(complaints) {
  const tableBody = document.getElementById("authorityTableBody");
  if (!tableBody) return;

  if (complaints.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2.5rem; color: #64748B;">No matching grievances found.</td></tr>`;
    return;
  }

  tableBody.innerHTML = complaints.map(c => {
    const lat = c.latitude ? Number(c.latitude).toFixed(4) : "—";
    const lon = c.longitude ? Number(c.longitude).toFixed(4) : "—";
    return `
      <tr>
        <td>
          <div style="font-weight: 800; color: #0F172A; font-family: monospace; font-size: 0.92rem;">#${c.complaint_id}</div>
          ${c.spam_flag ? '<span class="badge-tag badge-spam" style="margin-top: 3px; display: inline-block;">⚠️ Suspicious</span>' : ''}
          ${c.is_demo ? '<span class="badge-tag badge-demo" style="margin-top: 3px; display: inline-block;">DEMO</span>' : ''}
        </td>
        <td>
          <div style="font-weight: 700; color: #0F172A;">${c.category}</div>
          <div style="font-size: 0.78rem; color: #64748B;">${c.department}</div>
        </td>
        <td style="max-width: 250px;">
          <div style="font-size: 0.88rem; font-weight: 600; color: #0284C7; display: flex; align-items: flex-start; gap: 4px;">
            <span>📍</span> <span style="line-height: 1.3;">${c.location_name}</span>
          </div>
          <div style="font-size: 0.73rem; color: #64748B; font-family: monospace; margin-top: 3px;">
            GPS: ${lat}°, ${lon}°
          </div>
        </td>
        <td>
          <span class="priority-tag priority-${(c.priority || 'medium').toLowerCase()}">${c.priority}</span>
        </td>
        <td>
          <span class="status-tag status-${(c.status || 'submitted').toLowerCase().replace(/\s+/g, '-')}">${c.status}</span>
        </td>
        <td style="font-size: 0.8rem; color: #64748B; white-space: nowrap;">
          ${new Date(c.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
        </td>
        <td>
          <button class="btn btn-sm btn-primary" onclick="openComplaintInspector('${c.complaint_id}')">
            🔍 Inspect
          </button>
        </td>
      </tr>
    `;
  }).join("");
}

// 3. Complaint Inspector Modal (Privacy-Enforced: Location & Grievance Details Only)
async function openComplaintInspector(complaintId) {
  CURRENT_INSPECTING_COMPLAINT_ID = complaintId;

  try {
    const res = await fetch(`/api/authority/complaints/${complaintId}`, {
      headers: { "Authorization": `Bearer ${STATE.token}` }
    });
    const data = await res.json();

    if (res.ok && data.complaint) {
      const c = data.complaint;

      // Header & IDs
      const idEl = document.getElementById("inspectComplaintId");
      if (idEl) idEl.textContent = `#${c.complaint_id}`;

      // Pure Location & Geospatial Intelligence (No citizen personal information)
      const locEl = document.getElementById("inspectLocation");
      if (locEl) locEl.textContent = c.location_name || "Village Locality";

      const gpsEl = document.getElementById("inspectGPS");
      const latStr = c.latitude ? Number(c.latitude).toFixed(5) : "—";
      const lonStr = c.longitude ? Number(c.longitude).toFixed(5) : "—";
      if (gpsEl) gpsEl.textContent = `${latStr}° N, ${lonStr}° E`;

      const mapLink = document.getElementById("inspectMapLink");
      if (mapLink && c.latitude && c.longitude) {
        mapLink.href = `https://www.google.com/maps?q=${c.latitude},${c.longitude}`;
        mapLink.style.display = "inline-flex";
      } else if (mapLink) {
        mapLink.style.display = "none";
      }

      const dateEl = document.getElementById("inspectCreatedDate");
      if (dateEl) dateEl.textContent = new Date(c.created_at).toLocaleString();

      // Complaint texts
      const descEl = document.getElementById("inspectDesc");
      if (descEl) descEl.textContent = c.description;

      const transEl = document.getElementById("inspectTranscript");
      if (transEl) transEl.textContent = c.voice_transcript || "No voice recording attached.";

      // AI Analysis
      const catEl = document.getElementById("inspectAICat");
      if (catEl) catEl.textContent = c.ai_category || c.category;

      const priEl = document.getElementById("inspectAIPri");
      if (priEl) priEl.textContent = c.priority;

      const reasonEl = document.getElementById("inspectAIPriReason");
      if (reasonEl) reasonEl.textContent = c.priority_reason || "Assessed by AI Model";

      // Selectors & Form controls
      const statusSelect = document.getElementById("inspectStatusSelect");
      if (statusSelect) statusSelect.value = c.status;

      const deptSelect = document.getElementById("inspectDeptSelect");
      if (deptSelect) deptSelect.value = c.department;

      const prioritySelect = document.getElementById("inspectPrioritySelect");
      if (prioritySelect) prioritySelect.value = c.priority;

      const notesEl = document.getElementById("inspectResolutionNotes");
      if (notesEl) notesEl.value = c.resolution_notes || "";

      // Photo Evidence Render
      const photoContainer = document.getElementById("inspectPhotoContainer");
      if (photoContainer) {
        if (c.image_url) {
          photoContainer.innerHTML = `
            <div style="text-align: center; background: #0F172A; padding: 0.75rem; border-radius: 10px; border: 1px solid #334155;">
              <a href="${c.image_url}" target="_blank" title="Click to view full size">
                <img src="${c.image_url}" alt="Citizen Evidence Photo" style="max-width: 100%; max-height: 320px; border-radius: 6px; object-fit: contain; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
              </a>
              <div style="font-size: 0.78rem; color: #34D399; font-weight: 700; margin-top: 6px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                <span>📸 Verified Evidence:</span> <span>${c.image_name}</span> <span>(${Math.round((c.image_size || 0) / 1024)} KB)</span>
              </div>
            </div>
          `;
        } else if (c.is_demo) {
          photoContainer.innerHTML = `
            <div style="padding: 1.5rem; background: #FEF3C7; border: 1.5px dashed #D97706; border-radius: 10px; text-align: center; color: #92400E;">
              <div style="font-weight: 800; font-size: 0.95rem;">⚠️ DEMO DATA — Prototype Simulation</div>
              <div style="font-size: 0.82rem; margin-top: 4px;">This is a pre-seeded demonstration record for testing.</div>
            </div>
          `;
        } else {
          photoContainer.innerHTML = `
            <div style="padding: 1.5rem; background: #F8FAFC; border: 1.5px dashed #CBD5E1; border-radius: 10px; text-align: center; color: #94A3B8;">
              <div style="font-size: 1.8rem; margin-bottom: 4px;">📷</div>
              <div style="font-weight: 700; color: #64748B;">No photo evidence attached.</div>
            </div>
          `;
        }
      }

      // Spam Flag Button text
      const spamBtn = document.getElementById("inspectSpamToggleBtn");
      if (spamBtn) {
        spamBtn.textContent = c.spam_flag ? "✅ Mark Verified Citizen Submission" : "⚠️ Flag as Suspicious / Duplicate";
        spamBtn.setAttribute("data-flag", c.spam_flag ? "0" : "1");
      }

      openModal("complaintInspectorModal");
    }
  } catch (err) {
    showToast("Error fetching complaint dossier.", "error");
  }
}

// 4. Save Updates (Status, Resolution Notes, Department, Priority - Atomic PUT)
async function saveInspectorUpdates() {
  if (!CURRENT_INSPECTING_COMPLAINT_ID) return;

  const newStatus = document.getElementById("inspectStatusSelect").value;
  const resolutionNotes = document.getElementById("inspectResolutionNotes").value.trim();
  const department = document.getElementById("inspectDeptSelect").value;
  const prioritySelect = document.getElementById("inspectPrioritySelect");
  const priority = prioritySelect ? prioritySelect.value : null;

  if (newStatus === "Resolved" && !resolutionNotes) {
    showToast("Resolution note is mandatory when marking grievance as Resolved.", "warning");
    const notesEl = document.getElementById("inspectResolutionNotes");
    if (notesEl) {
      notesEl.focus();
      notesEl.style.borderColor = "#EF4444";
      setTimeout(() => { notesEl.style.borderColor = ""; }, 2500);
    }
    return;
  }

  const saveBtn = document.getElementById("inspectSaveBtn");
  if (saveBtn) {
    saveBtn.disabled = true;
    saveBtn.innerHTML = `⏳ <span>Saving...</span>`;
  }

  try {
    const payload = {
      status: newStatus,
      resolution_notes: resolutionNotes,
      department: department
    };
    if (priority) payload.priority = priority;

    const res = await fetch(`/api/authority/complaints/${CURRENT_INSPECTING_COMPLAINT_ID}/status`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${STATE.token}`
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok && data.success) {
      showToast(`Complaint #${CURRENT_INSPECTING_COMPLAINT_ID} updated to '${newStatus}' successfully!`, "success");
      closeModal("complaintInspectorModal");
      await loadAuthorityDashboard();
    } else {
      showToast(data.detail || "Update failed.", "error");
    }
  } catch (err) {
    console.error("Save inspector updates error:", err);
    showToast("Network error saving dossier.", "error");
  } finally {
    if (saveBtn) {
      saveBtn.disabled = false;
      saveBtn.innerHTML = `💾 <span data-i18n="saveChangesBtn">Save Updates</span>`;
    }
  }
}

async function toggleSpamFlag() {
  if (!CURRENT_INSPECTING_COMPLAINT_ID) return;
  const spamBtn = document.getElementById("inspectSpamToggleBtn");
  const targetFlag = parseInt(spamBtn.getAttribute("data-flag") || "1", 10);

  try {
    const res = await fetch(`/api/authority/complaints/${CURRENT_INSPECTING_COMPLAINT_ID}/flag-spam`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${STATE.token}`
      },
      body: JSON.stringify({ spam_flag: targetFlag, reason: "Authority action" })
    });

    if (res.ok) {
      showToast(`Spam status updated.`, "info");
      openComplaintInspector(CURRENT_INSPECTING_COMPLAINT_ID);
      await loadAuthorityDashboard();
    }
  } catch (err) {
    showToast("Network error updating spam flag.", "error");
  }
}

// Load Citizen Dashboard Home view
function loadCitizenDashboard() {
  const nameEl = document.getElementById("citizenWelcomeName");
  const langEl = document.getElementById("citizenCurrentLang");
  if (nameEl && STATE.user) nameEl.textContent = STATE.user.name;
  if (langEl) langEl.textContent = CURRENT_LANG.toUpperCase();
}

