from time import sleep
from datetime import datetime
from os import system as sys
from tkinter import Tk, Label
from psutil import process_iter, pid_exists
from PIL import Image, ImageTk
import subprocess

# retorna uma lista com os pids dos programas


def get_pid(p):
    pidlist = []
    for proc in process_iter(['pid', 'name']):
        if proc.info['name'] in p:
            pidlist.append(proc.info['pid'])
    if pidlist:
        return pidlist
# retorna hora e minuto


def get_hora():
    horario = datetime.today()  # obtém o horario
    h, min = list(map(int, horario.strftime("%H %M").split()))
    weekday = horario.strftime("%A")
    return h, min, weekday  # retorna uma lista com hora, minuto atual e dia da semana

# abre a imagem


def nao():
    try:
         # cria a variavel pra imagem
        imagem = Image.open('../nao.PNG')
        # converte a imagem para o tipo PhotoImage(suportado pelo Tkinter)
        imagem = ImageTk.PhotoImage(imagem)
        # cria a janela
        janela = Tk()
        janela.overrideredirect(True)  # retira as bordas
        # posição da imagem
        # obtém a posição para fica no x central da tela
        x = int((janela.winfo_screenwidth() - imagem.width()) / 2)
        # obtém a posição para fica no y central da tela
        y = int((janela.winfo_screenheight() - imagem.height()) / 2)
        janela.geometry(f'+{x}+{y}')  # define o local da imagem na tela
        # cria o elemento de GUI (interface gráfica do usuário)
        label = Label(janela, image=imagem)
        label.pack()  # configura a posição do widget na janela
        janela.wm_attributes("-topmost", True)  # deixa a janela acima das outras
        # após 5seg, executa a função da referencia no 2° argumento
        janela.after(2500, janela.destroy)
        janela.mainloop()  # abre a imagem
    except:
        pass


pid = int()
pids = list()
semana = ['Sunday', 'Monday', 'Tuesday',
          'Wednesday', 'Thursday', 'Friday', 'Saturday']
with open('../config.txt', 'r') as arquivo:
    config = arquivo.read().split()


for x in range(1, 5):
    config[x] = int(config[x])

h, min, ddsemana = get_hora()
ddsemana = semana.index(ddsemana)
tempo_agr = h*60 + min
tempo1 = config[1]*60 + config[2]
tempo2 = config[3]*60 + config[4]

for x in range(5, 12):
    if config[x] == 'True':
        config[x] = True

if config[0] == 'True' and config[ddsemana + 5] == True:
    estado = True
else:
    estado = False

acessoNegado = []
while tempo_agr <= tempo2:
    with open('../programs.txt', 'r') as arquivo:
        p = arquivo.read().split()
    if estado == True:
        print(tempo_agr, tempo1, tempo2)
        if tempo1 <= tempo_agr:
            print('check 1')
            t = 5
            tempo_agr = h * 60 + min
            try:
                pids = get_pid(p)
            except:
                pass
            print(get_pid(p))
            if pids:
                print('check 2')
                for x in pids:
                    try:
                        if pid_exists(x) and x not in acessoNegado:
                            killerCheck = subprocess.Popen(f"taskkill /f /pid {x}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            saida, erro = killerCheck.communicate()
                            # caso nao dê acesso negado
                            if "negado" in erro.decode('latin1'): #finaliza o programa através do pid
                                # sys(f"taskkill /f /pid {x} >nul")
                                acessoNegado.append(x)
                    except:
                        pass 
                if config[12] == "True":
                    nao()
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
    if config[0] == 'True':
        if config[ddsemana + 5] == True:
            estado = True
    else:
        estado = False
