import React from "react";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { AppActionDispatcher } from "../appstatemanager";

export type SettingsViewAction =
	| { type: "prepare data" }
	| { type: "download data" };

export default function Settingsview({
	dipsatcher,
}: {
	dipsatcher: AppActionDispatcher;
}) {
	return (
		<Stack direction={"row"} gap={3}>
			<Button
				onClick={() => dipsatcher({ type: "prepare data" })}
				variant="contained"
			>
				Prepare data
			</Button>
			<Button
				onClick={() => dipsatcher({ type: "download data" })}
				variant="contained"
			>
				Download data
			</Button>
		</Stack>
	);
}
