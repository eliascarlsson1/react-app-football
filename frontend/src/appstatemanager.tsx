import React from "react";
import { TabEvent, TabState, TabOption } from "./tabs";
import { AddROIEvent, EvaluateViewState } from "./evaluateview";
const _ = require("lodash");

export type AppState = { ROI: number; tab: TabOption };
export type AppAction = TabEvent | AddROIEvent;
export type AppActionDispatcher = (action: AppAction) => void;

class AppStateManager {
	#appState: AppState;
	#setState: React.Dispatch<React.SetStateAction<AppState>> = () => {};
	#componentStateManager: ComponentStateManager;

	constructor(appState: AppState) {
		this.#appState = appState;
		this.#componentStateManager = new ComponentStateManager(appState);
	}

	updateAppState(appState: AppState) {
		this.#appState = appState;
		this.#componentStateManager.setAppState(appState);
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

	setAppState(appState: AppState) {
		appState = this.#appState;
	}

	getEvaluateViewState(): EvaluateViewState {
		return { ROI: this.#appState.ROI };
	}

	getTabState(): TabState {
		return { tab: this.#appState.tab };
	}
}

export { AppStateManager };
