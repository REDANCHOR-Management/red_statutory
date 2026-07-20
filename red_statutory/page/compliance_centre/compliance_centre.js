frappe.pages['compliance-centre'].on_page_load = function (wrapper) {

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Compliance Centre',
		single_column: true
	});

	let body = $('<div class="p-3 d-flex align-items-end" id="register-toolbar" style="gap: 12px;"><div id="filters" class="d-flex" style="gap: 12px;"></div><button class="btn btn-primary" id="generate_register">Generate Wage Register</button></div>');

	$(page.body).append(body);

	// -----------------------------
	// Filters
	// -----------------------------

	const fields = [
		{
			fieldtype: "Select",
			fieldname: "register",
			label: "Register",
			options: [
				"Wage Register"
			].join("\n"),
			reqd: 1,
			default: "Wage Register"
		},
		{
			fieldtype: "Select",
			fieldname: "month",
			label: "Month",
			reqd: 1,
			options: [
				"January",
				"February",
				"March",
				"April",
				"May",
				"June",
				"July",
				"August",
				"September",
				"October",
				"November",
				"December"
			].join("\n")
		},
		{
			fieldtype: "Select",
			fieldname: "year",
			label: "Year",
			reqd: 1,
			default: String(new Date().getFullYear()),
			options: Array.from({ length: 11 }, (_, index) => String(new Date().getFullYear() - 5 + index)).join("\\n")
		}
	];

	let filter_group = new frappe.ui.FieldGroup({
		fields: fields,
		body: $("#filters")
	});

	filter_group.make();

	// -----------------------------
	// Generate
	// -----------------------------

	$("#generate_register").click(function () {

		let values = filter_group.get_values();

		if (!values)
			return;

		frappe.call({
			method: "red_statutory.page.compliance_centre.compliance_centre.generate",
			args: values,
			freeze: true,
			freeze_message: __("Generating PDF..."),
			callback: function (response) {
				if (response.message) {
					window.location.assign(response.message);
				}
			}
		});

	});

};
