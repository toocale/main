import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
url="chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html"
def unlock_okx(driver):
    # Open MetaMask UI (this is the main entry point)
    while True:
        try:
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller to initialize OKX Wallet")
            driver.get(url)
            time.sleep(2)
            # Wait for the password input field to appear
            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,':r1:')))
            # Enter the password (replace with your actual MetaMask password)
            password = "qwerty123"  # Replace with your MetaMask password
            password_input.send_keys(password)
            locator = By.XPATH, "//span[text()='Unlock']"
            unlock_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
            time.sleep(2)
            unlock_button.click()
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller unlocked OKX Wallet successfully!")
            break        
        except Exception as e:
            driver.refresh()
            time.sleep(2)




def switch_to_okx_popup(driver,original_handle):   
     handles = driver.window_handles
     #print(F"{datetime.now().strftime('%H:%M:%S')} : Number of tabs open",len(handles))
     if len(handles) > 1:
        for handle in handles:
            driver.switch_to.window(handle)
            #print("current url",driver.current_url)
            try:
                if driver.current_url.endswith("dapp-entry") or driver.current_url.startswith(f"{url}#/connect"): #Example XPath, needs adjustment
                    driver.save_screenshot("screenshot.png")
                    return f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller switched to okx popup"
            except:
                driver.switch_to.window(original_handle)
                return f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
    
def okx_action(driver,action,element_name):
    handles = driver.window_handles
    current_handle = driver.current_window_handle
    for i in handles:    
        driver.switch_to.window(i)
        current_url = driver.current_url
#print(f"datetime.now().strftime('%H:%M:%S') : current url",current_url)
        if current_url.endswith("dapp-entry") or current_url.startswith(f"{url}#/connect"):
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} Controller switched to OKX WALLET")
            time.sleep(10)
            next_btn = driver.find_element(By.XPATH, f'//div[text()="{element_name}"]')
            next_btn.click()
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller {action} on {element_name} in OKX WALLET")
            driver.switch_to.window(current_handle)
            return f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
        else:
            return f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
