from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from PIL import Image
from io import BytesIO
import os

firefox_options = Options()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
service = Service('/Users/sayzyyy/Downloads/geckodriver')

MIN_WIDTH = 900
MIN_HEIGHT = 1200

os.makedirs('parse_images', exist_ok=True)

def parse_image(url):

    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:

        driver.get(url)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.photo-zoom__preview.j-zoom-image.hide')))


        images = driver.find_elements(By.CSS_SELECTOR, 'img')

        print(f'Найдено изображений: {len(images)}')

        for index, img in enumerate(images):

            src = img.get_attribute('src')  

            width = img.get_attribute('width') 
            height = img.get_attribute('height') 

            art=url.split('/')
            art1=art[4]
            print(art[4])

            if src and width and height and (art1 in src):

                print(f'Получен URL: {src}, ширина: {width}, высота: {height}')

                width = int(width)
                height = int(height)

                if width < MIN_WIDTH or height < MIN_HEIGHT:

                    print(f'Пропущено изображение из-за некорректного размера: {width}x{height}')
                    continue

                try:

                    response = requests.get(src)

                    if response.status_code == 200:

                        content_type = response.headers.get('Content-Type')

                        if 'image' in content_type:

                            image = Image.open(BytesIO(response.content))
                            image_path = f'parse_images/image_{art1}.jpeg'
                            image.convert('RGB').save(image_path, 'JPEG')

                            print(f'Сохранено: {image_path}')

                        else:

                            print(f'Получен неверный тип содержимого: {content_type} для {src}')

                    else:

                        print(f'Ошибка загрузки изображения: статус {response.status_code} для {src}')

                except Exception as e:

                    print(f"Ошибка обработки изображения: {e}")

    except TimeoutException:

        print("Элемент не найден в указанное время.")

    except Exception as e:

        print(f"Произошла ошибка: {e}")

    finally:

        driver.quit()

def main(url):

    parse_image(url=url)

if __name__ == '__main__':
    main(url)