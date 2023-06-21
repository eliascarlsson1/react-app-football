import { ModelInformation } from "./appstatemanager";
import { FilterData } from "./test/create_test";

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

export async function getAllLeagueIdsToName(
	updateLeagueIdsToName: (leagueIdsToName: Map<string, string>) => void,
) {
	try {
		const response = await fetch(
			"http://localhost:5000/api/get-league-ids-to-names",
		);
		const data: Object = await response.json();
		const idToNameMap = new Map(Object.entries(data));
		updateLeagueIdsToName(idToNameMap);
	} catch (error) {
		console.error("Error in fetching league ids to name:", error);
	}
}

export async function getCurrentModels(
	updateCurrentModels: (currentModels: ModelInformation[]) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/current-models");
		const data: ModelInformation[] = await response.json();
		const dataToReturn =
			data.length === 0
				? [
						{
							name: "NO MODELS EXISTS",
							trainingData: [],
							xParameters: [],
							yParameter: "",
						},
				  ]
				: data;
		updateCurrentModels(dataToReturn);
	} catch (error) {
		console.error("Error in fetching current models:", error);
	}
}

export async function getCurrentTests(
	updateCurrentTests: (currentTests: string[]) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/current-tests");
		const data: string[] = await response.json();
		updateCurrentTests(data);
	} catch (error) {
		console.error("Error in fetching current tests:", error);
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

export async function deleteTest(testName: string, whenDone: () => void) {
	try {
		await fetch("http://localhost:5000/api/delete-test-call", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ testName }),
		});
		whenDone();
	} catch (error) {
		whenDone();
		console.error("Error in deleting test:", error);
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

export async function saveTest(
	filterData: FilterData,
	getResponse: (response: string) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/save-test-call", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ filterData }),
		});
		const responseText: string = await response.text();
		getResponse(responseText);
	} catch (error) {
		console.error("Error in saving test:", error);
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

export async function getRoiFromModel(
	roiInfo: object,
	getResponse: (response: object) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/api/get-roi-model", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(roiInfo),
		});
		const responseObject: object = await response.json();
		getResponse(responseObject);
	} catch (error) {
		console.error("Error in getting ROI from model:", error);
	}
}

export async function getStatsModelTest(
	testInfo: object,
	getResponse: (response: object) => void,
) {
	try {
		const response = await fetch(
			"http://localhost:5000/api/get-roi-model-test",
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(testInfo),
			},
		);
		const responseObject: object = await response.json();
		getResponse(responseObject);
	} catch (error) {
		console.error("Error in testing model: ", error);
	}
}

export async function getPrepareDataProgess(
	getResponse: (response: { status: string; total: string }) => void,
) {
	try {
		const response = await fetch("http://localhost:5000/prepare-data-progress");
		const responseObject = await response.json();
		getResponse(responseObject);
	} catch (error) {
		console.error("Error in getting prepare data progress: ", error);
	}
}

// Post function with leagueIds = string[]
export async function scrapeData(leagueIds: string[]) {
	try {
		await fetch("http://localhost:5000/api/scrape-leagues-by-id", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(leagueIds),
		});
	} catch (error) {
		console.error("Error in scraping data:", error);
	}
}

export async function prepareScrapedData(
	getResponse: (response: string) => void,
) {
	try {
		const response = await fetch(
			"http://localhost:5000/api/prepare-scraped-data",
			{ method: "POST" },
		);
		const responseText: string = await response.text();
		getResponse(responseText);
	} catch (error) {
		console.error("Error in preparing scraped data:", error);
	}
}
