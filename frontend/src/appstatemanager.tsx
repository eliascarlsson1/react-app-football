import React from "react";
import { TopMenuTabAction, TopMenuTabOption, TopMenuTabState } from "./App";
import { TrainModelViewState } from "./train-model/trainmodelview";
const _ = require("lodash");

export type AppState = {
	tab: TopMenuTabOption;
	historicalData: string[];
	x_parameters: string[];
	y_parameters: string[];
};
export type AppAction = TopMenuTabAction;
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
			x_parameters: ["x_par1", "x_par2", "x_par3"],
			y_parameters: ["y_par1", "y_par2", "y_par3"],
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
			x_parameters: this.#appState.x_parameters,
			y_parameters: this.#appState.y_parameters,
		};
	}
}

export { AppStateManager };
