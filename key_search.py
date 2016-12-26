'''
Search for a key in a B+Tree
'''
import json
import functools
import time

def search(relation, key):
    '''
    search for a key using linear search a btree
    '''
    def btree_search(relation, key):
        '''
        search for a key method
        '''

        def get_bucket(path, node):
            '''
            get the element using path from datadict
            '''
            return functools.reduce(lambda d, k: d[k], path, node)

        def reach_bucket(node, element, path):
            '''
            get the path for the bucket
            '''
            if not isinstance(node, list) and node is not None:
                #check the pointers until it hits an empty one or a bigger key
                for count in range(num_pointers-1):
                    if node["K%d" % (count)] is None or node["K%d" % (count)] > element:
                        path.append('P%d' % (count))
                        return reach_bucket(node['P%d' % (count)], element, path)
                #returns the last pointer
                path.append('P%d' % (num_pointers-1))
                return  reach_bucket(node['P%d' % (num_pointers-1)], element, path)

        #init an empty path for the element
        path = []
        #get the b+tree
        try:
            with open("Data/btree.{}.json".format(relation), "r") as openf:
                jsonlist = json.load(openf)
        except FileNotFoundError:
            print("btree.{}.json not found!".format(relation))
            return

        #get the number of pointers used in the b+tree
        num_pointers = len(jsonlist['root'])//2 + 1

        #get the path for the element inside the b+tree
        reach_bucket(jsonlist['root'], key, path)

        #check if the key is found or not
        if key in get_bucket(path, jsonlist['root']):
            print("{0} is found using path {1}".format(key, path))
        else:
            print("{} is not found!".format(key))


    def linear_search(relation, key):
        '''
        linear search
        '''
        try:
            with open("Data/relation.{}.json".format(relation), "r") as openf:
                jsonlist = json.load(openf)
        except FileNotFoundError:
            print("relation{}.json not found!".format(relation))
            return
        for mydic in jsonlist:
            if mydic["{}_id".format(relation[:-1])] == key:
                print("{} was found!".format(key))
                return
        print("{} was not found!/n".format(key))
    start_time = time.time()
    btree_search(relation, key)
    print("B+tree search execution time: {}\n".format(time.time() - start_time))
    start_time = time.time()
    linear_search(relation, key)
    print("Linear search execution time: {}".format(time.time() - start_time))
