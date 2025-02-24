import { mapById } from './jsonapi.js';

function monetize(number, element = null) {
  const suffix = ' €';
  let prefix;
  if (element) {
    element.classList.remove('negative');
    element.classList.remove('positive');
  }
  if (number < 0) {
    prefix = '–';
    if (element) {
      element.classList.add('negative');
    }
  } else {
    prefix = '+';
    if (element) {
      element.classList.add('positive');
    }
  }
  prefix += ' '
  return prefix + ((Math.abs(number) / 100).toFixed(2)).replace('.', ',') + suffix;
}

export default class TransactionForm {
  constructor(api) {
    this.api = api;
    this.form = document.querySelector('#transactionform');
    this.productList = document.querySelector('#productlist');
    this.search = document.querySelector('#search');
    this.quantity = document.querySelector('#quantity');
    this.transactionTable = document.querySelector('#transactiontable');
    this.search.addEventListener('input', this.searchChange.bind(this));
    this.form.addEventListener('submit', this.submit.bind(this));
  }

  updateBalance(value) {
    const balanceElement = document.querySelector('#balance');
    balanceElement.textContent = monetize(value, balanceElement);
  }

  searchChange(event) {
    this.productList.querySelectorAll('legend').forEach(element => {
      const display = event.target.value ? 'none' : null;
      element.style.display = display;
      element.closest('fieldset').style.margin = event.target.value ? 0 : null;
      this.productList.querySelector('#recentfieldset').style.display = display;
    });
    this.productList.querySelectorAll('label span.name').forEach(element => {
      const label = element.closest('label');
      if (!element.textContent.match(new RegExp(event.target.value, 'gi'))) {
        label.style.display = 'none';
      } else {
        label.style.display = null;
      }
    });
  }

  async submit(event) {
    event.preventDefault();
    console.log(new FormData(event.target))
    if (!window.confirm('Confirm?')) {
      return;
    }
    const result = await this.api.post(
      'transactions/?include=product',
      new FormData(event.target)
    );
    this.appendTransactions(result);
    this.updateBalance(result.data.attributes.balance);
    document.getElementById('buy-success').textContent = "Purchase successful!";
    location.assign('#/buy');
  }

  async fetchProducts() {
    const groups = await this.api.get('groups/?paginate_by=0');
    const products = await this.api.get(
      'products/?paginate_by=0&fields[products]=name,price'
    );
    const productMap = mapById(products.data);

    const fieldsets = new Map();
    for (const group of groups.data.filter((group) => group.attributes.name != "\u20ac")) {
      let fieldset = fieldsets.get(group.id);
      if (!fieldset) {
        fieldset = document
          .getElementById('productfieldset')
          .content.cloneNode(true);
        fieldset.querySelector('legend').textContent = group.attributes.name;
        fieldsets.set(group.id, fieldset);
      }
      for (let product of group.relationships.products.data) {
        product = productMap.get(product.id);
        const radio = this.createProductRadio(product);
        fieldset.querySelector('div').appendChild(radio);
      }
    }

    const fieldsetFragment = new DocumentFragment();
    for (const fieldset of Array.from(fieldsets.values()).sort((a, b) => {
      return a
        .querySelector('legend')
        .textContent.localeCompare(b.querySelector('legend').textContent);
    })) {
      fieldsetFragment.appendChild(fieldset);
    }

    this.productList.appendChild(fieldsetFragment);
  }

  appendTransactions(result) {
    const fragment = new DocumentFragment();
    const includedMap = mapById(result.included);
    for (const transaction of Array.isArray(result.data)
      ? result.data
      : [result.data]) {
      const tr = document
        .querySelector('#transactionrow')
        .content.cloneNode(true);
      const td = tr.querySelectorAll('td');
      const relatedProduct = includedMap.get(
        transaction.relationships.product.data.id
      );
      const cells = [
        new Date(transaction.attributes.timestamp).toLocaleString(),
        relatedProduct.attributes.name,
        monetize(transaction.attributes.total),
      ];
      cells.forEach((cell, i) => {
        td[i].textContent = cell;
      });

      if (transaction.attributes.state == 0) {
        const pendingText = document.createElement('span');
        pendingText.textContent = 'pending';
        pendingText.style.marginLeft = '1em';
        pendingText.style.color = 'red';
        td[1].appendChild(pendingText);
        const payHref = document.createElement('a');
        payHref.href = `?balanceState=inProgress&transactionId=${transaction.id}#/balance`;
        payHref.textContent = 'pay now';
        payHref.style.marginLeft = '1em'
        td[1].appendChild(payHref);
      }

      fragment.prepend(tr);
    }
    this.transactionTable.querySelector('tbody').prepend(fragment);
  }

  async updateRecentProducts(transactions) {
    const recentProducts = new Set(
      transactions.data
        .reverse()
        .map(transaction => transaction.relationships.product.data.id)
    );
    const fieldsetFragment = new DocumentFragment();
    const includedMap = mapById(transactions.included);
    for (const productId of recentProducts) {
      const product = includedMap.get(productId);
      const radio = this.createProductRadio(product);
      // I'm sorry, this doesn't seem to be the right place to do this kind of filtering...
      if (product.attributes.name !== 'Initial balance' && product.attributes.price >= 0)
        fieldsetFragment.appendChild(radio);
    }
    const fieldset = document.getElementById('recentfieldset'); 
    fieldset.querySelector('div').appendChild(fieldsetFragment);
    if (fieldset.hasChildNodes()) {
      fieldset.querySelector('input').checked = true;
    }
  }

  createProductRadio(product) {
    const radio = document
      .getElementById('productradio')
      .content.cloneNode(true);
    radio.querySelector('input').setAttribute('value', product.id);
    radio.querySelector('.name').textContent = `${product.attributes.name}`;
    radio.querySelector('.price').textContent = `${monetize(
      product.attributes.price * this.quantity.value
    )}`;
    return radio;
  }

  async fetchTransactions() {
    const transactions = await this.api.get(
      'transactions/?page[number]=last&include=product'
    );
    if (!transactions.data.length) {
      this.updateBalance(0)
      return;
    }
    this.updateBalance(
      transactions.data[transactions.data.length - 1].attributes.balance
    );
    this.appendTransactions(transactions);
    this.updateRecentProducts(transactions);
  }

  async onScanSuccess(decodedText, decodedResult) {
    let result;
    try {
      result = await this.api.get(`barcodes/${decodedText}/?include=product`);
    } catch (error) {
      console.error(error);
      return;
    }
    const product = result.included[0];
    this.search.value = `^${product.attributes.name}$`;
    Array.from(
      this.productList.querySelectorAll(`input[value=${product.id}]`)
    ).pop().checked = true;
    this.search.dispatchEvent(new Event('input'));
    this.search.focus();
    this.scanner.clear();
    location.assign('#/transaction');
  }

  fetch() {
    this.fetchProducts();
    this.fetchTransactions();
  }
}
