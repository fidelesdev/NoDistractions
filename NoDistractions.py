from subprocess import Popen
from os import system
import PySimpleGUI as sg
from psutil import process_iter
from os import path
import json
from sys import exit


for proc in process_iter(["pid", "name"]):
    if proc.info["name"] == "ND_appCloser.exe":
        system(f"taskkill /f /pid {proc.info['pid']} >nul")


sg.theme("DarkGrey8")  # tema da interface
horas = [str(i).zfill(2) for i in range(24)]  # intervalo da seleção de horario
minutos = [str(i).zfill(2) for i in range(60)]  # intervalo da seleção de minuto


class Config:
    def __init__(
        self,
        estado: bool = False,
        hora_inicial: int = 0,
        minuto_inicial: int = 0,
        hora_final: int = 0,
        minuto_final: int = 0,
        dom: bool = False,
        seg: bool = False,
        ter: bool = False,
        qua: bool = False,
        qui: bool = False,
        sex: bool = False,
        sab: bool = False,
        programs: str = "",
    ) -> None:
        self.estado = estado
        self.hora_inicial = hora_inicial
        self.minuto_inicial = minuto_inicial
        self.hora_final = hora_final
        self.minuto_final = minuto_final
        self.dom = dom
        self.seg = seg
        self.ter = ter
        self.qua = qua
        self.qui = qui
        self.sex = sex
        self.sab = sab
        self.programs = programs
        


try:  # obtém os dados do config.json
    with open("config.json", "r") as file:
        config_data = json.load(file)
    print(config_data)
    config = Config(
        estado=config_data["estado"],
        hora_inicial=config_data["hora_inicial"],
        minuto_inicial=config_data["minuto_inicial"],
        hora_final=config_data["hora_final"],
        minuto_final=config_data["minuto_final"],
        dom=config_data["dom"],
        seg=config_data["seg"],
        ter=config_data["ter"],
        qua=config_data["qua"],
        qui=config_data["qui"],
        sex=config_data["sex"],
        sab=config_data["sab"],
        programs=config_data["programs"]
    )


except:  # caso o try dê erro, no caso o arquivo existe mas está vazio:
    config = Config()


print(config)


layout = [
    [
        sg.Checkbox("ativar/desativar programa", config.estado)
    ],  # caixa de seleção ativar/desativar
    [
        sg.Combo(horas, default_value=str(config.hora_inicial).zfill(2)),
        sg.Text(":"),
        sg.Combo(minutos, default_value=str(config.minuto_inicial).zfill(2)),
    ],  # seleção de horario inicial
    [sg.Text("Até")],
    [
        sg.Combo(horas, default_value=str(config.hora_final).zfill(2)),
        sg.Text(":"),
        sg.Combo(minutos, default_value=str(config.minuto_final).zfill(2)),
    ],  # seleção de horario final
    [sg.Text("dom  seg     ter     qua     qui    sex    sab")],
    [
        sg.Checkbox("", config.dom),
        sg.Checkbox("", config.seg),
        sg.Checkbox("", config.ter),
        sg.Checkbox("", config.qua),
        sg.Checkbox("", config.qui),
        sg.Checkbox("", config.sex),
        sg.Checkbox("", config.sab),
    ],
    [sg.Text("Digite os programas que serão fechados:")],
    [sg.Multiline(config.programs, size=(150,1),expand_y=True)],
    [sg.Cancel("Cancelar"),sg.Submit("Salvar",button_color="#24a"), sg.Text("", key="-SALVO-")],
]  # Salvar dados


window = sg.Window(
    "NoDistractions", layout, size=(282, 330), icon="/icon.ico"
)  # cria a interface com tamanho 282x210

# tela do PySimpleGui
while True:
    global novaConfig
    event, values = window.read()  # abre a interface
    if event == "Salvar":
        window["-SALVO-"].update("Configurações salvas!")
    # se o usuario fechar a janela ou clicar em cancelar
    elif event == sg.WIN_CLOSED or event == "Cancelar":
        if "novaConfig" not in globals():  # caso nao existir a instância da NovaConfig, logo, não ter salvo
            exit() #encerra todo o resto do programa, não salvou da nisso fi
        break

    # atribui valores na lista para inserir no arquivo
    novaConfig = Config(
        values[0],
        values[1],
        values[2],
        values[3],
        values[4],
        values[5],
        values[6],
        values[7],
        values[8],
        values[9],
        values[10],
        values[11],
        values[12]
    )
    print(values)
    print(values[0])
    print(type(values[0]))

window.close()  # fecha a interface

# salva as informações no arquivo txt
print(novaConfig)
with open("./config.json", "w") as arquivo:
    json.dump(vars(novaConfig), arquivo, indent=4)
    #Config -> dict

#! if not path.exists("./programs.txt"):
#!     with open("./programs.txt", "w") as programs:
#!         programs.write("#A cada nome de programa pule uma linha")

if novaConfig.estado:
    print("aq ta bom")
    Popen(r".\ND_appCloser\ND_appCloser.exe", shell=True)
