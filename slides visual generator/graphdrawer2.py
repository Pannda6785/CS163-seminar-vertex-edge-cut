from graphviz import Graph

# Create an undirected graph object
undirected_graph = Graph()

# Set node attributes
undirected_graph.attr('node', shape='circle', fontcolor='black')

# Add edges based on the new provided list
undirected_graph.edge('1', '7')
undirected_graph.edge('4', '2')
undirected_graph.edge('9', '4')
undirected_graph.edge('4', '11')
undirected_graph.edge('4', '13')
undirected_graph.edge('7', '4')
undirected_graph.edge('1', '10')
undirected_graph.edge('10', '6')
undirected_graph.edge('10', '6')
undirected_graph.edge('9', '11')
undirected_graph.edge('12', '6')
undirected_graph.edge('15', '7')
undirected_graph.edge('14', '15')
undirected_graph.edge('10', '15')

# Render and save the graph as a PNG file
undirected_graph.render(r'D:/An/Projects/_tests_/undirected_graph_2', format='png')
