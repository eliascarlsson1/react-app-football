import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { AppActionDispatcher } from "../appstatemanager";
import MultiSelect from "../components/multiselect";
import DoubleTextSlider from "../components/doubletextslider";

export type FilterData = {
	odds: number[];
	confidenceOverOdds: number[];
	probability: number[];
	outcome: string[];
	testName: string;
};

export type SaveTestStatus = "idle" | "success" | "error" | "saving test";

export type SaveTestAction = {
	type: "save test";
	filterData: FilterData;
};

export type CreateTestState = {
	saveTestStatus: SaveTestStatus;
};

export default function CreateTest({
	state,
	dispatcher,
}: {
	state: CreateTestState;
	dispatcher: AppActionDispatcher;
}) {
	const [oddsFilter, setOddsFilter] = useState<number[]>([1.5, 2.5]);
	const [confidenceOverOdds, setConfidenceOverOdds] = useState<number[]>([
		0, 0.5,
	]);
	const [probability, setProbability] = useState<number[]>([50, 100]);
	const [outcome, setOutcome] = useState<string[]>(["0", "1"]);
	const [testName, setTestName] = useState<string>("");

	return (
		<Stack
			direction={"column"}
			sx={{
				border: "1px solid gray",
				borderColor: "gray.300",
				width: "650px",
			}}
			padding={3}
			gap={2}
		>
			<Typography variant="h5" gutterBottom>
				Create test
			</Typography>
			<DoubleTextSlider
				min={1}
				max={5}
				step={0.05}
				starting={oddsFilter}
				deliverValue={(value) => {
					setOddsFilter(value);
				}}
				label="Odds"
				width={300}
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
				width={300}
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
				width={300}
			/>
			<MultiSelect
				dataArray={["0", "1"]}
				deliverSelected={(outcome) => {
					setOutcome(outcome);
				}}
				selected={outcome}
				label={"Bet on outcome"}
			/>
			<Stack justifyContent={"center"}>
				<Stack direction={"row"} gap={1}>
					<TextField
						label="Test name"
						variant="outlined"
						onChange={(e) => {
							setTestName(e.target.value);
						}}
						style={{ width: 160 }}
					/>
					<Button
						variant="contained"
						onClick={() => {
							dispatcher({
								type: "save test",
								filterData: {
									odds: oddsFilter,
									confidenceOverOdds: confidenceOverOdds,
									probability: probability,
									outcome: outcome,
									testName: testName,
								},
							});
						}}
					>
						Save test
					</Button>
				</Stack>
				<Typography
					align="center"
					fontSize={15}
					paddingTop={0.5}
					paddingBottom={1}
					color={getColorFromSaveModelServerState(state.saveTestStatus)}
					width={300}
				>
					{state.saveTestStatus}
				</Typography>
			</Stack>
		</Stack>
	);
}

function getColorFromSaveModelServerState(state: SaveTestStatus): string {
	switch (state) {
		case "idle":
			return "white";
		case "saving test":
			return "blue";
		case "success":
			return "green";
		case "error":
			return "red";
	}
}
