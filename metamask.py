import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime

def unlock_metamask(driver):
    # Wait for MetaMask to load
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            if (!Object.hasOwn) {
                Object.hasOwn = function(obj, prop) {
                    return Object.prototype.hasOwnProperty.call(obj, prop);
                };
            }
            """
        }
    )

    # Open MetaMask UI (this is the main entry point)
    driver.get("chrome-extension://inpehkhkkppackeloacgfedelfoafcaj/home.html")
    time.sleep(2)
    #driver.get("chrome-extension://cfhnbohmelahhlapikkghkhbcghpoaed/popup.html")
    while True:
        try:
            # Wait for the password input field to appear
            password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'password')))
            # Enter the password (replace with your actual MetaMask password)
            password = "qwerty123"  # Replace with your MetaMask password
            password_input.send_keys(password)
            locator =By.TAG_NAME, "button"
            unlock_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
            # Click the Unlock button to unlock MetaMask
            driver.execute_script("arguments[0].click();", unlock_button)
            #unlock_button.click()
            return f"{datetime.now().strftime('%H:%M:%S')} : Controller unlocked Metamask successfully!"

            #open new tab
            #driver.execute_script("window.open('');") 
            #driver.close()
            break          
        except Exception as e:
            print(f"Error unlocking MetaMask: {e}")
            driver.refresh()
            time.sleep(2)




def switch_to_metamask_popup(driver,original_handle):   
     handles = driver.window_handles
     print(F"{datetime.now().strftime('%H:%M:%S')} : Number of tabs open",len(handles))
     if len(handles) > 1:
        for handle in handles:
            driver.switch_to.window(handle)
            try:
                if driver.current_url == "chrome-extension://inpehkhkkppackeloacgfedelfoafcaj/home.html" or driver.current_url == "chrome-extension://inpehkhkkppackeloacgfedelfoafcaj/popup.html" or "MetaMask" in driver.title: #Example XPath, needs adjustment
                    driver.save_screenshot("screenshot.png")
                    return f"{datetime.now().strftime('%H:%M:%S')} : Controller switched to metamask popup"
            except:
                driver.switch_to.window(original_handle)
                return f"{datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
    
def metamask_action(driver,action,element_name):
    handles = driver.window_handles
    current_handle = driver.current_window_handle
    list_of_titles = []
    list_of_urls = []
    for i in handles:    
        driver.switch_to.window(i)
        list_of_titles.append(driver.title)
        list_of_urls.append(driver.current_url)
    if "MetaMask" in driver.title:
        print(f"{datetime.now().strftime('%H:%M:%S')} Controller switched to metamask")
        time.sleep(10)
        next_btn = driver.find_element(By.XPATH, f'//button[text()="{element_name}"]')
        driver.execute_script("arguments[0].click();", next_btn)
        print(f"{datetime.now().strftime('%H:%M:%S')} : Controller {action} on {element_name} in metamask")
        driver.switch_to.window(current_handle)
        return f"{datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
    else:
        return f"{datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
