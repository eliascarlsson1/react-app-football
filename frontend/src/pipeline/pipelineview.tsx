import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import { AppActionDispatcher, AppStateManager } from "../appstatemanager";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import PipelineRow from "./pipelinerow";
import CreateNewPipeline from "./createnewpipeline";
import BetInformationView from "./betinformationview";
import type { GameBetInformation } from "./betinformationview";

export type PipelineInformation = {
	name: string;
	model: string;
	test: string;
	leagues: string[];
};

export type PipelineViewState = {
	pipelines: PipelineInformation[];
};

export type PipelineViewAction =
	| {
			type: "add pipeline";
			pipeline: PipelineInformation;
	  }
	| {
			type: "delete pipeline";
			name: string;
	  }
	| { type: "apply pipeline"; name: string };

// FIXME: Mock state, remove
const mockState: GameBetInformation = {
	homeTeam: "Home Team",
	awayTeam: "Away Team",
	date: "2023-07-07",
	pipelineName: "Pipeline Name",
	prediction: "Prediction",
	oddsPrediction: "Odds Prediction",
	model: {
		name: "Model Name",
		xParameters: ["xParameter1", "xParameter2"],
		yParameter: "yParameter",
		trainingData: ["Training Data 1", "Training Data 2"],
	},
	test: "Test Information",
	testDataForScrape: {
		id: "testId",
		roi: "testRoi",
		gamesBeforeFilter: 10,
		gamesAfterFilter: 8,
		zeroBeforeFilter: 2,
		zeroAfterFilter: 1,
		oneBeforeFilter: 4,
		oneAfterFilter: 3,
	},
	testDataForLeague: {
		id: "leagueId",
		roi: "leagueRoi",
		gamesBeforeFilter: 20,
		gamesAfterFilter: 15,
		zeroBeforeFilter: 3,
		zeroAfterFilter: 2,
		oneBeforeFilter: 6,
		oneAfterFilter: 4,
	},
	odds: {
		type: "over/under",
		goals: 2.5,
		odds: new Map([
			["Bookmaker1", { oddsOver: 1.8, oddsUnder: 2.0 }],
			["Bookmaker2", { oddsOver: 1.9, oddsUnder: 2.1 }],
		]),
		best_bookmaker: "Bookmaker1",
	},
	oddsportalLink:
		"https://www.oddsportal.com/football/england/premier-league/burnley-manchester-city-EkT4QbqS/",
};

export default function PipelineView({
	state,
	dispatcher,
	appStateManager,
}: {
	state: PipelineViewState;
	dispatcher: AppActionDispatcher;
	appStateManager: AppStateManager;
}) {
	const [open, setOpen] = React.useState(false);

	return (
		<div>
			<Stack direction={"column"}>
				<Typography variant="h5" gutterBottom>
					My pipelines
				</Typography>
				{state.pipelines.map((pipeline) => (
					<PipelineRow
						pipeline={pipeline}
						dispatcher={dispatcher}
						key={pipeline.name}
					></PipelineRow>
				))}
			</Stack>
			<Stack>
				<Typography variant="h5" gutterBottom>
					Add pipeline
				</Typography>
				<CreateNewPipeline
					dispatcher={dispatcher}
					state={appStateManager
						.getComponentState()
						.getCreateNewPipelineState()}
				></CreateNewPipeline>
			</Stack>

			<Dialog open={open}>
				<Stack>
					Use this modal to step page between different bet information views
					<BetInformationView state={mockState}></BetInformationView>
					<Button
						onClick={() => {
							setOpen(false);
						}}
					>
						Close modal
					</Button>
				</Stack>
			</Dialog>
			<Button
				onClick={() => {
					setOpen(true);
				}}
			>
				Open modal
			</Button>
		</div>
	);
}
