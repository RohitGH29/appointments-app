# Copyright (c) 2025, Rohit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Appointment(Document):
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
		frappe.enqueue(
			'appointments_app.utils.send_message',
			#  queue='short',
			 body=f"Appointment booked! Your queue number is {self.queue_number} at {self.clinic} on {self.date} at {self.shift}",
			 from_="+16204558661", 
			 to=self.contact_number
		)