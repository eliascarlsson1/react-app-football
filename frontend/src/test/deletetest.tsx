import React, { useState } from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import CancelIcon from "@mui/icons-material/Cancel";
import SingleSelect from "../components/singleselect";

import { AppActionDispatcher } from "../appstatemanager";

export type DeleteTestAction = {
	type: "delete test";
	name: string;
};
export type DeleteTestState = {
	currentTests: string[];
};

export default function DeleteTest({
	state,
	dispatcher,
}: {
	state: DeleteTestState;
	dispatcher: AppActionDispatcher;
}) {
	const [selectedTest, setSelectedTest] = useState<string>(
		state.currentTests[0],
	);
	const [confirmDelete, setConfirmDelete] = useState<boolean>(false);
	if (
		!state.currentTests.includes(selectedTest) &&
		state.currentTests.length !== 0
	) {
		setSelectedTest(state.currentTests[0] ?? "");
	}

	return (
		<Stack padding={3}>
			<Stack direction={"row"} gap={2}>
				<SingleSelect
					dataArray={state.currentTests}
					deliverSelected={(selected: string) => {
						setSelectedTest(selected);
					}}
					selected={selectedTest}
					label="Delete test"
					width={150}
				/>

				{confirmDelete ? (
					<Stack direction={"row"}>
						<IconButton
							aria-label="delete"
							onClick={() => {
								dispatcher({ type: "delete test", name: selectedTest });
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
