'''
B+Tree Generator
'''
#pylint:disable=C0304
#pylint:disable=E1126
#pylint:disable=E1101

import json
import functools
import math


def btree_gen(relation, size_bucket, num_pointers):
    '''
    main method
    '''

    def get_bucket(path):
        '''
        get the element using path from datadict
        '''
        return functools.reduce(lambda d, k: d[k], path, tree['root'])

    def set_bucket(path, value):
        '''
        insert the value in the bucket then sort it
        '''
        #if the root is the bucket
        if len(path) == 0:
            tree['root'].append(value)
            tree['root'].sort()
        #the root is a node
        else:
            bucket = get_bucket(path[:-1])[path[-1]]
            bucket.append(value)
            bucket.sort()

    def set_element(path, value):
        '''
        set the elements in the tree
        '''
        get_bucket(path[:-1])[path[-1]] = value

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

    def insert_in_tree(element):
        '''
        insert element inside the b+tree
        '''
        #get the path for the appropriate bucket
        path = []
        reach_bucket(tree['root'], element, path)
        #insert the element in the bucket
        set_bucket(path, element)
        bucket = get_bucket(path)
        size = len(bucket)

        #overflow in bucket
        if size > size_bucket:
            #halve the bucket
            list1 = bucket[:size//2]
            list2 = bucket[size//2:]
            #checks if the root is a bucket
            if len(path) != 0:
                structure_change(list1, list2, path, list2[0])
            else:
                tree['root'] = dict()
                tree['root']["P0"] = list1
                tree['root']["P1"] = list2
                for i in range(2, num_pointers):
                    tree['root']["P%d" % i] = None

                tree['root']["K0"] = list2[0]
                for i in range(1, num_pointers-1):
                    tree['root']["K%d" % i] = None

    def structure_change(list1, list2, path, parent_key):
        '''
        tree structure change
        '''
        #get the first non-occupied pointer
        first_pointer = int(path[-1][1])
        last_pointer = first_pointer+1
        while last_pointer < num_pointers:
            path[-1] = "P%d" % last_pointer
            if get_bucket(path) is None:
                break
            last_pointer += 1

        #swap the pointers
        for i in range(last_pointer, first_pointer, -1):
            path[-1] = "P%d" % (i - 1)
            current_pointer = get_bucket(path)
            path[-1] = "P%d" % i
            set_element(path, current_pointer)
        #swap the keys
        for i in range(last_pointer-1, first_pointer, -1):
            path[-1] = "K%d" % (i-1)
            current_key = get_bucket(path)
            path[-1] = "K%d" % (i)
            set_element(path, current_key)

        #insert new key and pointer
        path[-1] = "K%d" % (first_pointer)
        set_element(path, parent_key)
        path[-1] = "P%d" % (first_pointer+1)
        set_element(path, list2)
        path[-1] = "P%d" % (first_pointer)
        set_element(path, list1)

        #overlflow in nodes
        if last_pointer == num_pointers:
            split_node(path)


    def split_node(path):
        '''
        split node if Overflow
        '''
        dict1 = dict()
        dict2 = dict()
        del path[-1]
        #populating the first node
        for i in range(num_pointers):
            if i < num_pointers//2:
                dict1["P%d" % i] = get_bucket(path)["P%d" % i]
            else:
                dict1["P%d" % i] = None
        for i in range(num_pointers-1):
            if i < num_pointers//2 - 1:
                dict1["K%d" % i] = get_bucket(path)["K%d" % i]
            else:
                dict1["K%d" % i] = None
        #populating the second node
        for i in range(num_pointers):
            if i < math.ceil(num_pointers/2):
                dict2["P%d" % i] = get_bucket(path)["P%d" % ((num_pointers//2)+i+1)]
            else:
                dict2["P%d" % i] = None
        for i in range(num_pointers-1):
            if i < (math.ceil(num_pointers/2) - 1):
                dict2["K%d" % i] = get_bucket(path)["K%d" % ((num_pointers//2)+i+1)]
            else:
                dict2["K%d" % i] = None

        parent_key = get_bucket(path)["K%d" % (num_pointers/2)]
        #overflow in root
        if len(path) == 0:
            tree['root']["P0"] = dict1
            tree['root']["P1"] = dict2
            for i in range(2, num_pointers+1):
                tree['root']["P%d" % i] = None
            del tree['root']["P%d" % num_pointers]

            tree['root']["K0"] = parent_key
            for i in range(1, num_pointers):
                tree['root']["K%d" % i] = None
            del tree['root']["K%d" % (num_pointers-1)]
        else:
            structure_change(dict1, dict2, path, parent_key)


    try:
        with open("Data/relation.{}.json".format(relation), "r") as openf:
            json_list = json.load(openf)
    except FileNotFoundError:
        print("relation.{}.json not found!".format(relation))
        return

    #get the id of the relation
    id_list = [i['author_id'] for i in json_list]

    #init an empty tree
    tree = {
        'root':[]
    }
    #generating the tree
    for element in id_list:
        insert_in_tree(element)
    with open("Data/btree.{}.json".format(relation), "w") as openf:
        json.dump(tree, openf, sort_keys=True, indent=5, ensure_ascii=False)
        openf.write('\n')