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
			fieldtype: "Link",
			fieldname: "internal_client_code",
			label: "Customer",
			options: "Customer",
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

		frappe.call({

			method:
				"red_statutory.page.compliance_centre.compliance_centre.generate",

			args: values,

			callback: function () {

				frappe.show_alert({
					message: "Generating PDF...",
					indicator: "green"
				});

			}

		});

	});

};