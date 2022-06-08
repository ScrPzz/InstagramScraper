
def extract_shortcode_from_url(url):
    if url:
        return url.split('/')[-2]
    else:
        raise ValueError('Empty or invalid url!')

def _finditem_nested_dict(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _finditem_nested_dict(v, key)
            if item is not None:
                return item