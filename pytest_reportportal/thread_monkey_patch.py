import threading

# save the old thread
old_thread = threading.Thread


class MyThread(threading.Thread):
    """
    Overwrite the __init__ method of the Threading class in order to save the self.parent attribute
    """
    def __init__(self, *args, **kwargs):
        old_thread.__init__(self, *args, **kwargs)
        self.parent = threading.current_thread()


def set_new_thread_init_method():
    """
    Monkey patch the new Thread class with the modified init method
    """
    threading.Thread = MyThread


def set_new_thread_run_method(rp_client):
    """
    This function overrides the run method of each thread in order to call to the _log_batch
    method of the rp_client so the remaining logs of the thread will be uploaded since now threads can be running under
    nested steps or open new nested steps
    :param rp_client: The report portal client instance
    """
    original_run_method =  threading.Thread.run

    def new_run_method(self):
        try:
            original_run_method(self)
        finally:
            rp_client._log_batch(None, force=True)

    threading.Thread.run = new_run_method
