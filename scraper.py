import requests
import time
from multiprocessing import Pool, Lock, cpu_count
import copy_reg
import types


# This method is here for the multiprocessing Pool apply_async() to work
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


# This method is here for a synchronized lock between processes
def init_lock(l):
    global lock
    lock = l


class IScraper(object):
    def scrap(self, unique_id, proxy):
        raise NotImplementedError()


class ScraperLauncher:
    """
    Responsible for launching scrapers concurrently via proxies
    """

    _proxy_manager = None
    _scraper = None
    _cache = None
    _output_manager = None

    # queue of Google apps ids, filled by another thread
    _queue = None

    _concurrency_pool = None

    def __init__(self, proxy_manager, queue, scraper, output_manager, cache=None, pool_size=None):

        self._proxy_manager = proxy_manager
        self._queue = queue
        self._scraper = scraper
        self._cache = cache
        self._output_manager = output_manager

        self._pool_lock = Lock()

        if not pool_size:
            pool_size = cpu_count()

        self._concurrency_pool = Pool(pool_size, initializer=init_lock, initargs=(self._pool_lock,))

    def run(self):
        try:
            while True:
                google_app_id = self._queue.get()

                # if we use cache
                if self._cache:
                    value = self._cache.get(google_app_id)

                    # if we have this app in cache, output it and continue looping
                    if value:
                        self._output_manager.output(value, self._pool_lock)
                        continue

                # get proxy
                proxy = self._proxy_manager.get_proxy()

                # if no proxy available, keep waiting
                while not proxy:
                    time.sleep(2)
                    proxy = self._proxy_manager.get_proxy()

                scraper = self._scraper
                callback = self._callback

                res = self._concurrency_pool.apply_async(scraper.scrap, args=(google_app_id, proxy), callback=callback)

                self._queue.task_done()

        finally:
            self._concurrency_pool.close()
            self._concurrency_pool.join()

    def _callback(self, result):
        if result and self._cache:
            self._cache.set(result.get('id', 'unknown'), result, self._pool_lock)


class GooglePlayScraper(IScraper):

    _items_manager = None
    _output_manager = None

    CRAWL_URL = 'https://play.google.com/store/apps/details?id={0}'

    def __init__(self, items_manager, output_manager):

        self._items_manager = items_manager
        self._output_manager = output_manager

    def scrap(self, unique_id, proxy):
        """
        this function will scrap app_url via proxy, parse its items with items manager,
        and output its result with output manager
        :param unique_id: id of the google app we're scraping
        :param proxy: dict {protocol: address}
        """
        try:
            app_url = self.CRAWL_URL.format(unique_id.strip())

            # send request to Google
            response = requests.get(url=app_url, proxies=proxy)

            if response.status_code == requests.codes.ok:

                page = response.content

                # get all items from the response page
                items_dict = self._items_manager.get_items(page)

                if items_dict:
                    items_dict['id'] = unique_id

                    # output all items
                    self._output_manager.output(items_dict, lock)

                    return items_dict

        except Exception as e:
            # TODO: add failure message
            pass

        return None





