frappe.pages["compliance-centre"].on_page_load = function (wrapper) {

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: "Compliance Centre",
		single_column: true
	});

	$(wrapper).html(`
		<div class="container mt-4">

			<div class="row mb-3">

				<div class="col-md-3">
					<label><b>Month</b></label>
					<select id="red-month" class="form-control">
						<option value="1">January</option>
						<option value="2">February</option>
						<option value="3">March</option>
						<option value="4">April</option>
						<option value="5">May</option>
						<option value="6">June</option>
						<option value="7">July</option>
						<option value="8">August</option>
						<option value="9">September</option>
						<option value="10">October</option>
						<option value="11">November</option>
						<option value="12">December</option>
					</select>
				</div>

				<div class="col-md-2">
					<label><b>Year</b></label>
					<input
						type="number"
						id="red-year"
						class="form-control"
						value="${new Date().getFullYear()}">
				</div>

				<div class="col-md-4">
					<label><b>Internal Client Code</b></label>
					<input
						type="text"
						id="red-icc"
						class="form-control"
						placeholder="Enter Internal Client Code">
				</div>

				<div class="col-md-3">
					<label>&nbsp;</label>

					<button
						class="btn btn-primary btn-block"
						id="generate-register">

						Generate Wage Register

					</button>
				</div>

			</div>

			<hr>

			<div id="register-output"></div>

		</div>
	`);

	$("#generate-register").click(function () {

		const month = $("#red-month").val();
		const year = $("#red-year").val();
		const internal_client_code = $("#red-icc").val();

		if (!internal_client_code) {
			frappe.msgprint("Please enter Internal Client Code.");
			return;
		}

		frappe.call({

			method:
"red_statutory.red_statutory.page.compliance_centre.compliance_centre.generate_wage_register",

			args: {
				internal_client_code,
				month,
				year
			},

			freeze: true,
			freeze_message: "Generating Wage Register...",

			callback: function (r) {

				if (!r.message) {
					frappe.msgprint("No data found.");
					return;
				}

				render_wage_register(r.message);

			}

		});

	});

};


function money(value) {

	return Number(value || 0).toLocaleString(
		"en-IN",
		{
			minimumFractionDigits: 2,
			maximumFractionDigits: 2
		}
	);

}


function render_wage_register(data) {

	frappe.call({
		method: "frappe.client.get",
		args: {
			doctype: "Page",
			name: "compliance-centre"
		},
		callback: function () {

			frappe.require("/assets/red_statutory/wage_register.html", function () {

				const html = frappe.render_template(
					"wage_register",
					{register: data}
				);

				$("#register-output").html(html);

			});

		}
	});

}