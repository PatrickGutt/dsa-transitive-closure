import networkx as nx
import matplotlib.pyplot as plt
from system import System
from config import Config

class DirectedGraph:
    
    def __init__(self, edges: list):
        self.G = self.generate_directed_graph()
        self.name = 'EQUIVALENCE RELATION' + ' GRAPH'
        self.edges = edges
        self.nodes = self.map_nodes()
        self.num_of_nodes = self.compute_num_of_nodes()
        self.boolean_matrices = self.map_boolean_matrices()  
        self.G_transitive = None
        
        self.populate_boolean_matrices()
        self.add_edges()
        
    @classmethod
    def create_from_edges(cls, edges: list):
        return cls(edges)    
    
    @classmethod
    def create_from_boolean_matrix(cls, boolean_matrix: list):
        num_of_nodes = len(boolean_matrix)
        edges = []
        for i in range(num_of_nodes):
            for j in range(num_of_nodes):
                if boolean_matrix[i][j]:
                    edges.append((i + 1, j + 1))
                    
        return cls(edges)
    
    @classmethod
    def create_from_csv_file(cls, csv_file: str): 
        return cls(System.read_csv(csv_file))
    
    def get_transitive(self):
        if self.G_transitive is None:
            self.G_transitive = self.create_from_boolean_matrix(self.boolean_matrices['G+'])
        return self.G_transitive 
    
    def map_nodes(self):
        return {node: index for index, node in enumerate(sorted(set().union(*self.edges)))}
    
    def zeros_boolean_matrix(self):
        return [[0] * self.num_of_nodes for _ in range(self.num_of_nodes)]
    
    def map_boolean_matrices(self):
        b_m = {
            f'G{i}': self.zeros_boolean_matrix() 
            for i in range(1, self.num_of_nodes + 1)
        }
        b_m['G+'] = self.zeros_boolean_matrix()
        return b_m                      
    
    def populate_G1(self):
        for edge in self.edges:
            i, j = self.nodes[edge[0]], self.nodes[edge[1]]
            self.boolean_matrices['G1'][i][j] = 1  
       
    def populate_G2_to_Gn(self):
        num_of_nodes = self.num_of_nodes
        b_m = self.boolean_matrices                  
        for n in range(2, num_of_nodes + 1):
            for i in range(num_of_nodes):
                for j in range(num_of_nodes):
                    for k in range(num_of_nodes):
                        b_m[f'G{n}'][i][j] = b_m[f'G{n}'][i][j] or (b_m[f'G{n - 1}'][i][k] and b_m['G1'][k][j])
                        
    def populate_G_plus(self):
        num_of_nodes = self.num_of_nodes
        b_m = self.boolean_matrices
        for e in range(1, num_of_nodes + 1):
            for i in range(num_of_nodes):
                for j in range(num_of_nodes):
                    b_m['G+'][i][j] = b_m['G+'][i][j] or b_m[f'G{e}'][i][j]
    
    def populate_boolean_matrices(self):
        self.populate_G1()
        self.populate_G2_to_Gn()
        self.populate_G_plus()
                  
    def compute_num_of_nodes(self):
        return len(self.nodes)
  
    @staticmethod
    def generate_directed_graph():
        return nx.DiGraph()
    
    @staticmethod
    def print(matrix: list):
        for row in matrix:
            for element in row:
                print(element, end=' ')
            print()
      
    def add_edges(self):
        self.G.add_edges_from(self.edges)
        
    def get_graph(self):
        return self.G
    
    def get_edges(self):
        return self.edges
    
    def set_name(self, name: str):
        self.name = name
    
    @staticmethod
    def draw(graph: nx.DiGraph, axis: list, color: str):
        nx.draw_networkx(graph, 
                            ax = axis,
                            pos = nx.kamada_kawai_layout(graph), 
                            with_labels = True,
                            node_color = color, 
                            node_size = Config.node_size, 
                            edge_color = Config.edge_color, 
                            edgecolors = Config.node_border_color, 
                            width = Config.edge_thickness,
                            font_family = Config.font_family,
                            font_size = Config.font_size,
                            font_weight = Config.font_weight
                            )       
    
    def plot(self, file_path: str):
        fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = Config.fig_size)

        axs[0].set_title('original_graph')
        self.draw(self.get_graph(), axs[0], Config.node_color)
        
        axs[1].set_title('transitive_closure')
        self.draw(self.get_transitive().get_graph(), axs[1], Config.node_color_transitive)
       
        fig.patch.set_facecolor(Config.fig_background_color)
        
        plt.suptitle(self.name)
        plt.tight_layout()
        plt.savefig(file_path, format='png', bbox_inches='tight')