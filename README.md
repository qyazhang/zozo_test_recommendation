# zozo_test_recommendation
  This is the program for zozo's test to build a simple prototype of recommendataion system. All program is implemented with 
  Python3

### Recommendation sysytem with Item Collaborative Filtering
  This recommendation system is implemented with collaborative filtering (CF) algorithm, which is a classicial recommendation system
  used in large range of situation. Here, for certain, I choose to use ItemCF to give recommendation.
  
  The implementation of **ItemCF.py** referring to 
  > https://github.com/Lockvictor/MovieLens-RecSys/blob/master/itemcf.py
  
  Here I use the same movielens 1M dataset to train the model, whici is uploaded in 
  > ml-1m
  
  Updated from the original one, I choose to use the cosine similarity calculated with movie rates to give the similarity 
  between items.
  
  We could get the recommendation model by running 
  
    python ItemCF.py //In Win
    python3 ItemCF.py //In Linux/Mac
    
  However I didn't apply numeric calculation or matrix calculation library for calculation, the running speed is not so good.
  It may cost about 5 hours to complete the training.
  
  The **temp.txt** saved here is part of the result, where including the movie ID and related movie's ID and similarity.
  
### Recommendataion system with Word2Vec
  This recommendation system is implemented with Word2Vec algorithm, which is a new and good algorithm in NLP field.
  
  Here, considering the costume's selection also have some relationship similar to the one in side words and sentences, 
  we consider the shopping lists as sentences, and use Word2Vec skip-gram model to give recommendation with most related "words"
  
  Here, for I didn't find the shopping list dataset, I choose to use a music playlist dataset to simulate it. It is uploaded to 
  > dataset
  
  and is provided thanks to Cornell University
  > https://www.cs.cornell.edu/~shuochen/lme/data_page.html
  
  The implementation of **word2vecRec.py** is referring to the word2vec example provided by tensorflow
  > https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/word2vec/word2vec_basic.py
  
  We could get the result by running 
  
    python word2vecRec.py //In Win
    python3 word2vecRec.py //In Linux/Mac
  
  Here I load the dataset and add the tag of singers to each song ID to build an "artical". Use this artical and 
  word2vec in tensorflow, we could get the result model of word's similarity (or saying, relationship). The model and 
  result figure is saved in this repo as
  > log
  
  and
  > tsne.png
  
  Using this trained model, we could give recommendation with nearest word, which indicating similar singers.
  
