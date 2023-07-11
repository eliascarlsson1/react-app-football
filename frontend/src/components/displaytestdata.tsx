import React from "react";
import { Stack } from "@mui/material";
import { Typography } from "@mui/material";
import type { TestData } from "../model/test_model";

export default function DisplayTestData({ state }: { state: TestData }) {
	return (
		<Stack direction={"column"} padding={1} border={0.1} gap={0.5}>
			<Stack direction={"row"} gap={3}>
				<Typography>ID: {state.id}.</Typography>
				<Typography>ROI: {Number(state.roi).toPrecision(3)}.</Typography>
			</Stack>
				<Typography>
					Games before filter (0,1): {state.gamesBeforeFilter} (
					{state.zeroBeforeFilter},{state.oneBeforeFilter})
				</Typography>

				<Typography>
					Games after filter (0,1): {state.gamesAfterFilter} (
					{state.zeroAfterFilter},{state.oneAfterFilter})
				</Typography>
		</Stack>
	);
}
