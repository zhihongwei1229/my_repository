#my_array=[1,2,3,4,5,6];
#print (my_array.index(5))
#print(my_array[2]);
#my_array.insert(3,9);
#print(my_array);

#from table import *
#o1=Table('users_role1');
#print(o1.table_name);

from operator import *
import xml.etree.ElementTree as ET
def count_words(s, n):
    """Return the n most frequently occuring words in s."""

    # TODO: Count the number of occurences of each word in s

    # TODO: Sort the occurences in descending order (alphabetically in case of ties)

    # TODO: Return the top n words as a list of tuples (<word>, <count>)
    import string
    #string_list = s.split(" ")
    string_list = sorted(s.split(" "), key=str)
    print(string_list)
    exit(0)
    wordList = []
    countList = []
    for word in string_list:
        #print(word + "| ")
        try:
            wordIndex = wordList.index(word)
            countList[wordIndex][1]+= 1
        except ValueError:
            wordList.append(word)
            countList.append([word, 1])

    top_n = sorted(countList, key=itemgetter(1), reverse=True)
    del top_n[n:]

    return top_n


def test_run():
    """Test count_words() with some inputs."""
    print
    count_words("cat bat mat cat bat cat", 3)
    print
    count_words("betty bought a bit of butter but the butter was bitter", 3)


if __name__ == '__main__':
    test_run()
