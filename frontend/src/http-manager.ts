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
