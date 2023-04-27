import React from "react";
import Multiselect from "../components/multiselect";
import SingleTextSlider from "../components/singletextslider";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Checkbox from "@mui/material/Checkbox";
import Tooltip from "@mui/material/Tooltip";
import FormControlLabel from "@mui/material/FormControlLabel";

export type TrainModelViewState = {
	historicalData: string[];
	x_parameters: string[];
	y_parameters: string[];
};

let trainingData = [];
let testData = [];
let evaluateSplit = true;
let x_parameters = [];
let y_parameters = [];
let learningRate = 0;

export default function TrainModelView({
	state,
}: {
	state: TrainModelViewState;
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
				<SingleTextSlider
					min={0}
					max={1}
					step={0.01}
					deliverValue={(value) => {
						learningRate = value;
					}}
					label="Learning rate"
				/>
			</Stack>
		</Stack>
	);
}
