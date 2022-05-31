from src.geoloc_aux import fetch_country_code, fetch_country_name

class Geolocation:
    def __init__(self):
        pass

    def fetch_location(self, country):
        if len(country)==2:
            location_params=fetch_country_code(country)
        else:
            location_params=fetch_country_name(country)

        return location_params 

    def set_geolocation(self, driver, country):  
        location_params=self.fetch_location(country)
        driver.execute_cdp_cmd("Page.setGeolocationOverride", location_params)
    
    def choose_random_geolocation(self, driver):
        location_params=self.fetch_location('random')
        driver.execute_cdp_cmd("Page.setGeolocationOverride", location_params)