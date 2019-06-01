from web_app import MyWebApp
from scraper import ScraperLauncher, GooglePlayScraper
from proxy_manager import MyProxyManager
from items import ItemsManager, TitleAppItem, IconAppItem, EmailAppItem
from output_manager import FileOutputManager
from Queue import Queue
from threading import Thread
from cache import SimpleCache


class MyAPP:

    _items = None
    _items_manager = None
    _output_manager = None
    _proxy_manager = None
    _queue = None
    _scraper = None
    _scraper_launcher = None
    _web_app = None

    def __init__(self):
        self._items = [TitleAppItem(), EmailAppItem(), IconAppItem()]

        self._items_manager = ItemsManager(self._items)
        self._output_manager = FileOutputManager()
        self._proxy_manager = MyProxyManager()
        self._queue = Queue()
        self._cache = SimpleCache()
        self._scraper = GooglePlayScraper(items_manager=self._items_manager,
                                          output_manager=self._output_manager)

        self._scraper_launcher = ScraperLauncher(proxy_manager=self._proxy_manager, queue=self._queue,
                                                 scraper=self._scraper, output_manager=self._output_manager,
                                                 cache=self._cache)

        self._web_app = MyWebApp(queue=self._queue, host='localhost', port=5000)

    def main(self):
        t1 = Thread(target=self._web_app.run)
        t2 = Thread(target=self._scraper_launcher.run)

        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == '__main__':
    try:
        app = MyAPP()
        app.main()

    except Exception as e:
        print("ERROR: {}".format(e))
