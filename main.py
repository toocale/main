
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
import uuid
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
#from langchain.schema import HumanMessage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import base64
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from dotenv import load_dotenv
import json
import traceback
import os
from os import getenv
from prompt import system_prompt
import time
from datetime import datetime
from controller import mycontroller,ai_controller,fallback_controller
from okx import unlock_okx,switch_to_okx_popup
from simplified_html import simplify_html,execute_simplified_html,finding_elements,action_shadow_root
load_dotenv()


# Define paths for profile data
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get directory of the script
user_data_dir = os.path.join(script_dir, "chrome_profile") # Create profile dir next to script
profile_directory = "Default" # Use the default profile name
# Create the user data directory if it doesn't exist
#user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)
    print(f"Created user data directory: {user_data_dir}")
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_directory}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument("--disable-extensions-except=" + metamask_path)
#chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")
service = Service(log_path="chromedriver.log", verbose=True)
print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller to launch browser")

driver = uc.Chrome(service=service, options=chrome_options, headless=False)
#unlock_metamask(driver)
unlock_okx(driver)
time.sleep(3)

#input("Press Enter to continue...")
new_tab = driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[-1])

def navigate(url):
    print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller to navigate to {url}")
    session_id = str(uuid.uuid4())
    driver.get(url)
    return session_id
#input("Press Enter to continue...")


def screenshot():
    original_handle = driver.current_window_handle
    #switch_to_metamask_popup(driver, original_handle)
    time.sleep(2)
    print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller to take screenshot")
    driver.save_screenshot("screenshot.png")
    time.sleep(1)


def analyse_picture():
    original_handle = driver.current_window_handle
    #switch_to_metamask_popup(driver, original_handle)
    switch_to_okx_popup(driver, original_handle)
    screenshot()
    print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Agent to analyze screenshot")
    with open("screenshot.png", "rb") as f:
        image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    #html_string = simplify_html(driver)
    #message_list = prompt(image_bytes,html_string)
    #model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=1)
    model = ChatOpenAI(openai_api_key=getenv("OPENROUTER_API_KEY"),openai_api_base=getenv("OPENROUTER_BASE_URL"),model_name="deepseek/deepseek-prover-v2:free")
    prompt1 = ChatPromptTemplate.from_messages([
                                            ("system", system_prompt),
                                            ("human", "{input}")])
    chain = prompt1 |  model

    
    def get_memory(session_id: str):
        return InMemoryChatMessageHistory()
    
    chain_with_memory = RunnableWithMessageHistory(
                                                    chain,
                                                    get_memory,
                                                    input_messages_key="input")

    
    #message_list = prompt(image_bytes,html_string)
    response = chain_with_memory.invoke(
                            {"input": image_base64},
                            config={"configurable": {"session_id": session_id}})
    #response = chain.invoke([HumanMessage(content=message_list[0]["content"])], 
     #                       config={"configurable": {"session_id": session_id}})
    gemini_response = response.content
    if gemini_response.startswith("```json"):
        gemini_response = gemini_response[7:]
    if gemini_response.endswith("```"):
        gemini_response = gemini_response[:-3]
    gemini_response = gemini_response.strip()
    return gemini_response , original_handle


def gemini_response():
    try:       
        gemini_action , current_handle = analyse_picture()
        gemini_response = json.loads(gemini_action)
        action = gemini_response["action"]
        #print(gemini_response)
        element_name = gemini_response["element_name"]
        print(f"✅{datetime.now().strftime('%H:%M:%S')} : AI response is",end=" ")
        for key, value in gemini_response.items():
                print(f"{key} : {value},",end=" ")
        print("")
        controller=""
        if execute_simplified_html(driver,element_name,gemini_response):
            element_path,tag_list=execute_simplified_html(driver,element_name,gemini_response)
        if "okx" in driver.title.lower() or (driver.current_url).endswith("dapp-entry"):
            next_btn = driver.find_element(By.XPATH, f'//div[text()="{element_name}"]')
            next_btn.click()
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller {action} on {element_name} in OKX WALLET")
            time.sleep(10)
            driver.switch_to.window(current_handle)
            return f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller switched to original tab"
        elif ai_controller(gemini_response,driver):
            controller_name = "AI Controller"   
        elif mycontroller(element_path, gemini_response,driver):
            controller_name= "Mycontroller"
        elif action_shadow_root(driver, gemini_response,element_name):
            controller_name = "Shadow Root Controller"    
        if fallback_controller(gemini_response,driver,tag_list,element_path):
            controller_name = "Fallback Controller"
        return f"✅ {datetime.now().strftime('%H:%M:%S')} : {controller_name} handing over to Agent"
    except Exception as e:
        #traceback.print_exc()   
        return f"✅ {datetime.now().strftime('%H:%M:%S')} : Controller and Agent encountered an error {e}"
    
    
session_id = navigate("https://www.okx.com/")
while True:
    print(gemini_response())
    time.sleep(15)