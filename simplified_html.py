from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

#with open("html.html", 'r') as f:
    #html_html = f.read()


def simplify_html(driver):
    html_html= driver.page_source
    soup = BeautifulSoup(html_html, 'html.parser')
    lines = []
    allowed_tags = ['input', 'select', 'option', 'form', 'textarea']
    attributes = ["id", "value", "placeholder", "type", "name", "options", "data-testid"]
    for tag in soup.find_all():
        if tag.string and tag.string.strip():
            text = tag.string.strip()
            inside_button = tag.find_parent("button") or tag.find_parent("a") is not None
            if inside_button:
                context = "inside_button"
                lines.append(f"button.{tag.name}: visible text :{text}")
            elif tag.name == "button" or tag.name == "a":
                lines.append(f"{tag.name}: visible text :{text}")
        elif tag.name in allowed_tags:
            for attr_name, attr_value in tag.attrs.items():
                if attr_name in attributes:
                    attr = tag.get(attr_name)
                    if attr:
                        lines.append(f"{tag.name}.{attr_name}: {attr}")
                      #print(f"tag.name: {tag.name}, attr: {attr}")
    index_line =[]
    counter = 0              
    for line in lines:
        index_line.append(f"index:{counter}, {line}")
        counter += 1
        #print(f"line: {line}")
        #print(index_line)   
                 
    return index_line
#print(tagged_lines)


def finding_elements(driver,element_name,gemini_response):
    html_html = driver.page_source
    soup = BeautifulSoup(html_html, 'html.parser')
    tag_elements = soup.find_all()
    text_to_find = str(element_name)
    try:
        tag_list = ([])
        tag_list_allowed = ["div", "input", "button", "form", "textarea"]
        for tag in tag_elements:
            if tag.text.strip().lower() == text_to_find.lower():
                if not tag.find():          
                    tag_list.append(tag)
            elif tag.get("placeholder") == text_to_find:
                    tag_list.append(tag)
        for atag in tag_list:
            if atag.name in tag_list_allowed:
                for attr_name, attr_value in atag.attrs.items():
                    if attr_name == "id" and attr_value != None:
                        tag_name =atag.name 
                        attrname=attr_name
                        attrvalue=attr_value
                        return tag_name ,attr_name, attr_value,tag_list
                    elif attr_name == "placeholder" and attr_value != None:
                        tag_name =atag.name 
                        attrname=attr_name
                        attrvalue=attr_value
                        return tag_name ,attr_name, attr_value,tag_list
                    elif attr_name == "class" and attr_value != None:
                        tag_name =atag.name 
                        attrname=attr_name
                        attrvalue=attr_value[:1]
                        return tag_name ,attr_name, attr_value,tag_list
                    elif attr_name == "data-testid" and attr_value != None:
                        tag_name =atag.name 
                        attrname=attr_name
                        attrvalue=attr_value
                        return tag_name ,attr_name, attr_value,tag_list
                    elif attr_name == "name" and attr_value != None:
                        tag_name =atag.name 
                        attrname=attr_name
                        attrvalue=attr_value
                        return tag_name ,attrname, attrvalue,tag_list
    
           
    except:
        traceback.print_exc()
        return None , None, None, None, None
def execute_simplified_html(driver,element_name,gemini_response): 
    try:
        text_to_find = str(element_name)
        #print("finding elements",finding_elements(driver,element_name,gemini_response))
        if finding_elements(driver,element_name,gemini_response) != None:
            tag_name, attr_name, attr_value, tag_list = finding_elements(driver,element_name,gemini_response)
            #print("this are the values of ",tag_name, attr_name, attr_value, text_to_find)
            if tag_name and attr_name and attr_value :
                attr_value = attr_value if isinstance(attr_value, list) else [attr_value]
                attr_value = attr_value[0]
                if attr_name == "placeholder":
                    element_path = f"//{tag_name}[@{attr_name}='{attr_value}']"
                    return element_path,tag_list
                elif attr_name == "data-testid":
                    element_path = f"//{tag_name}[{attr_name}='{attr_value}']"
                    return element_path,tag_list
                elif attr_name == "id":
                    element_path = f"//{tag_name}[@{attr_name}='{attr_value}']"
                    return element_path,tag_list
                elif  attr_name == "name":
                    element_path = f"//{tag_name}[@{attr_name}='{attr_value}']"
                    return element_path,tag_list
                elif attr_name == "class" :
                    if tag_name == "input":
                        element_path = f"//{tag_name}[@placeholder='{text_to_find}']"
                        return element_path,tag_list
                    else:
                        element_path = f"//{tag_name}[normalize-space(text())='{text_to_find}']"
                        return element_path,tag_list   
            else:
                #print("Element not found")
                return None,None
        else:  
            return None,None
        
    except Exception as e:
        return None,None



# Recursive search that returns the element if found
def action_shadow_root(root,gemini_response,element_name):
    try:
        elements = root.find_elements(By.CSS_SELECTOR, "*")
    except Exception as e:
        #print(f"Failed to get elements from root: {e}")
        return None

    for el in elements:
        try:
            if el.tag_name in ['html', 'body']:
                continue

            # Match by visible text
            if el.text.strip() == element_name:
                el.click()
                #print("🖱️ Clicked.")
                return el  # RETURN IMMEDIATELY before sleep or changes

            # Match input with placeholder
            if el.tag_name == "input" and el.get_attribute("placeholder") == element_name:
                value = gemini_response.get("value")
                el.send_keys(value)
                return el

            # Recurse into shadow DOM
            shadow = el.shadow_root
            if shadow:
                #print(f"🌑 Entering shadow root of tag={el.tag_name}")
                result = action_shadow_root(shadow, gemini_response, element_name)
                if result:
                    return result

        except Exception as e:
            continue

    return None
"""
#element = action_shadow_root(driver, element_name)
#print(element)

#if element:
#print(f"🎯element found: {element.tag_name}, text='{element.text.strip()}'")
url = "https://bronto.finance/swap"
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
#options.add_argument("--headless")  # Optional: see browser if you remove this
driver = webdriver.Chrome(options=options)

# Replace with your actual page
driver.get(url)
input("Press Enter to continue...")

element_name ="WalletConnect"

from selenium.webdriver.common.by import By

def action_shadow_root_only(root, gemini_response, element_name):
    try:
        elements = root.find_elements(By.CSS_SELECTOR, "*")
    except Exception as e:
        print(f"❌ Failed to get elements from root: {e}")
        return None

    for el in elements:
        try:
            # Only proceed if inside a shadow root
            shadow = el.shadow_root
            if shadow:
                result = action_shadow_root_only(shadow, gemini_response, element_name)
                if result:
                    return result
                continue

            # Skip elements outside shadow DOM
            host_shadow = getattr(el, 'shadow_root', None)
            if not host_shadow:
                continue

            # Match by visible text
            if el.text.strip() == element_name:
                print(f"✅ Found element by text: <{el.tag_name}> '{el.text.strip()}'")
                el.click()
                print("🖱️ Clicked.")
                return el

            # Match input by placeholder
            if el.tag_name == "input" and el.get_attribute("placeholder") == element_name:
                value = gemini_response.get("value", "")
                print(f"✅ Found input with placeholder '{element_name}', typing: {value}")
                el.send_keys(value)
                return el

        except Exception as e:
            print(f"⚠️ Error processing element: {e}")
            continue

    return None
element = None
top_level_elements = driver.find_elements(By.CSS_SELECTOR, "*")

for el in top_level_elements:
    try:
        shadow = el.shadow_root
        if shadow:
            element = action_shadow_root_only(shadow, "gemini_response", element_name)
            if element:
                break
    except Exception as e:
        print(f"⚠️ Top-level shadow check error: {e}")
        continue

if not element:
   
    print("❌ Could not find the element inside shadow DOMs.")
time.sleep(10)
"""