import React, { useState, useRef } from "react";
import { AppStateManager, AppState } from "./appstatemanager";
import Stack from "@mui/material/Stack";
import BasicTabs from "./components/basictabs";
import EvaluateView from "./evaluate/evaluateview";
import TrainModelView from "./train-model/trainmodelview";

const appStateManager = new AppStateManager();

export type TopMenuTabOption = "Evaluate" | "Train model";
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

	const appDispatcher = appStateManager.getAppActionDispatcher();

	// App handles the top menu tab
	const tabValues: TopMenuTabOption[] = ["Evaluate", "Train model"];
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
				) : (
					<TrainModelView
						state={appStateManager.getComponentState().getTrainModelViewState()}
						dispatcher={appDispatcher}
					/>
				)}
			</Stack>
		</Stack>
	);
}

export default App;
