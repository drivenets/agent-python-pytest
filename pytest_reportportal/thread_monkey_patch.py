import threading


def set_new_thread_init_method():
    """
    Override the existing init method of the threading.Thread class in order for it to have the self.parent attribute
    """
    old_init = threading.Thread.__init__

    def new_thread_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        self.parent = threading.current_thread()

    threading.Thread.__init__ = new_thread_init
