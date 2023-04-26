import React, { useState } from "react";
import {
  AppStateManager,
  AppState,
} from "./appstatemanager";
import Tabs from "./tabs";
import PipelineView from "./pipelineview";
import EvaluateView from "./evaluateview";
import TrainModelView from "./train-model/trainmodelview";

const initialAppstate: AppState = {
  ROI: 0,
  tab: "pipeline",
};
const appStateManager = new AppStateManager(initialAppstate);

function App() {
  const [appState, setAppState] = useState<AppState>(initialAppstate);
  appStateManager.updateAppState(appState)
  appStateManager.updateSetState(setAppState)

  const appDispatcher =appStateManager.getAppActionDispatcher()

  return (
    <div className="App">
      <Tabs state={appStateManager.getComponentState().getTabState()} dispatcher={appDispatcher} />
      {appState.tab === "evaluate" ? (
        <EvaluateView
          state={appStateManager.getComponentState().getEvaluateViewState()}
          dispatcher={appDispatcher}
        />
      ) : appState.tab === "pipeline" ? (
        <PipelineView />
      ) : <TrainModelView/>}
    </div>
  );
}

export default App;
