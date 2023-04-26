import React from "react";

export type TabOption = "evaluate" | "pipeline" | "trainModel";
export type TabState = { tab: TabOption };
export type TabEvent = { type: "tabEvent"; tab: TabOption };

export default function Tabs({
	state,
	dispatcher,
}: {
	state: TabState;
	dispatcher: (action: TabEvent) => void;
}) {
	return (
		<div>
			<button
				type="button"
				onClick={() => dispatcher({ type: "tabEvent", tab: "evaluate" })}
			>
				Evaluate {state.tab === "evaluate" ? "Active" : ""}
			</button>
			<button
				type="button"
				onClick={() => dispatcher({ type: "tabEvent", tab: "pipeline" })}
			>
				Pipeline {state.tab === "pipeline" ? "Active" : ""}
			</button>
			<button
				type="button"
				onClick={() => dispatcher({ type: "tabEvent", tab: "trainModel" })}
			>
				Train model {state.tab === "trainModel" ? "Active" : ""}
			</button>
		</div>
	);
}
