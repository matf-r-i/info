from datetime import datetime
import sys
from math import floor
import linopy
import networkx as nx
import numpy as np


def get_non_zero_values_idx(values):
    return np.nonzero(values)[0]


def get_non_zero_values(values):
    return [x for x in values if x != 0]


def check_clique(solution, graph):
    subgraph = graph.subgraph(solution)
    num_of_edges = subgraph.number_of_edges()
    return num_of_edges == int(subgraph.number_of_nodes() * (num_of_edges - 1) / 2)


def print_solution(objective_value, true_obj, path, time, is_clique):
    print(f"graph: {path}")
    print(f"objective value: {objective_value}")
    print(f"\ntime exec: {time}")
    path_pr = path.split('\\')[-1]
    print(f"{path_pr}, {objective_value}, {true_obj}, {time}, {is_clique}")


def read_graph_file(file_path, verbosity: bool):
    """
        Parse .col file and return graph object
    """
    edges = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c'):  # graph description
                if verbosity:
                    print(*line.split()[1:])
            # first line: p name num_of_vertices num_of_edges
            elif line.startswith('p'):
                _, name, vertices_num, edges_num = line.split()
                if verbosity:
                    print('{0} {1} {2}'.format(name, vertices_num, edges_num))
            elif line.startswith('e'):
                _, v1, v2 = line.split()
                edges.append((v1, v2))
            else:
                continue
        return nx.Graph(edges)


def get_problem(graph: nx.Graph)->Model:

    ind_sets = get_ind_sets(graph)

    not_connected_edges_list = list(nx.complement(graph).edges)

    list_nodes = list(graph.nodes)
    list_nodes_int = [int(i) for i in list_nodes]
    list_nodes_int.sort()

    names = ['x' + str(i) for i in list_nodes_int]
    objective = [one] * max(list_nodes_int)
    lower_bounds = [zero] * max(list_nodes_int)
    upper_bounds = [one] * max(list_nodes_int)

    problem = Model()
    problem.objective.set_sense(problem.objective.sense.maximize)
    problem.variables.add(obj=objective,
                            lb=lower_bounds,
                            ub=upper_bounds,
                            names=names)

    constraints = [[['x' + edges_pair[0], 'x' + edges_pair[1]], [one, one]] for edges_pair in not_connected_edges_list]
    for ind_set in ind_sets:
        constraints.append([['x{0}'.format(x) for x in ind_set], [1.0] * len(ind_set)])

    constraint_names = ["c" + str(i) for i in range(len(constraints))]

    rhs = [one] * len(constraints)
    constraint_senses = ["L"] * len(constraints)
    # print(constraints)
    problem.linear_constraints.add(lin_expr=constraints,
                                    senses=constraint_senses,
                                    rhs=rhs,
                                    names=constraint_names)
    for i in list_nodes_int:
        if solve_integer:
            problem.variables.set_types(i - 1, problem.variables.type.binary)
        else:
            problem.variables.set_types(i - 1, problem.variables.type.continuous)

    return problem


verbosity = False
paths, graphs = [], []

graph = read_graph(path, verbosity)

problem_max_clique = get_problem(graph)
problem_max_clique.set_log_stream(None)
problem_max_clique.set_results_stream(None)
problem_max_clique.solve()

values = problem_max_clique.solution.get_values()
objective_value = problem_max_clique.solution.get_objective_value()
print_solution(objective_value, objective_value, path, (datetime.now() - start).total_seconds(),
                check_clique(values, graph))


