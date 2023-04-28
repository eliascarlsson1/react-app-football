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

export async function get_parameters(
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
		console.error("Error in fetching historical data:", error);
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
		console.error("Error in fetching historical data:", error);
	}
}
