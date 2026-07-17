frappe.query_reports["Wage Register"] = {
	filters: [
		{
			fieldname: "internal_client_code",
			label: "Internal Client Code",
			fieldtype: "Link",
			options: "Customer",
			reqd: 1
		},
		{
			fieldname: "month",
			label: "Month",
			fieldtype: "Select",
			options: [
				"1",
				"2",
				"3",
				"4",
				"5",
				"6",
				"7",
				"8",
				"9",
				"10",
				"11",
				"12"
			],
			reqd: 1
		},
		{
			fieldname: "year",
			label: "Year",
			fieldtype: "Int",
			reqd: 1
		}
	]
};
