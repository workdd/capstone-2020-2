import React from "react";
import "./App.css";
import MainPage from "./page/MainPage";
import { YobaProvidor } from "./context/YobaContext";

function App() {
  return (
    <YobaProvidor>
      <div className="App">
        <MainPage />
      </div>
    </YobaProvidor>
  );
}

export default App;
