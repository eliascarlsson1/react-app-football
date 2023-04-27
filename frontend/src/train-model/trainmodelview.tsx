import React, { useRef, useState } from "react";
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
	xParameters: string[];
	yParameters: string[];
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

export default function TrainModelView({
	state,
	dispatcher,
}: {
	state: TrainModelViewState;
	dispatcher: AppActionDispatcher;
}) {
	//FIXME: Y parameters should be single select

	const [trainingData, setTrainingData] = useState<string[]>([]);
	const [testData, setTestData] = useState<string[]>([]);
	const [evaluateSplit, setEvaluateSplit] = useState<boolean>(true);
	const [xParameters, setXParameters] = useState<string[]>(state.xParameters);
	const [yParameters, setYParameters] = useState<string[]>(state.yParameters);
	const [learningRate, setLearningRate] = useState<number>(0.3);
	const [maxDepth, setMaxDepth] = useState<number>(4);
	const [numberEstimators, setNumberEstimators] = useState<number>(250);

	const availableTrainingData = state.historicalData.filter(
		(data) => !testData.includes(data),
	);
	const availableTestData = state.historicalData.filter(
		(data) => !trainingData.includes(data),
	);

	return (
		<Stack direction={"row"}>
			<Stack>
				<Stack paddingLeft={1}>
					<Typography variant="h5" gutterBottom>
						Data
					</Typography>
				</Stack>
				<Multiselect
					dataArray={availableTrainingData}
					label="Training data"
					deliverSelected={(selectedData) => {
						setTrainingData(selectedData);
					}}
				/>
				<Stack direction={"row"}>
					<Multiselect
						dataArray={availableTestData}
						deliverSelected={(selectedData) => {
							setTestData(selectedData);
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
										setEvaluateSplit(e.target.checked);
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
					dataArray={state.xParameters}
					deliverSelected={(selectedData) => {
						setXParameters(selectedData);
					}}
					label="x-parameters"
					selected={xParameters}
				/>
				<Multiselect
					dataArray={state.yParameters}
					deliverSelected={(selectedData) => {
						setYParameters(selectedData);
					}}
					label="y-parameters"
					selected={yParameters}
				/>
				<SingleTextSlider
					min={0}
					max={500}
					step={1}
					starting={numberEstimators}
					deliverValue={(value) => {
						setNumberEstimators(value);
					}}
					label="Number of estimators"
				/>
				<SingleTextSlider
					min={0}
					max={1}
					step={0.01}
					starting={learningRate}
					deliverValue={(value) => {
						setLearningRate(value);
					}}
					label="Learning rate"
				/>
				<SingleTextSlider
					min={0}
					max={10}
					step={1}
					starting={maxDepth}
					deliverValue={(value) => {
						setMaxDepth(value);
					}}
					label="Max depth"
				/>
				<Button
					variant="contained"
					onClick={() =>
						dispatcher({
							type: "train model",
							trainingData,
							testData,
							evaluateSplit,
							xParameters,
							yParameters,
							learningRate,
							maxDepth,
							numberEstimators,
						})
					}
				>
					Train model
				</Button>
			</Stack>
		</Stack>
	);
}
