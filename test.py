al=["a","b","c","d"]


for i1,ball1 in enumerate(al[:-1]):
    for si2,ball2 in enumerate(al[i1+1:]):
        print(i1,si2+i1,ball1,ball2)