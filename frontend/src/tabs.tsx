import React from "react";

export type TabOption = "evaluate" | "pipeline";
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
    </div>
  );
}
