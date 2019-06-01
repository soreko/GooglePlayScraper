from bs4 import BeautifulSoup, SoupStrainer


class ItemsManager:
    """
    Responsible for getting all relevant items from the Google App HTML page.
    """

    _app_items = []

    def __init__(self, app_items):
        self._app_items = app_items

    def get_items(self, page):
        """
        gets data for each item in its item list and returns dictionary of {item_name: item_data, .....}
        :param page: Google Play Store App HTML page
        :return: dictionary
        """

        result = {}

        # parse HTML page with BeautifulSoup - most consuming time operation
        soup = BeautifulSoup(page, 'html.parser')

        for app_item in self._app_items:
            data = app_item.get_data(soup)
            result[app_item.name()] = data

        return result


class IAppItem(object):

    def get_data(self, html_page):
        """
        gets the relevant data from an html page
        :param html_page: html page
        :return: data as string
        """
        raise NotImplementedError()

    def name(self):
        """
        return item's name
        :return: name as string
        """
        raise NotImplementedError()


class TitleAppItem(IAppItem):

    _name = ''

    def __init__(self):
        self._name = 'title'

    def get_data(self, html_page_soup):

        data = html_page_soup.find('meta', itemprop='name')

        if data:
            data = data.get('content', '')

        else:
            data = ''

        return data

    def name(self):
        return self._name


class IconAppItem(IAppItem):

    _name = ''

    def __init__(self):
        self._name = 'icon'

    def get_data(self, html_page_soup):

        data = html_page_soup.find('meta', itemprop='image')

        if data:
            data = data.get('content', '')

        else:
            data = ''

        return data

    def name(self):
        return self._name


class EmailAppItem(IAppItem):

    _name = ''

    def __init__(self):
        self._name = 'email'

    def get_data(self, html_page_soup):
        import re
        data = html_page_soup.find('a', href=re.compile("mailto:"))

        if data:
            data = data.get_text()

        else:
            data = ''

        return data

    def name(self):
        return self._name
