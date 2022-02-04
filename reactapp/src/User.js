import React, { Component } from 'react';

class User extends Component {
  constructor() {
    super();
    this.state = {
      user: null,
    };
  }

  componentDidMount() {
    fetch('/api/', {
      headers: {
        Accept: 'application/vnd.api+json',
      },
    })
      .then(response => response.json())
      .then(result => {
        this.setState({
          user: result,
        });
      });
  }

  render() {
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining
    const username = this.state.user?.data.attributes.username ?? '...';
    return <p>{username}</p>;
  }
}

export default User;
