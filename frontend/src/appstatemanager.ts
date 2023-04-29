import React from "react";
import { TopMenuTabAction, TopMenuTabOption, TopMenuTabState } from "./App";
import {
	TrainModelViewState,
	TrainModelAction,
	TrainModelStatus,
} from "./model/trainmodelview";
import {
	getHistoricalData,
	getParameters,
	getCurrentModels,
	trainModel,
	prepareData,
	downloadLatestData,
	deleteModel,
	saveModel,
	getRoiTestModel,
} from "./http-manager";
import { DeleteModelAction, DeleteModelState } from "./model/deletemodel";
import { SettingsViewAction } from "./settingsview/settingsview";
import {
	SaveModelAction,
	SaveModelState,
	SaveModelStatus,
} from "./model/savemodel";
import { TestData, TestModelAction, TestModelState } from "./model/test_model";
const _ = require("lodash");

export type AppState = {
	tab: TopMenuTabOption;
	historicalData: string[] | null;
	xParameters: string[] | null;
	yParameters: string[] | null;
	statuses: {
		trainModelStatus: TrainModelStatus;
		saveModelState: SaveModelStatus;
	};
	currentModels: string[] | null;
	testResponse: TestData;
};
export type AppAction =
	| TopMenuTabAction
	| TrainModelAction
	| SettingsViewAction
	| DeleteModelAction
	| SaveModelAction
	| TestModelAction;
export type AppActionDispatcher = (action: AppAction) => void;

class AppStateManager {
	#appState: AppState;
	#setState: React.Dispatch<React.SetStateAction<AppState>> = () => {};
	#componentStateManager: ComponentStateManager;

	#recievedState = {
		historicalData: false,
		xParameters: false,
		yParameters: false,
	};

	constructor() {
		const initialAppState = this.getInitialAppState();
		this.#appState = initialAppState;
		this.#componentStateManager = new ComponentStateManager(initialAppState);
	}

	getInitialAppState(): AppState {
		const initalAppState: AppState = {
			tab: "Train model",
			historicalData: null,
			xParameters: null,
			yParameters: null,
			statuses: {
				trainModelStatus: "idle",
				saveModelState: "idle",
			},
			currentModels: null,
			testResponse: null,
		};
		return initalAppState;
	}

	atFirstRender() {
		getHistoricalData((historicalData) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.historicalData = historicalData;
			this.#setState(newAppState);
		});

		getParameters((parameters) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.xParameters = parameters;
			this.#setState(newAppState);
		}, "x");

		getParameters((parameters) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.yParameters = parameters;
			this.#setState(newAppState);
		}, "y");

		getCurrentModels((models) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.currentModels = models;
			this.#setState(newAppState);
		});
	}

	updateAppState(appState: AppState) {
		this.#appState = appState;
		this.#componentStateManager.updateAppState(appState);
	}

	updateSetState(setState: React.Dispatch<React.SetStateAction<AppState>>) {
		this.#setState = setState;
	}

	getAppActionDispatcher(): AppActionDispatcher {
		const appDispatcher: AppActionDispatcher = (action) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);

			switch (action.type) {
				case "top menu tab":
					newAppState.tab = action.selectedTab;
					this.#setState(newAppState);
					break;

				case "train model":
					newAppState.statuses.trainModelStatus = "training";
					this.#setState(newAppState);
					const getResponse = (response: string) => {
						const newAppState: AppState = _.cloneDeep(this.#appState);
						if (response === "success") {
							newAppState.statuses.trainModelStatus = "success";
						} else {
							newAppState.statuses.trainModelStatus = "error";
							console.log(response);
						}
						this.#setState(newAppState);
					};

					trainModel(action, getResponse);
					break;

				case "prepare data":
					prepareData((response) => {
						console.log(response);
					});
					break;

				case "download data":
					downloadLatestData((response) => {
						console.log(response);
					});
					break;

				case "delete model":
					this.#setState(newAppState);
					deleteModel(action.name, () => {
						getCurrentModels((models) => {
							const newAppState: AppState = _.cloneDeep(this.#appState);
							newAppState.currentModels = models;
							this.#setState(newAppState);
						});
					});
					break;

				case "save model":
					newAppState.statuses.saveModelState = "saving model";
					this.#setState(newAppState);
					saveModel(action.name, (response) => {
						const newAppState: AppState = _.cloneDeep(this.#appState);
						if (response === "success") {
							newAppState.statuses.saveModelState = "success";
						} else {
							newAppState.statuses.saveModelState = "error";
							console.log(response);
						}
						this.#setState(newAppState);
						getCurrentModels((models) => {
							const newAppState: AppState = _.cloneDeep(this.#appState);
							newAppState.currentModels = models;
							this.#setState(newAppState);
						});
					});
					break;

				case "test model":
					action.testData = this.#appState.historicalData ?? [];
					getRoiTestModel(action, (response) => {
						const rois: { id: string; roi: string }[] = [];
						Object.entries(response).forEach(([key, value]) => {
							rois.push({ id: key, roi: value });
						});
						const newAppState: AppState = _.cloneDeep(this.#appState);
						newAppState.testResponse = { ROI: rois };
						this.#setState(newAppState);
					});
			}
		};
		return appDispatcher;
	}

	getComponentState(): ComponentStateManager {
		return this.#componentStateManager;
	}
}

class ComponentStateManager {
	#appState: AppState;

	constructor(appState: AppState) {
		this.#appState = appState;
	}

	updateAppState(appState: AppState) {
		this.#appState = appState;
	}

	getTopMenuTabState(): TopMenuTabState {
		return { tab: this.#appState.tab };
	}

	getDeleteModelState(): DeleteModelState {
		return {
			currentModels: this.#appState.currentModels ?? [],
		};
	}

	getSaveModelState(): SaveModelState {
		return {
			saveModelServerState: this.#appState.statuses.saveModelState,
		};
	}

	getTestModelState(): TestModelState {
		return {
			currentModels: this.#appState.currentModels ?? [],
			testResponse: this.#appState.testResponse,
		};
	}

	getTrainModelViewState(): TrainModelViewState {
		return {
			historicalData: this.#appState.historicalData ?? [],
			xParameters: this.#appState.xParameters ?? [],
			yParameters: this.#appState.yParameters ?? [],
			trainModelStatus: this.#appState.statuses.trainModelStatus,
		};
	}
}

export { AppStateManager };
