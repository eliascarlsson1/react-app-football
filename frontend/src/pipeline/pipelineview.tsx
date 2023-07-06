import React from "react";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import { AppActionDispatcher, AppStateManager } from "../appstatemanager";
import PipelineRow from "./pipelinerow";
import CreateNewPipeline from "./createnewpipeline";

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
				<CreateNewPipeline
					dispatcher={dispatcher}
					state={appStateManager
						.getComponentState()
						.getCreateNewPipelineState()}
				></CreateNewPipeline>
			</Stack>
		</div>
	);
}
