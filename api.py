import os
import json
import pandas as pd
import shutil
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import random
import tqdm
from bs4 import BeautifulSoup
import flask

class MyDriver:

    def __init__(self, tabnum=1, headless=False):
        options = webdriver.ChromeOptions()
        options.add_extension("translate_extension.crx")
        options.add_argument("--lang=vi")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'vi'})
        # options.add_argument("--window-size=1600,900")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        self.tabnum = tabnum
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options) 
        self.warm_up()
        

    def turn_off(self):
        self.driver.quit()
        
    
    def go_to(self, link):
        self.driver.get(link)
        time.sleep(7)

    def warm_up(self):
        self.driver.get("https://www.wikipedia.org/")
        ####### Vietnamese Warmup #####
        time.sleep(1)
        actionChains = ActionChains(self.driver)
        h1_tag = self.driver.find_element(By.TAG_NAME, "h1")
        actionChains.context_click(h1_tag).perform()
        time.sleep(1)
        for _ in range(8):
            pyautogui.press('down')
            time.sleep(0.01)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('v')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('tab')
        time.sleep(0.5)
        pyautogui.press('enter')
        for i in range(self.tabnum-1):
            pyautogui.hotkey('ctrl', 't')
            time.sleep(0.5)
        #########################
TAB_NUM = 4
u = MyDriver(tabnum=TAB_NUM)

from flask import jsonify, make_response, Response
from flask import request
from flask import Flask
app = Flask(__name__)

prefix = """\
<!DOCTYPE html>
<html>
<body>
<h1></h1>
"""
suffix = "</br>"*200 + """
<h2></h2>
</body>
</html>
"""

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start_driver',methods=['POST'])
def start_driver():
    global u
    data = request.form.to_dict()
    tab_num = int(data["tab_num"])
    u = MyDriver(tabnum=tab_num)
    return make_response("ok", 200)

@app.route('/restart_driver',methods=['POST'])
def restart_driver():
    global u
    u.turn_off()
    data = request.form.to_dict()
    tab_num = int(data["tab_num"])
    u = MyDriver(tabnum=tab_num)
    return make_response("ok", 200)

@app.route('/stop_driver',methods=['POST'])
def stop_driver():
    global u
    u.turn_off()
    return make_response("ok", 200)

@app.route('/translate',methods=['POST'])
def translate():
    global u
    data = request.form.to_dict()
    input_data = json.loads(data["input"])
#     print(input_data)
    TAB_NUM = len(u.driver.window_handles)
    interval_tuple = []
    SAMPLE_PER_PAGE = len(input_data)//TAB_NUM
    for i in range(len(input_data)//SAMPLE_PER_PAGE):
        interval_tuple.append([i*SAMPLE_PER_PAGE, i*SAMPLE_PER_PAGE+(SAMPLE_PER_PAGE-1)])
    interval_tuple[-1][1] = len(input_data)-1
    ######### mkdir temp #######################
    cur_path = os.getcwd()
    html_truoc_khi_dich = os.path.join(cur_path, "html_truoc_khi_dich_temp")
    if os.path.exists(html_truoc_khi_dich):
        shutil.rmtree(html_truoc_khi_dich)
    os.makedirs(html_truoc_khi_dich, exist_ok=True)
    ###### create html files ###################
    ukey = []
    en_mapping_by_id = {}
    for x in input_data:
        if x.keys() not in ukey:
            ukey.append(x.keys())

    if len(ukey) != 1:
        print("WARNING")
    else:
        print("STEP 1 ...")
        ukey = list(ukey[0])
        for inter in interval_tuple:
            content = ""
            for i in range(inter[0], inter[1] +1):
                row = input_data[i]
                content += """<div class="data">\n"""
                content += f"""\t<h3>{i}</h3>\n"""
                for uk in ukey:
                    content += f"""\t<p class="{uk}">{row[uk]}</p>\n"""
                content += "</div></br>\n"
                en_mapping_by_id[i] = row
            content = f"{prefix}{content}{suffix}"
            with open(f"{html_truoc_khi_dich}/{inter[0]}_{inter[1]}.html", "w", encoding='utf-8') as fo:
                fo.write(content)
                fo.close()
        # time.sleep(10000)
        print("STEP 2 ...")
    ###### task schedule ######################
    json_files_path = "./"
    to_do_file = []
    for file in os.listdir(html_truoc_khi_dich):
        #### Get file list #####
        output_file = f"""{json_files_path}/{file}.json"""
        if os.path.exists(output_file):
            print(output_file)
            continue
        to_do_file.append(file)
    to_do_tab_list = []
    for group_index in range(0,len(to_do_file)//TAB_NUM):
        to_do_tab_list.append(to_do_file[group_index*TAB_NUM:(group_index+1)*TAB_NUM])
    print(to_do_tab_list)
    #############################################
    for files in tqdm.tqdm(to_do_tab_list):
        tab_map = {}
        for i in range(len(u.driver.window_handles)):
            #u.driver.switch_to.window(u.driver.window_handles[0])
            file = files[i]
            output_file = f"""{json_files_path}/{file}.json"""
            file_path = f"{html_truoc_khi_dich}/{file}"
            tab_map[u.driver.window_handles[i]] = {}
            tab_map[u.driver.window_handles[i]]["file_path"]   = file_path
            tab_map[u.driver.window_handles[i]]["output_file"] = output_file
        time.sleep(0.5)
        for i in range(len(u.driver.window_handles)):
            u.driver.switch_to.window(u.driver.window_handles[i])
            u.go_to(f"file:///"+tab_map[u.driver.window_handles[i]]["file_path"])
            actionChains = ActionChains(u.driver)
            h1_tag = u.driver.find_element(By.TAG_NAME, "h1")
            actionChains.context_click(h1_tag).perform()
            time.sleep(0.5)
            for _ in range(7):
                pyautogui.press('down')
                time.sleep(0.01)
            pyautogui.press("enter")

            time.sleep(0.5)
            elem = WebDriverWait(u.driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )
            footer_y = u.driver.find_element(By.TAG_NAME, "h2").location['y']
            tab_map[u.driver.window_handles[i]]["footer_y"] = footer_y
            tab_map[u.driver.window_handles[i]]["scroll_count"] = 0

        scroll_speed = 150 * TAB_NUM

        done_tab_list = []
        while len(done_tab_list) < TAB_NUM :
            for i in range(len(u.driver.window_handles)):
                if tab_map[u.driver.window_handles[i]]["scroll_count"] < tab_map[u.driver.window_handles[i]]["footer_y"] :
                    u.driver.switch_to.window(u.driver.window_handles[i])
                    tab_map[u.driver.window_handles[i]]["scroll_count"] += scroll_speed
                    u.driver.execute_script(f"window.scrollTo(0, "+str(tab_map[u.driver.window_handles[i]]["scroll_count"])+");")
                    time.sleep(0.01)
                else:
                    done_tab_list.append(u.driver.window_handles[i])
                    done_tab_list = list(set(done_tab_list))

        time.sleep(1)
        print("Scroll done !")

        for i in range(len(u.driver.window_handles)):
            u.driver.switch_to.window(u.driver.window_handles[i])  
            output = []
            soup = BeautifulSoup(u.driver.page_source, "html.parser")
            div_tags = soup.find_all("div",{"class":"data"})
            for div_tag in tqdm.tqdm(div_tags):
                mapping_id = div_tags[0].h3.text
                x = {
                    "mapping_id":mapping_id
                }
                for uk in ukey:
                    x[uk] = div_tag.find("p",{"class":uk}).text
                output.append(x)

            tab_map[u.driver.window_handles[i]]["output"] = output

    ############ postprocess output ############################################
    output_list = []
    for tab_id in tab_map:
        for sample in tab_map[tab_id]["output"]:
            output_list.append({"vi":sample,
                                "en":en_mapping_by_id[int(sample["mapping_id"])]
                               })
    
    return make_response(jsonify(output_list), 200)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8889)
