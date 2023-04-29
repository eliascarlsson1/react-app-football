import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { AppActionDispatcher } from "../appstatemanager";

export type SaveModelAction = { type: "save model"; name: string };
export type SaveModelStatus = "idle" | "saving model" | "success" | "error";
export type SaveModelState = { saveModelServerState: SaveModelStatus };

export default function Savemodel({
	state,
	dispatcher,
}: {
	state: SaveModelState;
	dispatcher: AppActionDispatcher;
}) {
	const [modelName, setModelName] = useState<string>("");
	return (
		<Stack justifyContent={"center"}>
			<Stack direction={"row"} gap={1}>
				<TextField
					label="Model name"
					variant="outlined"
					onChange={(e) => {
						setModelName(e.target.value);
					}}
				/>
				<Button
					onClick={() => dispatcher({ type: "save model", name: modelName })}
					variant="contained"
					disabled={modelName === ""}
				>
					Save model
				</Button>
			</Stack>
			<Typography
				align="center"
				fontSize={15}
				paddingTop={0.5}
				paddingBottom={1}
				color={getColorFromSaveModelServerState(state.saveModelServerState)}
				width={200}
			>
				{state.saveModelServerState}
			</Typography>
		</Stack>
	);
}

function getColorFromSaveModelServerState(state: SaveModelStatus): string {
	switch (state) {
		case "idle":
			return "white";
		case "saving model":
			return "blue";
		case "success":
			return "green";
		case "error":
			return "red";
	}
}
