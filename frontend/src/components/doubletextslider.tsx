import * as React from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Slider from "@mui/material/Slider";
import MuiInput from "@mui/material/Input";

const Input = styled(MuiInput)`
	width: 55px;
`;

export default function DoubleTextSlider({
	min,
	max,
	step,
	starting = [min, max],
	deliverValue,
	label = "",
	width = 250,
}: {
	min: number;
	max: number;
	step: number;
	starting?: number[];
	deliverValue: (value: number[]) => void;
	label?: string;
	width?: number;
}) {
	const [value, setValue] = React.useState<number[]>(starting);

	const getValueAsNumber = (value: number | "", how: "min" | "max"): number => {
		if (value === "") {
			if (how === "min") {
				return min;
			} else {
				return max;
			}
		} else {
			return value;
		}
	};

	const handleSliderChange = (newValue: number[]) => {
		const sortedValue = newValue.sort((a, b) => a - b);
		setValue(sortedValue);
		deliverValue(sortedValue);
	};

	const handleInputChangeMax = (event: React.ChangeEvent<HTMLInputElement>) => {
		const newValue =
			event.target.value === "" ? "" : Number(event.target.value);
		const numberValue = getValueAsNumber(newValue, "max");
		const sortedValue = [value[0], numberValue].sort((a, b) => a - b);
		setValue(sortedValue);
		deliverValue(sortedValue);
	};

	const handleInputChangeMin = (event: React.ChangeEvent<HTMLInputElement>) => {
		const newValue =
			event.target.value === "" ? "" : Number(event.target.value);
		const numberValue = getValueAsNumber(newValue, "min");
		const sortedValue = [numberValue, value[1]].sort((a, b) => a - b);
		setValue(sortedValue);
		deliverValue(sortedValue);
	};

	return (
		<Box sx={{ width: width }}>
			<Typography id="input-slider" gutterBottom>
				{label}
			</Typography>
			<Grid container spacing={2} alignItems="center">
				<Grid item>
					<Input
						value={value[0]}
						size="small"
						onChange={handleInputChangeMin}
						inputProps={{
							step,
							min,
							max,
							type: "number",
							"aria-labelledby": "input-slider",
						}}
					/>
				</Grid>
				<Grid item xs>
					<Slider
						value={value}
						min={min}
						max={max}
						step={step}
						onChange={(e, value) => handleSliderChange(value as number[])}
						aria-labelledby="input-slider"
					/>
				</Grid>
				<Grid item>
					<Input
						value={value[1]}
						size="small"
						onChange={handleInputChangeMax}
						inputProps={{
							step,
							min,
							max,
							type: "number",
							"aria-labelledby": "input-slider",
						}}
					/>
				</Grid>
			</Grid>
		</Box>
	);
}
