'''
Advanced Database course project
B+TREE
'''
import time
import relation_generator as rg
import tree_generator as tg
import key_search as ks
import natural_join as nj


def main():
    '''
    main function
    '''

    def command_checker(max_command):
        '''
        makes sure the input is valid
        '''
        #keep asking until a valid input
        while True:
            try:
                command = int(input("Pick a command to execute: "))
                if command < 1 or command > max_command:
                    raise ValueError
            except ValueError:
                print("Not a valid number. Try again...\n")
            else:
                break
        return command


    def user_input():
        '''
        Get user input
        '''

        print("\nAvailable commands:\n\n \
    [1] Generate files containing data \n \
    [2] Generate B+Trees \n \
    [3] Search for a specific key\n \
    [4] Natural join\n \
    [5] Exit\n")
        #gets a valid user input
        command = command_checker(5)

        #commands for generating a file
        if command == 1:
            print("\nAvailable commands:\n\n \
    [1] Generate a data file for authors \n \
    [2] Generate a data file for books \n \
    [3] Back\n ")
            command = command_checker(3)
            while True:
                try:
                    size_relation = int(input("State the desired size of the relation: "))
                    if size_relation < 1:
                        raise ValueError
                except ValueError:
                    print("Not a valid number")
                else:
                    break
            start_time = time.time()
            if command == 1:
                rg.author_gen(size_relation)
            elif command == 2:
                rg.book_gen(size_relation)
            print("Execution time: {}".format(time.time() - start_time))


        #commands for building a B+tree
        elif command == 2:
            print("\nAvailable commands:\n\n \
    [1] Build a B+-tree file on the author data file \n \
    [2] Build a B+-tree file on the book data file \n \
    [3] Back\n ")
            command = command_checker(3)
            #Gets the desired details for the B+tree
            while True:
                try:
                    print("Enter the desired M and L:\n")
                    num_pointers = int(input("M (number of pointers):"))
                    size_bucket = int(input("L (size of the bucket):"))
                    if num_pointers < 3 or size_bucket < 1:
                        raise ValueError
                except ValueError:
                    print("Not a valid number. Try again...\n")
                else: break
            start_time = time.time()
            if command == 1:
                tg.btree_gen("authors", size_bucket, num_pointers)
            elif command == 2:
                tg.btree_gen("books", size_bucket, num_pointers)
            print("Execution time: {}".format(time.time() - start_time))

        #commands for a key search
        elif command == 3:
            print("\nAvailable commands:\n\n \
    [1] Search inside authors\n \
    [2] Search inside books\n \
    [3] Back\n ")
            command = command_checker(3)
            #get the desired key
            while True:
                try:
                    key = int(input("Insert your desired key:"))
                    if key < 0:
                        raise ValueError
                except ValueError:
                    print("Not a valid number. Try again...\n")
                else: break

            if command == 1:
                ks.search("authors", key)

            elif command == 2:
                ks.search("books", key)

        elif command == 4:
            start_time = time.time()
            nj.natural_join()
            print("Execution time: {}".format(time.time() - start_time))
        else:
            return
        user_input()






    user_input()




main()
