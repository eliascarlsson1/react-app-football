import React from "react";
import { TopMenuTabAction, TopMenuTabOption, TopMenuTabState } from "./App";
import {
	TrainModelViewState,
	TrainModelAction,
	TrainModelStatus,
} from "./train-model/trainmodelview";
import { getHistoricalData, get_parameters, trainModel } from "./http-manager";
import { SettingsViewAction } from "./settingsview/settingsview";
const _ = require("lodash");

export type AppState = {
	tab: TopMenuTabOption;
	historicalData: string[];
	xParameters: string[];
	yParameters: string[];
	statuses: { trainModelStatus: TrainModelStatus };
};
export type AppAction =
	| TopMenuTabAction
	| TrainModelAction
	| SettingsViewAction;
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
			historicalData: [],
			xParameters: [],
			yParameters: [],
			statuses: { trainModelStatus: "idle" },
		};
		return initalAppState;
	}

	atFirstRender() {
		getHistoricalData((historicalData) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.historicalData = historicalData;
			this.#setState(newAppState);
			this.#recievedState.historicalData = true;
		});

		get_parameters((parameters) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.xParameters = parameters;
			this.#setState(newAppState);
			this.#recievedState.xParameters = true;
		}, "x");

		get_parameters((parameters) => {
			const newAppState: AppState = _.cloneDeep(this.#appState);
			newAppState.yParameters = parameters;
			this.#setState(newAppState);
			this.#recievedState.yParameters = true;
		}, "y");
	}

	loadingFirstRender = () => {
		return !(
			this.#recievedState.historicalData &&
			this.#recievedState.xParameters &&
			this.#recievedState.yParameters
		);
	};

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
					console.log(action)
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
					console.log("prepare data call");
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

	getTrainModelViewState(): TrainModelViewState {
		return {
			historicalData: this.#appState.historicalData,
			xParameters: this.#appState.xParameters,
			yParameters: this.#appState.yParameters,
			trainModelStatus: this.#appState.statuses.trainModelStatus,
		};
	}
}

export { AppStateManager };
