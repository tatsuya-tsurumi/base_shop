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

document.addEventListener('DOMContentLoaded', function () {
  const addButton = document.getElementById('add-to-cart-btn');
  if (addButton) {
    const csrfToken = document.getElementById('csrf-token').value;
    const alertBox = document.getElementById('alert-box');
    const alertMessage = document.getElementById('alert-message')

    addButton.addEventListener('click', function () {
      const url = this.dataset.url;

      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({})
      })
        .then(response => response.json())
        .then(data => {
          alertMessage.innerText = `${data.name}をカートに追加しました`;
          alertBox.classList.remove('d-none');
        });
    });
  }
});

  (function () {
    'use strict'
    const forms = document.querySelectorAll('.needs-validation')
    Array.from(forms).forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
  })()