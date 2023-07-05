import React from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { AppActionDispatcher } from "../appstatemanager";
import { PipelineInformation } from "./pipelineview";

export default function PipelineRow({
	pipeline,
	dispatcher,
}: {
	pipeline: PipelineInformation;
	dispatcher: AppActionDispatcher;
}) {
	return (
		<div>
			<Stack direction={"row"}>
				<span>
					{pipeline.name}
					{pipeline.leagues}
				</span>
				<Button
					variant="contained"
					style={{ width: "200px" }}
					onClick={() => {
						dispatcher({
							type: "delete pipeline",
							name: pipeline.name,
						});
					}}
				>
					Delete me
				</Button>
			</Stack>
		</div>
	);
}
