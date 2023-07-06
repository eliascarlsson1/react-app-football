import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { AppActionDispatcher, ModelInformation } from "../appstatemanager";
import SingleSelect from "../components/singleselect";
import MultiSelect from "../components/multiselect";

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
	const modelNames = state.currentModels.map((model) => model.name);
	const [selectedModel, setSelectedModel] = useState<string>(modelNames[0]);

	const testNames = state.currentTests;
	const [selectedTest, setSelectedTest] = useState<string>(testNames[0]);

	const [pipelineName, setPipelineName] = useState<string>("");

	const idToName = state.leagueIdsToName;
	const [selectedLeagues, setSelectedLeagues] = useState<string[]>([]);

	return (
		<div>
			<Stack direction={"row"} paddingY={3} gap={1}>
				<SingleSelect
					dataArray={modelNames}
					selected={selectedModel}
					deliverSelected={(selected) => {
						setSelectedModel(selected);
					}}
					label={"Select model"}
					width={200}
				/>
				<SingleSelect
					dataArray={testNames}
					selected={selectedTest}
					deliverSelected={(selected) => {
						setSelectedTest(selected);
					}}
					label={"Select test"}
					width={200}
				/>
				<MultiSelect
					dataArray={Array.from(idToName.keys())}
					deliverSelected={(selected: string[]) => {
						setSelectedLeagues(selected);
					}}
					selected={selectedLeagues}
					label="Select leagues"
				/>

				<TextField
					label="Pipeline name"
					variant="outlined"
					onChange={(e) => {
						setPipelineName(e.target.value);
					}}
				/>
				<Button
					variant="contained"
					style={{ width: "200px" }}
					onClick={() => {
						dispatcher({
							type: "add pipeline",
							pipeline: {
								name: pipelineName,
								model: selectedModel,
								test: selectedTest,
								leagues: selectedLeagues,
							},
						});
					}}
				>
					Add pipeline
				</Button>
			</Stack>
		</div>
	);
}
