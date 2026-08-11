/**
 * Vendor Invoice Intelligence Portal — Frontend Logic
 * =====================================================
 * Handles navigation, form submission, API communication,
 * loading states, error handling, and result rendering.
 *
 * Communicates with FastAPI backend at API_BASE.
 */

(() => {
  "use strict";

  // ── Configuration ──────────────────────────────────────────
  // When served from FastAPI (same origin), use relative paths.
  // When served from a different server (e.g., VS Code Live Server), use the full URL.
  const API_BASE =
    window.location.port === "8000" ? "" : "http://127.0.0.1:8000";

  // ── DOM references ─────────────────────────────────────────
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);

  // Navigation
  const navItems = $$("[data-view]");
  const viewPanels = $$("[data-view-panel]");

  // Mobile
  const menuToggle = $("#menuToggle");
  const sidebar = $("#sidebar");
  const scrim = $("#scrim");

  // Freight
  const freightForm = $("#freightForm");
  const freightSubmit = $("#freightSubmit");
  const freightApiError = $("#freightApiError");
  const freightResult = $("#freightResult");
  const freightValue = $("#freightValue");
  const freightEchoQty = $("#freightEchoQty");
  const freightEchoDollars = $("#freightEchoDollars");

  // Risk / Invoice
  const riskForm = $("#riskForm");
  const riskSubmit = $("#riskSubmit");
  const riskApiError = $("#riskApiError");
  const riskResult = $("#riskResult");
  const riskStatusBadge = $("#riskStatusBadge");
  const riskStatusIcon = $("#riskStatusIcon");
  const riskStatusTitle = $("#riskStatusTitle");
  const riskStatusSubtitle = $("#riskStatusSubtitle");
  const riskConfidence = $("#riskConfidence");
  const riskFlagProbability = $("#riskFlagProbability");
  const riskLevel = $("#riskLevel");
  const riskMeterMarker = $("#riskMeterMarker");
  const riskMeterValue = $("#riskMeterValue");

  // ══════════════════════════════════════════════════════════
  //  NAVIGATION
  // ══════════════════════════════════════════════════════════

  /**
   * Switch the active view panel and highlight the matching nav item.
   * @param {string} viewName  e.g. "overview", "freight", "risk"
   */
  function switchView(viewName) {
    // Update nav items
    navItems.forEach((btn) => {
      const isMatch = btn.getAttribute("data-view") === viewName;
      btn.classList.toggle("is-active", isMatch);
      if (isMatch) {
        btn.setAttribute("aria-current", "page");
      } else {
        btn.removeAttribute("aria-current");
      }
    });

    // Update view panels
    viewPanels.forEach((panel) => {
      const isMatch = panel.getAttribute("data-view-panel") === viewName;
      panel.classList.toggle("is-active", isMatch);
    });

    // Close mobile sidebar when navigating
    closeMobileSidebar();
  }

  // Attach click handlers to all nav items (sidebar + module cards)
  navItems.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const target = btn.getAttribute("data-view");
      if (target) switchView(target);
    });
  });

  // ══════════════════════════════════════════════════════════
  //  MOBILE SIDEBAR
  // ══════════════════════════════════════════════════════════

  function openMobileSidebar() {
    sidebar.classList.add("is-open");
    scrim.hidden = false;
    scrim.setAttribute("data-open", "true");
    menuToggle.setAttribute("aria-expanded", "true");
  }

  function closeMobileSidebar() {
    sidebar.classList.remove("is-open");
    scrim.hidden = true;
    scrim.removeAttribute("data-open");
    menuToggle.setAttribute("aria-expanded", "false");
  }

  menuToggle.addEventListener("click", () => {
    const isOpen = sidebar.classList.contains("is-open");
    isOpen ? closeMobileSidebar() : openMobileSidebar();
  });

  scrim.addEventListener("click", closeMobileSidebar);

  // ══════════════════════════════════════════════════════════
  //  HELPERS
  // ══════════════════════════════════════════════════════════

  /** Format a number as USD. */
  function formatUSD(n) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(n);
  }

  /** Format a number with commas. */
  function formatNumber(n) {
    return new Intl.NumberFormat("en-US").format(n);
  }

  /** Set the loading spinner on a submit button. */
  function setLoading(btn, loading) {
    if (loading) {
      btn.classList.add("is-loading");
      btn.disabled = true;
    } else {
      btn.classList.remove("is-loading");
      btn.disabled = false;
    }
  }

  /** Show an API error alert. */
  function showApiError(el, message) {
    el.textContent = message;
    el.hidden = false;
  }

  /** Hide an API error alert. */
  function hideApiError(el) {
    el.textContent = "";
    el.hidden = true;
  }

  /** Set a field-level validation error. */
  function setFieldError(fieldId, message) {
    const errorEl = $(`#err-${fieldId}`);
    const fieldEl = $(`#${fieldId}`);
    if (errorEl) errorEl.textContent = message;
    if (fieldEl) fieldEl.closest(".field")?.classList.toggle("has-error", !!message);
  }

  /** Clear all field errors within a form. */
  function clearFieldErrors(form) {
    form.querySelectorAll(".field__error").forEach((el) => (el.textContent = ""));
    form.querySelectorAll(".field.has-error").forEach((el) => el.classList.remove("has-error"));
  }

  /**
   * Validate a numeric input.
   * @returns {number|null} The parsed value, or null if invalid.
   */
  function validateNumericField(fieldId, label, { min = null, allowZero = false } = {}) {
    const input = $(`#${fieldId}`);
    if (!input) return null;

    const raw = input.value.trim();
    if (raw === "") {
      setFieldError(fieldId, `${label} is required`);
      return null;
    }

    const val = parseFloat(raw);
    if (isNaN(val)) {
      setFieldError(fieldId, `${label} must be a number`);
      return null;
    }

    if (min !== null) {
      if (!allowZero && val <= 0) {
        setFieldError(fieldId, `${label} must be greater than 0`);
        return null;
      }
      if (allowZero && val < 0) {
        setFieldError(fieldId, `${label} cannot be negative`);
        return null;
      }
    }

    return val;
  }

  /**
   * Generic fetch wrapper with timeout and error handling.
   */
  async function apiFetch(endpoint, body) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000);

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!response.ok) {
        let detail = `Server error (${response.status})`;
        try {
          const errJson = await response.json();
          if (errJson.detail) detail = errJson.detail;
        } catch {
          // Response wasn't JSON, use the default detail
        }
        throw new Error(detail);
      }

      return await response.json();
    } catch (err) {
      clearTimeout(timeout);
      if (err.name === "AbortError") {
        throw new Error("Request timed out. Please check if the API server is running.");
      }
      if (err instanceof TypeError && err.message.includes("fetch")) {
        throw new Error("Cannot connect to the API server. Is it running at " + API_BASE + "?");
      }
      throw err;
    }
  }

  // ══════════════════════════════════════════════════════════
  //  FREIGHT COST PREDICTION
  // ══════════════════════════════════════════════════════════

  freightForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearFieldErrors(freightForm);
    hideApiError(freightApiError);

    // Validate
    const quantity = validateNumericField("freightQuantity", "Quantity", { min: 0 });
    const dollars = validateNumericField("freightDollars", "Invoice Dollars", { min: 0 });

    if (quantity === null || dollars === null) return;

    // Send request
    setLoading(freightSubmit, true);

    try {
      const data = await apiFetch("/api/predict/freight", {
        quantity: quantity,
        dollars: dollars,
      });

      // Validate response shape
      if (data.predicted_freight === undefined || data.predicted_freight === null) {
        throw new Error("Malformed API response: missing predicted_freight");
      }

      // Update result panel
      freightValue.textContent = formatUSD(data.predicted_freight);
      freightEchoQty.textContent = formatNumber(quantity);
      freightEchoDollars.textContent = formatUSD(dollars);
      freightResult.setAttribute("data-state", "filled");
    } catch (err) {
      showApiError(freightApiError, err.message);
    } finally {
      setLoading(freightSubmit, false);
    }
  });

  // ══════════════════════════════════════════════════════════
  //  INVOICE RISK ASSESSMENT
  // ══════════════════════════════════════════════════════════

  /**
   * Determine the risk level label from the flag probability.
   * @param {number} probability  0–100 scale
   * @returns {string}
   */
  function getRiskLevel(probability) {
    if (probability < 30) return "Low";
    if (probability < 60) return "Medium";
    return "High";
  }

  riskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearFieldErrors(riskForm);
    hideApiError(riskApiError);

    // Validate all 7 fields
    const invoiceQuantity = validateNumericField("invoiceQuantity", "Invoice Quantity", { min: 0 });
    const invoiceDollars = validateNumericField("invoiceDollars", "Invoice Dollars", { min: 0 });
    const freight = validateNumericField("freight", "Freight", { min: 0, allowZero: true });
    const daysPoToInvoice = validateNumericField("daysPoToInvoice", "PO to Invoice Days", { min: 0, allowZero: true });
    const totalItemQuantity = validateNumericField("totalItemQuantity", "Total Item Quantity", { min: 0 });
    const totalItemDollars = validateNumericField("totalItemDollars", "Total Item Dollars", { min: 0 });
    const avgReceivingDelay = validateNumericField("avgReceivingDelay", "Avg Receiving Delay", { min: 0, allowZero: true });

    if (
      invoiceQuantity === null ||
      invoiceDollars === null ||
      freight === null ||
      daysPoToInvoice === null ||
      totalItemQuantity === null ||
      totalItemDollars === null ||
      avgReceivingDelay === null
    ) {
      return;
    }

    // Send request
    setLoading(riskSubmit, true);

    try {
      const data = await apiFetch("/api/predict/invoice", {
        invoice_quantity: invoiceQuantity,
        invoice_dollars: invoiceDollars,
        freight: freight,
        days_po_to_invoice: daysPoToInvoice,
        total_item_quantity: totalItemQuantity,
        total_item_dollars: totalItemDollars,
        avg_receiving_delay: avgReceivingDelay,
      });

      // Validate response shape
      if (!data.status || data.confidence === undefined || data.flag_probability === undefined) {
        throw new Error("Malformed API response: missing required fields");
      }

      const isFlagged = data.status.toLowerCase().includes("flag");
      const probability = data.flag_probability;
      const level = getRiskLevel(probability);

      // Status badge
      riskStatusBadge.setAttribute("data-status", isFlagged ? "flagged" : "approved");
      riskStatusIcon.textContent = isFlagged ? "🚨" : "✅";
      riskStatusTitle.textContent = isFlagged ? "Flagged for Manual Review" : "Approved";
      riskStatusSubtitle.textContent = isFlagged
        ? "This invoice requires manual review"
        : "Safe for automatic processing";

      // Stats
      riskConfidence.textContent = `${data.confidence.toFixed(2)}%`;
      riskFlagProbability.textContent = `${probability.toFixed(2)}%`;
      riskLevel.textContent = level;

      // Risk meter — map probability (0–100) to marker position (0%–100%)
      const meterPct = Math.max(0, Math.min(100, probability));
      riskMeterMarker.style.left = `${meterPct}%`;
      riskMeterValue.textContent = `${meterPct.toFixed(1)}%`;

      // Show result
      riskResult.setAttribute("data-state", "filled");
    } catch (err) {
      showApiError(riskApiError, err.message);
    } finally {
      setLoading(riskSubmit, false);
    }
  });

  // ══════════════════════════════════════════════════════════
  //  INPUT TOUCH STATE (for CSS :invalid styling)
  // ══════════════════════════════════════════════════════════
  document.querySelectorAll("input[required]").forEach((input) => {
    input.addEventListener("blur", () => {
      input.setAttribute("data-touched", "true");
    });
  });
})();
