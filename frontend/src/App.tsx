import React, { useState, useRef } from "react";
import { AppStateManager, AppState } from "./appstatemanager";
import Stack from "@mui/material/Stack";
import BasicTabs from "./components/basictabs";
import EvaluateView from "./evaluate/evaluateview";
import TrainModelView from "./model/trainmodelview";
import Settingsview from "./settingsview/settingsview";
import DeleteModel from "./model/deletemodel";
import TestModel from "./model/test_model";

const appStateManager = new AppStateManager();

export type TopMenuTabOption = "Evaluate" | "Train model" | "Settings";
export type TopMenuTabAction = {
	type: "top menu tab";
	selectedTab: TopMenuTabOption;
};
export type TopMenuTabState = { tab: TopMenuTabOption };

function useFirstRender() {
	const ref = useRef(true);
	const firstRender = ref.current;
	ref.current = false;
	return firstRender;
}

function App() {
	const [appState, setAppState] = useState<AppState>(
		appStateManager.getInitialAppState(),
	);

	appStateManager.updateAppState(appState);
	appStateManager.updateSetState(setAppState);

	if (useFirstRender()) {
		appStateManager.atFirstRender();
	}

	// Loaded data successfully?
	if (
		!(
			appState.historicalData &&
			appState.xParameters &&
			appState.yParameters &&
			appState.currentModels
		)
	) {
		return <div>Waiting for server..</div>;
	}

	const appDispatcher = appStateManager.getAppActionDispatcher();

	// App handles the top menu tab
	const tabValues: TopMenuTabOption[] = ["Evaluate", "Train model", "Settings"];
	const deliverSelectedIndex = (selectedIndex: number) => {
		const selectedTab = tabValues[selectedIndex];
		appDispatcher({ type: "top menu tab", selectedTab });
	};

	return (
		<Stack direction="column" padding={3}>
			<BasicTabs
				values={tabValues}
				startingIndex={tabValues.indexOf(appState.tab)}
				deliverSelectedIndex={deliverSelectedIndex}
			/>
			<Stack padding={3}>
				{appState.tab === "Evaluate" ? (
					<EvaluateView />
				) : appState.tab === "Train model" ? (
					<Stack direction={"row"}>
						<TrainModelView
							state={appStateManager
								.getComponentState()
								.getTrainModelViewState()}
							dispatcher={appDispatcher}
							appStateManager={appStateManager}
						/>
						<DeleteModel
							state={appStateManager.getComponentState().getDeleteModelState()}
							dispatcher={appDispatcher}
						/>
						<TestModel
							state={appStateManager.getComponentState().getTestModelState()}
							dispatcher={appDispatcher}
						/>
					</Stack>
				) : (
					<Settingsview dipsatcher={appDispatcher} />
				)}
			</Stack>
		</Stack>
	);
}

export default App;
