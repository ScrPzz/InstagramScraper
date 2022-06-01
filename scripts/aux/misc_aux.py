
def extract_shortcode_from_url(url):
    if url:
        return url.split('/')[-2]
    else:
        raise ValueError('Empty or invalid url!')