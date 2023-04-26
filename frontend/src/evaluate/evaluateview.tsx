import React from "react";

export type EvaluateViewState = { ROI: number };
export type AddROIAction = { type: "AddROIAction" };

export default function Evaluateview({
	state,
	dispatcher,
}: {
	state: EvaluateViewState;
	dispatcher: (action: AddROIAction) => void;
}) {
	return (
		<div>
			{state.ROI}{" "}
			<button
				onClick={() => dispatcher({ type: "AddROIAction" })}
				type="button"
			>
				Add to ROI
			</button>
		</div>
	);
}
