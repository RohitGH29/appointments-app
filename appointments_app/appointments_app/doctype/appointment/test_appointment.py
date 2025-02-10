# Copyright (c) 2025, Rohit and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestAppointment(UnitTestCase):
	"""
	Unit tests for Appointment.
	Use this class for testing individual functions and methods.
	"""
	def test_add_to_appointment_queue(self):
		doctor = frappe.get_doc({"doctype": "Doctor", "first_name": "Test Doctor1", "speciality": "Medicine"}).insert()
		clinic= frappe.get_doc({"doctype": "Clinic", "name":"Test Clinic", "doctor": doctor.name, "contact_number": "+911234567892"}).insert()
		shift = frappe.get_doc({"doctype": "Schedule Shift", "start_time": "9:00:00", "end_time": "10:00:00", "clinic": clinic}).insert()
		day = '2025-02-10'

		appointment = frappe.get_doc({
			"doctype": "Appointment",
			"clinic": clinic.name,
			"shift": shift.name,
			"date": day,
			"patient_name": "Test Patient",
		}).insert()
		self.assertEqual(appointment.queue_number,1)
		
		appointment = frappe.get_doc({
			"doctype": "Appointment",
			"clinic": clinic.name,
			"shift": shift.name,
			"date": day,
			"patient_name": "Test Patient",
		}).insert()
		self.assertEqual(appointment.queue_number,2)

	def tearDown(self):
		frappe.db.rollback()

	

	


class IntegrationTestAppointment(IntegrationTestCase):
	"""
	Integration tests for Appointment.
	Use this class for testing interactions between multiple components.
	"""

	pass
