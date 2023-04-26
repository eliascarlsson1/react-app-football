import React, { useState } from "react";
import { AppStateManager, AppState } from "./appstatemanager";
import Tabs from "./tabs";
import EvaluateView from "./evaluate/evaluateview";
import TrainModelView from "./train-model/trainmodelview";

const appStateManager = new AppStateManager();

function App() {
	const [appState, setAppState] = useState<AppState>(
		appStateManager.getInitialAppState(),
	);
	appStateManager.updateAppState(appState);
	appStateManager.updateSetState(setAppState);

	const appDispatcher = appStateManager.getAppActionDispatcher();

	return (
		<div className="App">
			<Tabs
				state={appStateManager.getComponentState().getTabState()}
				dispatcher={appDispatcher}
			/>
			{appState.tab === "evaluate" ? (
				<EvaluateView
					state={appStateManager.getComponentState().getEvaluateViewState()}
					dispatcher={appDispatcher}
				/>
			) : (
				<TrainModelView
					state={appStateManager.getComponentState().getTrainModelViewState()}
				/>
			)}
		</div>
	);
}

export default App;
