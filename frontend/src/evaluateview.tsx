import React from "react";

export type EvaluateViewState = { ROI: string };

export default function Evaluateview({ state }: { state: EvaluateViewState }) {
  return <div>{state.ROI}</div>;
}
