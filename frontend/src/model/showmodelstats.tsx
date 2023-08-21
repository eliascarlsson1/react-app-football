import React, { useState } from "react";
import DisplayTestData from "../components/displaytestdata";
import Stack from "@mui/material/Stack";
import { ModelInformation } from "../appstatemanager";
import { Dialog } from "@mui/material";
import { Pagination } from "@mui/material";
import SingleSelect from "../components/singleselect";
import MultiSelect from "../components/multiselect";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

export type ShowModelStatsViewState = {
	currentModels: ModelInformation[];
	historicalData: string[];
	ROI: { id: string; roi: string }[];
	accuracy: string[];
	permutationImportanceTestSrc: string | null;
	permutationImportanceTrainSrc: string | null;
	permutationImportanceValSrc: string | null;
	featureImportanceSrc: string | null;
	confidenceBarplotSrc: string | null;
	showModelStatsViewOpen: "closed" | "open" | "loading";
};

export type ShowModelStatsAction =
	| {
			type: "show model stats";
			modelName: string;
			testData: string[];
	  }
	| { type: "close show model stats" };

export default function ShowModelStats({
	state,
	dispatcher,
}: {
	state: ShowModelStatsViewState;
	dispatcher: any;
}) {
	const [selectedModel, setSelectedModel] = useState<string>(
		state.currentModels[0].name,
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
	const [selectedData, setSelectedData] = useState<string[]>([]);

	return (
		<Stack direction={"row"}>
			<SingleSelect
				dataArray={currentModelNames}
				label={"Select model"}
				deliverSelected={(selected) => {
					setSelectedModel(selected);
				}}
				selected={selectedModel}
			/>
			<MultiSelect
				label={"Select data to test"}
				dataArray={dataToTest}
				deliverSelected={(selected) => {
					setSelectedData(selected);
				}}
			/>
			<Button
				disabled={
					state.showModelStatsViewOpen === "loading" ||
					selectedData.length === 0
				}
				onClick={() => {
					dispatcher({
						type: "show model stats",
						modelName: selectedModel,
						testData: selectedData,
					});
				}}
			>
				Show model stats
			</Button>
			{state.showModelStatsViewOpen === "loading" ? (
				<Typography>Loading...</Typography>
			) : (
				""
			)}
			{state.showModelStatsViewOpen === "open" ? (
				<Dialog open={state.showModelStatsViewOpen === "open"}>
					<Stack>
						{state.ROI.map((roi) => {
							return (
								<Typography>
									{roi.id} {roi.roi}
								</Typography>
							);
						})}
						{state.accuracy.map((acc) => {
							return <Typography>{acc}</Typography>;
						})}
						<div className="App">
							{state.permutationImportanceTestSrc && (
								<img src={state.permutationImportanceTestSrc} alt="Image" />
							)}
							{state.featureImportanceSrc && (
								<img src={state.featureImportanceSrc} alt="Image" />
							)}
							{state.confidenceBarplotSrc && (
								<img src={state.confidenceBarplotSrc} alt="Image" />
							)}
						</div>
						<Button
							onClick={() => {
								dispatcher({ type: "close show model stats" });
							}}
						>
							Close
						</Button>
					</Stack>
				</Dialog>
			) : (
				""
			)}
		</Stack>
	);
}
