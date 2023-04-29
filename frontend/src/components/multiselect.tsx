import * as React from "react";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

export default function MultiSelect({
	dataArray,
	deliverSelected,
	selected = [],
	label = null,
	width = 300,
}: {
	dataArray: string[];
	deliverSelected: (selectedData: string[]) => void;
	selected?: string[];
	label?: string | null;
	width?: number;
}) {
	const [value, setValue] = React.useState(selected);

	return (
		<Autocomplete
			multiple
			id="fixed-tags-demo"
			value={value}
			onChange={(event, newValue) => {
				setValue(newValue);
				deliverSelected(newValue);
			}}
			options={dataArray}
			renderTags={(tagValue) =>
				tagValue.map((option) => <Chip key={option} label={option} />)
			}
			style={{ width: width }}
			renderInput={(params) => <TextField {...params} label={label} />}
		/>
	);
}
