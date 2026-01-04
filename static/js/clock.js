function updateClock() {
  const now = new Date().toLocaleString("id-ID", {
    timeZone: "Asia/Jakarta",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });

  const date = new Date().toLocaleDateString("id-ID", {
    timeZone: "Asia/Jakarta",
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric"
  });

  document.getElementById("clock").innerText = now;
  document.getElementById("date").innerText = date;
}

setInterval(updateClock, 1000);
updateClock();
