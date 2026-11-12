const menu = document.querySelector('[data-menu]');
const nav = document.querySelector('[data-nav]');
const form = document.querySelector('[data-form]');

menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') === 'true';
  menu.setAttribute('aria-expanded', String(!open));
  nav?.classList.toggle('open', !open);
});

nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
  menu?.setAttribute('aria-expanded', 'false');
  nav.classList.remove('open');
}));

form?.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const data = new FormData(form);
  const subject = 'Travel enquiry from ' + data.get('name');
  const body = [
    'Name: ' + data.get('name'),
    'Phone: ' + data.get('phone'),
    'From: ' + data.get('from'),
    'Destination: ' + data.get('destination'),
    'Travel date: ' + (data.get('date') || 'Not specified'),
    'Travellers: ' + data.get('travellers'),
    '',
    'Additional details:',
    data.get('message') || 'None'
  ].join('\n');
  window.location.href = 'mailto:ritikatiwari17828@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
});

document.querySelectorAll('[data-year]').forEach((item) => {
  item.textContent = new Date().getFullYear();
});
