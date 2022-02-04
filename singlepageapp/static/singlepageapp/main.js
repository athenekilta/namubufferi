import JSONAPIClient from './modules/jsonapi.js';
import TransactionForm from './modules/transactions.js';

const burger = document.querySelector('#burger');
burger.addEventListener('toggle', event => {
  const body = document.querySelector('body');
  if (burger.open) {
    body.scrollIntoView();
  }
  body.classList.toggle('stop-scrolling');
});
burger.querySelectorAll('a[href*="#/').forEach(a => {
  a.addEventListener('click', event => {
    if (event.target.href === location.href) {
      burger.removeAttribute('open');
    }
  });
});

// https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onhashchange#using_an_event_listener
function hashHandler() {
  if (!location.hash) {
    location.replace('#/account');
    return;
  }
  if (location.hash.startsWith('#/')) {
    document.querySelectorAll('main > section').forEach(section => {
      section.style.display = 'none';
    });
    // https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector#escaping_special_characters
    document.querySelector(location.hash.replace('/', '\\/')).style.display =
      null;
  }
  burger.removeAttribute('open');
}

hashHandler();
window.addEventListener('hashchange', hashHandler, false);
document.querySelector('#loader').style.display = 'none';

const api = new JSONAPIClient('/api/');

const transactionForm = new TransactionForm(api);
transactionForm.fetch();

const user = await api.get('');
document.querySelector('#user').textContent = user.data.attributes.username;
