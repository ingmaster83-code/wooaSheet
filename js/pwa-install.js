const CONVERT_IDS = ['convertBtn','processBtn','downloadBtn','startBtn','mergeBtn','splitBtn'];
let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault(); deferredPrompt = e;
  document.querySelectorAll('#heroInstallBtn').forEach(b => b.style.display='inline-flex');
  CONVERT_IDS.forEach(id => { const el=document.getElementById(id); if(el) el.addEventListener('click', tryInstall, {once:true}); });
});
function tryInstall() { if(deferredPrompt){ deferredPrompt.prompt(); deferredPrompt.userChoice.then(()=>{ deferredPrompt=null; }); } }
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#heroInstallBtn').forEach(b => b.addEventListener('click', tryInstall));
});
if('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js');
