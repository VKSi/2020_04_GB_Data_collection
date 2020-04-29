import json

def items_grabbing(items):
    """
    Grab and add info into the database about all products on the current 'visual' block of hints

    Args:
        items(list of selenium.webdriver.remote.webelement.WebElement): Collection of web-elements for each items
                on the current 'visual' hits block

    Returns:
        list: Collection of information about hits, including  new items
    """
    data = []
    for item in items:
        if not item.text:  # skip empty 'hidden' items
            continue

        link = item.get_attribute('href')
        description = json.loads(item.get_attribute('data-product-info'))

        name = description['productName']
        description.pop('productName')

        id = description['productId']
        description.pop('productId')

        data.append({'_id': id, 'name':name, 'link':link, 'description':description})
    return data