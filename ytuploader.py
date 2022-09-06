from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
import getpass
from time import sleep
import os
import glob
from bs4 import BeautifulSoup as bs
from timelist import horas
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


user = getpass.getuser()

url = 'https://studio.youtube.com/channel/'

meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

videoslist = glob.glob('videos/*')

def programar():
    try:
        # try:
        #     with open('data/timedate.json', 'r', encoding='UTF-8') as j:
        #         timedate = json.load(j)
            
        #     d = timedate['dia']
        #     m = timedate['mes']
        #     mes = str(m[:3] + '.').lower()
        #     ano = timedate['ano']
        #     horai = timedate['hora']
            
        # except FileNotFoundError:
        d = vdia.get()
        m = cbmes.get()
        ano = vano.get()
        mes = str(m[:3] + '.').lower()
        horai = cbhora.get()

        if d == '' or m == 'Escolha o mês' or ano == '' or horai == 'Escolha a hora de início':
            raise ValueError


        timedate = {}
        timedate['dia'] = d
        timedate['mes'] = m
        timedate['ano'] = ano
        timedate['hora'] = horai

        with open('data/timedate.json', 'w', encoding='UTF-8') as file:
            json.dump(timedate, file)

        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument(f"user-data-dir=C:/Users/{user}/AppData/Local/Google/Chrome/User Data/")
        service = Service(ChromeDriverManager().install())
        service.creationflags = CREATE_NO_WINDOW
        driver = Chrome(service=service, options=options)

        try:
            janela.withdraw()

            driver.get(url)

            wa = WebDriverWait(driver, 1000)

            wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="avatar-btn"]')))
            avatar_btn = driver.find_element(By.XPATH, '//*[@id="avatar-btn"]')
            avatar_btn.click()

            wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="items"]/ytd-compact-link-renderer[3]')))
            altern = driver.find_element(By.XPATH, '//*[@id="items"]/ytd-compact-link-renderer[3]')
            altern.click()

            sleep(1)

            page = driver.page_source
            soup = bs(page, 'html.parser')
            clist = soup.find_all('ytd-account-section-list-renderer')
            canais = clist[0].find_all('ytd-account-item-renderer', {'class':'style-scope ytd-account-item-section-renderer'})

            with open('data/video.txt', 'r', encoding='UTF-8') as v:
                vi = int(v.read())

            for i in range(vi, len(videoslist)):
                while True:
                    with open('data/video.txt', 'w', encoding='UTF-8') as file:
                        file.write(str(i))
                    try:
                        abspath = os.path.abspath(videoslist[i])

                        try:
                            with open('data/canal.txt', 'r', encoding='UTF-8') as file:
                                ini = int(file.read())
                        except FileNotFoundError:
                            ini = 0

                        for c in range(ini, len(canais)):
                            while True:
                                try:
                                    with open('data/canal.txt', 'w', encoding='UTF-8') as file:
                                        file.write(str(c))

                                    driver.get(url)

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="avatar-btn"]')))
                                    avatar_btn = driver.find_element(By.XPATH, '//*[@id="avatar-btn"]')
                                    avatar_btn.click()

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="items"]/ytd-compact-link-renderer[3]')))
                                    altern = driver.find_element(By.XPATH, '//*[@id="items"]/ytd-compact-link-renderer[3]')
                                    altern.click()

                                    xpath = '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer[1]/div[2]/ytd-account-item-section-renderer/div[2]/ytd-account-item-renderer[{}]'

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]')))
                                    canal = driver.find_element(By.XPATH, xpath.format(str(c+1)))
                                    canal.click()

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="upload-icon"]')))
                                    up = driver.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[2]/div[1]/ytcp-quick-actions/a[1]/ytcp-icon-button/tp-yt-iron-icon')
                                    up.click()

                                    video_input = driver.find_element(By.XPATH, '//*[@id="content"]/input')
                                    video_input.send_keys(abspath)

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="audience"]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')))
                                    conteudo = driver.find_element(By.XPATH, '//*[@id="audience"]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')
                                    conteudo.click()
                                    sleep(1)

                                    for a in range(3):
                                        wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="next-button"]')))
                                        prox1 = driver.find_element(By.XPATH, '//*[@id="next-button"]')
                                        prox1.click()
                                        sleep(1)

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="schedule-radio-button"]')))
                                    programar = driver.find_element(By.XPATH, '//*[@id="schedule-radio-button"]')
                                    programar.click()

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="datepicker-trigger"]/ytcp-dropdown-trigger')))
                                    databox = driver.find_element(By.XPATH, '//*[@id="datepicker-trigger"]/ytcp-dropdown-trigger')
                                    databox.click()

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-2"]/input')))
                                    data_input = driver.find_element(By.XPATH, '//*[@id="input-2"]/input')
                                    data_input.clear()
                                    data_input.send_keys(f'{d} de {mes} de 2022')
                                    data_input.send_keys(Keys.ENTER)

                                    hora_input = driver.find_element(By.XPATH, '//*[@id="input-1"]/input')
                                    # hora_input.click()
                                    hora_input.clear()
                                    hora_input.send_keys(horai)

                                    sleep(1)

                                    wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="done-button"]')))
                                    publicar = driver.find_element(By.XPATH, '//*[@id="done-button"]')
                                    publicar.click()

                                    sleep(2)

                                    break
                                except exceptions.UnexpectedAlertPresentException:
                                    sleep(5)
                                    continue

                        horai_list = horai.split(':')
                        h1 = horai_list[0]
                        h2 = horai_list[1]

                        h1 = int(h1)
                        h1 = h1+1
                        h1 = str(h1)

                        horai = f'{h1}:{h2}'

                        timedate['hora'] = horai

                        with open('data/timedate.json', 'w', encoding='UTF-8') as j:
                            json.dump(timedate, j)

                        with open('data/canal.txt', 'w', encoding='UTF-8') as f:
                            f.write('0')

                        break
                    except exceptions.UnexpectedAlertPresentException:
                        sleep(5)
                        continue

            with open('data/video.txt', 'w', encoding='UTF-8') as f:
                f.write('0')

            os.remove('data/timedate.json')

            driver.quit()
            messagebox.showinfo(title='Youtube Uploader', message='Vídeos programados com sucesso!')
            janela.destroy()
        except exceptions.NoSuchWindowException:
            janela.deiconify()
        except:
            messagebox.showerror(title='Youtube Uploader - ERRO!', message='Ocorreu um erro inesperado.\nVerifique se os dados informados estão corretos ou se sua conexão está funcionando.\nClique em "Ok" para voltar a tela inicial.')
            janela.deiconify()
    except ValueError:
        messagebox.showwarning(title='Youtube Uploader - ATENÇÃO!', message='Um ou mais dados não foram informados.')


janela = Tk()
janela.title('Youtube Uploader')
janela.resizable(False, False)
janela.iconbitmap('up.ico')

frame = LabelFrame(janela)
frame.pack(fill=BOTH, expand=False, padx=10, pady=10, ipadx=10, ipady=10)

Label(frame, text="Dia:").grid(column=0, row=0, pady=10, padx=5)
vdia = Entry(frame, bg='white', borderwidth=2, width=2)
vdia.grid(row=0, column=1)

cbmes = ttk.Combobox(frame, values=meses, state='readonly', width=13)
cbmes.set('Escolha o mês')
cbmes.grid(column=2, row=0, pady=10, padx=20)

Label(frame, text="Ano:").grid(column=3, row=0, pady=10)
vano = Entry(frame, bg='white', borderwidth=2, width=4)
vano.grid(column=4, row=0, padx=5, pady=10)

cbhora = ttk.Combobox(frame, values=horas, state='readonly', width=21)
cbhora.set('Escolha a hora de início')
cbhora.grid(columnspan=5, column=1, row=1, pady=10)

btnprogram = Button(frame, text='Iniciar', width=15, command=programar)
btnprogram.grid(row=2,columnspan=5, column=1, pady=10)

try:
    with open('data/timedate.json', 'r', encoding='UTF-8') as jsonfile:
        timedate = json.load(jsonfile)
    vdia.insert(0, timedate['dia'])
    vano.insert(0, timedate['ano'])
    cbmes.set(timedate['mes'])
    cbhora.set(timedate['hora'])
except FileNotFoundError:
    pass


janela.mainloop()


# print('Escolha a hora do final: ')
# for i, h in enumerate(horas):
#     print(f'{i}-{h}', end=' ')
# print()

# r2 = int(input())
# horaf = horas[r2]

