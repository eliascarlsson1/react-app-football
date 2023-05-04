import React from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import LinearProgress from "@mui/material/LinearProgress";
import { AppActionDispatcher, AppStateManager } from "../appstatemanager";
import DeleteModel from "../model/deletemodel";
import DeleteTest from "../test/deletetest";

export type SettingsViewAction =
	| { type: "prepare data" }
	| { type: "download data" };

export type PrepareDataStatus = null | { status: string; total: string };

export type SettingsViewState = {
	prepareDataStatus: PrepareDataStatus;
};

export default function Settingsview({
	state,
	dispatcher,
	appStateManager,
}: {
	state: SettingsViewState;
	dispatcher: AppActionDispatcher;
	appStateManager: AppStateManager;
}) {
	const progress =
		(Number(state.prepareDataStatus?.status) /
			Number(state.prepareDataStatus?.total)) *
		100;

	const preparing = state.prepareDataStatus !== null;

	return (
		<Stack>
			<Stack direction={"row"} gap={3}>
				<Stack gap={2}>
					<Button
						onClick={() => dispatcher({ type: "prepare data" })}
						disabled={preparing}
						variant="contained"
					>
						Prepare data
					</Button>
					{!preparing ? (
						""
					) : (
						<LinearProgress variant="determinate" value={progress} />
					)}
				</Stack>
				<Button
					onClick={() => dispatcher({ type: "download data" })}
					variant="contained"
				>
					Download data
				</Button>
			</Stack>
			<Stack>
				<DeleteModel
					state={appStateManager.getComponentState().getDeleteModelState()}
					dispatcher={dispatcher}
				/>
				<DeleteTest
					state={appStateManager.getComponentState().getDeleteTestState()}
					dispatcher={dispatcher}
				/>
			</Stack>
		</Stack>
	);
}
