# Copyright (c) 2025, Rohit and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase
from appointments_app.appointments_app.doctype.appointment_queue.appointment_queue import create_queues_for_today
import frappe.utils

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestAppointmentQueue(UnitTestCase):
	"""
	Unit tests for AppointmentQueue.
	Use this class for testing individual functions and methods.
	"""

	def test_create_queues_for_today(self):
		doctor = frappe.get_doc({"doctype": "Doctor", "first_name": "Test Doctor1", "speciality": "Medicine"}).insert()
		clinic= frappe.get_doc({"doctype": "Clinic", "name":"Test Clinic", "doctor": doctor.name, "contact_number": "+911234567892", "is_published": True}).insert()
		test_shift1 = frappe.get_doc({"doctype": "Schedule Shift", "start_time": "9:00:00", "end_time": "10:00:00", "clinic": clinic}).insert()
		test_shift2 = frappe.get_doc({"doctype": "Schedule Shift", "start_time": "10:00:00", "end_time": "12:00:00", "clinic": clinic}).insert()
		
		# assert no queue exist
		self.assertEqual(frappe.db.count("Appointment Queue"),0)
		create_queues_for_today()

		# assert exactly one queue exists
		self.assertEqual(frappe.db.count("Appointment Queue"),2)

		# that queue is for above clinic & shift & today's date
		queue = frappe.get_doc("Appointment Queue", {"clinic": clinic.name, "shift": test_shift1.name, "date": frappe.utils.today()})
		self.assertTrue(queue)

	def tearDown(self):
		frappe.db.rollback()

class IntegrationTestAppointmentQueue(IntegrationTestCase):
	"""
	Integration tests for AppointmentQueue.
	Use this class for testing interactions between multiple components.
	"""

	pass
