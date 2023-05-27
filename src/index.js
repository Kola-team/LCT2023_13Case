import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

import { persistStore } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { Provider } from 'react-redux';
import { store } from './storage/store';
import { PersistGate } from 'redux-persist/integration/react';

const root = ReactDOM.createRoot(document.getElementById('root'));

let persistor = persistStore(store);

// const qwe = () => storage.removeItem('persist:root_ideas');
// qwe()  //очистка sorage;


root.render(

  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <App />
    </PersistGate>
  </Provider>
);

