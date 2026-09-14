document.querySelectorAll('.flash').forEach((message) => {
  window.setTimeout(() => message.classList.add('fade'), 4200);
});
