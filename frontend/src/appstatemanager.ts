import React from "react";
import { TopMenuTabAction, TopMenuTabOption, TopMenuTabState } from "./App";
import {
	TrainModelViewState,
	TrainModelAction,
} from "./train-model/trainmodelview";
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
			historicalData: ["test1", "test2", "test3", "test4", "test5"],
			xParameters: ["x_par1", "x_par2", "x_par3"],
			yParameters: ["y_par1", "y_par2", "y_par3"],
		};
		return initalAppState;
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
					console.log(action);
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
