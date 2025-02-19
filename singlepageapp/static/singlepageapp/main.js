import JSONAPIClient from './modules/jsonapi.js';
import TransactionForm from './modules/transactions.js';
import csrftoken from './modules/csrftoken.js';

const mobileCheck = function() {
  let check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};

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

  const isMobile = mobileCheck();
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

