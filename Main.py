from dearpygui.dearpygui import *
import q
from Manager.Database_Manager import DBM
from Handbook.Rules import Rules
from Manager.Item_Manager import ItemManager
from Frontend.On_Start import ui_start

get_path = q.get_path





def on_exit_callback():
    q.dbm.Save_out
    save_init_file(get_path("utils", "config_save.ini"))
    stop_dearpygui()


def startup():
    q.idm = ItemManager()
    q.rules = Rules()
    q.dbm=DBM()
    q.cbh = q.dbm.cbh.callback_func()
    ui_start()
    q.dbm.Startup


def main():

    create_context()
    with font_registry(): font_choice = add_font(get_path("utils", "Helvetica.ttf"), 13)
    configure_app(init_file=get_path("utils", "config_save.ini"), docking=True, docking_space=True)
    create_viewport(title="rpg", width=1450, height=880)
    set_viewport_pos((20, 20))
    set_exit_callback(on_exit_callback)
    bind_font(font_choice)
    setup_dearpygui()
    
    startup()
    
    show_viewport()
    start_dearpygui()
    destroy_context()



if __name__ == '__main__':
    main()