import { configureStore } from '@reduxjs/toolkit';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from "redux";
import { persistReducer } from 'redux-persist';
import thunk from 'redux-thunk'

import userReducer from './slises/userSlice';
import dataReduser from './slises/dataSlise';

const reducers = combineReducers({
  user: userReducer,
  data: dataReduser
});

const persistConfig = {
  key: 'root_ideas',
  storage
}; 

const persistedReducer = persistReducer(persistConfig, reducers);

export const store = configureStore({
  reducer: persistedReducer,
  devTools: process.env.NODE_ENV !== 'production',
  middleware: [thunk]
});

