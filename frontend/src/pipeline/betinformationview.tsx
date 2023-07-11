import React from "react";
import { Stack } from "@mui/material";
import { Typography } from "@mui/material";
import { Link } from "@mui/material";
import type { ModelInformation } from "../appstatemanager";
import type { TestData } from "../model/test_model";
import DisplayTestData from "../components/displaytestdata";

// This is per game and not per pipeline, more scalable...

export type Odds =
	| {
			type: "over/under";
			goals: number;
			odds: Map<string, { oddsOver: number; oddsUnder: number }>;
			best_bookmaker: string;
	  }
	| {
			type: "1x2";
			odds: Map<
				string,
				{ oddsHomeTeam: number; oddsAwayTeam: number; oddsDraw: number }
			>;
	  };

// FIXME: Some infromation about prediction probability, and a curve over probability for this model...
export type GameBetInformation = {
	homeTeam: string;
	awayTeam: string;
	date: string;
	pipelineName: string;
	prediction: string;
	oddsPrediction: string;
	model: ModelInformation;
	test: string; // FIXME: Test information later
	testDataForScrape: TestData;
	testDataForLeague: TestData;
	odds: Odds;
	oddsportalLink: string;
	timeOfScrape: string;
	//FIXME: Time of scrape broken?
};

export default function BetInformationView({
	state,
}: {
	state: GameBetInformation;
}) {
	const betType =
		state.model.yParameter === "OvUn25"
			? "Over under 2.5 goals"
			: "FIXME: Another bet";

	const prediction = state.prediction === "0" ? "Over" : "Under";

	return (
		<Stack direction={"column"} gap={1} padding={3} alignItems={"flex-start"}>
			<Stack direction={"row"} gap={1} alignItems={"center"}>
				<Typography>
					{state.homeTeam} vs {state.awayTeam} ({state.date})
				</Typography>
				<Link href={state.oddsportalLink}>(Oddsportal)</Link>
			</Stack>
			<Typography>
				{betType}. Prediction: {prediction} (odds:{" "}
				{Number(state.oddsPrediction).toPrecision(3)}). Scraped at{" "}
				{state.timeOfScrape}
			</Typography>
			<Typography>
				Pipeline: {state.pipelineName} (model: {state.model.name},test:{" "}
				{state.test}). Model trained on {state.model.trainingData.join(", ")}
			</Typography>
			<Stack direction={"column"}>
				<Typography>Stats for model and test on historical data:</Typography>
				<DisplayTestData state={state.testDataForLeague} />
			</Stack>
		</Stack>
	);
}
