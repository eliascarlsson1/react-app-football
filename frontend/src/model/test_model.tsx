import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import SingleSelect from "../components/singleselect";
import { AppActionDispatcher, ModelInformation } from "../appstatemanager";
import MultiSelect from "../components/multiselect";
import DoubleTextSlider from "../components/doubletextslider";

export type TestData = { ROI: { id: string; roi: string }[] } | null;

export type TestModelAction = {
	type: "test model";
	modelName: string;
	testData: string[];
	filterData: FilterData;
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
	//FIXME: Get filter data from create_test component
	const [selectedModel, setSelectedModel] = useState<string>(
		state.currentModels[0].name,
	);
	const [oddsFilter, setOddsFilter] = useState<number[]>([1.5, 2.5]);
	const [confidenceOverOdds, setConfidenceOverOdds] = useState<number[]>([
		0, 0.5,
	]);
	const [probability, setProbability] = useState<number[]>([50, 100]);
	// FIXME: Dependant on yparam
	const [outcome, setOutcome] = useState<string[]>(["0", "1"]);

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
						testData: selectedDataToTest,
						filterData: {
							odds: oddsFilter,
							confidenceOverOdds: confidenceOverOdds,
							probability: probability,
							outcome: outcome,
						},
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
			<MultiSelect
				dataArray={dataToTest}
				deliverSelected={(selected: string[]) => {
					setSelectedDataToTest(selected);
				}}
				selected={selectedDataToTest}
				label="Data to test"
			/>
			<DoubleTextSlider
				min={1}
				max={5}
				step={0.05}
				starting={oddsFilter}
				deliverValue={(value) => {
					setOddsFilter(value);
				}}
				label="Odds"
			/>
			<DoubleTextSlider
				min={-0.5}
				max={0.5}
				step={0.01}
				starting={confidenceOverOdds}
				deliverValue={(value) => {
					setConfidenceOverOdds(value);
				}}
				label="Confidence over odds"
			/>
			<DoubleTextSlider
				min={0}
				max={100}
				step={1}
				starting={probability}
				deliverValue={(value) => {
					setProbability(value);
				}}
				label="Calculated probability"
			/>
			<MultiSelect
				dataArray={["0", "1"]}
				deliverSelected={(outcome) => {
					setOutcome(outcome);
				}}
				selected={outcome}
				label={"Bet on outcome"}
			/>
		</Stack>
	);
}
