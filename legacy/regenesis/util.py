from threading import Thread
from Queue import Queue
import logging

def serialize_soap(entry):
    d = {}
    for k, v in entry:
        if isinstance(v, bool):
            d[k] = v
        elif isinstance(v, int):
            d[k] = v
        elif isinstance(v, float):
            d[k] = v
        elif isinstance(v, type(None)):
            d[k] = None
        elif isinstance(v[0], basestring):
            d[k] = u''.join(v)
        else:
            d[k] = [serialize_soap(i) for i in v[0]]
    return d


def run_threaded(items, func, num_threads=10, no_thread=False, max_queue=100, sleep=None):
    def queue_consumer():
        while True:
            item = queue.get(True)
            try:
                func(item)
            except Exception, e:
                logging.exception(e)
            queue.task_done()

    queue = Queue(maxsize=max_queue)

    for i in range(num_threads):
         t = Thread(target=queue_consumer)
         t.daemon = True
         t.start()

    for item in items:
        queue.put(item, True)

    queue.join()  


