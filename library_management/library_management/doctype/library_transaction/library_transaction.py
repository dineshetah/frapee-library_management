# Copyright (c) 2025, DCCODE and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.document import DocStatus

class LibraryTransaction(Document):
	def before_submit(self):
		
		if self.type =="Issue":
			self.validate_issued()
			 # set the article status to be Issued
			article = frappe.get_doc("Article", self.article)
			article.status = "Issued"
			article.save()

		if self.type =="Return":
			self.validate_returne()
			 # set the article status to be Issued
			article = frappe.get_doc("Article", self.article)
			article.status = "Available"
			article.save()
	



	def validate_issued(self):  #article cannot be issued if it is already issued
		self.validate_membership()
		article = frappe.get_doc("Article", self.article)
		if article.status =="Issued":
			frappe.throw("Article is already issued by another member")

	def validate_returne(self): # article cannot be returned if it is not issued first
		article = frappe.get_doc("Article", self.article)
		if article.status =="Available":
			frappe.throw("Article cannot be returned without being issued first")

	def validate_membership(self):
		 # check if a valid membership exist for this library member
		vaild_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member":self.library_member,
                "docstatus":DocStatus.submitted(),
				"to_date":(">", self.date),
				"from_date":("<", self.date)
			},
		)
		if vaild_membership:
			frappe.throw("The member does not have a valid membership")
	
