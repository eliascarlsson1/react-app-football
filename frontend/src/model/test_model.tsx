import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import SingleSelect from "../components/singleselect";
import { AppActionDispatcher } from "../appstatemanager";

export type TestData = { ROI: number } | null;
export type TestModelAction = { type: "test model" };
export type TestModelState = {
	currentModelNames: string[];
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
		state.currentModelNames[0],
	);

	return (
		<Stack>
			<SingleSelect
				dataArray={state.currentModelNames}
				deliverSelected={(selected: string) => {
					setSelectedModel(selected);
				}}
				selected={selectedModel}
				label="Test model"
			/>
			<Button onClick={() => dispatcher({ type: "test model" })}>
				Test model
			</Button>
		</Stack>
	);
}
