import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from io import StringIO

from uk_bin_collection.uk_bin_collection.common import create_webdriver
from uk_bin_collection.uk_bin_collection.get_bin_data import AbstractGetBinDataClass


class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def get_data(self, df: pd.DataFrame) -> dict:
        # Create dictionary of data to be returned
        data = {"bins": []}

        # Output collection data into dictionary
        for i, row in df.iterrows():
            dict_data = {
                "type": row["Collection Name"],
                "collectionDate": row["Next Collection Due"],
            }

            data["bins"].append(dict_data)

        return data

    def parse_data(self, page: str, **kwargs) -> dict:
        driver = None
        try:
            page = "https://chiltern.gov.uk/collection-dates"

            # Assign user info
            user_postcode = kwargs.get("postcode")
            user_paon = kwargs.get("paon")
            web_driver = kwargs.get("web_driver")
            headless = kwargs.get("headless")

            # Create Selenium webdriver
            driver = create_webdriver(web_driver, headless, None, __name__)
            driver.get(page)

            # Enter postcode in text box and wait
            inputElement_pc = driver.find_element(
                By.ID,
                "COPYOFECHOCOLLECTIONDATES_ADDRESSSELECTION_ADDRESSSELECTIONPOSTCODE",
            )
            inputElement_pc.send_keys(user_postcode)
            inputElement_pc.send_keys(Keys.ENTER)

            time.sleep(4)

            # Select address from dropdown and wait
            inputElement_ad = Select(
                driver.find_element(
                    By.ID,
                    "COPYOFECHOCOLLECTIONDATES_ADDRESSSELECTION_ADDRESSSELECTIONADDRESS",
                )
            )

            inputElement_ad.select_by_visible_text(user_paon)

            time.sleep(4)

            # Submit address information and wait
            driver.find_element(
                By.ID, "COPYOFECHOCOLLECTIONDATES_ADDRESSSELECTION_NAV1_NEXT"
            ).click()

            time.sleep(4)

            # Read next collection information into Pandas
            table = driver.find_element(
                By.ID, "COPYOFECHOCOLLECTIONDATES_PAGE1_DATES2"
            ).get_attribute("outerHTML")

            # Wrap the HTML table in a StringIO object to address the warning
            table_io = StringIO(table)
            df = pd.read_html(table_io, header=[1])[0]

            # Parse data into dict
            data = self.get_data(df)
        except Exception as e:
            # Here you can log the exception if needed
            print(f"An error occurred: {e}")
            # Optionally, re-raise the exception if you want it to propagate
            raise
        finally:
            # This block ensures that the driver is closed regardless of an exception
            if driver:
                driver.quit()
        return data
