document.addEventListener("DOMContentLoaded", function () {
  var e = document.querySelector(".page-loading");
  e.classList.remove("active"),
    setTimeout(function () {
      e.remove();
    }, 1e3);
});
