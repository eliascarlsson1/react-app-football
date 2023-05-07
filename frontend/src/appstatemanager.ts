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
	getStatsModelTest,
	getPrepareDataProgess,
	getCurrentTests,
	saveTest,
	deleteTest,
	getRoiFromModel,
} from "./http-manager";
import { DeleteModelAction, DeleteModelState } from "./model/deletemodel";
import {
	SettingsViewState,
	SettingsViewAction,
	PrepareDataStatus,
} from "./settingsview/settingsview";
import {
	SaveModelAction,
	SaveModelState,
	SaveModelStatus,
} from "./model/savemodel";
import {
	SaveTestAction,
	SaveTestStatus,
	CreateTestState,
} from "./test/create_test";
import { TestData, TestModelAction, TestModelState } from "./model/test_model";
import { DeleteTestAction, DeleteTestState } from "./test/deletetest";
import { getTestDataArray, getTrainModelRoi } from "./appstatemanagerutils";
const _ = require("lodash");

export type ModelInformation = {
	name: string;
	xParameters: string[];
	yParameter: string;
	trainingData: string[];
};

export type AppState = {
	tab: TopMenuTabOption;
	historicalData: string[] | null;
	xParameters: string[] | null;
	yParameters: string[] | null;
	statuses: {
		trainModelStatus: TrainModelStatus;
		saveModelState: SaveModelStatus;
		prepareDataStatus: PrepareDataStatus;
		saveTestStatus: SaveTestStatus;
	};
	trainModelRoi: { id: string; roi: string }[];
	currentModels: ModelInformation[] | null;
	currentTests: string[] | null;
	testResponse: TestData[] | null;
	intervals: { prepareDataIntervalId: NodeJS.Timeout | null };
};
export type AppAction =
	| TopMenuTabAction
	| TrainModelAction
	| SettingsViewAction
	| DeleteModelAction
	| SaveModelAction
	| TestModelAction
	| SaveTestAction
	| DeleteTestAction;
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
				prepareDataStatus: null,
				saveTestStatus: "idle",
			},
			currentModels: null,
			trainModelRoi: [],
			currentTests: null,
			testResponse: null,
			intervals: { prepareDataIntervalId: null },
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

		getCurrentTests((tests) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.currentTests = tests;
			this.#setState(newAppState);
		});
	}

	onRender(
		appState: AppState,
		setState: React.Dispatch<React.SetStateAction<AppState>>,
	) {
		this.#setState = setState;
		this.#appState = appState;
		this.#componentStateManager.updateAppState(appState);

		// Prepare data status
		const prepareDataStatus = this.#appState.statuses.prepareDataStatus;
		const prepareDataIntervalId =
			this.#appState.intervals.prepareDataIntervalId;
		if (
			prepareDataStatus !== null &&
			prepareDataStatus.status === prepareDataStatus.total &&
			prepareDataIntervalId !== null
		) {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.statuses.prepareDataStatus = null;
			this.#setState(newAppState);
			clearInterval(prepareDataIntervalId);
		}
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
							if (action.testData.length > 0) {
								getRoiFromModel(
									{ testData: action.testData, modelName: "current_model" },
									(response) => {
										const newAppState: AppState = _.cloneDeep(this.#appState);
										newAppState.trainModelRoi = getTrainModelRoi(response);
										this.#setState(newAppState);
									},
								);
							} else {
								newAppState.trainModelRoi = [];
								this.#setState(newAppState);
							}
						} else {
							newAppState.statuses.trainModelStatus = "error";
							console.log(response);
						}
						this.#setState(newAppState);
					};

					trainModel(action, getResponse);
					break;

				case "prepare data":
					const getPreparedata = () => {
						getPrepareDataProgess((response) => {
							const newAppState: AppState = _.cloneDeep(this.#appState);
							const status = response.status;
							const total = response.total;
							newAppState.statuses.prepareDataStatus = {
								status: status,
								total: total,
							};
							this.#setState(newAppState);
						});
					};

					prepareData((response) => {
						getPreparedata();
					});

					this.#appState.intervals.prepareDataIntervalId = setInterval(() => {
						getPreparedata();
					}, 5000);

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

				case "delete test":
					this.#setState(newAppState);
					deleteTest(action.name, () => {
						getCurrentTests((tests) => {
							const newAppState: AppState = _.cloneDeep(this.#appState);
							newAppState.currentTests = tests;
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
					getStatsModelTest(action, (response) => {
						const testDataArray = getTestDataArray(response);
						const newAppState: AppState = _.cloneDeep(this.#appState);
						newAppState.testResponse = testDataArray;
						this.#setState(newAppState);
					});
					break;

				case "save test":
					newAppState.statuses.saveTestStatus = "saving test";
					this.#setState(newAppState);
					saveTest(action.filterData, (response) => {
						const newAppState: AppState = _.cloneDeep(this.#appState);
						if (response === "success") {
							newAppState.statuses.saveTestStatus = "success";
						} else {
							newAppState.statuses.saveTestStatus = "error";
							console.log(response);
						}
						this.#setState(newAppState);
						getCurrentTests((tests) => {
							const newAppState: AppState = _.cloneDeep(this.#appState);
							newAppState.currentTests = tests;
							this.#setState(newAppState);
						});
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
		const currentModelNames = this.#appState.currentModels?.map(
			(model) => model.name,
		);
		return {
			currentModels: currentModelNames ?? [],
		};
	}

	getDeleteTestState(): DeleteTestState {
		return {
			currentTests: this.#appState.currentTests ?? [],
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
			historicalData: this.#appState.historicalData ?? [],
			currentTests: this.#appState.currentTests ?? [],
		};
	}

	getSettingsViewState(): SettingsViewState {
		return {
			prepareDataStatus: this.#appState.statuses.prepareDataStatus,
		};
	}

	getCreateTestState(): CreateTestState {
		return {
			saveTestStatus: this.#appState.statuses.saveTestStatus,
		};
	}

	getTrainModelViewState(): TrainModelViewState {
		return {
			historicalData: this.#appState.historicalData ?? [],
			xParameters: this.#appState.xParameters ?? [],
			yParameters: this.#appState.yParameters ?? [],
			trainModelStatus: this.#appState.statuses.trainModelStatus,
			trainModelRoi: this.#appState.trainModelRoi,
		};
	}
}

export { AppStateManager };
