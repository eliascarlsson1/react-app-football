import React, { useState } from "react";
import Multiselect from "../components/multiselect";
import SingleTextSlider from "../components/singletextslider";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { AppActionDispatcher } from "../appstatemanager";
import SingleSelect from "../components/singleselect";
import SaveModel from "./savemodel";
import { AppStateManager } from "../appstatemanager";
import MultiSelect from "../components/multiselect";
import DeleteModel from "../model/deletemodel";

export type TrainModelStatus = "idle" | "training" | "success" | "error";

export type TrainModelViewState = {
	historicalData: string[];
	xParameters: string[];
	yParameters: string[];
	trainModelStatus: "idle" | "training" | "success" | "error";
	trainModelRoi: { id: string; roi: string }[];
};

export type TrainModelAction = {
	type: "train model";
	trainingData: string[];
	xParameters: string[];
	yParameter: string;
	learningRate: number;
	maxDepth: number;
	numberEstimators: number;
	testData: string[];
};

export default function TrainModelView({
	state,
	dispatcher,
	appStateManager,
}: {
	state: TrainModelViewState;
	dispatcher: AppActionDispatcher;
	appStateManager: AppStateManager;
}) {
	const [trainingData, setTrainingData] = useState<string[]>([]);
	const [xParameters, setXParameters] = useState<string[]>(state.xParameters);
	const [yParameter, setYParameters] = useState<string>(state.yParameters[0]);
	const [learningRate, setLearningRate] = useState<number>(0.3);
	const [maxDepth, setMaxDepth] = useState<number>(4);
	const [numberEstimators, setNumberEstimators] = useState<number>(250);

	// historical data not in training data
	const testDataArray = state.historicalData.filter(
		(data) => !trainingData.includes(data),
	);

	const [testData, setTestData] = useState<string[]>([]);

	return (
		<Stack
			sx={{
				border: "1px solid gray",
				borderColor: "gray.300",
				width: "650px",
			}}
			padding={3}
		>
			<Stack direction={"row"} gap={17} paddingLeft={1} alignItems={"start"}>
				<Typography variant="h5" gutterBottom>
					Train model with XGBoost
				</Typography>
				<MultiSelect
					dataArray={testDataArray}
					deliverSelected={(selectedData) => {
						setTestData(selectedData);
					}}
					label="Test data"
				/>

				{state.trainModelRoi.map((roi) => {
					return (
						<Typography>
							{roi.id} {roi.roi}
						</Typography>
					);
				})}
				<Stack>
					<Button
						variant="contained"
						style={{ width: "200px" }}
						onClick={() =>
							dispatcher({
								type: "train model",
								trainingData,
								xParameters,
								yParameter,
								learningRate,
								maxDepth,
								numberEstimators,
								testData,
							})
						}
						disabled={state.trainModelStatus === "training"}
					>
						Train model
					</Button>
					<Typography
						align="center"
						fontSize={15}
						paddingTop={0.5}
						paddingBottom={1}
						color={getColorFromTrainModelViewState(state.trainModelStatus)}
						width={200}
					>
						{state.trainModelStatus}
					</Typography>
				</Stack>
			</Stack>
			<Stack direction={"row"} gap={3}>
				<Stack>
					<Stack gap={2}>
						<Multiselect
							dataArray={state.historicalData}
							label="Training data"
							deliverSelected={(selectedData) => {
								setTrainingData(selectedData);
							}}
						/>
						<SingleSelect
							dataArray={state.yParameters}
							deliverSelected={(selectedData) => {
								setYParameters(selectedData);
							}}
							selected={yParameter}
							label="y-parameter"
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
					</Stack>
				</Stack>
				<Stack>
					<Multiselect
						dataArray={state.xParameters}
						deliverSelected={(selectedData) => {
							setXParameters(selectedData);
						}}
						label="x-parameters"
						selected={xParameters}
					/>
				</Stack>
			</Stack>
			<Stack paddingTop={5} alignItems={"center"}>
				<SaveModel
					state={appStateManager.getComponentState().getSaveModelState()}
					dispatcher={dispatcher}
				/>
			</Stack>
			<DeleteModel
				state={appStateManager.getComponentState().getDeleteModelState()}
				dispatcher={dispatcher}
			/>
		</Stack>
	);
}

function getColorFromTrainModelViewState(
	trainModelStatus: TrainModelStatus,
): string {
	switch (trainModelStatus) {
		case "idle":
			return "white";
		case "training":
			return "blue";
		case "success":
			return "green";
		case "error":
			return "red";
	}
}
