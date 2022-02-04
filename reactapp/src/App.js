import './App.css';
import User from './User';
import TransactionForm from './TransactionForm';

function App() {
  return (
    <div>
      <header>
        <h1>Namubufferi</h1>
      </header>
      <main>
        <section>
          <h2>User</h2>
          <User />
        </section>
        <section>
          <h2>Transactions</h2>
          <TransactionForm />
        </section>
      </main>
    </div>
  );
}

export default App;
