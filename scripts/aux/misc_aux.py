""" Some misc auxiliary functions """


def extract_shortcode_from_url(url):
    """Extract shortdoce from complete Instagram url"""
    if url:
        return url.split("/")[-2]
    else:
        raise ValueError("Empty or invalid url!")


def _finditem_nested_dict(obj, key):
    """ Recursively find item by key value \
        in a nested dictionary"""
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = _finditem_nested_dict(v, key)
            if item is not None:
                return item


def parse_url_list_from_file(path):
    urls = []
    with open(path) as file:
        while line := file.readline().rstrip():
            urls.append(line)
    return urls
