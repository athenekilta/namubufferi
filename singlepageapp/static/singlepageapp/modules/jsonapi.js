import csrftoken from './csrftoken.js';

export default class JSONAPIClient {
  constructor(root) {
    this.root = root;
  }

  static headers = {
    'X-CSRFToken': csrftoken,
    Accept: 'application/vnd.api+json',
    // 'Content-Type': 'application/vnd.api+json',
  };

  async request(path, method, body = null) {
    const response = await fetch(encodeURI(`${this.root}${path}`), {
      method: method,
      headers: JSONAPIClient.headers,
      body: body,
    });

    if (response.status == 404) {
      throw response.status;
    }

    let result = null;
    if (response.status != 204) {
      result = response.json();
    }
    if (!response.ok) {
      throw result.errors;
    }
    return result;
  }

  post(path, body = new FormData()) {
    return this.request(path, 'POST', body);
  }

  get(path) {
    return this.request(path, 'GET');
  }

  delete(path) {
    return this.request(path, 'DELETE');
  }
}

export function mapById(arr) {
  return new Map(arr.map(obj => [obj.id, obj]));
}
