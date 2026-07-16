frappe.pages['compliance-centre'].on_page_load = function(wrapper) {

	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Compliance Centre',
		single_column: true
	});

	page.add_field({
		label: 'Internal Client Code',
		fieldname: 'internal_client_code',
		fieldtype: 'Link',
		options: 'Customer'
	});

	page.add_field({
		label: 'Month',
		fieldname: 'month',
		fieldtype: 'Select',
		options: [
			'January','February','March','April','May','June',
			'July','August','September','October','November','December'
		].join('\n')
	});

	page.add_field({
		label: 'Year',
		fieldname: 'year',
		fieldtype: 'Int'
	});

	page.add_action_item('Fetch Salary Slips', function () {
		frappe.msgprint('Coming Soon');
	});

};
