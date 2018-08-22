# Project utility functions

def get_string_datetime(datetime):
    """
        datatime(datetime.datetime.now()): datetime object
        returns string datetime till micro seconds
    """
    return datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

def find_longest_sub_list(list_of_lists):
    """
        Find the list having largest length
    """
    largest = []
    if list_of_lists:
        largest = list_of_lists[0]
        for list in list_of_lists[1:]:
            if len(list) > len(largest):
                largest = list
    
    return largest



if __name__ == "__main__":
    list = [
        ['A'],
         ['A', 'B', 'C', 'E'],
        ['A', 'B'],
        ['A', 'B', 'C']
    ]
    # list = []
    print(find_longest_sub_list(list))
