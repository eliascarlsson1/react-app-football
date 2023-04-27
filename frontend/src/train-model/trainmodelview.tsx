import React from "react";
import Multiselect from "../components/multiselect";
import SingleTextSlider from "../components/singletextslider";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Checkbox from "@mui/material/Checkbox";
import Tooltip from "@mui/material/Tooltip";
import FormControlLabel from "@mui/material/FormControlLabel";
import Button from "@mui/material/Button";
import { AppActionDispatcher } from "../appstatemanager";

export type TrainModelViewState = {
	historicalData: string[];
	x_parameters: string[];
	y_parameters: string[];
};

export type TrainModelAction = {
	type: "train model";
	trainingData: string[];
	testData: string[];
	evaluateSplit: boolean;
	xParameters: string[];
	yParameters: string[];
	learningRate: number;
	maxDepth: number;
	numberEstimators: number;
};

let trainingData: string[] = [];
let testData: string[] = [];
let evaluateSplit = true;
let xParameters: string[] = [];
let yParameters: string[] = [];
let learningRate = 0.3;
let maxDepth = 4;
let numberEstimators = 250;

export default function TrainModelView({
	state,
	dispatcher,
}: {
	state: TrainModelViewState;
	dispatcher: AppActionDispatcher;
}) {
	//FIXME: Find out if that checkbox is checked

	return (
		<Stack direction={"row"}>
			<Stack>
				<Stack paddingLeft={1}>
					<Typography variant="h5" gutterBottom>
						Data
					</Typography>
				</Stack>
				<Multiselect
					dataArray={state.historicalData}
					label="Training data"
					deliverSelected={(selectedData) => {
						trainingData = selectedData;
					}}
				/>
				<Stack direction={"row"}>
					<Multiselect
						dataArray={state.historicalData}
						deliverSelected={(selectedData) => {
							testData = selectedData;
						}}
						label="Test data"
						width={220}
					/>
					<Tooltip title="Evaluate test data one by one">
						<FormControlLabel
							control={
								<Checkbox
									defaultChecked
									onChange={(e) => {
										evaluateSplit = e.target.checked;
									}}
								/>
							}
							label="Split"
						/>
					</Tooltip>
				</Stack>
			</Stack>
			<Stack>
				<Stack paddingLeft={1}>
					<Typography variant="h5" gutterBottom>
						Parameters
					</Typography>
				</Stack>
				<Multiselect
					dataArray={state.x_parameters}
					deliverSelected={(selectedData) => {
						xParameters = selectedData;
					}}
					label="x-parameters"
					selected={state.x_parameters}
				/>
				<Multiselect
					dataArray={state.y_parameters}
					deliverSelected={(selectedData) => {
						yParameters = selectedData;
					}}
					label="y-parameters"
					selected={state.y_parameters}
				/>
				<SingleTextSlider
					min={0}
					max={500}
					step={1}
					starting={numberEstimators}
					deliverValue={(value) => {
						numberEstimators = value;
					}}
					label="Number of estimatros"
				/>
				<SingleTextSlider
					min={0}
					max={1}
					step={0.01}
					starting={learningRate}
					deliverValue={(value) => {
						learningRate = value;
					}}
					label="Learning rate"
				/>
				<SingleTextSlider
					min={0}
					max={10}
					step={1}
					starting={maxDepth}
					deliverValue={(value) => {
						maxDepth = value;
					}}
					label="Max depth"
				/>
				<Button
					variant="contained"
					onClick={() => dispatcher(getTrainModelAction())}
				>
					Train model
				</Button>
			</Stack>
		</Stack>
	);
}

function getTrainModelAction(): TrainModelAction {
	return {
		type: "train model",
		trainingData,
		testData,
		evaluateSplit,
		xParameters,
		yParameters,
		learningRate,
		maxDepth,
		numberEstimators,
	};
}
