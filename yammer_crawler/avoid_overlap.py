#!/usr/bin/env python


# for MacOS
import matplotlib
matplotlib.use('TkAgg')
# for MacOS
import matplotlib.pyplot as plt


from adjustText import adjust_text
import numpy as np

def draw_overlap():
    np.random.seed(0)
    x, y = np.random.random((2,30))
    print("DEBUG x: {}".format(x))
    print("DEBUG y: {}".format(y))

    fig, ax = plt.subplots()

    #plt.plot(x, y, 'bo')
    p_scatter = ax.scatter(x, y, s=155, alpha=0.5, marker='o', cmap=plt.get_cmap("Spectral"))

    texts = [plt.text(x[i], y[i],\
                      'Text%s' % i, ha='center', va='center') for i in range(len(x))]

    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))
    plt.show()


if __name__ == '__main__':
    draw_overlap()
