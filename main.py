from datetime import datetime
from labirinth import Labirinth
from astar import Astar
from interface import Interface

import random
          
def main():
    M = 16
    N = 34
    random.seed(datetime.now().timestamp())
    labirinth = Labirinth(M, N)
    labirinth.create_matriz()
    labirinth.random_init_path()

    astar = Astar(labirinth)
    path = astar.search()
    interface = Interface(labirinth, N, M, path)
    interface.run()

if __name__ == "__main__":
    main()