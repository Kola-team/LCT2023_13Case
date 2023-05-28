import AppView from "./components/AppView/AppView";

import { useEffect } from "react";
import { useDispatch } from "react-redux";

import { setAllFlight, setTabs } from "./storage/slises/dataSlise";

function App() {

  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(setAllFlight());
    dispatch(setTabs("Сезонность спроса"));
  }, [])

  return (
    <AppView />
  );
}

export default App;
