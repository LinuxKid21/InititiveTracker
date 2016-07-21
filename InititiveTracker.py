import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Hello World")

		self.columns = []
		self.delete_button_ids = {}
		self.is_reversed = False
		self.auto_update = False

		#frame is the black outline around the app
		frame = Gtk.Frame()
		frame.set_halign(Gtk.Align.CENTER)
		frame.set_valign(Gtk.Align.CENTER)
		
		#vbox contains the options on top and the feilds below
		vbox = Gtk.Box(spacing=6, orientation = Gtk.Orientation.VERTICAL)
		margin = 10
		vbox.set_margin_left(margin)
		vbox.set_margin_right(margin)
		vbox.set_margin_top(margin)
		vbox.set_margin_bottom(margin)

		# contains combo for ascending or descending, auto update checkbox and update button
		ordering_box = Gtk.Box(spacing=6, orientation = Gtk.Orientation.HORIZONTAL)
		button = Gtk.Button(label="Update")
		button.connect("clicked", self.update_button_pressed)
		ordering_box.pack_start(Gtk.Label(label="Order:"), False,False,0)
		combo_box = self.create_combo_box_from_list(["Ascending", "Descending"])
		combo_box.connect("changed", self.order_changed)
		auto_update_checkbox = Gtk.CheckButton()
		auto_update_checkbox.connect("toggled", self.auto_update_toggled)
		ordering_box.pack_start(combo_box, False,False,0)
		ordering_box.pack_start(Gtk.Label(label="Auto Update:"), False,False,0)
		ordering_box.pack_start(auto_update_checkbox, False,False,0)
		ordering_box.pack_start(button, False,False,0)

		vbox.pack_start(ordering_box, False,False,0)
		
		# hbox has fields on left and + button on the right
		hbox = Gtk.Box(spacing=6, orientation = Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, False,False,0)

		# this contains the fields(perhaps should have used grid! The code is somewhat messy)
		self.inititive_properties_box = Gtk.Box(spacing=6, orientation = Gtk.Orientation.VERTICAL)

		button = Gtk.Button(label="+")
		button.connect("clicked", self.add_button_clicked)
		hbox.pack_start(self.inititive_properties_box, False,False,0)
		hbox.pack_start(button, False,False,0)

		self.__add_rows()

		frame.add(vbox)
		self.add(frame)

	# helper for __add_rows(the plural one)
	def __add_row(self, name):

		f = Gtk.Box(spacing=6, orientation = Gtk.Orientation.HORIZONTAL)
		label = Gtk.Label(label=name)
		label.set_size_request(90, -1)
		label.set_xalign(0)
		f.add(label)
		self.inititive_properties_box.pack_start(f, False, False, 0)

		return f

	# adds the labels to the left of the rows
	def __add_rows(self):
		self.name_row = self.__add_row("Name")
		self.init_roll_row = self.__add_row("Inititive Roll")
		self.init_mod_row = self.__add_row("Inititive Mod")
		self.health_row = self.__add_row("Health")

		self.add_column()
		self.inititive_properties_box.show_all()

	# add an entry with specific width(must at least be larger than 5 chars currently)
	def __add_sized_entry(self,width):
		entry = Gtk.Entry()
		entry.set_width_chars(5)
		entry.set_size_request(width,-1)
		entry.connect("focus-out-event", self.entry_focus_left)
		return entry

	# adds all the fields to their respective hboxes
	def add_column(self):
		col = []
		column_width = 150
		f = Gtk.Box(spacing=6, orientation = Gtk.Orientation.HORIZONTAL)
		entry = Gtk.Entry()
		entry.set_width_chars(5)
		entry.set_size_request(column_width-80,-1)
		f.pack_start(entry, True, True, 0)
		delete_button = Gtk.Button(label="X")
		delete_button.connect("clicked", self.remove_button_clicked)
		f.pack_start(delete_button, False, False, 0)
		f.set_size_request(column_width,-1)
		self.name_row.pack_start(f, False, False, 0)
		col.append(f)
		entry = self.__add_sized_entry(column_width)
		self.init_roll_row.pack_start(entry, False, False, 0)
		col.append(entry)
		entry = self.__add_sized_entry(column_width)
		self.init_mod_row.pack_start(entry, False, False, 0)
		col.append(entry)
		entry = self.__add_sized_entry(column_width)
		self.health_row.pack_start(entry, False, False, 0)
		col.append(entry)
		self.inititive_properties_box.show_all()

		self.columns.append(col)
		self.delete_button_ids[delete_button] = len(self.columns)-1

	# called when the + button was clicked
	def add_button_clicked(self, widget):
		self.add_column()

	# called when the X next to the name field is clicked and removes that column
	def remove_button_clicked(self, widget):
		if len(self.columns) > 1:
			col = self.delete_button_ids[widget]
			for j in self.columns[col]:
				j.destroy()
			self.columns.remove(self.columns[col])
			for (k,v) in self.delete_button_ids.items():
				if v > self.delete_button_ids[widget]: self.delete_button_ids[k] -= 1
			del(self.delete_button_ids[widget])

	# called when update is hit manually
	def update_button_pressed(self, widget):
		self.update_order()
	
	# updates the order of fields
	def update_order(self):
		try:
			columns_sorted = []
			# collect data to sort
			for col in self.columns:
				(name_delete, roll, mod, health) = col
				roll_i = int(roll.get_text())
				mod_i = int(mod.get_text())
				columns_sorted.append((roll_i+mod_i,mod_i,col))

			# done seperately because an exception might occur!
			# remove everything because it will be sorted and replaced
			for col in self.columns:
				(name_delete, roll, mod, health) = col
				self.name_row.remove(name_delete)
				self.init_roll_row.remove(roll)
				self.init_mod_row.remove(mod)
				self.health_row.remove(health)
			# sort!
			columns_sorted.sort(reverse = self.is_reversed)

			# use the sorted data to place everything where it should be
			for column_holder in columns_sorted:
				col = column_holder[2]
				(name_delete, roll, mod, health) = col
				self.name_row.pack_start(name_delete, False, False, 0)
				self.init_roll_row.pack_start(roll, False, False, 0)
				self.init_mod_row.pack_start(mod, False, False, 0)
				self.health_row.pack_start(health, False, False, 0)
		except ValueError:
			print("invalid field somewhere!")

	# creates a combo box with options gathered from a python list
	def create_combo_box_from_list(self, items):
		combo = Gtk.ComboBoxText()
		combo.set_entry_text_column(0)
		for item in items:
			combo.append_text(item)
		combo.set_active(0)
		return combo

	# called when the order combo box is changed
	def order_changed(self, combo):
		if self.auto_update:
			text = combo.get_active_text()
			self.is_reversed = text.lower() == 'descending'
			self.update_order()

	def auto_update_toggled(self, toggle):
		self.auto_update = toggle.get_active()
		if self.auto_update: self.update_order()
	
	def entry_focus_left(self, entry, what_is_this_arg):
		if self.auto_update: self.update_order()



win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

