import matplotlib.pyplot as plt
import numpy as np

def plot_Ising_configuration(spins):
    '''

    this is just a helper function to plot the configuration of spins  given by 'spins'

    '''
    N = np.shape(spins)[1]
    fig, ax = plt.subplots()
    fig.add_axes()
    ax = fig.axes[0]
    for i in range(N):
        ax.plot([i, i], [0,N-1], 'k')
        ax.plot([0,N-1], [i,i], 'k')

    colors = ['b', 'gold'] # note: blue is down, red is up!
    for i in range(N):
        for j in range(N):
            fig.gca().add_patch(plt.Circle((i,j), radius=0.35, fc=colors[int((spins[i,j]+1)/2.)]))

    ax.set_ylim(-1,N+1)
    ax.set_xlim(-1,N+1)
    ax.set_aspect('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis('off')
    fig.show()


def plot_ILGT_configuration(spins, dual=False):
    '''

    this is just a helper function to plot the configuration of spins  given by 'spins'
    note that (i,j) denotes a vertex coordinate, such that the location of the plaquette
    center is at (i+0.5, j+0.5) and thus, the x spin is at (i+1, j+0.5) etc.

    Parameters
    ----------
    spins  :  int
        spin configuration, dimension is NxNx2
    dual   :  bool
        Plot the configuration in dual space or not. Default is False.
    '''
    N = np.shape(spins)[1]
    fig, ax = plt.subplots()
    fig.add_axes()
    ax = fig.axes[0]
    for i in range(N+1):
        ax.plot([i, i], [0,N], 'k')
        ax.plot([0,N], [i,i], 'k')

    if not dual:
        colors = ['b', 'gold'] # note: blue is down, red is up!
        for i in range(N):
            fig.gca().add_patch(plt.Circle((0,i+0.5), radius=0.2, fc=colors[int((spins[-1,i,0]+1)/2.)]))
            fig.gca().add_patch(plt.Circle((i+0.5,0), radius=0.2, fc=colors[int((spins[i,-1,1]+1)/2.)]))
            for j in range(N):
                fig.gca().add_patch(plt.Circle((i+1,j+0.5), radius=0.2, fc=colors[int((spins[i,j,0]+1)/2.)]))
                fig.gca().add_patch(plt.Circle((i+0.5,j+1), radius=0.2, fc=colors[int((spins[i,j,1]+1)/2.)]))

    if dual:
        excitation = []
        for i in range(N):
            if spins[-1, i,0]==1: ax.plot([-0.5, 0.5], [i+0.5, i+0.5], 'b', lw=3)
            if spins[i, -1,1]==1: ax.plot([i+0.5, i+0.5], [-0.5, 0.5], 'b', lw=3)
            for j in range(N):
                j_up = (N+j-1)%N
                i_left = (i+N-1)%N
                if spins[i,j,0]==1: ax.plot([i+0.5, i+1.5], [j+0.5, j+0.5], 'b', lw=3)
                if spins[i,j,1]==1: ax.plot([i+0.5, i+0.5], [j+0.5, j+1.5], 'b', lw=3)
                if spins[i,j, 0]*spins[i_left, j, 0]*spins[i,j,1]*spins[i,j_up, 1]==-1: excitation.append([i+0.5,j+0.5])
        if len(excitation)>0: plt.scatter(np.array(excitation)[:,0], np.array(excitation)[:,1], color='red', s=350, marker=(5,1))
    ax.set_ylim(-1,N+1)
    ax.set_xlim(-1,N+1)
    ax.set_aspect('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis('off')
    fig.show()


def create_periodic_padding(configs, kernel_size):
    N = np.shape(configs)[1]
    padding = kernel_size-1
    x = []
    for config in configs:
        padded = np.zeros((N+2*padding, N+2*padding, 2))
        # lower left corner
        padded[:padding,:padding, :] = config[N-padding:,N-padding:,:]
        # lower middle
        padded[padding:N+padding, :padding, :] = config[:,N-padding:,:]
        # lower right corner
        padded[N+padding:, :padding, :] = config[:padding, N-padding:, :]
        # left side
        padded[:padding, padding:N+padding, :] = config[N-padding:, :, :]
        # center
        padded[padding:N+padding, padding:N+padding, :] = config[:,:,:]
        # right side
        padded[N+padding:, padding:N+padding, :] = config[:padding, :, :]
        # top left corner
        padded[:padding, N+padding:,:] = config[N-padding:, :padding, :]
        # top middle
        padded[padding:N+padding, N+padding:, :] = config[:, :padding, :]
        # top right corner
        padded[N+padding:, N+padding:, :] = config[:padding, :padding, :]
        x.append(padded)
    return np.array(x)
