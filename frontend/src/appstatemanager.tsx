import React from "react";
import { TabEvent, TabState, TabOption } from "./tabs";
import { AddROIEvent, EvaluateViewState } from "./evaluate/evaluateview";
import { TrainModelViewState } from "./train-model/trainmodelview";
const _ = require("lodash");

export type AppState = {
	ROI: number;
	tab: TabOption;
	historicalData: string[];
};
export type AppAction = TabEvent | AddROIEvent;
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
			ROI: 0,
			tab: "trainModel",
			historicalData: ["test1", "test2"],
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
				case "tabEvent":
					newAppState.tab = action.tab;
					this.#setState(newAppState);
					break;
				case "addROIEvent":
					newAppState.ROI++;
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

	getEvaluateViewState(): EvaluateViewState {
		return { ROI: this.#appState.ROI };
	}

	getTabState(): TabState {
		return { tab: this.#appState.tab };
	}

	getTrainModelViewState(): TrainModelViewState {
		return { historicalData: this.#appState.historicalData };
	}
}

export { AppStateManager };
