# Billiard Ball Strategy Algorithm
## :star: Description
The algorithm is designed to find the opitmal solution of the billiards game. It contains the rules in the following:
1. Calculate angle of reflection (α)
2. Determine whether there are ball on ball-moving trajectory
3. Choose the optimal solution
4. Special conditon: applying Convex Hull of the balls

## :orange_book: Rules of the Algorithm
### 1. Caculate angle of reflection (α)

Calculate the angle of reflection (α) between the trajectory of cue ball and the trajectory of the ball being hitten.
If α = 0, then it's a direct collision, and if α = 90, then there is not possible for cue ball to hit the ball. As the result, the conditions can be classify into :bulb:two cases:

1. 0 < alpha < 90 : possible solution
2. alpha > 90 : impossible solution, needed to be exculded

![](https://i.imgur.com/fgd6DFj.png)

### 2. Determine whether there are ball on ball-moving trajectory
#### :bulb: Case 1: There is obstacle on the trajetory of cue ball

Suppose that we are going to hit "12 ball" into the hole. Because there is a green ball on the trajectory of cue ball, in this case, the solution of hitting 12 ball will be exculded.

![](https://i.imgur.com/cI5yDG0.png)


#### :bulb: Case 2: There is obstacle on the trajetory of the ball being hiiten

Suppose that we are going to hit "12 ball" into the hole. Because there is a green ball on the trajectory of 12 ball, in this case, the solution of hitting 12 ball will be exculded.

![](https://i.imgur.com/gBvDu5B.png)




### 3. Choose the optimal solution
After sifting all the possible solutions to the game, we will refer to the following factors to find the optimal solution: 

1. Angle of reflection(α)
3. D1: Distance from cue ball to the ball being hitten
4. D2: Distance from the ball being hitten to the hole


Giving weights to these three factors separatedly, and calculate weighted average. The solution with least weighted average will be the optimal solution.

For example, in solution 1, α、D1、D2 are all smaller than the factors in solution2. Thus we will choose solution 1 as the optimal solution.

![](https://i.imgur.com/WvHx3aV.png)

### 4. Special conditon: applying Convex Hull of the balls

Unfortunately, it is possible that there is no solution after following the rules above. In this case, we will detection the Convex Hull of all the balls on the table, and calculate the center of gravity(CG) of the area to be the target which the cue ball will hit.

![](https://i.imgur.com/pkiWJMN.png)