import React from "react";
import Multiselect from "../components/multiselect";

export type TrainModelViewState = { historicalData: string[] };

export default function TrainModelView({
	state,
}: {
	state: TrainModelViewState;
}) {
	return (
		<div>
			<Multiselect
				dataArray={state.historicalData}
				label="Training data"
				deliverSelected={(selectedData) => {
					console.log(selectedData);
				}}
			/>
		</div>
	);
}
