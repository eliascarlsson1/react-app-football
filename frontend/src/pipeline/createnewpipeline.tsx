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
						name: "pipeline name",
						model: "model name",
						test: "test name",
						leagues: ["league1", "league2"],
					});
				}}
			></Button>
		</div>
	);
}
