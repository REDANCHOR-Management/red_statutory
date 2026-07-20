frappe.pages['compliance-centre'].on_page_load = function (wrapper) {

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Compliance Centre',
		single_column: true
	});

	let body = $(`
		<div class="p-4">

			<div id="filters" style="max-width:700px;"></div>

			<div class="mt-4">
				<button class="btn btn-primary" id="generate_register">
					Generate Register
				</button>
			</div>

		</div>
	`);

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
			fieldtype: "Data",
			fieldname: "internal_client_code",
			label: "Internal Client Code",
			reqd: 1
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
			fieldtype: "Int",
			fieldname: "year",
			label: "Year",
			reqd: 1,
			default: new Date().getFullYear()
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

		if (values.register !== "Wage Register") {
			frappe.throw(__("Only Wage Register is available."));
		}

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
