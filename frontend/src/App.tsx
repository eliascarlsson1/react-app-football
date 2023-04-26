import React, { useState } from "react";
import Tabs, { TabEvent } from "./tabs";
import PipelineView from "./pipelineview";
import EvaluateView, { AddROIEvent } from "./evaluateview";
const _ = require("lodash");

type AppState = { ROI: number; tab: "evaluate" | "pipeline" };
type AppAction = TabEvent | AddROIEvent;
type AppActionDispatcher = (action: AppAction) => void;

function App() {
  const [appState, setAppState] = useState<AppState>({
    ROI: 0,
    tab: "pipeline",
  });

  const appDispatcher: AppActionDispatcher = (action) => {
    const newAppState: AppState = _.cloneDeep(appState);
    switch (action.type) {
      case "tabEvent":
        newAppState.tab = action.tab;
        setAppState(newAppState);
        break;
      case "addROIEvent":
        newAppState.ROI++;
        setAppState(newAppState);
        break;
    }
  };

  return (
    <div className="App">
      <Tabs state={{ tab: appState.tab }} dispatcher={appDispatcher} />
      {appState.tab === "evaluate" ? (
        <EvaluateView
          state={{ ROI: appState.ROI }}
          dispatcher={appDispatcher}
        />
      ) : (
        <PipelineView />
      )}
    </div>
  );
}

export default App;
