from subprocess import Popen
from os import system
import PySimpleGUI as sg
from psutil import process_iter
from os import path

comentario = ""

for proc in process_iter(["pid", "name"]):
    if proc.info["name"] == "ND_appCloser.exe":
        system(f"taskkill /f /pid {proc.info['pid']} >nul")


sg.theme("DarkGrey8")  # tema da interface
horas = [str(i).zfill(2) for i in range(24)]  # intervalo da seleção de horario
minutos = [str(i).zfill(2) for i in range(60)]  # intervalo da seleção de minuto

try:  # se o arquivo existir(erro caso estiver vazio):
    with open("./config.txt", "r") as arquivo:
        config = arquivo.read().split()  # cria uma lista com o conteúdo do arquivo
        print(config)
    print(len(config))
    if len(config) > 12:  # retira o comentario

        for n in range(12, len(config)):
            print(config[12])
            comentario += config[12] + " "
            del config[12]

    if config[0] == "False":
        config[0] = (
            False  # tranforma a str 'False' em booleano False, pois bool('False') = True
        )
    elif config[0] == "True":
        config[0] = True
    else:
        0 / 0

    for n in range(
        1, 5
    ):  # resolve caso nao existe ou nao corresponde das horas e minutos
        if str(config[n]).isnumeric():  # se for numerico
            if 0 > int(config[n]) or int(config[n]) > 60:  # se for maior que 60

                0 / 0
        else:
            0 / 0

    for n in range(5, 12):
        if config[n] == "False":
            config[n] = (
                False  # tranforma a str 'False' em booleano False, pois bool('False') = True
            )
        elif config[n] == "True":
            config[n] = True
        else:
            0 / 0

except:  # caso o try dê erro, no caso o arquivo existe mas está vazio:
    config = [
        False,
        "00",
        "00",
        "00",
        "00",
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]  # estado, hora, min

for n, x in enumerate(config):
    if x == "False":
        config[n] = (
            False  # tranforma a str 'False' em booleano False, pois bool('False') = True
        )
    elif x == "True":
        config[n] = True
print(config)


layout = [
    [
        sg.Checkbox("ativar/desativar programa", config[0])
    ],  # caixa de seleção ativar/desativar
    [
        sg.Combo(horas, default_value=config[1]),
        sg.Text(":"),
        sg.Combo(minutos, default_value=config[2]),
    ],  # seleção de horario inicial
    [sg.Text("Até")],
    [
        sg.Combo(horas, default_value=config[3]),
        sg.Text(":"),
        sg.Combo(minutos, default_value=config[4]),
    ],  # seleção de horario final
    [sg.Text("dom  seg     ter     qua     qui    sex    sab")],
    [
        sg.Checkbox("", config[5]),
        sg.Checkbox("", config[6]),
        sg.Checkbox("", config[7]),
        sg.Checkbox("", config[8]),
        sg.Checkbox("", config[9]),
        sg.Checkbox("", config[10]),
        sg.Checkbox("", config[11]),
    ],
    # [sg.Checkbox('não!', config[12])],
    [sg.Submit("Salvar e sair"), sg.Text("", key="-SALVO-")],
]  # Salvar dados


window = sg.Window(
    "config", layout, size=(282, 210)
)  # cria a interface com tamanho 220x145

# tela do PySimpleGui
while True:
    event, values = window.read()  # abre a interface
    if event == "Salvar e sair":
        window["-SALVO-"].update("Configurações salvas!")

    elif (
        event == sg.WIN_CLOSED or event == "Cancel"
    ):  # se o usuario fechar a janela ou clicar em cancelar
        break

    # atribui valores na lista para inserir no arquivo
    config[0] = str(values[0])
    for x in range(1, 5):
        config[x] = values[x]
    for x in range(5, 12):
        config[x] = str(values[x])


window.close()  # fecha a interface

# salva as informações no arquivo txt
with open("./config.txt", "w") as arquivo:
    for x in config:
        arquivo.write(f"{x}\n")
    # arquivo.write(f'\n {comentario}')

if not path.exists("./programs.txt"):
    with open("./programs.txt", "w") as programs:
        programs.write("")

if config[0] == "True":
    Popen(r".\ND_appCloser\ND_appCloser.exe", shell=True)
