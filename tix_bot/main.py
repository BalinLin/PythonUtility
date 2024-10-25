import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

# ocr packages
import base64
import ddddocr

getElement = lambda xpath : f"document.evaluate(\"{xpath}\", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null).snapshotItem(1)"

### 請先透過 cmd 輸入以下指令，開啟 chrome 遠端除錯功能，並且手動登入網站
### MacOS ###
# sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

### Windows ###
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%UserProfile%\Desktop\Chrome"

# indievox
programUrl = 'https://tixcraft.com/activity/game/24_jaychou'
# test = 'https://tixcraft.com/activity/game/24_p12tienmu'

# programUrl = test

if __name__ == "__main__":
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)

    while True:
        cmd = input("cmd: ")

        if cmd == 'bye':
            break

        if cmd == 'pay':
            form1 = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_strCardNo")
            form1.send_keys("--------")

            form2 = driver.find_element(By.ID, "check_num")
            form2.send_keys("---")

            select1 = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_strMM")
            select = Select(select1)
            select.select_by_value("--")

            select2 = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_strYY")
            select = Select(select2)
            select.select_by_value("----")

            # btn = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btn_box")
            # btn.click()

        if cmd == 'go':
            print(f"cmd == go")
            driver.get(programUrl)
            print(f"driver.get({programUrl})")
            # 持續按 "立即訂購"
            while True:
                try:
                    btn_next = driver.find_elements(By.XPATH, "//*[@id='gameList']//button")[0]
                    btn_next.click()
                    print("成功點到立即訂購")
                    break
                except Exception as e:
                    print("找不到按鈕重試中...")
                    time.sleep(0.05)

            # 要選位子
            while True:
                try:
                    element = driver.find_element(By.XPATH, "//li[contains(., '熱賣中') or contains(., '剩餘')]")
                    element.click()
                    # driver.execute_script(getElement(f"//li[contains(., '熱賣中')]/a") + ".click()")
                    print("成功點到位子立即訂購")
                    break
                except Exception as e:
                    print("找不到按鈕重試中...")
                    time.sleep(0.05)

            # 馬上選數量
            while True:
                try:
                    ticket_nums_select = driver.find_element(By.TAG_NAME, "select")
                    # 創建 Select 物件
                    select = Select(ticket_nums_select)
                    # 獲取所有選項
                    options = select.options
                    print(f"options={options}")
                    max_value = max(int(option.get_attribute("value")) for option in options)
                    print(f"max_value = {max_value}")
                    val = min(4, max_value)
                    select.select_by_value(str(val))
                    print("成功選數量")
                    break
                except Exception as e:
                    print("找不到選單重試中...")
                    time.sleep(0.05)

            # 馬上按同意
            while True:
                try:
                    checkbox = driver.find_element(By.ID, "TicketForm_agree")
                    if not checkbox.is_selected():
                        checkbox.click()
                    print("成功按同意")
                    break
                except Exception as e:
                    print("找不到同意重試中...")
                    time.sleep(0.05)

            # focus
            driver.execute_script("document.getElementById('TicketForm_verifyCode').focus();")
            submit_btn = driver.find_element(By.XPATH, "//button[text() = '確認張數']")

            while True:
                try:
                    # 查找驗證碼圖片元素
                    verify_image = driver.find_element(By.ID, "TicketForm_verifyCode-image")

                    # 使用 Selenium 的 screenshot_as_png 方法獲取圖片數據
                    image_data = verify_image.screenshot_as_png
                    print(type(image_data))
                    # 將圖片數據轉換為 Base64
                    image_base64 = base64.b64encode(image_data).decode('utf-8')

                    print("Try ocr")
                    print("start to ddddocr")
                    ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
                    orc_answer = ocr.classification(image_base64)
                    print("pass ocr answer", orc_answer)
                    vc_input = driver.find_element(By.ID, "TicketForm_verifyCode")
                    vc_input.clear()
                    vc_input.send_keys(orc_answer)  # 將 OCR 的答案輸入欄位

                    vc_text = driver.find_element(By.ID, "TicketForm_verifyCode").get_attribute('value')
                    if len(vc_text) == 4:
                        print("驗證碼已經輸入完畢")
                        # submit_btn.click()
                    else:
                        print("驗證碼還沒輸入完畢")
                    break
                except Exception as e:
                    print("找不到驗證碼重試中...")
                    # Refresh ocr id
                    verify_image = driver.find_element(By.ID, "TicketForm_verifyCode-image")
                    verify_image.click()
                    time.sleep(0.2)

            # 輸完驗證碼，開始準備尋找下一步
            while True:
                try:
                    # 付款方式
                    input_radio = driver.find_element(By.XPATH, "//input[@type='radio']")
                    input_radio.click()

                    btn_next = driver.find_element(By.ID, "submitButton")
                    # btn_next.click()
                    print("成功點到我同意本節目規則，下一步")

                    # 有可能會跳出選擇配送方式的 alert 那就忽略再按
                    has_alert = True
                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                    except Exception as e:
                        print("沒有 alert")
                        has_alert = False
                        break
                    if not has_alert:
                        break
                except Exception as e:
                    print("找不到按鈕重試中...")
                    time.sleep(0.05)