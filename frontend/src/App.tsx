import React, { useState } from "react";
import Tabs, { TabOptions } from "./tabs";
import PipelineView from "./pipelineview";
import EvaluateView from "./evaluateview";

type AppState = { ROI: string; tab: "evaluate" | "pipeline" };

function App() {
  const [appState, setAppState] = useState<AppState>({
    ROI: "0",
    tab: "pipeline",
  });
  const setTab: (tab: TabOptions) => void = (tab) => {
    const newAppState: AppState = { ROI: appState.ROI, tab };
    setAppState(newAppState);
  };

  return (
    <div className="App">
      <Tabs state={{ tab: appState.tab }} dispatcher={setTab} />
      {appState.tab === "evaluate" ? (
        <EvaluateView state={{ ROI: appState.ROI }} />
      ) : (
        <PipelineView />
      )}
    </div>
  );
}

export default App;
