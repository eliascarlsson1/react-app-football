import React from "react";
import Multiselect from "../components/multiselect";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

export type TrainModelViewState = {
	historicalData: string[];
	x_parameters: string[];
	y_parameters: string[];
};

let trainingData = [];
let testData = [];
let x_parameters = [];
let y_parameters = [];

export default function TrainModelView({
	state,
}: {
	state: TrainModelViewState;
}) {
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
				<Multiselect
					dataArray={state.historicalData}
					deliverSelected={(selectedData) => {
						testData = selectedData;
					}}
					label="Test data"
				/>
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
						x_parameters = selectedData;
					}}
					label="x-parameters"
					selected={state.x_parameters}
				/>
				<Multiselect
					dataArray={state.y_parameters}
					deliverSelected={(selectedData) => {
						y_parameters = selectedData;
					}}
					label="y-parameters"
					selected={state.y_parameters}
				/>
			</Stack>
		</Stack>
	);
}
