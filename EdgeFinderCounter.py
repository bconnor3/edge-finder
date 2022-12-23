import json
import re

import ElementSerializer
from ElementEnum import *
from Node import Node
from Square import Square
from Triangle import Triangle

# Join the directory and file names
file_path = 'OSU_sm_1_size_10_SVE_4_1.inp'

domain = {}
grains = {}
elements = {}
node_domains = dict()
triangle_domains = dict()
square_domains = dict()
shape_found = ElementEnum.DEFAULT


def find_nodes(file_lines, grain_id):
    global shape_found
    while node_line := next(file_lines):
        if "CPS3" in node_line:
            shape_found = ElementEnum.TRIANGLE
            return
        node_line = re.sub("\s*", "", node_line)
        node_values = node_line.split(",")
        node = build_node(node_values)
        node_domains[grain_id].append(node)


def build_node(node_values):
    if len(node_values) != 3:
        return
    return Node(node_values[0], node_values[1], node_values[2])


def find_triangles(file_lines, grain_id):
    global shape_found
    while triangle_line := next(file_lines):
        if "CPS4" in triangle_line:
            shape_found = ElementEnum.SQUARE
            return
        triangle_line = re.sub("\s*", "", triangle_line)
        triangle_values = triangle_line.split(",")
        triangle = build_triangle(triangle_values)
        triangle_domains[grain_id].append(triangle)


def build_triangle(triangle_values):
    if len(triangle_values) != 4:
        return
    return Triangle(triangle_values[0], triangle_values[1], triangle_values[2], triangle_values[3])


def find_squares(file_lines, grain_id):
    global shape_found
    while square_line := next(file_lines):
        if "Elset" in square_line:
            shape_found = ElementEnum.DEFAULT
            return
        square_line = re.sub("\s*", "", square_line)
        square_values = square_line.split(",")
        square = build_square(square_values)
        square_domains[grain_id].append(square)


def build_square(square_values):
    if len(square_values) != 5:
        return
    return Square(square_values[0], square_values[1], square_values[2], square_values[3], square_values[4])


def build_nodes_and_elements():
    with open(file_path, 'r') as f:
        file_lines = iter(f.readlines())
        for file_line in file_lines:
            if '*Node' and 'Output' in file_line:
                return
            if file_line.startswith('*Part, name=GRAIN-'):
                grain_id = int(file_line.split('-')[1])
                triangle_domains[grain_id] = []
                square_domains[grain_id] = []
                node_domains[grain_id] = []
                continue
            if "*Node" in file_line or shape_found == ElementEnum.NODE:
                find_nodes(file_lines, grain_id)
            if "CPS3" in file_line or shape_found == ElementEnum.TRIANGLE:
                find_triangles(file_lines, grain_id)
            if "CPS4" in file_line or shape_found == ElementEnum.SQUARE:
                find_squares(file_lines, grain_id)


def print_elements(domains, element_type):
    for key, values in domains.items():
        print(f"Grain ID:\t{key}")
        print(f"{element_type} values")
        print("------------")
        for value in values:
            print(value, "\t")


def write_to_json(file_name, dict_to_write):
    with open(file_name, 'w') as json_file:
        json.dump(dict_to_write, json_file, cls=ElementSerializer.ElementSerializer)


if __name__ == '__main__':
    build_nodes_and_elements()
    write_to_json('json/nodes.json', node_domains)
    write_to_json('json/triangles.json', triangle_domains)
    write_to_json('json/squares.json', square_domains)

    # print_elements(node_domains, ElementEnum.NODE.value)
    # print_elements(triangle_domains, ElementEnum.TRIANGLE.value)
    # print_elements(square_domains, ElementEnum.SQUARE.value)


# # Initialize variables to track the max and min values
# max_x = float('-inf')
# min_x = float('inf')
# max_y = float('-inf')
# min_y = float('inf')
#
# # Iterate over the keys in the dictionary
# for grain_ID in domain:
#     # Iterate over the tuples in the list of nodal information
#     for node in domain[grain_ID]:
#         # Extract the x and y values from the tuple
#         x, y = node[1], node[2]
#
#         # Update the max and min values as needed
#         max_x = max(max_x, x)
#         min_x = min(min_x, x)
#         max_y = max(max_y, y)
#         min_y = min(min_y, y)
#
# edge_1 = {}
# edge_2 = {}
# edge_3 = {}
# edge_4 = {}
#
# for grain_ID in domain:
#     edge_1[grain_ID] = []
#     edge_2[grain_ID] = []
#     edge_3[grain_ID] = []
#     edge_4[grain_ID] = []
#     for coord in domain[grain_ID]:
#         node_id, x, y = coord
#         if coord[1] == min_x:
#             edge_1[grain_ID].append((int(node_id)))
#         if coord[1] == max_x:
#             edge_2[grain_ID].append((int(node_id)))
#         if coord[2] == min_y:
#             edge_3[grain_ID].append((int(node_id)))
#         if coord[2] == max_y:
#             edge_4[grain_ID].append((int(node_id)))
#
# edges = [edge_1, edge_2, edge_3, edge_4]
#
# vertex_1 = {}
# vertex_2 = {}
# vertex_3 = {}
# vertex_4 = {}
# for grain_ID in domain:
#     vertex_1[grain_ID] = []
#     vertex_2[grain_ID] = []
#     vertex_3[grain_ID] = []
#     vertex_4[grain_ID] = []
#     for coord in domain[grain_ID]:
#         node_id, x, y = coord
#         if coord[1] == min_x and coord[2] == min_y:
#             vertex_1[grain_ID].append((int(node_id)))
#         if coord[1] == min_x and coord[2] == max_y:
#             vertex_2[grain_ID].append((int(node_id)))
#         if coord[1] == min_x and coord[2] == max_y:
#             vertex_3[grain_ID].append((int(node_id)))
#         if coord[1] == max_x and coord[2] == max_y:
#             vertex_4[grain_ID].append((int(node_id)))
#
# with open("BCs.txt", "w") as file:
#     for grain_ID in vertex_1:
#         if len(vertex_1[grain_ID]) == 0:
#             continue
#         elif len(vertex_1[grain_ID]) > 0:
#
#             file.write(f"*Nset, nset=vertex_1, instance=GRAIN-{grain_ID}\n")
#             file.write('%s\n' % ', '.join(map(str, vertex_1[grain_ID])))
#     # Use a for loop to write to the file multiple times
#     count = 1
#     for edge in edges:
#         count = count + 1
#         file.write('**Name: Disp-BC-%s Type: Displacement/Rotation' % (count))
#         file.write('\n*Boundary\n')
#         file.write(f"edge{count - 1}, 1, 1, 2\n")
#         file.write(f"edge{count - 1}, 2, 2\n")
#
# with open("Nsets.txt", "w") as file:
#     # Use a for loop to write to the file multiple times
#     count = 0
#     for edge in edges:
#         count = count + 1
#         for grain_ID in edge:
#             if len(edge[grain_ID]) == 0:
#                 continue
#             elif len(edge[grain_ID]) > 0:
#                 file.write('\n')
#                 file.write(f"*Nset, nset=edge_{count}, instance=GRAIN-{grain_ID}\n")
#                 file.write('%s\n' % ', '.join(map(str, edge[grain_ID])))
