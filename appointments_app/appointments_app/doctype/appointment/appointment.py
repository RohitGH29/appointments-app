# Copyright (c) 2025, Rohit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):

	
	def validate(self):
		# validate the contact number, if it doesn't have a country code , prepand +91 by default or contact number length should be 10 digits except the country code
		if not self.contact_number:
			frappe.throw("Contact number is required")
		if len(self.contact_number) == 10:	
			self.contact_number = f"+91{self.contact_number}"
		elif len(self.contact_number) == 13 and self.contact_number.startswith("+91"):
			self.contact_number = self.contact_number
		else:
			frappe.throw("Contact number should be 10 digits with country code by default is +91")
			
		


	def after_insert(self):
		self.queue_number = self.add_to_appointment_queue()
		# attach csrf token + queue number as key & key number as value
		frappe.cache.set_value(f"{frappe.session.sid}:queue_number", self.queue_number)
		self.save(ignore_permissions= True)
		self.send_confirmation_message()

	def add_to_appointment_queue(self):
		filters = {
			"date": self.date,
			"shift": self.shift,
			"clinic": self.clinic
		}
		appointment_queue_exists = frappe.db.exists(
			"Appointment Queue",
			filters,
		)

		if appointment_queue_exists:
			q = frappe.get_doc("Appointment Queue", filters)
		else:	
			q= frappe.new_doc("Appointment Queue")
			q.update(filters)
			q.save(ignore_permissions=True)

		q.append("queue",{"appointment": self.name, "status": "Pending"})
		q.save(ignore_permissions=True)

		return len(q.queue)

	# Here we use a confiramtion message to let the user know that their appointment has been booked
	def send_confirmation_message(self):
		schedule_shift = frappe.get_doc("Schedule Shift", self.shift)
		start_time = schedule_shift.start_time
		end_time = schedule_shift.end_time

		frappe.enqueue(
			'appointments_app.utils.send_message',
			#  queue='short',
			 body=f"Appointment booked! Patient name: {self.patient_name} your queue number is {self.queue_number} at Clinic name: {self.clinic} on Date: {self.date} at Shift: {start_time} - {end_time}",
			 from_="+16204558661", 
			 to=self.contact_number
		)