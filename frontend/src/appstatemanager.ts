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
	scrapeData,
	getAllLeagueIdsToName,
	prepareScrapedData,
	getPipelineInformation,
	deletePipeline,
	addPipeline,
	applyPipeline,
} from "./http-manager";
import { DeleteModelAction, DeleteModelState } from "./model/deletemodel";
import {
	DataViewAction,
	DataViewState,
	PrepareDataStatus,
} from "./dataview/dataview";
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
import {
	PipelineInformation,
	PipelineViewAction,
	PipelineViewState,
} from "./pipeline/pipelineview";
import { CreateNewPipelineState } from "./pipeline/createnewpipeline";
import { TestData, TestModelAction, TestModelState } from "./model/test_model";
import { DeleteTestAction, DeleteTestState } from "./test/deletetest";
import { getTestDataArray, getTrainModelRoi } from "./appstatemanagerutils";
import { GameBetInformation } from "./pipeline/betinformationview";
const _ = require("lodash");

export type BasicStringStatus = "idle" | "loading" | "success" | "error";

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
	leagueIdsToName: Map<string, string> | null;
	statuses: {
		trainModelStatus: TrainModelStatus;
		saveModelState: SaveModelStatus;
		prepareDataStatus: PrepareDataStatus;
		saveTestStatus: SaveTestStatus;
		prepareScrapeStatus: BasicStringStatus;
	};
	trainModelRoi: { id: string; roi: string }[];
	currentModels: ModelInformation[] | null;
	currentTests: string[] | null;
	testResponse: TestData[] | null;
	intervals: { prepareDataIntervalId: NodeJS.Timeout | null };
	pipelines: PipelineInformation[] | null;
	gameBetInformation: GameBetInformation[];
};
export type AppAction =
	| TopMenuTabAction
	| TrainModelAction
	| DataViewAction
	| DeleteModelAction
	| SaveModelAction
	| TestModelAction
	| SaveTestAction
	| DeleteTestAction
	| PipelineViewAction;
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
			leagueIdsToName: null,
			statuses: {
				trainModelStatus: "idle",
				saveModelState: "idle",
				prepareDataStatus: null,
				saveTestStatus: "idle",
				prepareScrapeStatus: "idle",
			},
			currentModels: null,
			trainModelRoi: [],
			currentTests: null,
			testResponse: null,
			intervals: { prepareDataIntervalId: null },
			pipelines: null,
			gameBetInformation: [],
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

		getAllLeagueIdsToName((leagueIdsToName) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.leagueIdsToName = leagueIdsToName;
			this.#setState(newAppState);
		});

		getPipelineInformation((pipelines) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.pipelines = pipelines;
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
					break;

				case "scrape data":
					scrapeData(action.leagueIds);
					break;
				case "prepare scraped data":
					newAppState.statuses.prepareScrapeStatus = "loading";
					this.#setState(newAppState);
					prepareScrapedData((response) => {
						const newAppState: AppState = _.cloneDeep(this.#appState);
						if (response === "Success") {
							newAppState.statuses.prepareScrapeStatus = "success";
						} else {
							newAppState.statuses.prepareScrapeStatus = "error";
						}
						this.#setState(newAppState);
						// Set timeout to set idle after 5 seconds
						setTimeout(() => {
							const newAppState: AppState = _.cloneDeep(this.#appState);
							newAppState.statuses.prepareScrapeStatus = "idle";
							this.#setState(newAppState);
						}, 5000);
					});
					break;
				case "delete pipeline":
					deletePipeline(action.name, (response) => {
						if (response === "success") {
							getPipelineInformation((pipelines) => {
								const newAppState: AppState = _.cloneDeep(this.#appState);
								newAppState.pipelines = pipelines;
								this.#setState(newAppState);
							});
						} else {
							console.log(response);
						}
					});
					break;
				case "add pipeline":
					addPipeline(action.pipeline, (response) => {
						if (response === "success") {
							getPipelineInformation((pipelines) => {
								const newAppState: AppState = _.cloneDeep(this.#appState);
								newAppState.pipelines = pipelines;
								this.#setState(newAppState);
							});
						} else {
							console.log(response);
						}
					});
					break;
				case "apply pipeline":
					applyPipeline(action.name, (response) => {
						const newAppState: AppState = _.cloneDeep(this.#appState);
						newAppState.gameBetInformation = response;
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

	getDataViewState(): DataViewState {
		return {
			prepareDataStatus: this.#appState.statuses.prepareDataStatus,
			leagueIdsToName: this.#appState.leagueIdsToName,
			prepareScrapeStatus: this.#appState.statuses.prepareScrapeStatus,
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

	getPipelineViewState(): PipelineViewState {
		return {
			pipelines: this.#appState.pipelines ?? [],
			gameBetInformation: this.#appState.gameBetInformation,
		};
	}

	getCreateNewPipelineState(): CreateNewPipelineState {
		return {
			currentModels: this.#appState.currentModels ?? [],
			currentTests: this.#appState.currentTests ?? [],
			leagueIdsToName: this.#appState.leagueIdsToName ?? new Map(),
		};
	}
}

export { AppStateManager };
