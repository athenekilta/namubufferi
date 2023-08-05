(function () {
  const modalName = document.currentScript.getAttribute('modalName');

  function submitForm() {
    document.getElementById(modalName).showModal();
  }

  function cancelSubmit() {
    event.preventDefault();
    document.getElementById(modalName).close();
  }

  function confirmSubmit() {
    document.getElementById(modalName).close();
    document.querySelector('form').submit();
  }

  document.querySelector('#' + modalName + ' .btn-error').addEventListener('click', cancelSubmit);
  document.querySelector('#' + modalName + ' .btn-primary').addEventListener('click', confirmSubmit);

  window.submitForm = submitForm;
  window.cancelSubmit = cancelSubmit;
  window.confirmSubmit = confirmSubmit;
})();