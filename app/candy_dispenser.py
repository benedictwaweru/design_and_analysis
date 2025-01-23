import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

import random
import os

class CandyDispenser:
	def __init__(self, master):
		self.master = master
		self.master.title("Candy Dispenser")

		self.candies = []
		self.colors = ["Purple", "Red", "Yellow", "Light Pink", "Chocolate", "Orange", "Pink"]
		self.max_candies = 7

		# INFO: Spring properties
		self.spring_base_y = 400
		self.spring_min_height = 30
		self.spring_max_height = 200
		self.spring_increment = (self.spring_max_height - self.spring_min_height) / self.max_candies
		self.coils = 8
		self.spring_width = 40
		self.enclosure_width = 150

		# INFO: Initialize candies into the dispenser
		last_color = None
		for _ in range(7):
			available_colors = [c for c in self.colors if c != last_color]
			if available_colors:
				new_color = random.choice(available_colors)
				self.candies.append(new_color)
				last_color = new_color

		self.canvas = tk.Canvas(master, width=400, height=600, bg="light blue")
		self.canvas.pack()

		self.create_enclosure()

		# INFO: Create the platform
		platform_width = self.enclosure_width - 20
		x_center = 200
		self.platform = self.canvas.create_rectangle(
			x_center - platform_width/2, self.spring_base_y - self.spring_max_height - 10,
			x_center - platform_width/2, self.spring_base_y - self.spring_max_height,
			fill="gray",
			outline="black"
		)

		# INFO: Create the spring
		self.spring = self.create_spring(self.spring_max_height)

		self.display_candies()

		# Buttons
		button_frame = tk.Frame(master)
		button_frame.pack(fill=tk.X, padx=5, pady=5)
		
		self.push_button = tk.Button(button_frame, text="Push", command=self.push)
		self.push_button.pack(side=tk.LEFT, padx=5)

		self.pop_button = tk.Button(button_frame, text="Pop", command=self.pop)
		self.pop_button.pack(side=tk.LEFT, padx=5)

		self.is_empty_button = tk.Button(button_frame, text="isEmpty", command=self.is_empty)
		self.is_empty_button.pack(side=tk.LEFT, padx=5)

		self.is_full_button = tk.Button(button_frame, text="isFull", command=self.is_full)
		self.is_full_button.pack(side=tk.LEFT, padx=5)

		self.top_button = tk.Button(button_frame, text="Check Top", command=self.top)
		self.top_button.pack(side=tk.LEFT, padx=5)

		self.show_candies_button = tk.Button(button_frame, text="Show no. of candies", command=self.show_candies)
		self.show_candies_button.pack(side=tk.LEFT, padx=5)

	def create_enclosure(self):
		x_center = 200
		width = self.enclosure_width
		height = 370

		x1 = x_center - width/2
		x2 = x_center + width/2
		y1 = self.spring_base_y - height
		y2 = self.spring_base_y - 10

		# INFO: Create rectangular enclosure
		self.enclosure = self.canvas.create_rectangle(
			x1, y1,
			x2, y2,
			fill="white",
			outline="black",
			width=2
		)

		base_height = 25
		connector_width = width - 60
		self.base_connector = self.canvas.create_rectangle(
			x_center - connector_width/2, y2,
			x_center + connector_width/2, y2 + base_height,
			fill="gray",
			outline="black"
		)
	
	def create_spring(self, height):
		points = []
		segments = self.coils * 2
		spacing = height / (segments / 2)
		x_center = 200
		y_start = self.spring_base_y

		points.append(x_center)
		points.append(y_start)

		for i in range(segments + 1):
			x = x_center + ((-1) ** i) * (self.spring_width / 2)
			y = y_start - (i * spacing / 2)
			points.append(x)
			points.append(y)

		return self.canvas.create_line(
			points,
			fill="red",
			width=3,
			smooth=True
		)
	
	def update_spring(self):
		weight_factor = len(self.candies) / self.max_candies
		current_height = self.spring_max_height * (1 - (weight_factor * 0.6))

		self.canvas.delete(self.spring)
		self.spring = self.create_spring(current_height)

		platform_y = self.spring_base_y - current_height
		platform_width = self.enclosure_width - 20
		x_center = 200

		self.canvas.coords(
			self.platform,
			x_center - platform_width/2, platform_y - 10,
			x_center + platform_width/2, platform_y
		)

	def display_candies(self):
		current_dir = os.path.dirname(os.path.abspath(__file__))


		self.canvas.delete("candies")

		self.candy_images = {
			"Purple": Image.open(os.path.join(current_dir, "images/candy(1).jpeg")),
			"Red": Image.open(os.path.join(current_dir, "images/candy(2).jpeg")),
			"Yellow": Image.open(os.path.join(current_dir, "images/candy(3).jpeg")),
			"Light Pink": Image.open(os.path.join(current_dir, "images/candy(4).jpeg")),
			"Chocolate": Image.open(os.path.join(current_dir, "images/candy(5).jpeg")),
			"Orange": Image.open(os.path.join(current_dir, "images/candy(6).jpeg")),
			"Pink": Image.open(os.path.join(current_dir, "images/candy(7).jpeg"))
		}

		candy_size = (35, 35)

		for color, img in self.candy_images.items():
			self.candy_images[color] = ImageTk.PhotoImage(img.resize(candy_size))



		spring_height = self.spring_max_height * (1 - (len(self.candies) / self.max_candies * 0.6))
		base_y = self.spring_base_y - spring_height

		for i, color in enumerate(self.candies):
			candy_image = self.candy_images.get(color)
			if candy_image:
				x = 200
				y = base_y - 25 - (i * 35)
				self.canvas.create_image(x, y, image=candy_image, tags="candies")

		self.update_spring()

	def push(self):
		if len(self.candies) >= self.max_candies:
			messagebox.showwarning("WARNING", "The dispenser is full. Cannot add candy")
			return

		current_colors = set(self.candies)
		available_colors = [color for color in self.colors if color not in current_colors]

		if available_colors:
			new_color = random.choice(available_colors)
			self.candies.append(new_color)
			self.display_candies()
		else:
			messagebox.showwarning("Stack is full", "No more candies available to add")

	def pop(self):
		if self.candies:
			self.candies.pop()
			self.display_candies()

		else:
			messagebox.showwarning("Stack is empty", "Cannot remove candy")

	def is_empty(self):
		if not self.candies:
			messagebox.showwarning("Is it empty?", "Yes, the dispenser is empty")
		else:
			messagebox.showwarning("Is it empty?", "No, the dispenser is not empty")

	def is_full(self):
		if len(self.candies) == 7:
			messagebox.showwarning("Is it full?", "Yes, the dispenser is full")
		else:
			messagebox.showwarning("Is it full?", "No, the dispenser is not full")

	def top(self):
		if self.candies:
			top_candy = self.candies[-1]
			messagebox.showwarning("What is the top candy?", f"The top candy is {top_candy}")
		else:
			messagebox.showwarning("Stack is empty", "No candies in the dispenser")

	def show_candies(self):
		number_of_candies = len(self.candies)
		if number_of_candies == 1:
			messagebox.showwarning("No. of candies", f"There is {number_of_candies} candy in the dispenser")
		else:
			messagebox.showwarning("No. of candies", f"There are {number_of_candies} candies in the dispenser")


if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	root.deiconify()
	app = CandyDispenser(root)
	root.mainloop()
