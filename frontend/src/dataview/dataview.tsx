import React from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import LinearProgress from "@mui/material/LinearProgress";
import { AppActionDispatcher, AppStateManager } from "../appstatemanager";

export type DataViewAction =
	| { type: "prepare data" }
	| { type: "download data" }
	| { type: "scrape data"; leagueIds: string[] };

export type PrepareDataStatus = null | { status: string; total: string };

export type DataViewState = {
	prepareDataStatus: PrepareDataStatus;
	leagueIdsToName: Map<string, string> | null;
};

export default function DataView({
	state,
	dispatcher,
	appStateManager,
}: {
	state: DataViewState;
	dispatcher: AppActionDispatcher;
	appStateManager: AppStateManager;
}) {
	const progress =
		(Number(state.prepareDataStatus?.status) /
			Number(state.prepareDataStatus?.total)) *
		100;

	const preparing = state.prepareDataStatus !== null;

	//FIXME: Add options for leagues to scrape.

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
				<Button
					onClick={() =>
						dispatcher({ type: "scrape data", leagueIds: ["BL", "PL"] })
					}
					variant="contained"
				>
					Scrape PL
				</Button>
			</Stack>
			<Stack></Stack>
		</Stack>
	);
}
