import React, { Component } from 'react';
import csrftoken from './csrftoken';

function monetize(number) {
  const currency = '€';
  return `${number < 0 ? `-${currency}` : currency}${Math.abs(
    number / 100
  ).toFixed(2)}`;
}

const headers = new Headers({
  Accept: 'application/vnd.api+json',
  'X-CSRFToken': csrftoken,
});

class TransactionForm extends Component {
  constructor() {
    super();
    this.state = {
      products: [],
      transactions: [],
      productMap: new Map(),
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    fetch('/api/products/?paginate_by=0', {
      headers: headers,
    })
      .then(response => response.json())
      .then(result => {
        this.setState({
          products: result.data,
          productMap: new Map(
            result.data.map(product => [product.id, product])
          ),
        });
      });

    fetch(encodeURI('/api/transactions/?page[number]=last'), {
      headers: headers,
    })
      .then(response => response.json())
      .then(result => {
        this.setState({ transactions: result.data });
      });
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch('/api/transactions/', {
      method: 'POST',
      headers: headers,
      body: new FormData(event.target),
    })
      .then(response => response.json())
      .then(result => {
        this.setState(state => ({
          transactions: [...state.transactions, result.data],
        }));
      });
  }

  render() {
    const transactionHistory = this.state.transactions.map(transaction => {
      return (
        <tr key={transaction.id}>
          <td>{new Date(transaction.attributes.timestamp).toLocaleString()}</td>
          <td>
            {
              this.state.productMap.get(
                transaction.relationships.product.data.id
              )?.attributes.name
            }
          </td>
          <td className="monetary">{monetize(transaction.attributes.total)}</td>
          <td className="monetary">
            {monetize(transaction.attributes.balance)}
          </td>
        </tr>
      );
    });
    const options = this.state.products.map(product => {
      return (
        <option key={product.id} value={product.id}>
          {product.attributes.name}: {monetize(product.attributes.price * -1)}
        </option>
      );
    });
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <select name="product">{options}</select>
          <input name="quantity" type="hidden" value="-1"></input>
          <button type="submit">Submit</button>
        </form>
        <table>
          <thead>
            <tr>
              <th>timestamp</th>
              <th>product</th>
              <th>total</th>
              <th>balance</th>
            </tr>
          </thead>
          <tbody>{transactionHistory.reverse()}</tbody>
        </table>
      </div>
    );
  }
}

export default TransactionForm;
