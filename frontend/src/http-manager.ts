export async function getHistoricalData(
	updateHistoricalData: (historicalData: string[]) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/historical");
		const data: string[] = await response.json();
		updateHistoricalData(data);
	} catch (error) {
		console.error("Error in fetching historical data:", error);
	}
}

export async function getCurrentModels(
	updateCurrentModels: (currentModels: string[]) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/current-models");
		const data: string[] = await response.json();
		updateCurrentModels(data);
	} catch (error) {
		console.error("Error in fetching current models:", error);
	}
}

export async function getParameters(
	updateParameters: (historicalData: string[]) => void,
	x_or_y: "x" | "y",
) {
	try {
		const url = `http://localhost:5000/api/parameters/${x_or_y}`;
		const response = await fetch(url);
		const parameters = await response.json();
		const parametersArray: string[] = Object.values(parameters);
		updateParameters(parametersArray);
	} catch (error) {
		console.error("Error in fetching parameters:", error);
	}
}

export async function trainModel(
	info: object,
	getResponse: (response: string) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/train-model-call", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(info),
		});
		const responseText: string = await response.text();
		getResponse(responseText);
	} catch (error) {
		console.error("Error in training model:", error);
	}
}

export async function deleteModel(modelName: string, whenDone: () => void) {
	try {
		await fetch("http://localhost:5000/api/delete-model-call", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ modelName }),
		});
		whenDone();
	} catch (error) {
		whenDone();
		console.error("Error in deleting model:", error);
	}
}

export async function saveModel(
	modelName: string,
	getResponse: (response: string) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/save-model-call", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ modelName }),
		});
		const responseText: string = await response.text();
		getResponse(responseText);
	} catch (error) {
		console.error("Error in saving model:", error);
	}
}

export async function prepareData(getResponse: (response: string) => void) {
	try {
		const response = await fetch(
			"http://localhost:5000/api/prepare-data-call",
			{ method: "POST" },
		);
		const responseText: string = await response.text();
		getResponse(responseText);
	} catch (error) {
		console.error("Error in preparing data:", error);
	}
}

export async function downloadLatestData(
	getResponse: (response: string) => void,
) {
	try {
		const response = await fetch(
			"http://localhost:5000/api/download-latest-data-call",
			{ method: "POST" },
		);
		const responseText: string = await response.text();
		getResponse(responseText);
	} catch (error) {
		console.error("Error in preparing data:", error);
	}
}
