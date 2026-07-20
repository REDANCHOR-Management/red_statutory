frappe.pages['compliance-centre'].on_page_load = function (wrapper) {

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Compliance Centre',
		single_column: true
	});

	const app = $(`
		<div class="p-4">

			<div id="filters"></div>

			<div class="mt-4">
				<button class="btn btn-primary" id="generate_btn">
					Generate
				</button>
			</div>

		</div>
	`);

	$(page.body).append(app);

	// Filters will be added here.

	$('#generate_btn').on('click', function () {

		// Collect filters

		// Call backend

		// Download PDF

	});

};