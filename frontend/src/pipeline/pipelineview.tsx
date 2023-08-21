import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import { Pagination } from "@mui/material";
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
	gameBetInformationOpen: boolean;
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
	| { type: "apply pipeline"; name: string }
	| { type: "close game bet information" };

export default function PipelineView({
	state,
	dispatcher,
	appStateManager,
}: {
	state: PipelineViewState;
	dispatcher: AppActionDispatcher;
	appStateManager: AppStateManager;
}) {
	const [page, setPage] = React.useState(1);
	const handlePageChange = (
		event: React.ChangeEvent<unknown>,
		value: number,
	) => {
		setPage(value);
	};

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

			<Dialog open={state.gameBetInformationOpen}>
				<Stack alignItems={"center"} width={500} paddingY={3}>
					{state.gameBetInformation.length > 0 ? (
						<BetInformationView
							state={state.gameBetInformation[page - 1]}
						></BetInformationView>
					) : (
						"No bet information available"
					)}
					<Stack
						direction={"row"}
						alignItems={"center"}
						paddingTop={1}
						justifyContent={"space-between"}
						width={"95%"}
					>
						<Pagination
							count={state.gameBetInformation.length}
							onChange={handlePageChange}
						/>
						<Button
							onClick={() => {
								dispatcher({ type: "close game bet information" });
							}}
						>
							Close modal
						</Button>
					</Stack>
				</Stack>
			</Dialog>
		</div>
	);
}
