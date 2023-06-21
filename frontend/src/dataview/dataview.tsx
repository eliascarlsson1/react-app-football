import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import LinearProgress from "@mui/material/LinearProgress";
import {
	AppActionDispatcher,
	AppStateManager,
	BasicStringStatus,
} from "../appstatemanager";
import MultiSelect from "../components/multiselect";

export type DataViewAction =
	| { type: "prepare data" }
	| { type: "download data" }
	| { type: "prepare scraped data" }
	| { type: "scrape data"; leagueIds: string[] };

export type PrepareDataStatus = null | { status: string; total: string };

export type DataViewState = {
	prepareDataStatus: PrepareDataStatus;
	leagueIdsToName: Map<string, string> | null;
	prepareScrapeStatus: BasicStringStatus;
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
		<Stack direction={"column"} gap={3}>
			<Stack gap={1}>
				<Stack>
					{" "}
					<Typography variant="h5" gutterBottom>
						Prepare Data Buttons
					</Typography>
				</Stack>
				<Stack direction={"row"} gap={2}>
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
					<Stack>
						<Button
							onClick={() => dispatcher({ type: "download data" })}
							variant="contained"
						>
							Download data
						</Button>
					</Stack>
				</Stack>
			</Stack>
			<Stack direction={"column"} gap={2} alignItems="flex-start">
				<Stack>
					<Typography variant="h5" gutterBottom>
						Scraped odds
					</Typography>
				</Stack>
				<Stack gap={1}>
					<MultiSelect
						dataArray={Array.from(nameToId.keys())}
						deliverSelected={(selected: string[]) => {
							setSelectedLeagues(selected);
						}}
						selected={selectedLeagues}
						label="Scrape leagues"
					></MultiSelect>
					<Stack direction={"row"} justifyContent="center">
						<Button onClick={onScrapeClick} variant="contained">
							Scrape
						</Button>
					</Stack>
					<Stack direction={"row"} justifyContent="center">
						<Stack>
							<Button
								onClick={() => {
									dispatcher({ type: "prepare scraped data" });
								}}
								variant="contained"
							>
								Prepare scraped games
							</Button>
							<Stack direction={"row"} justifyContent="center">
								<Typography variant="body1" gutterBottom>
									{getPrepareScrapeMessage(state.prepareScrapeStatus)}
								</Typography>
							</Stack>
						</Stack>
					</Stack>
				</Stack>
			</Stack>
		</Stack>
	);
}

function getPrepareScrapeMessage(status: BasicStringStatus): string {
	switch (status) {
		case "success":
			return "Scrape success";
		case "error":
			return "Scrape error";
		case "loading":
			return "Scrape in progress";
		case "idle":
			return "";
	}
}
