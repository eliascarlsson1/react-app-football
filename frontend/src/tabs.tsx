import React from "react";

export type TabOptions = "evaluate" | "pipeline";
export type TabState = { tab: TabOptions };

export default function Tabs({
  state,
  dispatcher,
}: {
  state: TabState;
  dispatcher: (tab: TabOptions) => void;
}) {
  return (
    <div>
      <button type="button" onClick={() => dispatcher("evaluate")}>
        Evaluate {state.tab === "evaluate" ? "Active" : ""}
      </button>
      <button type="button" onClick={() => dispatcher("pipeline")}>
        Pipeline {state.tab === "pipeline" ? "Active" : ""}
      </button>
    </div>
  );
}
