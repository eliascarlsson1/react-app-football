import React from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import LinearProgress from "@mui/material/LinearProgress";
import { AppActionDispatcher } from "../appstatemanager";

export type SettingsViewAction =
	| { type: "prepare data" }
	| { type: "download data" };

export type PrepareDataStatus = null | { status: string; total: string };

export type SettingsViewState = {
	prepareDataStatus: PrepareDataStatus;
};

export default function Settingsview({
	state,
	dipsatcher,
}: {
	state: SettingsViewState;
	dipsatcher: AppActionDispatcher;
}) {
	const progress =
		(Number(state.prepareDataStatus?.status) /
			Number(state.prepareDataStatus?.total)) *
		100;

	const preparing = state.prepareDataStatus !== null;

	return (
		<Stack direction={"row"} gap={3}>
			<Stack gap={2}>
				<Button
					onClick={() => dipsatcher({ type: "prepare data" })}
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
				onClick={() => dipsatcher({ type: "download data" })}
				variant="contained"
			>
				Download data
			</Button>
		</Stack>
	);
}
