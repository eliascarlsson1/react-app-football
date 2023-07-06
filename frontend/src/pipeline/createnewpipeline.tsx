import React from "react";
import Button from "@mui/material/Button";
import { AppActionDispatcher, ModelInformation } from "../appstatemanager";

export type CreateNewPipelineState = {
	currentTests: string[];
	leagueIdsToName: Map<string, string>;
	currentModels: ModelInformation[];
};

export default function CreateNewPipeline({
	state,
	dispatcher,
}: {
	state: CreateNewPipelineState;
	dispatcher: AppActionDispatcher;
}) {
	return (
		<div>
			<span>Input field1</span>
			<span>Input field2</span>
			<Button
				variant="contained"
				style={{ width: "200px" }}
				onClick={() => {
					dispatcher({
						type: "add pipeline",
						pipeline: {
							name: "new pipeline",
							model: "model",
							test: "test",
							leagues: ["league1", "league2"],
						},
					});
				}}
			></Button>
		</div>
	);
}
