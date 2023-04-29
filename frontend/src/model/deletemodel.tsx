import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import CancelIcon from "@mui/icons-material/Cancel";
import SingleSelect from "../components/singleselect";

import { AppActionDispatcher } from "../appstatemanager";

export type DeleteModelAction = {
	type: "delete model";
	name: string;
};
export type DeleteModelState = {
	currentModels: string[];
};

export default function DeleteModel({
	state,
	dispatcher,
}: {
	state: DeleteModelState;
	dispatcher: AppActionDispatcher;
}) {
	const [selectedModel, setSelectedModel] = useState<string>(
		state.currentModels[0],
	);
	const [confirmDelete, setConfirmDelete] = useState<boolean>(false);
	if (
		!state.currentModels.includes(selectedModel) &&
		state.currentModels.length !== 0
	) {
		setSelectedModel(state.currentModels[0] ?? "");
	}

	return (
		<Stack padding={3}>
			
				<Stack direction={"row"} gap={2}>
					<SingleSelect
						dataArray={state.currentModels}
						deliverSelected={(selected: string) => {
							setSelectedModel(selected);
						}}
						selected={selectedModel}
						label="Delete model"
						width={150}
					/>

					{confirmDelete ? (
						<Stack direction={"row"}>
							<IconButton
								aria-label="delete"
								onClick={() => {
									dispatcher({ type: "delete model", name: selectedModel });
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
						<Button onClick={() => setConfirmDelete(true)}> Delete</Button>
					)}
				</Stack>
			
		</Stack>
	);
}
