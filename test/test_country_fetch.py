
from scripts.aux.geoloc_aux import fetch_country_code, fetch_country_name




def test_country_code_fetch():
    country_params=fetch_country_code(country='it')
    assert country_params['latitude']==41.87194
    assert country_params['longitude']==12.56738


def test_country_name_fetch():
    country_params=fetch_country_name(country='ital')
    assert country_params['latitude']==41.87194
    assert country_params['longitude']==12.56738
    
