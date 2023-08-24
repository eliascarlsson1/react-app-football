import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import SingleSelect from "../components/singleselect";
import DisplayTestData from "../components/displaytestdata";
import { AppActionDispatcher, ModelInformation } from "../appstatemanager";
import MultiSelect from "../components/multiselect";
import DoubleTextSlider from "../components/doubletextslider";

export type TestData = {
	id: string;
	roi: string;
	gamesBeforeFilter: number;
	gamesAfterFilter: number;
	zeroBeforeFilter: number;
	zeroAfterFilter: number;
	oneBeforeFilter: number;
	oneAfterFilter: number;
};

export type TestModelAction = {
	type: "test model";
	modelName: string;
	testName: string;
	testData: string[];
};
export type TestModelState = {
	currentModels: ModelInformation[];
	historicalData: string[];
	testResponse: TestData[] | null;
	currentTests: string[];
};

export default function Test_model({
	dispatcher,
	state,
}: {
	dispatcher: AppActionDispatcher;
	state: TestModelState;
}) {
	//FIXME: Get filter data from create_test component
	const [selectedModel, setSelectedModel] = useState<string>(
		state.currentModels[0].name,
	);
	const [selectedTest, setSelectedTest] = useState<string>(
		state.currentTests[0] ?? "",
	);
	const currentModelNames = state.currentModels.map((model) => model.name);

	if (
		!currentModelNames.includes(selectedModel) &&
		state.currentModels.length !== 0
	) {
		setSelectedModel(state.currentModels[0].name ?? "");
	}

	const currentModelSelected = state.currentModels.find(
		(model) => model.name === selectedModel,
	);

	const trainingData = currentModelSelected?.trainingData ?? [];

	const dataToTest = state.historicalData.filter(
		(data) => !trainingData.includes(data),
	);

	const [selectedDataToTest, setSelectedDataToTest] = useState<string[]>([]);

	return (
		<Stack
			direction={"column"}
			sx={{
				border: "1px solid gray",
				borderColor: "gray.300",
			}}
			padding={3}
			gap={2}
			alignItems={"flex-start"}
		>
			<Stack direction={"row"}>
				<Typography variant="h5" gutterBottom>
					Test model
				</Typography>
			</Stack>
			<SingleSelect
				dataArray={currentModelNames}
				deliverSelected={(selected: string) => {
					setSelectedModel(selected);
				}}
				selected={selectedModel}
				label="Select model"
			/>
			<SingleSelect
				dataArray={state.currentTests}
				deliverSelected={(selected: string) => {
					setSelectedTest(selected);
				}}
				selected={selectedTest ?? ""}
				label="Select test"
			/>
			<MultiSelect
				dataArray={dataToTest}
				deliverSelected={(selected: string[]) => {
					setSelectedDataToTest(selected);
				}}
				selected={selectedDataToTest}
				label="Data to test"
			/>
			<Button
				onClick={() =>
					dispatcher({
						type: "test model",
						modelName: selectedModel,
						testName: selectedTest,
						testData: selectedDataToTest,
					})
				}
				variant="contained"
				style={{ width: 250 }}
			>
				Test model
			</Button>
			<Stack direction={"column"} gap={1}>
				{state.testResponse !== null
					? state.testResponse.map((response) => (
							<DisplayTestData state={response} />
					  ))
					: "No test response"}
			</Stack>
		</Stack>
	);
}
