// Taby (Jaro/Podzim) — náhrada původního Webflow runtime.
// Aktivace přepíná CSS třídy, o zbytek se stará assets/css/main.css
// (.w-tab-pane { display: none } a .w--tab-active { display: block }).
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-tabs]").forEach(function (root) {
    var links = Array.prototype.slice.call(root.querySelectorAll(".w-tab-link"));
    var panes = Array.prototype.slice.call(root.querySelectorAll(".w-tab-pane"));

    links.forEach(function (link, index) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        links.forEach(function (other, i) {
          other.classList.toggle("w--current", i === index);
          other.setAttribute("aria-selected", i === index ? "true" : "false");
          other.setAttribute("tabindex", i === index ? "0" : "-1");
        });
        panes.forEach(function (pane, i) {
          pane.classList.toggle("w--tab-active", i === index);
        });
      });
    });
  });
});
