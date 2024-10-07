import logging
import random
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


# noinspection PyTypeChecker
class Operator:

    # noinspection PyMissingConstructor
    def __init__(self):
        raise TypeError("This class is not instantiable")

    def query_element_d(self,
                        value: str,
                        by: str = By.CSS_SELECTOR,
                        timeout: int = 10,
                        count: int = 3,
                        raise_e: bool = True) -> WebElement:
        return self.query_element(src=self, value=value, by=by, timeout=timeout, count=count, raise_e=raise_e)

    def query_element(self,
                      src: WebDriver or WebElement,
                      value: str,
                      by: str = By.CSS_SELECTOR,
                      timeout: int = 10,
                      count: int = 3,
                      raise_e: bool = True) -> WebElement or None:
        elements = self.query_elements(src=src, value=value, by=by, timeout=timeout, count=count, raise_e=raise_e)
        if elements:
            return elements[0]
        return None

    def query_elements_d(self,
                         value: str,
                         by: str = By.CSS_SELECTOR,
                         timeout: int = 10,
                         count: int = 3,
                         raise_e: bool = True) -> list[WebElement]:
        return self.query_elements(src=self, value=value, by=by, timeout=timeout, count=count, raise_e=raise_e)

    def query_elements(self,
                       src: WebDriver or WebElement,
                       value: str,
                       by: str = By.CSS_SELECTOR,
                       timeout: int = 10,
                       count: int = 3,
                       raise_e: bool = True) -> list[WebElement]:
        while count > 0:
            try:
                WebDriverWait(self, timeout).until(ec.presence_of_element_located((by, value)))
                return src.find_elements(by=by, value=value)
            except Exception as e:
                count -= 1
                logging.debug(str(e))
        if raise_e:
            raise RuntimeError(f'elements were not found: by={by}, value={value}')
        return []

    def click(self, ele):
        ActionChains(self).move_to_element(ele).click().perform()

    def click_and_move_by_x_offset(self, ele, x_offset):
        action_chains = ActionChains(self)
        action_chains.click_and_hold(ele).perform()
        moved_x_offset = 0
        while True:
            if moved_x_offset >= x_offset:
                break
            delta_x_offset = x_offset - moved_x_offset
            delta_x_offset = min(x_offset / random.randint(2, 5), delta_x_offset)
            action_chains.move_by_offset(delta_x_offset, 0).perform()
            moved_x_offset += delta_x_offset
            time.sleep(random.uniform(0.005, 0.7))
