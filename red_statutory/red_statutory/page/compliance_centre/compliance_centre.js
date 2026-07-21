frappe.pages["compliance-centre"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Compliance Centre",
		single_column: true,
	});

	const month_options = [
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
		"December",
	];
	const current_year = new Date().getFullYear();
	const year_options = Array.from({ length: 11 }, (_, index) => String(current_year - 5 + index));

	const toolbar = $(
		'<div style="display:flex;align-items:end;gap:12px;padding:16px;border-bottom:1px solid var(--border-color);"></div>'
	).appendTo(page.body);

	const register = frappe.ui.form.make_control({
		parent: toolbar,
		df: {
			fieldname: "register",
			fieldtype: "Data",
			label: __("Register"),
			default: __("Wage Register"),
			read_only: 1,
		},
		render_input: true,
	});
	const internal_client_code = frappe.ui.form.make_control({
		parent: toolbar,
		df: {
			fieldname: "internal_client_code",
			fieldtype: "Data",
			label: __("Internal Client Code"),
			reqd: 1,
		},
		render_input: true,
	});
	const month = frappe.ui.form.make_control({
		parent: toolbar,
		df: {
			fieldname: "month",
			fieldtype: "Select",
			label: __("Month"),
			options: month_options.join("\n"),
			reqd: 1,
			default: month_options[new Date().getMonth()],
		},
		render_input: true,
	});
	const year = frappe.ui.form.make_control({
		parent: toolbar,
		df: {
			fieldname: "year",
			fieldtype: "Select",
			label: __("Year"),
			options: year_options.join("\n"),
			reqd: 1,
			default: String(current_year),
		},
		render_input: true,
	});
	toolbar.find(".frappe-control").css({ margin: 0, "min-width": "180px" });

	$(
		'<button class="btn btn-primary" style="margin-bottom:1px;white-space:nowrap;">Generate Wage Register</button>'
	)
		.appendTo(toolbar)
		.on("click", () => {
			const values = {
				internal_client_code: internal_client_code.get_value(),
				month: month.get_value(),
				year: year.get_value(),
			};
			if (!values.internal_client_code || !values.month || !values.year) {
				frappe.msgprint(__("Internal Client Code, Month, and Year are required."));
				return;
			}

			const query = new URLSearchParams(values).toString();
			window.location.assign(
				`/api/method/red_statutory.red_statutory.reports.wage_register.pdf.download_wage_register?${query}`
			);
		});

	register.set_value(__("Wage Register"));
};
