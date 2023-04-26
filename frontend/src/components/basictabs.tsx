import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";

interface TabPanelProps {
	children?: React.ReactNode;
	index: number;
	value: number;
}

function a11yProps(index: number) {
	return {
		id: `simple-tab-${index}`,
		"aria-controls": `simple-tabpanel-${index}`,
	};
}

export default function BasicTabs({
	values,
	startingIndex,
	deliverSelectedIndex,
}: {
	values: string[];
	startingIndex: number;
	deliverSelectedIndex: (selectedTabIndex: number) => void;
}) {
	const [value, setValue] = React.useState(startingIndex);

	const handleChange = (event: React.SyntheticEvent, selectedIndex: number) => {
		setValue(selectedIndex);
		deliverSelectedIndex(selectedIndex);
	};

	return (
		<Box sx={{ width: "100%" }}>
			<Box sx={{ borderBottom: 1, borderColor: "divider" }}>
				<Tabs
					value={value}
					onChange={handleChange}
					aria-label="basic tabs example"
				>
					{values.map((value, index) => (
						<Tab key={`${value}${index}`} label={value} {...a11yProps(0)} />
					))}
				</Tabs>
			</Box>
		</Box>
	);
}
