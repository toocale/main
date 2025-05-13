from datetime import datetime
import time
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback

def mycontroller(element_path, gemini_response,driver):
    try:
        action = gemini_response["action"]
        locator = gemini_response["locator"]
        #print(f"Controller action in controller {locator} and {element_path}")
        if locator != element_path:
            if action in ["click","type","select","clear","refresh"] or element_path != None:
                if action == "click":
                    element = driver.find_element(By.XPATH, element_path)
                    element.click()
                    return f"{datetime.now().strftime('%H:%M:%S')} : Controller clicked {element} in {gemini_response['element_name']}"
                elif action == "type":
                    element = driver.find_element(By.XPATH, element_path)
                    print(f"Controller action in controller ")
                    element.clear()
                    element.send_keys(gemini_response["value"])
                    return f"{datetime.now().strftime('%H:%M:%S')} : Controller typed {gemini_response['value']} in {gemini_response['element_name']}"
                elif action == "select":
                    element = driver.find_element(By.XPATH, element_path)
                    element.click()
                    time.sleep(1)
                    element.send_keys(gemini_response["value"])
                    return f"{datetime.now().strftime('%H:%M:%S')} : Controller selected {gemini_response['value']} in {gemini_response['element_name']}"
                elif action == "clear":
                    element = driver.find_element(By.XPATH, element_path)
                    element.clear()
                    return f"{datetime.now().strftime('%H:%M:%S')} : Controller cleared {gemini_response['element_name']}"
                elif action == "refresh":
                        driver.refresh()
                        return f"{datetime.now().strftime('%H:%M:%S')} : Controller refreshed {gemini_response['element_name']}"
            
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

def ai_controller(gemini_response,driver):
    try:
        action = gemini_response["action"]
        element_name = gemini_response["element_name"]
        if action in ["click","type","select","clear","refresh"]:
            if action == "click":
                by_method = gemini_response["by_method"]
                locator = gemini_response["locator"]
                by = getattr(By, by_method)
                element = driver.find_element(by, locator)
                try:
                    element.click()
                    return f"✅{datetime.now().strftime('%H:%M:%S')} : AI Controller clicked {element_name}"
                except:
                    element.seend_keys(Keys.RETURN)
                    return f"✅{datetime.now().strftime('%H:%M:%S')} : AI Controller failed to click {element_name}"
            elif action == "type":
                by_method = gemini_response["by_method"]
                locator = gemini_response["locator"]
                by = getattr(By, by_method)
                element = driver.find_element(by, locator)
                element.clear()
                element.send_keys(gemini_response["value"])
                return f"✅{datetime.now().strftime('%H:%M:%S')} : AI Controller typed {gemini_response['value']} in {gemini_response['element_name']}"
            elif action == "clear":
                by_method = gemini_response["by_method"]
                locator = gemini_response["locator"]
                by = getattr(By, by_method)
                element = driver.find_element(by, locator)
                element.clear()
                return f"✅{datetime.now().strftime('%H:%M:%S')} : AI Controller cleared {gemini_response['element_name']}"
            elif action == "refresh":
                driver.refresh()
                return f"✅{datetime.now().strftime('%H:%M:%S')} : AI Controller refreshed {gemini_response['element_name']}"
            else:
                return None
        else:
            return None
    except:
        return None
        

def fallback_controller(gemini_response,driver,tag_list,element_path):
    try:
        action = gemini_response["action"]
        locator = gemini_response["locator"]
        element_name = gemini_response["element_name"]
        if action == "click" and len(tag_list)>1:
            try:
                if "div" not in locator and "div" not  in element_path:
                    for i in tag_list:
                        if i.name ==  "div":
                            locator = f"//div[text()='{element_name}']"
                            element=driver.find_element(By.XPATH, locator)
                            try:
                                element.click()
                            except:
                                driver.execute_script("arguments[0].click();", element)

                            return f"✅{datetime.now().strftime('%H:%M:%S')} : Fallback Controller clicked {element_name} from Fallback controller"

            except:
                if "span" not in locator and  "span" not in element_path and "span" in tag_list:
                    locator = f"//span[text()='{element_name}']"
                    element=driver.find_element(By.XPATH, locator)
                    element.click()
                    return f"✅{datetime.now().strftime('%H:%M:%S')} :Fallback Controller clicked {element_name} from Fallback controller"
                return f"✅{datetime.now().strftime('%H:%M:%S')} : Fallback Controller failed to click {element_name} from Fallback controller"
        else:
            return None
    except:
        return None
           

        