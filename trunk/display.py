#! /usr/bin/python
#
#      Display.py version 0.0.1
#         (c) 2006 Blug.in
#
#       Insert GPL Here
#
#	Changelog:
#		Original Class message Defined by 
#				Tejas Dinkar <tejasdinkar AT gmail DOT com>


class message:
	def destroy(self,*args):
		import gtk
		self.box.destroy()
		gtk.main_quit()
	
	def __init__(self,title, message):
		import gtk
		self.box = gtk.Dialog(title)
		self.button = self.box.add_button("OK",gtk.BUTTONS_OK)
		self.box.vbox.set_size_request(325,175)
		self.buffer = gtk.TextBuffer()
		self.buffer.set_text(message)
		self.scroll = gtk.ScrolledWindow()
		self.text = gtk.TextView(self.buffer)
		self.text.set_editable(False)
		self.text.set_cursor_visible(False)
		self.scroll.add(self.text)
		self.box.connect("delete_event",self.destroy)
		self.button.connect("clicked",self.destroy)
		self.box.vbox.add(self.scroll)
		self.box.show_all()
		gtk.main()

if __name__ == '__main__':
	message("Hello World!", """\
Hello to all.
This App is (c) 2006 BLUG
The Bangalore Linux User's Group""")
