import React from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import DeleteIcon from "@mui/icons-material/Delete";
import CancelIcon from "@mui/icons-material/Cancel";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { AppActionDispatcher } from "../appstatemanager";
import { PipelineInformation } from "./pipelineview";

export default function PipelineRow({
	pipeline,
	dispatcher,
}: {
	pipeline: PipelineInformation;
	dispatcher: AppActionDispatcher;
}) {
	const [confirmDelete, setConfirmDelete] = React.useState<boolean>(false);

	return (
		<div>
			<Stack direction={"row"} padding={1} alignItems={"center"} gap={1}>
				<Typography fontSize={14} gutterBottom>
					{pipeline.name} (model: {pipeline.model}, test: {pipeline.test},
					leagues:{pipeline.leagues.join(", ")})
				</Typography>
				{confirmDelete ? (
					<Stack direction={"row"}>
						<IconButton
							aria-label="delete"
							onClick={() => {
								dispatcher({
									type: "delete pipeline",
									name: pipeline.name,
								});
								setConfirmDelete(false);
							}}
						>
							<DeleteIcon />
						</IconButton>
						<IconButton
							aria-label="delete"
							onClick={() => setConfirmDelete(false)}
						>
							<CancelIcon />
						</IconButton>
					</Stack>
				) : (
					<Button onClick={() => setConfirmDelete(true)} variant="contained">
						Delete
					</Button>
				)}
				<IconButton
					onClick={() =>
						dispatcher({ type: "apply pipeline", name: pipeline.name })
					}
				>
					<PlayArrowIcon />
				</IconButton>
			</Stack>
		</div>
	);
}
