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

export default function SinlgeTextSlider({
	min,
	max,
	step,
	starting = min,
	deliverValue,
	label = "",
	width = 250,
}: {
	min: number;
	max: number;
	step: number;
	starting?: number;
	deliverValue: (value: number) => void;
	label?: string;
	width?: number;
}) {
	const [value, setValue] = React.useState<number | "">(starting);

	const handleSliderChange = (event: Event, newValue: number | "") => {
		setValue(newValue);
	};

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setValue(event.target.value === "" ? "" : Number(event.target.value));
	};

	const handleBlur = () => {
		if (value === "") {
			setValue(min);
			return;
		}

		if (value < min) {
			setValue(min);
		} else if (value > max) {
			setValue(max);
		}
	};

	return (
		<Box sx={{ width: width }}>
			<Typography id="input-slider" gutterBottom>
				{label}
			</Typography>
			<Grid container spacing={2} alignItems="center">
				<Grid item xs>
					<Slider
						value={typeof value === "number" ? value : min}
						min={min}
						max={max}
						step={step}
						onChange={(e, value) =>
							handleSliderChange(
								e,
								typeof value === "object" ? value[min] : value,
							)
						}
						aria-labelledby="input-slider"
					/>
				</Grid>
				<Grid item>
					<Input
						value={value}
						size="small"
						onChange={handleInputChange}
						onBlur={handleBlur}
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
