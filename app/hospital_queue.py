import bisect as bs

import customtkinter
from tkinter import messagebox
from PIL import Image

import os

class HospitalQueue:
	def __init__(self):
		self.queue = []
		self.counter = 0

	def add_patient(self, name, age):
		patient = (-age, self.counter, {"name": name, "age": age})
		bs.insort(self.queue, patient)
		self.counter += 1

	def update_patient_age(self, name, new_age = None):
		for i, (_, _, patient) in enumerate(self.queue):
			if patient['name'].lower() == name.lower():
				self.queue.pop(i)
				if new_age is not None:
					self.add_patient(name=name, age=new_age)
				return True
			
		return False
	
	def admit_patient(self):
		if self.queue:
			return self.queue.pop(0)[2]
		
		return None
	
	def remove(self, name):
		for i, (_, _, patient) in enumerate(self.queue):
			if patient['name'].lower() == name.lower():
				self.queue.pop(i)
				return True
			
		return False
	
	def get_queue_length(self):
		return len(self.queue)
	
	def is_empty(self):
		return len(self.queue) == 0
	
	def get_highest_priority(self):
		if self.queue:
			return self.queue[0][2]
		
		return None



class Hospital(customtkinter.CTk):
	def __init__(self):
		super().__init__()

		self.geometry("850x600")
		self.title("Hospital")

		self.resizable(False, False)

		self.patient_queue = HospitalQueue()

		self.setup_ui()

	def setup_ui(self):
		customtkinter.CTkLabel(self, text="Reception", font=("Arial", 20)).pack(pady=10)


		customtkinter.CTkLabel(self, text="Add Patient").place(x=85, y=80)
		self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Patient Name")
		self.name_entry.place(x=80, y=110)

		self.age_entry = customtkinter.CTkEntry(self, placeholder_text="Patient's Age")
		self.age_entry.place(x=80, y=150)

		customtkinter.CTkButton(self, text="Add Patient", command=self.add_patient).place(x=80, y=190)


		customtkinter.CTkButton(self, text="Admit Next Patient", command=self.admit_oldest_patient).place(x=80, y=230)


		customtkinter.CTkLabel(self, text="Update Patient Details").place(x=350, y=80)
		self.update_name_entry = customtkinter.CTkEntry(self, placeholder_text="Patient Name")
		self.update_name_entry.place(x=350, y=110)

		self.update_age_entry = customtkinter.CTkEntry(self, placeholder_text="Patient's Age")
		self.update_age_entry.place(x=350, y=150)

		customtkinter.CTkButton(self, text="Update Patient", command=self.update_patient_details).place(x=350, y=190)

		customtkinter.CTkButton(self, text="Is Queue Empty?", command=self.check_if_empty).place(x=350, y=230)


		customtkinter.CTkLabel(self, text="Remove Patient by Name").place(x=600, y=80)
		self.index_entry = customtkinter.CTkEntry(self, placeholder_text="Patient Name")
		self.index_entry.place(x=600, y=110)
		customtkinter.CTkButton(self, text="Remove Patient", command=self.remove_patient).place(x=600, y=150)

		customtkinter.CTkButton(self, text="View Oldest Patient", command=self.get_highest_priority).place(x=600, y=190)


		customtkinter.CTkButton(self, text="Queue Length", command=self.get_length).place(x=600, y=230)


		customtkinter.CTkLabel(self, text="Patient Queue").place(x=80, y=300)
		self.queue_frame = customtkinter.CTkFrame(self, width=500, height=200, corner_radius=10)
		self.queue_frame.place(x=80, y=330)

	def add_patient(self):
		name = self.name_entry.get()
		age = self.age_entry.get()

		if not name or not age.isdigit():
			messagebox.showwarning("Error!", "Please enter a valid name and age")
			return
		
		self.patient_queue.add_patient(name, int(age))
		self.update_visual_queue()
		self.clear_entries()

	def update_patient_details(self):
		name = self.update_name_entry.get()
		new_age = self.update_age_entry.get()

		if not name:
			messagebox.showerror("Error", "Please enter the name of the patient to continue")
			return
		
		new_age = int(new_age) if new_age.isdigit() else None
		success = self.patient_queue.update_patient_age(name, new_age)


		if success:
			messagebox.showinfo("Success", f"Patient {name} updated successfully")
			self.update_name_entry.delete(0, "end")
			self.update_age_entry.delete(0, "end")
			self.update_visual_queue()

		else:
			messagebox.showerror("Error", f"Patient {name} not found")
			self.clear_entries()


	def update_visual_queue(self):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		for widget in self.queue_frame.winfo_children():
			widget.destroy()

		for _, _, patient in self.patient_queue.queue:
			frame = customtkinter.CTkFrame(self.queue_frame, height=50, width=380, corner_radius=10)
			frame.pack(pady=5, padx=10, fill="x")

			patient_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(current_dir, "images/avatar.jpg")), dark_image=Image.open(os.path.join(current_dir, "images/avatar.jpg")), size=(30, 30))

			customtkinter.CTkLabel(frame, image=patient_image, text="").pack(side="left", padx=10)


			customtkinter.CTkLabel(frame, text=f"Name: {patient['name']}, Age: {patient['age']}").pack(side="left", padx=10)


	def clear_entries(self):
		self.name_entry.delete(0, "end")
		self.age_entry.delete(0, "end")
		self.index_entry.delete(0, "end")

	def admit_oldest_patient(self):
		patient = self.patient_queue.admit_patient()
		if patient:
			messagebox.showinfo("Admitted Patient", f"Admitted: {patient['name']}, Age: {patient['age']}")
		else:
			messagebox.showinfo("Queue empty", "No patients in the queue")

	def check_if_empty(self):
		if self.patient_queue.is_empty():
			messagebox.showinfo("Queue Length", "The queue is empty")

		else:
			messagebox.showinfo("Queue Length", "The queue is not empty")

	def remove_patient(self):
		name = self.index_entry.get()

		if not name:
			messagebox.showerror("Error", "Please enter the name of a patient")
			return
		
		success = self.patient_queue.remove(name)

		if success:
			messagebox.showinfo("Success", f"Removed: {name} from queue")
			self.clear_entries()
			self.update_visual_queue()

		else:
			messagebox.showerror("Error", f"Patient {name} not found")

	def get_highest_priority(self):
		patient = self.patient_queue.get_highest_priority()
		if patient:
			messagebox.showinfo("Highest Priority", f"Name: {patient['name']}, Age: {patient['age']}")
		else:
			messagebox.showinfo("No patients in the queue")

	def get_length(self):
		length = self.patient_queue.get_queue_length()
		messagebox.showinfo("Queue Length", f"The queue has {length} patients")


if __name__ == "__main__":
	app = Hospital()
	app.mainloop()
