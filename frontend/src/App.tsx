import React, { useState, useRef } from "react";
import { AppStateManager, AppState } from "./appstatemanager";
import Stack from "@mui/material/Stack";
import BasicTabs from "./components/basictabs";
import EvaluateView from "./evaluate/evaluateview";
import TrainModelView from "./model/trainmodelview";
import DataView from "./dataview/dataview";
import DeleteTest from "./test/deletetest";
import TestModel from "./model/test_model";
import CreateTest from "./test/create_test";
import PipelineView from "./pipeline/pipelineview";
import DeleteModel from "./model/deletemodel";
import ShowModelStats from "./model/showmodelstats";

const appStateManager = new AppStateManager();

export type TopMenuTabOption =
	| "Evaluate"
	| "Train model"
	| "Test"
	| "Data"
	| "Pipeline";
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

	if (useFirstRender()) {
		appStateManager.atFirstRender();
	}

	appStateManager.onRender(appState, setAppState);

	// Loaded data successfully?
	//FIXME: Add more checks here
	if (
		!(
			appState.historicalData &&
			appState.xParameters &&
			appState.yParameters &&
			appState.currentModels &&
			appState.currentTests
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
		"Data",
		"Pipeline",
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
					<Stack direction={"row"} gap={2} alignItems={"flex-start"}>
						<TrainModelView
							state={appStateManager
								.getComponentState()
								.getTrainModelViewState()}
							dispatcher={appDispatcher}
							appStateManager={appStateManager}
						/>
						<Stack gap={3}>
							<ShowModelStats
								state={appStateManager
									.getComponentState()
									.getShowModelStatsViewState()}
								dispatcher={appDispatcher}
							/>
							<DeleteModel
								state={appStateManager
									.getComponentState()
									.getDeleteModelState()}
								dispatcher={appDispatcher}
							/>
						</Stack>
					</Stack>
				) : appState.tab === "Test" ? (
					<Stack alignItems={"flex-start"} direction={"row"} gap={2}>
						<CreateTest
							state={appStateManager.getComponentState().getCreateTestState()}
							dispatcher={appDispatcher}
						/>
						<TestModel
							state={appStateManager.getComponentState().getTestModelState()}
							dispatcher={appDispatcher}
						/>
						<Stack>
							<ShowModelStats
								state={appStateManager
									.getComponentState()
									.getShowModelStatsViewState()}
								dispatcher={appDispatcher}
							/>
							<DeleteTest
								state={appStateManager.getComponentState().getDeleteTestState()}
								dispatcher={appDispatcher}
							/>
						</Stack>
					</Stack>
				) : appState.tab === "Pipeline" ? (
					<PipelineView
						state={appStateManager.getComponentState().getPipelineViewState()}
						dispatcher={appDispatcher}
						appStateManager={appStateManager}
					></PipelineView>
				) : (
					<DataView
						state={appStateManager.getComponentState().getDataViewState()}
						dispatcher={appDispatcher}
						appStateManager={appStateManager}
					/>
				)}
			</Stack>
		</Stack>
	);
}

export default App;
