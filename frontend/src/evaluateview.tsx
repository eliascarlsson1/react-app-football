import React from "react";

export type EvaluateViewState = { ROI: number };
export type AddROIEvent = { type: "addROIEvent" };

export default function Evaluateview({
	state,
	dispatcher,
}: {
	state: EvaluateViewState;
	dispatcher: (action: AddROIEvent) => void;
}) {
	return (
		<div>
			{state.ROI}{" "}
			<button onClick={() => dispatcher({ type: "addROIEvent" })} type="button">
				Add to ROI
			</button>
		</div>
	);
}
