from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from undetected_chromedriver import Chrome

from m_pyutil.selenium.moperator import Operator


class ChromeCli(WebDriver, Operator):

    def __init__(self,
                 proxy: str = None,
                 headless: bool = False,
                 images_disabled: bool = True,
                 extensions: list = None,
                 unpacked_extensions: list = None,
                 **kwargs):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        if headless:
            options.add_argument('--headless=new')
        if images_disabled:
            options.add_argument('--blink-settings=imagesEnabled=false')
        if extensions:
            for extension in extensions:
                options.add_extension(extension)
        if unpacked_extensions:
            options.add_argument(f'--load-extension={",".join(unpacked_extensions)}')
        if kwargs:
            for key, value in kwargs.items():
                options.add_argument(f'{key}={value}')

        super().__init__(options=options)
        self.maximize_window()


class UcChromeCli(Chrome, Operator):

    def __init__(self,
                 proxy: str = None,
                 headless: bool = False,
                 images_disabled: bool = True,
                 extensions: list = None,
                 unpacked_extensions: list = None,
                 **kwargs):
        options = Options()
        options.add_argument('--disable-gpu')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        if headless:
            options.add_argument('--headless=new')
        if images_disabled:
            options.add_argument('--blink-settings=imagesEnabled=false')
        if extensions:
            for extension in extensions:
                options.add_extension(extension)
        if unpacked_extensions:
            options.add_argument(f'--load-extension={",".join(unpacked_extensions)}')
        if kwargs:
            for key, value in kwargs.items():
                options.add_argument(f'{key}={value}')

        super().__init__(options=options)
        self.maximize_window()
