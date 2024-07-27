import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GObject

class TwoItemRow(GObject.GObject):
    start_item = GObject.Property(type=str)
    end_item = GObject.Property(type=str)

    def __init__(self, start_item, end_item):
        super().__init__()
        self.start_item = start_item
        self.end_item = end_item

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("GtkColumnView Example")
        self.set_default_size(400, 300)

        # Create the list store with custom row type
        list_store = Gio.ListStore(item_type=TwoItemRow)
        list_store.append(TwoItemRow("Hello", "World"))
        list_store.append(TwoItemRow("Foo", "Bar"))
        list_store.append(TwoItemRow("Baz", "Qux"))

        # Create a single selection model
        selection_model = Gtk.SingleSelection(model=list_store)

        # Create the GtkColumnView
        column_view = Gtk.ColumnView.new(model=selection_model)

        # Function to setup factory for creating cell widgets
        def setup_factory(column_title, item_property):
            factory = Gtk.SignalListItemFactory()
            factory.connect('bind', lambda factory, list_item: list_item.set_child(
                Gtk.Label(label=list_item.get_item().get_property(item_property))))
            column = Gtk.ColumnViewColumn(title=column_title, factory=factory)
            column_view.append_column(column)

        # Setup columns
        setup_factory("Start Item", "start_item")
        setup_factory("End Item", "end_item")

        # Add the column view to the window
        self.set_child(column_view)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
