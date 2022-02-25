from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from threading import Thread
import time

# Writing to log function
def log(text):
    now = time.time()
    with open("log.txt", "a") as l:
        l.write(text + "\n")


def init():
    # Temporary driver
    ser = Service("C:\\Users\\afbar\\Downloads\\chromedriver_win32\\chromedriver.exe")
    driver = webdriver.Chrome(service=ser)
    driver.maximize_window()

    # Log file setup
    with open("log.txt", "w") as l:
        l.write("")

    # Return
    return driver


def loadSave(save, driver):
    driver.execute_script(f'window.localStorage.setItem("dimensionSave","{save}")')
    driver.refresh()


def storeSave(driver):
    log("Save thread starting")
    while driver.session_id:
        save = driver.execute_script(
            'return window.localStorage.getItem("dimensionSave")'
        )
        if save is not None:
            with open("session.txt", "w") as f:
                f.write(save)
            log("Saving")
        else:
            print("Game has not produced a save yet, retrying in 15s")
        time.sleep(15)


if __name__ == "__main__":
    driver = init()

    # Open AD website
    driver.get("https://ivark.github.io/")

    # Load savefile
    try:
        with open("session.txt", "r") as f:
            save = f.read()
        if save:
            loadSave(save, driver)
    except FileNotFoundError:
        log("Missing save file, starting new game")

    # Run save thread
    save_thread = Thread(target=storeSave, args=(driver,))
    save_thread.start()


# MAIN LOOP
while True:
    # Click Max all
    driver.execute_script('$("#maxall.storebtn").click()')
    # Get antimatter
    antimatter = driver.execute_script("return player.money;")
    log(f"Antimatter: {antimatter}")
    # Initial 1st dimension
    if antimatter == "10":
        driver.execute_script('$("#first.storebtn").click()')
    driver.execute_script('$("#softReset.storebtn").click()')
    time.sleep(0.5)

    # Check for 1st dimension availability
    # ad1check = driver.execute_script('return $("#first.storebtn").length')
    # if ad1check:
    #     driver.execute_script('$("#first.storebtn").click()')
    # time.sleep(1)

    # Get antimatter
    # try:
    #     antimatter = driver.execute_script("return player.money;")
    #     log(f"Antimatter: {antimatter}")
    # except:
    #     print("Could not get antimatter")
