import flet as ft
from flet import *
import pandas as pd
import webbrowser
import urllib.parse
from functools import partial

class MyApp:
    def __init__(self):
        self.dict_login = {
            'Nome': '',
            'Sobrenome': '',
            'Loja': ''
        }
        self.endereco_dict = {
            "Loja A": "Rua blabla",
            "Loja B": "Avenida blabla",
            "Loja C": "Rodovia blabla"
        }
        self.cliente_dict = {}

    def abrir_whatsapp(self, numero, opcao_loja):
        nome_cliente = self.cliente_dict.get(numero, "Cliente.")
        mensagem = f"Olá, {nome_cliente}!\nAqui é a {self.dict_login['Nome']} do atendimento SUA MARCA. \nPassando para te falar que o atendimento SUA MARCA está perto de você no endereço {self.endereco_dict[opcao_loja]} e também aqui no WhatsApp."
        url = f"https://wa.me/55{numero}?text={urllib.parse.quote(mensagem)}"
        webbrowser.open(url)

    def main(self, page: ft.Page):
        page.window_width = 600
        page.scroll = ft.ScrollMode.AUTO

        #função upload
        def inativar_button(e):
            e.control.visible = False
            page.update()

            numero = e.control.text.replace('Enviar mensagem para ', '')
            self.abrir_whatsapp(numero, opcao_loja.value)

        def handle_file_upload(result_event: FilePickerResultEvent):
            if result_event.files:
                arquivo = result_event.files[0]
                file_path = arquivo.path
                dados = pd.read_excel(file_path)
                dados = dados[["Nome do cliente", "Numero de telefone"]]

                self.cliente_dict = dict(zip(dados["Numero de telefone"], dados["Nome do cliente"]))

                botao_upload.visible = False
            

                numeros = []
                for i, valores in dados.iterrows():
                    numero = valores["Numero de telefone"]
                    numeros.append(numero)

                # Criar botões de redirecionamento de WhatsApp para cada número
                for numero in numeros:
                            botao_wpp = FilledButton(text=f"Enviar mensagem para {numero}", on_click=inativar_button)
                            page.add(botao_wpp)


        def gera_saudacao(e):
            self.dict_login['Nome'] = Nome.value
            self.dict_login['Sobrenome'] = Sobrenome.value
            self.dict_login["Loja"] = opcao_loja.value

            # verifica se os valores foram todos preenchidos
            for i in self.dict_login.values():
                if not i:
                    page.banner.open = True
                    page.update()
                    return

            Nome.disabled = True
            Sobrenome.disabled = True
            opcao_loja.disabled = True
            greetings.controls.append(ft.Text(f"Olá, {Nome.value} {Sobrenome.value}.\nAgora atuando como: {opcao_loja.value}."))
            page.add(botao_upload)
            botao_arquivo.visible = False
            page.update()

        def fecha_banner(e):
            page.banner.open = False
            page.update()

        # itens da página
        titulo = Text(value="Olá Atendente, seja bem vindo(a)!", size=20, weight='bold')
        Nome = TextField(label="Nome", width=300)
        Sobrenome = TextField(label='Sobrenome', width=300)
        loja = Text(value="Por favor, selecione a loja", size=15)
        opcao_loja = ft.Dropdown( # BOTÃO DROPDOWN DE OPÇÕES
            width=300,
            options=[
                ft.dropdown.Option("Loja A"),
                ft.dropdown.Option("Loja B"),
                ft.dropdown.Option("Loja C"),
            ],
        )
        botao_arquivo = FilledButton(text="INCIAR")
        botao_upload = FilledButton(text="GERAR AGENDA")

        file_picker = ft.FilePicker()

        def handle_file_picker_click(e):
            file_picker.pick_files()

        botao_arquivo.on_click = gera_saudacao
        botao_upload.on_click = handle_file_picker_click
        greetings = ft.Column()

        file_picker.on_result = handle_file_upload

        page.overlay.append(file_picker)

        page.banner = Banner(
            bgcolor=colors.RED_300,
            leading=Icon(
                icons.DANGEROUS_OUTLINED,
                color=colors.RED_400
            ),
            content=Text('Por favor, preencha todos os campos'),
            actions=[
                TextButton("OK", on_click=fecha_banner)
            ]
        )

        # formatação da página
        page.padding = 30
        page.add(
            titulo, Nome, Sobrenome, loja, opcao_loja, botao_arquivo, greetings
        )

my_app = MyApp()
ft.app(target=my_app.main, upload_dir="uploads")