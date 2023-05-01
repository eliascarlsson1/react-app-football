import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import SingleSelect from "../components/singleselect";
import { AppActionDispatcher, ModelInformation } from "../appstatemanager";

export type TestData = { ROI: { id: string; roi: string }[] } | null;
export type TestModelAction = {
	type: "test model";
	modelName: string;
	testData: string[];
	testName: string;
};
export type TestModelState = {
	currentModels: ModelInformation[];
	historicalData: string[];
	testResponse: TestData;
};

export default function Test_model({
	dispatcher,
	state,
}: {
	dispatcher: AppActionDispatcher;
	state: TestModelState;
}) {
	const [selectedModel, setSelectedModel] = useState<string>(
		state.currentModels[0].name,
	);

	const currentModelNames = state.currentModels.map((model) => model.name);

	if (
		!currentModelNames.includes(selectedModel) &&
		state.currentModels.length !== 0
	) {
		setSelectedModel(state.currentModels[0].name ?? "");
	}

	return (
		<Stack>
			<SingleSelect
				dataArray={currentModelNames}
				deliverSelected={(selected: string) => {
					setSelectedModel(selected);
				}}
				selected={selectedModel}
				label="Test model"
			/>
			<Button
				onClick={() =>
					dispatcher({
						type: "test model",
						modelName: selectedModel,
						testName: "",
						testData: [],
					})
				}
			>
				Test model
			</Button>
			<Stack direction={"column"}>
				{state.testResponse
					? state.testResponse.ROI.map((league) => (
							<Typography>
								{league.id}: {league.roi}
							</Typography>
					  ))
					: "No test response"}
			</Stack>
		</Stack>
	);
}
