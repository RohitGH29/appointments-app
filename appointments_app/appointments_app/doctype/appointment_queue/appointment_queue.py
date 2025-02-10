# Copyright (c) 2025, Rohit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AppointmentQueue(Document):
	pass


def create_queues_for_today():
	if frappe.flags.in_test:
		clinics = frappe.get_all("Clinic", filters={"is_published": True, "name": "Test Clinic"}, pluck="name")
	else:	
		clinics = frappe.get_all("Clinic", filters={"is_published": True}, pluck="name")

	for clinic in clinics:
		# create an appointment queue if doesn't exist, use ignore_if_duplicate=True
		# to ignore duplicate entry error
		shifts = frappe.get_all("Schedule Shift", filters={"clinic": clinic}, pluck="name")
		for shift in shifts:
			frappe.get_doc(
				{
					"doctype": "Appointment Queue",
					"clinic": clinic,
					"date": frappe.utils.today(),
					"shift": shift,
				}
			).insert(ignore_if_duplicate=True)
		

# csrf token: 1b4bee30b92048b2e07f9f6ba50d02e4710a21ffc14957f72888e738		