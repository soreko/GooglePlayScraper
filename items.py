import re


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

        for app_item in self._app_items:
            data = app_item.get_data(page)
            result[app_item.name()] = data

        return result


class IAppItem(object):

    def get_data(self, html_page):
        """
        gets the relevant data from an html page
        :param html_page: html page as string
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

    def get_data(self, html_page):

        match = re.findall('meta itemprop="name" content="([^"]+)"', html_page)

        if match:
            data = match[0]

        else:
            data = ''

        return data

    def name(self):
        return self._name


class IconAppItem(IAppItem):

    _name = ''

    def __init__(self):
        self._name = 'icon'

    def get_data(self, html_page):

        match = re.findall('meta itemprop="image" content="([^"]+)"', html_page)

        if match:
            data = match[0]

        else:
            data = ''

        return data

    def name(self):
        return self._name


class EmailAppItem(IAppItem):

    _name = ''

    def __init__(self):
        self._name = 'email'

    def get_data(self, html_page):

        match = re.findall('a href="mailto:([^"]+)"', html_page)

        if match:
            data = match[0]

        else:
            data = ''

        return data

    def name(self):
        return self._name
