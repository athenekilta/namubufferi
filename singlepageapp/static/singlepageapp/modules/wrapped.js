import { mapById } from './jsonapi.js';

function monetize(number) {
  return ((Math.abs(number) / 100).toFixed(2)).replace('.', ',') + ' €';
}

export default class Wrapped {
  constructor(api) {
    this.api = api;
    this.container = document.querySelector('#\\/wrapped .content');
    this.year = new Date().getFullYear();
  }

  async fetch() {
    this.container.innerHTML = '<div class="spinner"></div>';

    try {
      const response = await this.api.get(`transactions/?paginate_by=0&include=product`);

      const transactions = response.data;
      const included = mapById(response.included);

      const currentYearTransactions = transactions.filter(t => {
        const date = new Date(t.attributes.timestamp);
        return date.getFullYear() === this.year;
      });

      if (currentYearTransactions.length === 0) {
        this.renderEmpty();
        return;
      }

      const stats = this.calculateStats(currentYearTransactions, included);
      this.render(stats);

    } catch (e) {
      console.error(e);
      this.container.innerHTML = '<p>Failed to load your Wrapped data.</p>';
    }
  }

  calculateStats(transactions, productsMap) {
    let totalSpent = 0;
    let totalCount = 0;
    const productCounts = {};
    const monthlyCounts = new Array(12).fill(0);

    transactions.forEach(t => {
      const qty = t.attributes.quantity;
      const price = t.attributes.price;
      const amount = qty * price;
      // We assume negative quantity means a purchase
      if (amount < 0) {
        totalSpent += amount
        totalCount += 1

        const productId = t.relationships.product.data.id;
        const product = productsMap.get(productId);

        if (product) {
          const name = product.attributes.name;
          if (!productCounts[name]) {
            productCounts[name] = { count: 0, name: name, id: productId };
          }
          productCounts[name].count++;
        }

        const date = new Date(t.attributes.timestamp);
        monthlyCounts[date.getMonth()]++;
      }
    });

    const sortedProducts = Object.values(productCounts).sort((a, b) => b.count - a.count);
    const top5 = sortedProducts.slice(0, 5);

    const leastCommon = sortedProducts.length > 0 ? sortedProducts[sortedProducts.length - 1] : null;

    return {
      totalSpent,
      totalCount,
      top5,
      leastCommon,
      monthlyCounts
    };
  }

  renderEmpty() {
    this.container.innerHTML = `
      <div class="wrapped-container">
        <h1>${this.year} Wrapped</h1>
        <p>You haven't made any purchases this year.</p>
      </div>
    `;
  }

  render(stats) {
    const { totalSpent, totalCount, top5, leastCommon, monthlyCounts } = stats;

    const maxMonth = Math.max(...monthlyCounts);
    const monthNames = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];

    let topProductsHtml = top5.map((p, index) => `
      <div class="rank-row" style="animation-delay: ${3 + (index * 0.1)}s">
        <span class="rank">#${index + 1}</span>
        <span class="product-name">${p.name}</span>
        <span class="count">${p.count}</span>
      </div>
    `).join('');

    let graphHtml = monthlyCounts.map((count, index) => {
      const height = maxMonth > 0 ? (count / maxMonth) * 100 : 0;
      return `
        <div class="bar-container">
          <div class="bar-value">${count}</div>
          <div class="bar" style="height: 0%" data-height="${height}%" title="${count} purchases"></div>
          <div class="label">${monthNames[index]}</div>
        </div>
      `;
    }).join('');

    this.container.innerHTML = `
      <div class="wrapped-container animated-entry">
        <header class="wrapped-header">
          <h1>${this.year}</h1>
          <h2>NAMU WRAPPED</h2>
        </header>

        <div class="stat-card big-stat">
          <h3>Rahaa Tuhlattu</h3>
          <div class="value">${monetize(totalSpent)}</div>
        </div>

        <div class="stat-card big-stat">
          <h3>Namua syöty</h3>
          <div class="value">${totalCount}</div>
        </div>

        <div class="stat-card">
          <h3>Top 5 namut</h3>
          <div class="top-list">
            ${topProductsHtml}
          </div>
        </div>

        <div class="stat-card">
          <h3>Kuukausittainen namuttelusi</h3>
          <div class="graph">
            ${graphHtml}
          </div>
        </div>

        ${leastCommon ? `
        <div class="stat-card">
          <h3>Harvinaisin herkkusi</h3>
          <p>Söit vähiten namua <strong>${leastCommon.name}</strong>, jota söit ${leastCommon.count} kpl</p>
        </div>
        ` : ''}
        
      </div>
    `;

    // Trigger graph animation
    requestAnimationFrame(() => {
      setTimeout(() => {
        this.container.querySelectorAll('.bar').forEach(bar => {
          bar.style.height = bar.dataset.height;
        });
      }, 1000); // Wait for cards to slide in
    });
  }
}