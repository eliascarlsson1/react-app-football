import React, { useRef, useState } from "react";
import Multiselect from "../components/multiselect";
import SingleTextSlider from "../components/singletextslider";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { AppActionDispatcher } from "../appstatemanager";
import SingleSelect from "../components/singleselect";

export type TrainModelStatus = "idle" | "training" | "success" | "error";

export type TrainModelViewState = {
	historicalData: string[];
	xParameters: string[];
	yParameters: string[];
	trainModelStatus: "idle" | "training" | "success" | "error";
};

export type TrainModelAction = {
	type: "train model";
	trainingData: string[];
	xParameters: string[];
	yParameter: string;
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
	const [xParameters, setXParameters] = useState<string[]>(state.xParameters);
	const [yParameter, setYParameters] = useState<string>(state.yParameters[0]);
	const [learningRate, setLearningRate] = useState<number>(0.3);
	const [maxDepth, setMaxDepth] = useState<number>(4);
	const [numberEstimators, setNumberEstimators] = useState<number>(250);

	return (
		<Stack
			sx={{
				border: "1px solid gray",
				borderColor: "gray.300",
				width: "650px",
			}}
			padding={3}
		>
			<Stack direction={"row"} gap={20} paddingLeft={1} alignItems={"start"}>
				<Typography variant="h5" gutterBottom>
					Train model with XGBoost
				</Typography>
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
