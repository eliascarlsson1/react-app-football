import React from "react";
import { Stack } from "@mui/material";
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
};

export default function BetInformationView({
	state,
}: {
	state: GameBetInformation;
}) {
	return (
		<Stack direction={"column"} gap={1}>
			<h3>Hello From Game Bet Information</h3>
			<DisplayTestData state={state.testDataForLeague}/>
		</Stack>
	);
}