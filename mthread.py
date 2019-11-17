import threading
import utils
import time
import constant


class MoveLeavesThread(threading.Thread):
    def __init__(self, leaf_list):
        threading.Thread.__init__(self)
        self.leaf_list = leaf_list
        self.lock = threading.Lock()

    def run(self):
        while True:
            remove_list = []
            self.lock.acquire()
            for leaf in self.leaf_list:
                if utils.is_out_of_range(leaf):
                    remove_list.append(leaf)
                else:
                    if leaf.direction_x==-1 and leaf.direction_y==-1:
                        leaf.position_y += leaf.speed
                    else:
                        leaf.position_x += leaf.direction_x
                        leaf.position_y += leaf.direction_y
            for leaf in remove_list:
                self.leaf_list.remove(leaf)
            self.lock.release()

            time.sleep(0.001)


class UpdateUIThread(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self)
        self.application = application

    def run(self):
        while True:
            self.application.update_ui()
            time.sleep(0.001)
        # pass

class AddLeafThread(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self)
        self.application = application

    def run(self):
        while self.application.running:
            self.application.add_leaf()
            time.sleep(constant.add_leaf_speed_factor)

