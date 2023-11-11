# This exercise describes
# • the TSP (Traveling Salesman Problem) problem, which has been first formulated in 1930 and is one of the most intensively studied problems in optimization,
# • its formulation, we will see formulation slightly more complex than the ones seen before 
# • solution by means of the ompr library, which is a higher-level (compared to lpSolveAPI) library to # interact with MILP solvers.
# 
# One definition for the TSP:
# The Traveling Salesman Problem (TSP) asks the following question: Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each
# city exactly once and returns to the origin city? 
# With this basic definition you have a set of vertices (cities) and a set of edges (connections between cities).
# Each edge has an associated distance d > 0. That distance could be travel time, distance in km or the monetary cost associated with traveling from one city to another. Restrictions on the distances lead to special cases of the problem.
# For example the metric-TSP requires that the triangle inequality holds for all triples of edges (as for the euclidean distance).
# In this exercise, we will construct a TSP with random points within an Euclidean space.