from time import sleep
from datetime import datetime
from psutil import process_iter, pid_exists
import subprocess
from os import path, getcwd
import json


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

pastaAtual = str(path.basename(getcwd()))
if pastaAtual == "ND_appCloser":
    urlConfig = r"..\config.json"  # pasta anterior
    urlPrograms = r"..\programs.txt"  # pasta anterior
else:
    urlConfig = "config.json"  # mesma pasta
    urlPrograms = "programs.txt"  # mesma pasta

try:  # obtém os dados do config.json
    with open(urlConfig, "r") as file:
        config_data = json.load(file)

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
    )


except:  # caso o try dê erro, no caso o arquivo existe mas está vazio:
    config = Config()


# retorna uma lista com os pids dos programas
def get_pid(p):
    pidlist = []
    for proc in process_iter(["pid", "name"]):
        if proc.info["name"] in p:
            pidlist.append(proc.info["pid"])
    if pidlist:
        return pidlist


# adiciona os ".exe" ao final de cada nome de programa no arquivo
def addExe(program):
    return program + ".exe"


# retorna hora e minuto
def get_hora():
    horario = datetime.today()  # obtém o horario
    h, min = list(map(int, horario.strftime("%H %M").split()))
    weekday = horario.strftime("%A")
    return h, min, weekday  # retorna uma lista com hora, minuto atual e dia da semana


pid = int()
pids = list()

semana = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
h, min, ddsemana = get_hora()
ddsemana = semana.index(ddsemana)
tempo_agr = h * 60 + min
tempo1 = int(config.hora_inicial) * 60 + int(config.minuto_inicial)
tempo2 = int(config.hora_final) * 60 + int(config.minuto_final)


# verificar a url atual para obter os arquivos. a url atual do appCloser muda se for iniciada diretamente ou pela interface

semanaConfig = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]
estado = getattr(config, semanaConfig[ddsemana])

acessoNegado = []
while tempo_agr <= tempo2:
    with open(urlPrograms, "r") as arquivo:
        pBruto = arquivo.read().split()
        p = list(map(addExe, pBruto))
    if estado == True:
        print(tempo_agr, tempo1, tempo2)
        if tempo1 <= tempo_agr:
            print("check 1")
            t = 5
            tempo_agr = h * 60 + min
            try:
                pids = get_pid(p)
            except:
                pass
            print(get_pid(p))
            if pids:
                print("check 2")
                for x in pids:
                    try:
                        if pid_exists(x) and x not in acessoNegado:
                            killerCheck = subprocess.Popen(
                                f"taskkill /f /pid {x}",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                            )
                            saida, erro = killerCheck.communicate()
                            # caso nao dê acesso negado
                            if "negado" in erro.decode(
                                "latin1"
                            ):  # finaliza o programa através do pid
                                # sys(f"taskkill /f /pid {x} >nul")
                                acessoNegado.append(x)
                    except:
                        pass
                # if config[12] == "True":
                # nao()
            else:
                # print(f'não possui nenhum processo destes aberto')
                pass
        else:
            t = 30
    else:
        t = 300
    sleep(t)
    h, min, ddsemana = get_hora()
    ddsemana = semana.index(ddsemana)
    estado = getattr(config, semanaConfig[ddsemana])

