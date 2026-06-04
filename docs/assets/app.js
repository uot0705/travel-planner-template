(() => {
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
