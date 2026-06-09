const clock = document.getElementById("live-clock");
if (clock) {
  setInterval(() => {
    clock.textContent = new Date().toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  }, 1000);
}

const depositInput = document.getElementById("deposit_amount");
const depositPreview = document.getElementById("deposit-preview");
const itemInputs = document.querySelectorAll(".js-deposit-input");

function updateDepositPreview() {
  if (!depositInput || !depositPreview) return;
  const perItem = Number(depositInput.dataset.depositPerItem || 0);
  const gadda = Number(document.getElementById("gadda_qty")?.value || 0);
  const rajai = Number(document.getElementById("rajai_qty")?.value || 0);
  const suggested = Math.max(0, gadda + rajai) * perItem;
  depositInput.value = suggested;
  depositPreview.textContent = `₹${suggested}`;
}

itemInputs.forEach((input) => input.addEventListener("input", updateDepositPreview));
