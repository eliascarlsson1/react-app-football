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

export default function MultiSelect({
	dataArray,
	deliverSelected,
	selected = [],
	label = null,
}: {
	dataArray: string[];
	deliverSelected: (selectedData: string[]) => void;
	selected?: string[];
	label?: string | null;
}) {
	const theme = useTheme();
	const filteredSelected = selected.filter((value) =>
		dataArray.includes(value),
	);
	const [selectedData, setSelectedData] =
		React.useState<string[]>(filteredSelected);

	const handleChange = (event: SelectChangeEvent<typeof selectedData>) => {
		const {
			target: { value },
		} = event;
		const selectedData = typeof value === "string" ? value.split(",") : value;
		setSelectedData(selectedData);
		deliverSelected(selectedData);
	};

	return (
		<div>
			<FormControl sx={{ m: 1, width: 300 }}>
				{label ? <InputLabel>{label}</InputLabel> : ""}
				<Select
					multiple
					value={selectedData}
					onChange={handleChange}
					input={<OutlinedInput label={label} />}
					renderValue={(selected) => (
						<Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
							{selected.map((value) => (
								<Chip key={value} label={value} />
							))}
						</Box>
					)}
					MenuProps={MenuProps}
				>
					{dataArray.map((data) => (
						<MenuItem
							key={data}
							value={data}
							style={getStyles(data, selectedData, theme)}
						>
							{data}
						</MenuItem>
					))}
				</Select>
			</FormControl>
		</div>
	);
}
