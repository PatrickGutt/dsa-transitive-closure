from config import Config
from directed_graph import DirectedGraph
from system import System

def main():
    
    cwd = System.get_cwd()
    data_dir_path = System.get_file_path(cwd, Config.data_dir)    
    data_files = System.list_dir(data_dir_path)
    output_dir = System.get_file_path(Config.output_dir)
    
    
    for file in data_files:
        file_path = System.get_file_path(cwd, Config.data_dir, file)
        file_name = System.get_file_name(file)
        output_file_path = System.get_file_path(output_dir, file_name)

        graph = DirectedGraph.create_from_csv_file(file_path)
        graph.set_name(file_name)
        graph.plot(output_file_path + '.png')

if __name__ == '__main__':
    main()