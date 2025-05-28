document.addEventListener("DOMContentLoaded", function() {
  const btn = document.getElementById("toggle-orders-btn");
  if (!btn) return;

  let expanded = false;

  btn.addEventListener("click", function() {
    const hiddenOrders = document.querySelectorAll(".extra-order");

    if (!expanded) {
      // 全て表示
      hiddenOrders.forEach(el => el.classList.remove("d-none"));
      btn.textContent = "元に戻す";
      expanded = true;
    } else {
      // 3件までに戻す
      hiddenOrders.forEach(el => el.classList.add("d-none"));
      btn.textContent = "もっと見る";
      expanded = false;
    }
  });
});
