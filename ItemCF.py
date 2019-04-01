import sys
import random
import math
import os
import copy
from operator import itemgetter

from collections import defaultdict

random.seed(0)


class ItemBasedCF(object):

    def __init__(self):
        self.traindataset = {}
        self.testdataset = {}

        self.rec_movie_num = 7

        self.movie_sim_mat = {}
        self.movie_popular = {}
        self.movie_list = {}
        self.movie_last_ID = 0
        self.movie_count = 0

        print('Set recommended movie number = %d' %
              self.rec_movie_num, file=sys.stderr)

    def create_dataset(self, rateFilename, movieFilename, pivot=0.75):
        # load rating data into training dataset and testing dataset
        traindataset_len = 0
        testdataset_len = 0
        fp1 = open(rateFilename, 'r')
        for line in fp1:
            user, movie, rating, _ = line.split('::')
            if random.random() < pivot:
                self.traindataset.setdefault(user, {})
                self.traindataset[user][movie] = int(rating)
                traindataset_len += 1
            else:
                self.testdataset.setdefault(user, {})
                self.testdataset[user][movie] = int(rating)
                testdataset_len += 1

        fp2 = open(movieFilename, 'rb')
        for line in fp2:
            movieID, name, typeName = line.decode(
                "utf-8", 'ignore').split('::')
            self.movie_last_ID = movieID

        for user, movies in self.traindataset.items():
            for item in movies.items():
                if item[0] in self.movie_list:
                    self.movie_list[item[0]][user] = item[1]
                else:
                    self.movie_list.setdefault(item[0], {})

        print('training dataset size = %s' % traindataset_len, file=sys.stderr)
        print('testing dataset size = %s' % testdataset_len, file=sys.stderr)

    def calc_movie_sim(self):
        for user, movies in self.traindataset.items():
            for movie in movies:
                # count item popularity
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                self.movie_popular[movie] += 1

        print('count movies number and popularity succ', file=sys.stderr)

        # save the total number of movies
        self.movie_count = len(self.movie_popular)
        print('total movie number = %d' % self.movie_count, file=sys.stderr)

        # calculate movie similarity matrix

        print('calculating movie similarity matrix...', file=sys.stderr)
        simfactor_count = 0
        PRINT_STEP = 100000
        
        f = open("temp.txt", 'w+')
        for movieItem1 in self.movie_list.items():
            self.movie_sim_mat.setdefault(movieItem1[0], defaultdict(int))
            for movieItem2 in self.movie_list.items():
                # print(item1)
                item1Copy = copy.deepcopy(movieItem1)
                item2Copy = copy.deepcopy(movieItem2)
                for userWithRateItem1 in list(item1Copy[1]):
                    # print(userWithRateItem1)
                    if userWithRateItem1 not in item2Copy[1]:
                        item1Copy[1].pop(userWithRateItem1)
                for userWithRateItem2 in list(item2Copy[1]):
                    # print(userWithRateItem1)
                    if userWithRateItem2 not in item1Copy[1]:
                        item2Copy[1].pop(userWithRateItem2)
                #print(item1Copy[0])
                #print(item2Copy[0])
                sum_mul = 0
                one_mul = 0
                two_mul = 0
                for (k,v), (k2,v2) in zip(item1Copy[1].items(), item2Copy[1].items()):
                    #print(k, v)
                    #print(k2, v2)
                    sum_mul += v*v2
                    one_mul += v*v
                    two_mul += v2*v2
                #print(simfactor_count, file = f)
                #print(item1Copy[0],item2Copy[0],sum_mul,one_mul,two_mul,file = f)
                if (math.sqrt(one_mul) * math.sqrt(two_mul) == 0):
                    self.movie_sim_mat[item1Copy[0]][item2Copy[0]] = 0
                else:
                    self.movie_sim_mat[item1Copy[0]][item2Copy[0]] = sum_mul / (
                        math.sqrt(one_mul) * math.sqrt(two_mul))
                    #print(movie_sim_mat[item1Copy[0]][item2Copy[0]], file = f)

                #print("cosin sim")
                #print(item1Copy[0], item2Copy[0])
                #print(movie_sim_mat[item1Copy[0]][item2Copy[0]])
                simfactor_count += 1
                if simfactor_count % PRINT_STEP == 0:
                    print('calculating movie similarity factor(%d)' %
                        simfactor_count, file=sys.stderr)

        print('calculate movie similarity matrix(similarity factor) succ',
              file=sys.stderr)
        print('Total similarity factor number = %d' %
              simfactor_count, file=sys.stderr)
        for line in self.movie_sim_mat.items():
            print(line, file = f)
        # count item popularity
        # print(movie_sim_mat[item1[0]][item2[0]])
        # count co-rated users between items

        print('build co-rated users matrix succ', file=sys.stderr)

        simfactor_count = 0

    def recommend(self, movie):
        ''' Find K similar movies and recommend N movies. '''
        N = self.rec_movie_num
        rank = {}
        
        similar_dict = self.movie_sim_mat.get(movie)
        sorted_movie = sorted(similar_dict.items(key=lambda k_v: k_v[1],reverse=True))
        # return the N best movies
        return sorted_movie[:N]

if __name__ == '__main__':
    ratingfile = os.path.join('ml-1m', 'ratings.dat')
    moviefile = os.path.join('ml-1m', 'movies.dat')
    itemcf = ItemBasedCF()
    itemcf.create_dataset(ratingfile, moviefile)
    itemcf.calc_movie_sim()
    print(itemcf.recommend('115'))
