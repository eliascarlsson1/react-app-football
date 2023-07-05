import React from "react";
import { AppActionDispatcher } from "../appstatemanager";
import PipelineRow from "./pipelinerow";

export type PipelineInformation = {
	name: string;
	model: string;
	test: string;
	leagues: string[];
};

export type PipelineViewState = {
	pipelines: PipelineInformation[];
};

export type PipelineViewAction =
	| {
			type: "add pipeline";
			name: string;
			model: string;
			test: string;
			leagues: string[];
	  }
	| {
			type: "delete pipeline";
			name: string;
	  };

export default function PipelineView({
	state,
	dispatcher,
}: {
	state: PipelineViewState;
	dispatcher: AppActionDispatcher;
}) {
	return (
		<div>
			{state.pipelines.map((pipeline) => (
				<PipelineRow
					pipeline={pipeline}
					dispatcher={dispatcher}
					key={pipeline.name}
				></PipelineRow>
			))}
		</div>
	);
}
