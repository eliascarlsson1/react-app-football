import React from "react";
import Button from "@mui/material/Button";
import { AppActionDispatcher } from "../appstatemanager";

export type SettingsViewAction = { type: "prepare data" };

export default function Settingsview({
	dipsatcher,
}: {
	dipsatcher: AppActionDispatcher;
}) {
	return (
		<div>
			<Button
				onClick={() => dipsatcher({ type: "prepare data" })}
				variant="contained"
			>
				Prepare data
			</Button>
		</div>
	);
}
