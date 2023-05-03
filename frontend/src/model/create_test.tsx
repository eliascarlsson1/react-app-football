import React, { useState } from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { Typography } from "@mui/material";
import SingleSelect from "../components/singleselect";
import { AppActionDispatcher, ModelInformation } from "../appstatemanager";
import MultiSelect from "../components/multiselect";
import DoubleTextSlider from "../components/doubletextslider";

export type FilterData = {
	odds: number[];
	confidenceOverOdds: number[];
	probability: number[];
	outcome: string[];
};

export default function CreateTest() {
	const [oddsFilter, setOddsFilter] = useState<number[]>([1.5, 2.5]);
	const [confidenceOverOdds, setConfidenceOverOdds] = useState<number[]>([
		0, 0.5,
	]);
	const [probability, setProbability] = useState<number[]>([50, 100]);
	const [outcome, setOutcome] = useState<string[]>(["0", "1"]);

	return (
		<Stack direction={"column"}>
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
