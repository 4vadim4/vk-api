# -*- coding: UTF-8 -*-
import requests
import threading
import time
from Queue import Queue
import sys
import datetime



DUROV_USER_ID = 1    #looking for Pavel Durov
VK_GET_FRIENDS_URL = 'https://api.vk.com/method/friends.get?user_id=%(user_id)d&v=%(vk_api_version)s'
VK_API_VERSION = '5.52'
user = *******      #id for start the search
MAX_COUNT = 10
friends_queue = Queue()
POINTER = []
#global semaphore
maxth = 2
semaphore = threading.BoundedSemaphore(maxth)

"""
create class for creating object's
"""

class FriendData:
    def __init__(self, level, id_user, value):
        self.level = level
        self.id_user = id_user
        self.value = value


"""
func start_user() - starting func, if's needed for filling the queue stack
"""

def start_user():
    users_friend = requests.get(VK_GET_FRIENDS_URL %{'user_id': user, 'vk_api_version': VK_API_VERSION})
    users_friend_list = users_friend.json()
    catalog = users_friend_list["response"]["items"]
    ctlg = catalog[:MAX_COUNT]
    if DUROV_USER_ID in catalog:
        f = open('text.txt', 'a')
        f.write('Durov is found, he is a friend of %s \n' %(user))
        f.close()
        print('OK')
    else:
        for one in ctlg:
            single = FriendData(1, one, '%s' %user)
            friends_queue.put(single)
        return friends_queue


"""
main func deep_beginning() receives from queue,  value of ID "friends of friends", monitors the depth and
keep track of whether Durov found, when the depth reaches or Durov is found, the func stop own work

"""

def deep_beginning(queue_object):
        if queue_object.level < 6:
            users_friend_global = requests.get(VK_GET_FRIENDS_URL % {'user_id': queue_object.id_user, 'vk_api_version': VK_API_VERSION})
            users_friend_list_global = users_friend_global.json()
            try:
                catalog2 = users_friend_list_global["response"]["items"]
                ctlg2 = catalog2[:MAX_COUNT]
            except KeyError:
                print('Friend with ID #%d - deleted !' % (queue_object.id_user))

            else:
                if DUROV_USER_ID in catalog2:
                    f = open('text.txt', 'a')
                    f.write('Durov is found, he in a friendzone of user %s. On level %d. Friends chain is %s \n' %(queue_object.id_user, queue_object.level, queue_object.value))
                    f.close()
                    POINTER.append('OK')
                    print('WE FOUND HIS !')
                    friends_queue.queue.clear()
                else:
                    for one2 in ctlg2:
                        single2 = FriendData(queue_object.level+1, one2, '%s-%s' %(queue_object.value, one2))
                        print(single2.value)
                        print(datetime.datetime.now())
                        friends_queue.put(single2)
                        return friends_queue

        else:
            friends_queue.queue.clear()
            print("The End")
            sys.exit()


"""
func thread() creating threads and passing the ID "friends of friends" from queue in func deep_beginning()
"""


def thread(friends_queue):
    while not friends_queue.empty():

        t = []
        while len(t) < 6:
            item = friends_queue.get()
            thread_friend = threading.Thread(target=deep_beginning, args=(item,))
            t.append(thread_friend)
        for i in t:

            i.start()

        for i in t:
            i.join()

        time.sleep(1)

"""
start script
"""

thread(start_user())
