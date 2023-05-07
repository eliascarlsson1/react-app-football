import React, { useState, useRef } from "react";
import { AppStateManager, AppState } from "./appstatemanager";
import Stack from "@mui/material/Stack";
import BasicTabs from "./components/basictabs";
import EvaluateView from "./evaluate/evaluateview";
import TrainModelView from "./model/trainmodelview";
import Settingsview from "./settingsview/settingsview";
import DeleteModel from "./model/deletemodel";
import TestModel from "./model/test_model";
import CreateTest from "./test/create_test";

const appStateManager = new AppStateManager();

export type TopMenuTabOption = "Evaluate" | "Train model" | "Test" | "Settings";
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
	console.log("App render");

	const [appState, setAppState] = useState<AppState>(
		appStateManager.getInitialAppState(),
	);

	if (useFirstRender()) {
		appStateManager.atFirstRender();
	}

	appStateManager.onRender(appState, setAppState);

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
	const tabValues: TopMenuTabOption[] = [
		"Evaluate",
		"Train model",
		"Test",
		"Settings",
	];
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
					<Stack direction={"row"} gap={1}>
						<TrainModelView
							state={appStateManager
								.getComponentState()
								.getTrainModelViewState()}
							dispatcher={appDispatcher}
							appStateManager={appStateManager}
						/>
					</Stack>
				) : appState.tab === "Test" ? (
					<Stack>
						<CreateTest
							state={appStateManager.getComponentState().getCreateTestState()}
							dispatcher={appDispatcher}
						/>
						<TestModel
							state={appStateManager.getComponentState().getTestModelState()}
							dispatcher={appDispatcher}
						/>
					</Stack>
				) : (
					<Settingsview
						state={appStateManager.getComponentState().getSettingsViewState()}
						dispatcher={appDispatcher}
						appStateManager={appStateManager}
					/>
				)}
			</Stack>
		</Stack>
	);
}

export default App;
