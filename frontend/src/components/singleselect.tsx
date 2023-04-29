import * as React from "react";
import { Theme, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import Chip from "@mui/material/Chip";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
	PaperProps: {
		style: {
			maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
			width: 250,
		},
	},
};

function getStyles(
	data: string,
	selectedData: readonly string[],
	theme: Theme,
) {
	return {
		fontWeight:
			selectedData.indexOf(data) === -1
				? theme.typography.fontWeightRegular
				: theme.typography.fontWeightMedium,
	};
}

export default function SingleSelect({
	dataArray,
	deliverSelected,
	selected,
	label = null,
	width = 300,
}: {
	dataArray: string[];
	deliverSelected: (selectedData: string) => void;
	selected: string;
	label?: string | null;
	width?: number;
}) {
	const theme = useTheme();

	const handleChange = (event: SelectChangeEvent<typeof selected>) => {
		const {
			target: { value },
		} = event;
		const selectedData = value;
		deliverSelected(selectedData);
	};

	return (
		<div>
			<FormControl sx={{ width }}>
				{label ? <InputLabel>{label}</InputLabel> : ""}
				<Select
					value={selected}
					onChange={handleChange}
					input={<OutlinedInput label={label} />}
					renderValue={(selected) => (
						<Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
							<Chip label={selected} />
						</Box>
					)}
					MenuProps={MenuProps}
				>
					{dataArray.map((data) => (
						<MenuItem
							key={data}
							value={data}
							style={getStyles(data, [selected], theme)}
						>
							{data}
						</MenuItem>
					))}
				</Select>
			</FormControl>
		</div>
	);
}
