import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  token: null
}

export const userSlice = createSlice({
  name: 'user',
  initialState,

  reducers: {
    logOut: (state) => {
      state.token = false;
    },
    logIn: (state) => {
      state.token = true;
    }
  }
}


);

export const { logIn, logOut } = userSlice.actions;

export default userSlice.reducer;
