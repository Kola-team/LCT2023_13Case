import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

const initialState = {
    tabs: 'Сезонность спроса',
    seasonalDemandData: [],
    stacks: [],
};

export const setAllFlight = createAsyncThunk(
    'user/setAllFlight',
    async () => {
        const response = await fetch('/all_flight/')
            .then((data) => data.json());
        return response;
    }
);

export const setSeasonalDemandData = createAsyncThunk(
    'user/setSeasonalDemandData',
    async (fltNum) => {
        const response = await fetch('/seasonality', {
            method: 'POST',
            body: JSON.stringify({
                flt_num: fltNum
            }),
            headers: { "content-type": "application/json" }
        })
            .then((data) => data.json());
        return response;
    }
);

export const dataSlice = createSlice({
    name: 'data',
    initialState,
    reducers: {
        setTabs: (state, action) => {
            state.tabs = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(setAllFlight.fulfilled, (state, action) => {
                state.allFlight = action.payload.items;
            })
        .addCase(setSeasonalDemandData.fulfilled, (state, action) => {
            state.seasonalDemandData = action.payload;
        })
    },
});

export const { setTabs } = dataSlice.actions
export default dataSlice.reducer
