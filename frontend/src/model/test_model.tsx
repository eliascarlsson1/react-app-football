import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import SingleSelect from "../components/singleselect";
import { AppActionDispatcher } from "../appstatemanager";

export type TestData = { ROI: object[] } | null;
export type TestModelAction = {
	type: "test model";
	modelName: string;
	testData: string[];
	testName: string;
};
export type TestModelState = {
	currentModels: string[];
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
		state.currentModels[0],
	);

	if (
		!state.currentModels.includes(selectedModel) &&
		state.currentModels.length !== 0
	) {
		setSelectedModel(state.currentModels[0] ?? "");
	}

	return (
		<Stack>
			<SingleSelect
				dataArray={state.currentModels}
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
					? state.testResponse.ROI.map((obj) => (
							<Typography>
								{obj.id}: {obj.roi}
							</Typography>
					  ))
					: "No test response"}
			</Stack>
		</Stack>
	);
}
