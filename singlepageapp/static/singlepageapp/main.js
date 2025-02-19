import JSONAPIClient from './modules/jsonapi.js';
import TransactionForm from './modules/transactions.js';
import csrftoken from './modules/csrftoken.js';

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
    location.replace('#/buy');
    return;
  }
  if (location.hash.startsWith('#')) {
    document.querySelectorAll('main > section').forEach(section => {
      section.style.display = 'none';
    });

    document.querySelectorAll('main > header > nav > a').forEach(href => {
      href.className = "";
    });
    // https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector#escaping_special_characters

    document.querySelector(location.hash.replace("/","\\/")).style.display =
      'block'
    document.querySelector('main > header > nav > a[href="'+location.hash+'"]').className = "active"
    
  }
  burger.removeAttribute('open');
}

hashHandler();
window.addEventListener('hashchange', hashHandler, false);
document.querySelector('#loader').style.display = 'none';

const api = new JSONAPIClient('/api/');

const transactionForm = new TransactionForm(api);
transactionForm.fetch();

// balance

const CODE = 68266
const productId_cent = '745fd2c2-336c-4f10-9753-bbb2d09063bc'

const formatUrl = (code, price, id) =>
	"https://mobilepay.fi/Yrityksille/Maksulinkki/maksulinkki-vastaus"
	+ `?phone=${code}&amount=${price}&comment=Namubufferi-${id}&lock=1`

const getMobileUrl = (code, price, id) => {
  return `mobilepayfi://send?phone=${code}&amount=${price}&comment=NB-${id}&lock=1`
}

const searchParams = new URLSearchParams(window.location.search);
const inProgress = searchParams.get('balanceState') === 'inProgress';
const storedTransactionId = searchParams.get('transactionId');

if (inProgress && storedTransactionId) {
  handleInProgressTransaction(storedTransactionId);
}

async function handleInProgressTransaction(txId) {
  document.getElementById('balance-add').style.display = 'none';
  document.getElementById('balance-mobilepay').style.display = 'none';

  const res = await fetch('/api/transactions/' + txId + '/?include=product', {
    credentials: 'include',
    headers: {'Accept': 'application/vnd.api+json'}
  });
  if (!res.ok) {
    searchParams.delete('balanceState');
    searchParams.delete('transactionId');
    history.replaceState(null, '', '?' + searchParams.toString() + '#' + location.hash);
    return;
  }
  const data = await res.json();

  if(data.data.attributes.state === 1) {
    document.getElementById('balance-alert').textContent = 'Transaction is already paid';
    searchParams.delete('balanceState');
    searchParams.delete('transactionId');
    history.replaceState(null, '', '?' + searchParams.toString() + location.hash);
    document.getElementById('balance-add').style.display = 'block';
    return;
  }

  const amount = Math.abs(data.data.attributes.quantity / 100);


  document.getElementById('balance-mobilepay').style.display = 'block';

  const isMobile = navigator.userAgentData.mobile;
  if (isMobile && localStorage.getItem('olkkari') !== '1') {
    document.getElementById('balance-mobilepay-link').href = getMobileUrl(CODE, amount, txId);
    document.getElementById('balance-qrcode').style.display = 'none';
  } else {
    document.getElementById('balance-qrcode').style.display = 'block';
    document.getElementById('balance-mobilepay-link').href = formatUrl(CODE, amount, txId);
    generateQR(amount, txId);
  }
}

async function addBalance() {
  document.getElementById('balance-alert').textContent = ''
  let amount = Number(document.getElementById('balance-add-amount').value)

  document.getElementById('balance-add').style.display = 'none'
  document.getElementById('balance-mobilepay').style.display = 'none'

  const formData = new FormData()
  formData.append('quantity', -(amount*100).toFixed(0))
  formData.append('product', productId_cent)
  formData.append('state', 0)

  const res = await fetch('/api/transactions/?include=product', {credentials: 'include', method: 'POST', headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/vnd.api+json'}, body: formData})

  const data = await res.json()
  if (!res.ok) {
    document.getElementById('balance-alert').textContent = 'Failed to add balance'
    return
  }

  searchParams.set('balanceState', 'inProgress');
  searchParams.set('transactionId', data.data.id);
  history.replaceState(null, '', '?' + searchParams.toString() + location.hash);

  handleInProgressTransaction(data.data.id);
}

async function confirmBalance() {
  const id = searchParams.get('transactionId');
  document.getElementById('balance-mobilepay').style.display = 'none'
  const formData = new FormData()
  formData.append('state', 1)
  const res = await fetch('/api/transactions/'+id+'/update/', {credentials: 'include', method: 'POST', headers: {'X-CSRFToken': csrftoken, 'Accept': 'application/vnd.api+json'}, body: formData})
  await res
  await transactionForm.fetchTransactions()
  document.getElementById('balance-add').style.display = 'block'
  document.getElementById('balance-alert').textContent = 'Added balance successfully'

  searchParams.delete('balanceState');
  searchParams.delete('transactionId');
  history.replaceState(null, '', '?' + searchParams.toString());
}


document.getElementById('balance-add-submit').addEventListener('click', addBalance)
document.getElementById('balance-confirm').addEventListener('click', confirmBalance)


var code = new QRCode("balance-qrcode", {correctLevel: QRCode.CorrectLevel.L});

function generateQR(price, id) {
	code.makeCode(formatUrl(CODE, price, id));
}

