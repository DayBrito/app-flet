import flet as ft
import flet_material
import asyncio

# usuários pra validação 
user_dict = {'day@gmail.com': 123456, 'mari@gmail.com': 78910}



#
class MainFormUI(ft.UserControl):
    def __init__ (self):
        #

        #
        super().__init__()

    def build(self):
        return ft.Container(
            width=450,
            height=550,
            bgcolor=ft.colors.with_opacity(0.01, 'white'),
            border_radius=10,
            padding=40,
            

        )






def main(page: ft.Page):
    page.horizontal_alignment = 'center',
    page.vertical_alignment = 'center',

    #
    form = MainFormUI()

    #
    page.add(form)
    page.update()


#
if __name__ == '__main__':
    ft.app(target=main)
