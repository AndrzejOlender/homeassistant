
try {
  new Function("import('/hacsfiles/frontend/main-60575625.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-60575625.js';
  document.body.appendChild(el);
}
  