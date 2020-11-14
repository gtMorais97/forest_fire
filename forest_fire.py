import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

forest_shape = (200,200)
forest_density = 0.7
p_fire = 0.1
p_extinguish = 0.15

def make_forest(shape, density):
    forest = np.zeros(shape)
    for i in range(len(forest)):
        for j in range(len(forest[i])):
          r = np.random.rand()
          if r < density:
            forest[i][j] = 1 #plant tree
    return forest

forest = make_forest(forest_shape, forest_density)
burning_trees = []

def get_first_tree():
    i = np.random.randint(forest.shape[0])
    j = np.random.randint(forest.shape[1])

    if forest[i][j] == 1:
        return (i,j)
    else:
        return get_first_tree()


first_tree = get_first_tree()
forest[first_tree[0]][first_tree[1]] = 2
burning_trees.append(first_tree)


def step():
    burning_aux=[]

    for tree in burning_trees:
        adjecent_trees = get_adjecent_trees(tree)
        for adj_tree in adjecent_trees:
          r = np.random.rand()
          if r<p_fire:
            forest[adj_tree[0]][adj_tree[1]] = 2 #set tree on fire
            burning_aux.append(adj_tree)

    for tree in burning_trees:
        r = np.random.rand()
        if r<p_extinguish:
            forest[tree[0]][tree[1]] = 3 #burnt tree
            burning_trees.remove(tree)

    burning_trees.extend(burning_aux)
    return forest


def get_adjecent_trees(tree):
    start_i = max(0, tree[0]-1)
    stop_i = min(len(forest)-1, tree[0]+1) +1

    start_j = max(0, tree[1]-1)
    stop_j = min(len(forest[0])-1, tree[1]+1) +1

    adjacent_trees = []
    for i in range(start_i, stop_i):
        for j in range(start_j, stop_j):
          if forest[i][j]==1 and (i,j) not in burning_trees:
            adjacent_trees.append((i,j))

    return adjacent_trees


fig = plt.figure(figsize=(15,15))

CM = mpl.colors.ListedColormap(['tan', 'forestgreen','maroon','grey'])
im = plt.imshow(forest, cmap=CM, vmin=0, vmax=3, interpolation='none', animated=True)

def updatefig(*args):
    im.set_array(step())
    return im,

anim = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
plt.axis('off')
plt.show()
