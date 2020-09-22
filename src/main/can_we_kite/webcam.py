from selenium import webdriver
import os


def take_screenshot(date):
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver", log_path=os.path.join("logs", "gecko_driver.log"))

    driver.get('https://www.onekite.com/asso/webcams_onekite/monteynard-4K/full.html')
    driver.execute_script("window.scrollTo(0, 450);")

    image_path = os.path.join("images", f"{date.strftime('%Y_%m_%d_%H%M%S')}.png")
    screenshot = driver.save_screenshot(image_path)
    driver.quit()
    print(f"Webcam: Image saved: {image_path}")
