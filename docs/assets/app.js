(() => {
  const BUDGET_STORAGE_KEY = "korea-traver-budget-v1";
  const dayButtons = Array.from(document.querySelectorAll("[data-day-button]"));
  const dayPanels = Array.from(document.querySelectorAll("[data-day-panel]"));

  function showDay(dayId) {
    dayButtons.forEach((button) => {
      const active = button.dataset.dayButton === dayId;
      button.setAttribute("aria-selected", String(active));
      button.classList.toggle("is-active", active);
    });

    dayPanels.forEach((panel) => {
      panel.hidden = panel.dataset.dayPanel !== dayId;
    });

    if (window.location.hash !== `#${dayId}`) {
      history.replaceState(null, "", `#${dayId}`);
    }
  }

  if (dayButtons.length && dayPanels.length) {
    dayButtons.forEach((button) => {
      button.addEventListener("click", () => showDay(button.dataset.dayButton));
    });

    const initialDay = window.location.hash.replace("#", "");
    const knownDay =
      dayButtons.find((button) => button.dataset.dayButton === initialDay)?.dataset.dayButton ||
      dayButtons[0].dataset.dayButton;
    showDay(knownDay);
  }

  const budgetPage = document.querySelector("[data-budget-page]");
  if (budgetPage) {
    const budgetRows = Array.from(document.querySelectorAll("[data-budget-row]"));
    const budgetInputs = Array.from(document.querySelectorAll("[data-budget-input]"));
    const actualTotalNode = document.querySelector("[data-budget-actual-total]");
    const diffNode = document.querySelector("[data-budget-diff]");
    const resetButton = document.querySelector("[data-budget-reset]");
    const resetDialog = document.querySelector("[data-reset-dialog]");
    const cancelResetButton = document.querySelector("[data-cancel-reset]");
    const confirmResetButton = document.querySelector("[data-confirm-reset]");

    const formatter = new Intl.NumberFormat("ja-JP");
    const loadState = () => {
      try {
        return JSON.parse(localStorage.getItem(BUDGET_STORAGE_KEY) || "{}");
      } catch {
        return {};
      }
    };
    const saveState = (state) => {
      localStorage.setItem(BUDGET_STORAGE_KEY, JSON.stringify(state));
    };
    const parseAmount = (value) => {
      const numeric = Number.parseInt(String(value || "").replace(/[^\d]/g, ""), 10);
      return Number.isFinite(numeric) ? numeric : 0;
    };
    const formatYen = (value) => `${value < 0 ? "-" : ""}¥${formatter.format(Math.abs(value))}`;

    const state = loadState();

    budgetInputs.forEach((input) => {
      const slug = input.dataset.budgetInput;
      if (!slug) {
        return;
      }
      const saved = state[slug];
      if (saved && Number.isFinite(saved.actual)) {
        input.value = String(saved.actual);
      }
      input.addEventListener("input", () => {
        const amount = parseAmount(input.value);
        if (amount > 0) {
          state[slug] = { actual: amount };
        } else {
          delete state[slug];
        }
        saveState(state);
        updateBudgetSummary();
      });
    });

    function updateBudgetSummary() {
      let estimateTotal = 0;
      let actualTotal = 0;

      budgetRows.forEach((row) => {
        estimateTotal += parseAmount(row.dataset.estimateYen);
        const slug = row.dataset.budgetRow;
        if (!slug) {
          return;
        }
        actualTotal += Number.isFinite(state[slug]?.actual) ? state[slug].actual : 0;
      });

      if (actualTotalNode) {
        actualTotalNode.textContent = formatYen(actualTotal);
      }
      if (diffNode) {
        diffNode.textContent = formatYen(actualTotal - estimateTotal);
      }
    }

    const resetBudgetState = () => {
      localStorage.removeItem(BUDGET_STORAGE_KEY);
      Object.keys(state).forEach((key) => delete state[key]);
      budgetInputs.forEach((input) => {
        input.value = "";
      });
      updateBudgetSummary();
    };

    if (resetButton) {
      resetButton.addEventListener("click", () => {
        if (resetDialog && typeof resetDialog.showModal === "function") {
          resetDialog.showModal();
          return;
        }
        if (window.confirm("入力した金額をこの端末から消しますか？")) {
          resetBudgetState();
        }
      });
    }

    if (cancelResetButton) {
      cancelResetButton.addEventListener("click", () => {
        resetDialog?.close();
      });
    }

    if (confirmResetButton) {
      confirmResetButton.addEventListener("click", () => {
        resetBudgetState();
        resetDialog?.close();
      });
    }

    if (resetDialog) {
      resetDialog.addEventListener("click", (event) => {
        const rect = resetDialog.getBoundingClientRect();
        const clickedInside =
          event.clientX >= rect.left &&
          event.clientX <= rect.right &&
          event.clientY >= rect.top &&
          event.clientY <= rect.bottom;
        if (!clickedInside) {
          resetDialog.close();
        }
      });
    }

    const focusSlug = window.location.hash.replace("#", "");
    if (focusSlug) {
      const targetRow = document.getElementById(`budget-${focusSlug}`);
      if (targetRow) {
        targetRow.classList.add("is-focused");
        window.setTimeout(() => {
          targetRow.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 120);
      }
    }

    updateBudgetSummary();
  }

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-nmap-app]");
    if (!trigger) {
      return;
    }

    event.preventDefault();

    const appUrl = trigger.getAttribute("data-nmap-app");
    const webUrl = trigger.getAttribute("data-nmap-web");
    if (!appUrl || !webUrl) {
      return;
    }

    let hidden = false;
    let timerId = null;

    const onVisibilityChange = () => {
      hidden = document.hidden;
      if (hidden && timerId !== null) {
        window.clearTimeout(timerId);
        timerId = null;
      }
    };

    document.addEventListener("visibilitychange", onVisibilityChange, { once: false });
    window.location.href = appUrl;

    timerId = window.setTimeout(() => {
      document.removeEventListener("visibilitychange", onVisibilityChange);
      if (!hidden) {
        window.open(webUrl, "_blank", "noopener,noreferrer");
      }
    }, 900);
  });
})();
