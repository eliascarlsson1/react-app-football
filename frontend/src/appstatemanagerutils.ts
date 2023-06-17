import { TestData } from "./model/test_model";

export function getTestDataArray(response: object): TestData[] {
	const testDataArray: TestData[] = [];
	Object.entries(response).forEach(([key, value]) => {
		const testData: TestData = {
			id: value.id,
			roi: value.roi,
			gamesBeforeFilter: value.gamesBeforeFilter,
			gamesAfterFilter: value.gamesAfterFilter,
			zeroBeforeFilter: value.zeroBeforeFilter,
			zeroAfterFilter: value.zeroAfterFilter,
			oneBeforeFilter: value.oneBeforeFilter,
			oneAfterFilter: value.oneAfterFilter,
		};
		testDataArray.push(testData);
	});
	return testDataArray;
}

export function getTrainModelRoi(
	response: object,
): { id: string; roi: string }[] {
	const trainModelRoi: { id: string; roi: string }[] = [];
	Object.entries(response).forEach(([key, value]) => {
		const roi: { id: string; roi: string } = {
			id: key,
			roi: value,
		};
		trainModelRoi.push(roi);
	});
	return trainModelRoi;
}
