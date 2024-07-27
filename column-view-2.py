import sys
import gi

gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')

from gi.repository import Adw, Gtk, Gio, GObject


class Person(GObject.GObject):
    person_id = GObject.Property(type=str, default='')
    person_name = GObject.Property(type=str, default='')

    def __init__(self, person_id, person_name):
        super().__init__()
        self.set_property('person_id', person_id)
        self.set_property('person_name', person_name)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Dynamic MVC GTK4 Example")
        self.set_default_size(400, 300)

        # Main layout container
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(layout)

        # Prepare the model
        self.model = Gio.ListStore(item_type=Person)
        nodes = [
            (1, "Clark Kent"),
            (2, "Bruce Wayne"),
            (3, "Barry Allen"),
        ]
        for person_id, name in nodes:
            self.model.append(Person(person_id=person_id, person_name=name))

        # Set up selection and view
        selection_model = Gtk.SingleSelection(model=self.model)
        column_view = Gtk.ColumnView.new(model=selection_model)
        layout.append(column_view)
        column_view.set_hexpand(True)
        column_view.set_vexpand(True)

        # Create factories for each column
        id_factory = Gtk.SignalListItemFactory()
        id_factory.connect("setup", self._on_factory_setup)
        id_factory.connect("bind", self._on_factory_bind_id)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self._on_factory_setup)
        name_factory.connect("bind", self._on_factory_bind_name)

        # Create and add columns, ID column first
        id_column = Gtk.ColumnViewColumn(title="ID", factory=id_factory)
        name_column = Gtk.ColumnViewColumn(title="Name", factory=name_factory)
        column_view.append_column(id_column)
        column_view.append_column(name_column)

        # Button to update names
        update_button = Gtk.Button(label="Update Names")
        update_button.connect("clicked", self.update_names)
        update_button.set_halign(Gtk.Align.CENTER)
        layout.append(update_button)
        update_button.set_margin_top(0)
        update_button.set_margin_bottom(6)
        update_button.set_margin_start(6)
        update_button.set_margin_end(6)

    @staticmethod
    def _on_factory_setup(factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    @staticmethod
    def _on_factory_bind_id(factory, list_item):
        label = list_item.get_child()
        person = list_item.get_item()
        label.set_text(str(person.get_property("person_id")))

    @staticmethod
    def _on_factory_bind_name(factory, list_item):
        label = list_item.get_child()
        person = list_item.get_item()
        person.bind_property("person_name", label, "label", GObject.BindingFlags.SYNC_CREATE)

    def update_names(self, button):
        for person in self.model:
            new_name = person.person_name + " Updated"
            person.set_property("person_name", new_name)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
