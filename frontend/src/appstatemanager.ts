import React from "react";
import { TopMenuTabAction, TopMenuTabOption, TopMenuTabState } from "./App";
import {
	TrainModelViewState,
	TrainModelAction,
} from "./train-model/trainmodelview";
import { getHistoricalData } from "./http-manager";
const _ = require("lodash");

export type AppState = {
	tab: TopMenuTabOption;
	historicalData: string[];
	xParameters: string[];
	yParameters: string[];
};
export type AppAction = TopMenuTabAction | TrainModelAction;
export type AppActionDispatcher = (action: AppAction) => void;

class AppStateManager {
	#appState: AppState;
	#setState: React.Dispatch<React.SetStateAction<AppState>> = () => {};
	#componentStateManager: ComponentStateManager;

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
		};
		return initalAppState;
	}

	atFirstRender() {
		const newAppState: AppState = _.cloneDeep(this.#appState);
		getHistoricalData((historicalData) => {
			newAppState.historicalData = historicalData;
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
		};
	}
}

export { AppStateManager };
