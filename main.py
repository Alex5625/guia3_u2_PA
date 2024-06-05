import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GObject


APPID = 'com.fabio.duran.liststore'


class Row(GObject.Object):

    def __init__(self, num, name, age):
        super().__init__()
        self.num = num
        self.name = name
        self.age = age


class Gtk4TestTest(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(
            self, application=app, title='Columnview Test')

        self.model = Gio.ListStore()
        self.model.append(Row(1, 'Pepito', 40))
        self.model.append(Row(2, 'Maria', 30))
        self.model.append(Row(3, 'Luna', 20))
        



        # Menu
        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)
        self.set_title("Guía 3")

        # Listado del menu
        menu = Gio.Menu.new()

        # Create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # crea un menu
        self.menu_popover = Gtk.MenuButton()
        self.menu_popover.set_popover(self.popover)
        self.menu_popover.set_icon_name("open-menu-symbolic")



        # Add an about dialog
        about_menu = Gio.SimpleAction.new("about", None)
        about_menu.connect("activate", self.show_about_dialog)
        self.add_action(about_menu)
        menu.append("Acerca de", "win.about")

        #----------Treeview celdas---------------------------------
        smodel = Gtk.SingleSelection(model=self.model)
        smodel.connect("selection-changed", self.on_selected_items_changed)

        self.columnview = Gtk.ColumnView()
        self.columnview.set_model(smodel)

        factory1 = Gtk.SignalListItemFactory()  
        factory1.connect("setup", self.on_list_item_setup)
        factory1.connect("bind", self.on_list_item_bind, 1)
        self.column1 = Gtk.ColumnViewColumn(title='Código', factory=factory1)
        self.column1.set_resizable(True)
        self.column1.set_expand(True)

        factory2 = Gtk.SignalListItemFactory()
        factory2.connect("setup", self.on_list_item_setup)
        factory2.connect("bind", self.on_list_item_bind, 2)
        self.column2 = Gtk.ColumnViewColumn(title='Nombre', factory=factory2)
        self.column2.set_resizable(True)
        self.column2.set_expand(True)

        factory3 = Gtk.SignalListItemFactory()
        factory3.connect("setup", self.on_list_item_setup)
        factory3.connect("bind", self.on_list_item_bind, 3)
        self.column3 = Gtk.ColumnViewColumn(title='Edad', factory=factory3)
        self.column3.set_resizable(True)
        self.column3.set_expand(True)
        self.set_child(self.columnview)
        #----------Treeview celdas---------------------------------


        #Botones Header bar --------------------------------------
        self.boton_limpiar = Gtk.Button()
        self.boton_limpiar.set_label("Limpiar")
        self.boton_limpiar.connect("clicked", self.on_clicked_clean_list)

        self.boton_guardar = Gtk.Button()
        self.boton_guardar.set_label("Guardar")
        self.boton_guardar.connect("clicked", self.on_clicked_open_dialog)
        
        
        self.boton_agregar = Gtk.Button()
        self.boton_agregar.set_label("Agregar")
        self.boton_agregar.connect("clicked", self.on_clicked_save_list)

        #Botones Header bar --------------------------------------
        
        #Orden de añadidura:-------------------------------------

        header_bar.pack_end(self.menu_popover)
        header_bar.pack_start(self.boton_agregar)
        header_bar.pack_start(self.boton_guardar)
        header_bar.pack_start(self.boton_limpiar)

        self.columnview.append_column(self.column1)
        self.columnview.append_column(self.column2)
        self.columnview.append_column(self.column3)
        
        #------------------------------------------------------------


    def on_clicked_save_list(self,widget):

        # ------crear mensaje de dialogo ---------
        dialog = Gtk.MessageDialog(title="Añadir Columnas",
                                   transient_for=self,
                                   modal=True,
                                   default_width=300,
                                   default_height=50)

        self.entry1 = Gtk.Entry()
        self.entry1.set_placeholder_text("Columna 1")
        dialog.get_content_area().append(self.entry1)

        self.entry2 = Gtk.Entry()
        self.entry2.set_placeholder_text("Columna 2")
        dialog.get_content_area().append(self.entry2)

        self.entry3 = Gtk.Entry()
        self.entry3.set_placeholder_text("Columna 3")
        dialog.get_content_area().append(self.entry3)

        dialog.add_buttons("Guardar", Gtk.ResponseType.OK,
                           "No Guardar", Gtk.ResponseType.CLOSE)
        
        dialog.set_deletable(True)

        dialog.connect("response", self.on_response_dialog_columns)
        
        dialog.set_visible(True)

        pass


    def on_response_dialog_columns(self, widget, response):
        # print(response)

        dialog = Gtk.FileDialog.new()

        #SI APRETO GUARDAR
        if response == Gtk.ResponseType.OK:
            #guardar archivo
            print("ingresa datos al treeview")
            self.save_list_on_treeview()

        #SI LE PONE Q NO QUIERE GUARDAR
        elif response == Gtk.ResponseType.CLOSE:
            #no guardar el archivo
            print("No se agrego nada")

        #SI APRETO NINGUNA DE LAS 2     
        elif response == Gtk.ResponseType.DELETE_EVENT:
            print("Te saliste apretando ESC")
        #widget.destroy()
        widget.set_visible(False)

    def save_list_on_treeview(self):
        #usar buffer para sacar los datos
        self.columna_1  = int(self.entry1.get_text())
        self.columna_2  = self.entry2.get_text()
        self.columna_3  = int(self.entry3.get_text())
        print(f"Los textos a ingresar son: {self.columna_1}, {self.columna_2}, {self.columna_3}")

        #usar el model para agregar los datos

        self.model.append(Row(self.columna_1,self.columna_2, self.columna_3))

    def on_clicked_clean_list(self,widget):

        #eliminar datos del model !!!!!
        self.model.remove_all()
        pass



    def on_clicked_open_dialog(self,widget):

        # ------crear mensaje de dialogo ---------
        dialog = Gtk.MessageDialog(title="Ventana de guardado",
                                   transient_for=self,
                                   modal=True,
                                   default_width=300,
                                   default_height=50)

        dialog.add_buttons("Guardar", Gtk.ResponseType.OK,
                           "No Guardar", Gtk.ResponseType.CLOSE)
        
        dialog.set_deletable(True)

        dialog.connect("response", self.on_response_dialog_save)
        
        dialog.set_visible(True)

        pass


#ACCIONES Q HACER SI APRETA X BOTON EN EL DIALOGO
    def on_response_dialog_save(self, widget, response):
        # print(response)

        dialog = Gtk.FileDialog.new()
        if response == Gtk.ResponseType.OK:
            #guardar archivo
            print("VOY A GUARDAR EL ARCHIVO")
            dialog.save(self, None, self.save_dialog_open_response)
        elif response == Gtk.ResponseType.CLOSE:
            #no guardar el archivo
            print("NO QUISITE GUARDAR EL ARCHIVO")
        elif response == Gtk.ResponseType.DELETE_EVENT:
            print("Te saliste apretando ESC")
        #widget.destroy()
        widget.set_visible(False)

#GUARDA EL ARCHIVO
    def save_dialog_open_response(self, widget, response):
        texto = ""
        archivo = widget.save_finish(response)
        print(f"File path is {archivo.get_path()}")

        #sacar datos del liststore

        for i in range(self.model.get_n_items()):
            item = self.model.get_item(i)
            print(item)
            texto += str(item.num) + "," + item.name + "," + str(item.age) + "\n"
        #print(f"{row_data}")
        # guardar = self.texto.get_text()

        with open(archivo.get_path(), "w") as archivo:
            archivo.write(texto)



    def show_about_dialog(self, action, param):

        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Alex_5625"])
        self.about.set_copyright("Copyright 2024 Alexis")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("https://www.instagram.com/mrm00ns?igsh=dWFkZnk2Y3ZtdTVj")
        self.about.set_website_label("Mi instagram")
        self.about.set_version("2.0")
        self.about.set_logo_icon_name("example")
        self.about.set_visible(True)


    def on_selected_items_changed(self, selection, position, n_items):
        selected_item = selection.get_selected_item()
        if selected_item is not None:
            print(
                f"nombre:{selected_item.name} " +
                f"edad:{selected_item.age}")

    def on_list_item_setup(self, factory, item):
        label = Gtk.Inscription()
        item.set_child(label)

    def on_list_item_bind(self, factory, item, i):
        print(item)
        match i:
            case 1:
                item.get_child().set_text(str(item.get_item().num))
            case 2:
                item.get_child().set_text(item.get_item().name)
            case 3:
                item.get_child().set_text(str(item.get_item().age))


class Gtk4TestApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self, application_id=APPID)

    def do_activate(self):
        window = Gtk4TestTest(self)
        window.present()


def main():
    app = Gtk4TestApp()
    app.run()


if __name__ == '__main__':
    main()

