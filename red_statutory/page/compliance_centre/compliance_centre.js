frappe.pages['compliance-centre'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Compliance Centre',
		single_column: true
	});
};
