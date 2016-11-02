import numpy as np
import pandas as pd
from pandas import *


def avg_medal_count():
    countries = ['Russian Fed.', 'Norway', 'Canada', 'United States',
                 'Netherlands', 'Germany', 'Switzerland', 'Belarus',
                 'Austria', 'France', 'Poland', 'China', 'Korea',
                 'Sweden', 'Czech Republic', 'Slovenia', 'Japan',
                 'Finland', 'Great Britain', 'Ukraine', 'Slovakia',
                 'Italy', 'Latvia', 'Australia', 'Croatia', 'Kazakhstan']

    gold = [13, 11, 10, 9, 8, 8, 6, 5, 4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    silver = [11, 5, 10, 7, 7, 6, 3, 0, 8, 4, 1, 4, 3, 7, 4, 2, 4, 3, 1, 0, 0, 2, 2, 2, 1, 0]
    bronze = [9, 10, 5, 12, 9, 5, 2, 1, 5, 7, 1, 2, 2, 6, 2, 4, 3, 1, 2, 1, 0, 6, 2, 1, 0, 1]

    olympic_medal_counts = {'country_name': Series(countries),
                            'gold': Series(gold),
                            'silver': Series(silver),
                            'bronze': Series(bronze)}
    df = DataFrame(olympic_medal_counts)

    # YOUR CODE HERE
    if True:
        avg_bronze_at_least_one_gold = np.mean(df['bronze'][df.gold>=1])
        return avg_bronze_at_least_one_gold
    if False:
        #avg_medal_list = df[Series['gold', 'silver', 'bronze']][df.gold >= 1]
        avg_medal_list = df[['gold', 'silver', 'bronze']][(df.gold>=1) | (df.silver >=1) | (df.bronze >= 1)]
        avg_medal_count = np.mean(avg_medal_list)

        avg_medal_count_2 = df[['gold', 'silver', 'bronze']].apply(np.mean)
        return avg_medal_count_2
    if True:
        value_list = [4,2,1]
        medal_list = df[['gold', 'silver', 'bronze']]
        point_list =np.dot(medal_list, value_list)
        olympic_points = {
            'country_name': Series(countries),
            'points': Series(point_list),
        }
        olympic_points_df = DataFrame(olympic_points)
        return olympic_points_df



if True: #numpy
    if False:
        array = np.array([1, 4, 5, 8], float)
        print (array)
        array = np.array([[1, 2, 3], [4, 5, 6]], float)  # a 2D array/Matrix
        print (array)

    if False:
        array = np.array([1, 4, 5, 8], float)
        print(array[1])
        print(array[:2])
        print(array[2:])

    if False:
        two_D_array = np.array([[1, 2, 3], [4.5, 5, 6]], float)
        print(two_D_array[1][1])
        print(two_D_array[1, :])
        print(two_D_array[:, 2])

    if False:
        array_1 = np.array([[1, 2], [3, 4]], float)
        array_2 = np.array([[5, 6], [7, 8]], float)
        #array_2 = np.array([[5, 6], [7, 8], [10, 20]], float)
        print(array_1 + array_2)
        print(array_1 - array_2)
        print(array_1 * array_2)  #multiple on each dimention's element at the same location, not dot product

    if False:
        array_1 = np.array([1, 2, 3], float)
        array_2 = np.array([[6, 10], [7, 11], [8, 12]], float)
        print(np.mean(array_1))
        print(np.mean(array_2)) #add up all dimentions' all elements and divide by all elements' number
        print(np.dot(array_1, array_2))  # [1*6+2*7+3*8, 1*10+2*11+3*12]

if True: #pandas
    if False:
        #d = pd.Series([])
        d = {'name':pd.Series(['Braund', 'Cummings', 'Heikkinen', 'Allen'], index=['a','b','c','d']),
             'age': pd.Series([23, 38, 26, 35], index=['a','b','c','d']),
             'fare': pd.Series([7.25, 17.83, 8.05], index=['a', 'b', 'd']),
             'survived?': pd.Series([False, True, True, False], index=['a', 'b', 'c', 'd'])
            }
        df = DataFrame(d)
        df_survived = df['survived?'][df['age']>30]
        df_row = df.loc['a']
        #print(df)
        #print(df[df['age']>30])
        #print(df_survived)
        print(df_row)
        #print(df['survived?'][df['age']>30])

    if False:
        series = pd.Series(['Dave', 'Cheng-Han', 359, 9001],
                           index=['Instructor', 'Curriculum Manager',
                                  'Course Number', 'Power Level'])
        print(series['Instructor'])
        #print(series[['Instructor', 'Curriculum Manager', 'Course Number']])

    if False:
        cuteness = pd.Series([1, 2, 3, 4, 5], index=['Cockroach', 'Fish', 'Mini Pig','Puppy', 'Kitten'])
        print(cuteness > 3)
        print(cuteness[cuteness > 3])

    if False:
        data = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
                'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions',
                         'Lions', 'Lions'],
                'wins': [11, 8, 10, 15, 11, 6, 10, 4],
                'losses': [5, 8, 6, 1, 5, 10, 6, 12]}
        football = pd.DataFrame(data)
        print(football['year'])
        print("")
        print(football.year)  # shorthand for football['year']
        #print(football[['year', 'wins', 'losses']])

    if False:
        data = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
                'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions',
                         'Lions', 'Lions'],
                'wins': [11, 8, 10, 15, 11, 6, 10, 4],
                'losses': [5, 8, 6, 1, 5, 10, 6, 12]}
        football = pd.DataFrame(data)
        print(football.iloc[[0]])

        print(football.loc[[0]])

        print(football[3:5])
        print("")
        print(football[football.wins > 10])
        print("")
        print(football[(football.wins > 10) & (football.team == "Packers")])

    if False:
        d = {
            'one': Series([1,2,3], index=['a', 'b', 'c']),
            'two': Series([1,2,3,4], index=['a', 'b', 'c', 'd'])
        }
        df = DataFrame(d)
        df_mean = df.apply(np.mean)
        df_great_than_one = df['one'].map(lambda x:x>= 1)
        df_great_than_one_2 = df.applymap(lambda x:x>=1)
        print(df_great_than_one_2)
    if False:
        print(avg_medal_count())


