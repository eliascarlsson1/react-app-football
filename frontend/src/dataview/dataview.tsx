import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import LinearProgress from "@mui/material/LinearProgress";
import { AppActionDispatcher, AppStateManager } from "../appstatemanager";
import MultiSelect from "../components/multiselect";

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

	// Leagues to scrape
	const idToName = state.leagueIdsToName ?? new Map();
	const nameToId: Map<string, string> = new Map();
	for (const [id, name] of idToName) {
		nameToId.set(name, id);
	}
	const [selectedLeagues, setSelectedLeagues] = useState(
		Array.from(nameToId.keys()),
	);
	const onScrapeClick = () => {
		const selectedIds: string[] = [];
		for (const name of selectedLeagues) {
			const id = nameToId.get(name);
			if (id) {
				selectedIds.push(id);
			}
		}
		dispatcher({ type: "scrape data", leagueIds: selectedIds });
	};

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
				<Stack direction={"column"}>
					<MultiSelect
						dataArray={Array.from(nameToId.keys())}
						deliverSelected={(selected: string[]) => {
							setSelectedLeagues(selected);
						}}
						selected={selectedLeagues}
						label="Scrape leagues"
					></MultiSelect>
					<Button onClick={onScrapeClick} variant="contained">
						Scrape
					</Button>
				</Stack>
			</Stack>
			<Stack></Stack>
		</Stack>
	);
}
