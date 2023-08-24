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
	ROI: Map<string, string>;
	accuracy: string[];
	permutationImportanceTestSrc: string | null;
	permutationImportanceTrainSrc: string | null;
	permutationImportanceValSrc: string | null;
	featureImportanceSrc: string | null;
	confidenceBarplotSrc: string | null;
	showModelStatsViewOpen: "closed" | "open" | "loading";
	allModelInformation: ModelInformation[] | null;
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
	const selectedModelInformation =
		state.allModelInformation?.find((model) => model.name === selectedModel) ??
		null;

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
				<Dialog
					open={state.showModelStatsViewOpen === "open"}
					fullWidth={true}
					maxWidth={"lg"}
				>
					<Stack overflow={"hidden"}>
						<Stack
							padding={2}
							direction={"row"}
							flex={"grow"}
							borderBottom={1}
							borderColor={"gray"}
							justifyContent={"space-between"}
						>
							<Stack direction={"row"}>
								<Typography variant={"h5"}>
									Model statistics for model: "{selectedModel}"
								</Typography>
							</Stack>
							<Stack direction={"row"}>
								<Button
									onClick={() => {
										dispatcher({ type: "close show model stats" });
									}}
								>
									Close modal
								</Button>
							</Stack>
						</Stack>
						<Stack style={{ overflowY: "auto", overflowX: "hidden" }}>
							<Stack padding={1}>
								<Typography fontWeight={"bold"}>
									Selected training data:
								</Typography>
								<Typography>{selectedData.join(", ")}</Typography>
							</Stack>
							<Stack padding={1}>
								<Typography fontWeight={"bold"}>
									Model parameters (WIP):
								</Typography>
								{selectedModelInformation !== null ? (
									<Stack>
										<Typography>
											{selectedModelInformation.learningRate}
										</Typography>
										<Typography>{selectedModelInformation.maxDepth}</Typography>
										<Typography>{selectedModelInformation.name}</Typography>
										<Typography>
											{selectedModelInformation.numberEstimators}
										</Typography>
										<Typography>
											{selectedModelInformation.trainingData.join(", ")}
										</Typography>
										<Typography>
											{selectedModelInformation.xParameters.join(", ")}
										</Typography>
										<Typography>
											{selectedModelInformation.yParameter}
										</Typography>
									</Stack>
								) : (
									""
								)}
							</Stack>
							<Stack padding={1}>
								<Typography fontWeight={"bold"}>ROI:</Typography>
								<Typography>{JSON.stringify(state.ROI)}</Typography>
							</Stack>
							<Stack padding={1}>
								<Typography fontWeight={"bold"}>Accuracy:</Typography>
								{state.accuracy.map((acc) => {
									return <Typography>{acc}</Typography>;
								})}
							</Stack>
							<Stack padding={1} maxWidth={"50%"}>
								<Typography fontWeight={"bold"}>Confidence plot:</Typography>
								{state.confidenceBarplotSrc && (
									<img
										src={`http://localhost:5000${state.confidenceBarplotSrc}`}
										alt="Image"
									/>
								)}
							</Stack>
							<Stack padding={1} maxWidth={"50%"}>
								<Typography fontWeight={"bold"}>
									Feature importance plots:
								</Typography>
								{state.featureImportanceSrc && (
									<img
										src={`http://localhost:5000${state.featureImportanceSrc}`}
										alt="Image"
									/>
								)}
							</Stack>
							<Stack padding={1}>
								<Typography fontWeight={"bold"}>
									Permutation importance plots:
								</Typography>
								<Stack maxWidth={"50%"}>
									{state.permutationImportanceTrainSrc && (
										<img
											src={`http://localhost:5000${state.permutationImportanceTestSrc}`}
											alt="Image"
										/>
									)}
									{state.permutationImportanceTestSrc && (
										<img
											src={`http://localhost:5000${state.permutationImportanceTrainSrc}`}
											alt="Image"
										/>
									)}
									{state.permutationImportanceValSrc && (
										<img
											src={`http://localhost:5000${state.permutationImportanceValSrc}`}
											alt="Image"
										/>
									)}
								</Stack>
							</Stack>
						</Stack>
					</Stack>
				</Dialog>
			) : (
				""
			)}
		</Stack>
	);
}
