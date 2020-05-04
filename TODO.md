# To do
AD:
1. Change .successors()

   - Change this function to only consider words that share a syllable with our current word

2. Be able to find words that contain a syllable

   - sqllite3?

---------
TP:
3. chain together smaller portmanteaus into larger portmanteuas in a concurrent fashion

    - have threads doing random restart of BFS/DFS (optimal length?)
    - put these portmanteaus into some sort of Data Structure
    - chain portmanteaus from this datastructure along to find the best portmanteau
