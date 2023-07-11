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
	gameBetInformation: GameBetInformation[];
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

	console.log(state.gameBetInformation);
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
					{state.gameBetInformation.length > 0 ? (
						<BetInformationView
							state={state.gameBetInformation[0]}
						></BetInformationView>
					) : (
						"No bet information available"
					)}
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
