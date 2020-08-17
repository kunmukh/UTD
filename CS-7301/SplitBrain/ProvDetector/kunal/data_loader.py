
import os
import pickle
import re
from utils import *
from random import shuffle

_BASE_PATH = "data";

NODE_TYPE_FILE = "File"
NODE_TYPE_PROCESS = "Process"
NODE_TYPE_NET = "InetChannel"

def replace_ip_parts(ip, new, start=2):
    delimiter = "." if "." in ip else ":"
    parts = ip.split(delimiter)
    for i in range(start, len(parts)):
        parts[i] = new
    return delimiter.join(parts)

def get_basename(path):
    if "/" in path:
        return path.split("/")[-1]
    return path

def is_windows(path):
    return path.startswith("C:/") or path.isupper()

import uuid
def rand_string(length=6):
    s = str(uuid.uuid4())
    return s[0:length]

class Config(object):

    def __init__(self):
        self.dict = dict()
        self.preprocessing = False
        #self.no_duplicate = False    
            
        self.basename = False
        self.abstract_name = False
        self.abstract_ip = False

        # both, forward, backward
        self.direction = "both"

        # max lenth
        # same length
        # contain self-node    
        self.fix_length = False

        self.max_samples = None
        
    def __str__(self):
        return str(self.__dict__)

class Node(object):

    def __init__(self, node_type, label, hop=None):
        self.type = node_type
        self.label = label
        self.hop = hop
        self.labels = None

        if node_type == NODE_TYPE_NET:
            parts = label.split("/")
            self.srcip = parts[0].strip()
            self.srdport = parts[1].split(":")[1].strip() 
            self.dstip = parts[2].strip()
            self.dstport = parts[3].split(":")[1].strip() 

    def get_label(self, include_type=False):
        if include_type:
            return self.type+":"+self.label
        return self.label

class Edge(object):

    def __init__(self, label, srcNode=None, dstNode=None):
        self.label = label
        self.srcNode = srcNode
        self.dstNode = dstNode

    def get_label(self):
        dst_type = self.dstNode.type
        if dst_type == NODE_TYPE_PROCESS:
            prefix = "P"
        elif dst_type == NODE_TYPE_FILE:
            prefix = "F"
        if dst_type == NODE_TYPE_NET:
            prefix = "N"

        return prefix+"_"+self.label

class Path(object):

    def __init__(self):
        self.edges = []
        self.ndss_score=None
        self.anomaly_score=None
        self.file_name = None
        self.line_num = 0
        self.line = ""

    def add_edge(self, edge):
        self.edges.append(edge)        

    def get_nodes(self):
        res = []
        res.append(self.edges[0].srcNode)
        for edge in self.edges:
            res.append(edge.dstNode)
        return res

    def get_length(self):
        return len(self.edges)

    def to_words(self, include_edge=False, include_type=False):
        res = []
        node = self.edges[0].srcNode
        res.append(node.get_label(include_type))
        for edge in self.edges:
            if include_edge:
                res.append(edge.get_label())            
            node = edge.dstNode
            res.append(node.get_label(include_type))
        return res

    
class PathDataLoader(object):

    def __init__(self, program_name, is_benign, base_path=_BASE_PATH):
        self.processed = False 
        self.program = program_name
        self.is_benign = is_benign
        self.base_path = os.path.join(base_path, "benign" if is_benign else "anomaly")
        self.folder_path = os.path.join(self.base_path, program_name)
        self.config = Config()
        self.file_names = None

    def get_files_in_folder(self):
        folder = self.folder_path
        return [os.path.join(folder, name) for name in os.listdir(folder) if name.endswith(".csv")]

    def get_file_names(self):
        folder = self.folder_path
        if self.file_names:
            return self.file_names
        else:
            return [os.path.join(folder, name) for name in os.listdir(folder) if name.endswith(".csv")]

    def get_file_count(self):
        return len(self.get_file_names()) 

    def get_line_count(self):
        total = 0
        for name in self.get_file_names():
            total += len(open(name).readlines())-1
        return total

    def get_used_file_count(self):
        res = []
        for name in self.get_file_names():
            paths = self.load_paths_from_file(name) 
            if len(paths) > 0:
                res.append(name)
        return len(res) 

    def get_agents(self):
        res = set();
        for name in self.get_file_names():
            agent = name.split("+")[-1].split(".") [0]
            res.add(agent)
        return res
         
    def get_db_names(self):
        res = set();
        for name in self.get_file_names():
            db = name.split("-")[2].split("+")[0]
            res.add(db)
        return res

    def is_self(self, name):
        basename = get_basename(name)
        return basename.lower().replace(".exe","") == self.program
        

    def get_all_names(self):
        res = set()
        for file_name in self.get_file_names():
            for line in open(file_name).readlines()[1:]:
                line = self.process_line(line)[0]
                parts = line.split(" <-- ")
                for part in parts:
                    if "[" not in part:
                        continue
                    part = self.build_node(part).label
                    if self.is_self(part):
                        res.add(part)
        return res

    def get_path_count(self):
        return len(self.load_paths())       
 
    # Load #num paths from each file
    def load_paths(self, num=None):
        res = []
        for name in self.get_file_names():
            paths = self.load_paths_from_file(name, num) 
            for path in paths:
                res.append(path)
                if self.config.max_samples and len(res) >= self.config.max_samples:
                    return res
        return res

    def load_path_groups(self, k, num=1, rand=False):
        res = []
        for name in self.get_file_names():
            path_groups = self.load_k_paths_from_file(name, k, num, rand)
            for path_group in path_groups:
                res.append(path_group)
                if self.config.max_samples and len(res) >= self.config.max_samples:
                    return res
        return res

    def build_node(self, text):
        index1 = text.index("[")
        index2 = text.index("]")
        node_type = text[index1+1:index2]
        index1 = text.index("(")
        index2 = text.index(")")
        hop = int(text[index1+1:index2])
        label = text[index2+1:].strip()
        return Node(node_type, label, hop)
    
    def process_line(self, line):
        line = line.replace("\n","")
        if line[-1] == ",":
            line = line[0:-1]
        cols = line.split(",")
        line = ",".join(cols[3:])
        return (line, float(cols[1]), float(cols[2]))

    def load_k_paths_from_file(self, file_name, k, generate_num, rand):
        res = []
        paths = self.load_paths_from_file(file_name)
        if len(paths) < k:
            return [paths]

        if not rand:
            index = 0
            while (index + k) < len(paths) and len(res) < generate_num:
                res.append(paths[index:index+k])
                index += 1
        else:
            while len(res) < nCr(len(paths), k)*2 and len(res) < generate_num:
                shuffle(paths)
                res.append(paths[0:k])
        return res

    def load_paths_from_file(self, file_name, k=None):
        res = []
        if k:
            k+= 1
        line_num = 0
        for line in open(file_name).readlines()[1:k]:
            line_num += 1
            line, ndss_score, anomaly_score = self.process_line(line)
            path = Path()
            parts = line.split(" <-- ")
            parts.reverse()
            srcNode = self.build_node(parts[0])
            edge = None
            for i in range(1, len(parts)):
                part = parts[i]
                if i%2 ==0:
                    dstNode = self.build_node(part)
                    edge.srcNode = srcNode
                    edge.dstNode = dstNode
                    srcNode = dstNode
                else:
                    edge = Edge(part)
                    path.add_edge(edge)
            path = self.prune_path(path)                
            if path:
                path.file_name = file_name
                path.line_num = line_num
                path.line = line
                path.ndss_score = ndss_score
                path.anomaly_score = anomaly_score
                res.append(path)

        return res

    def prune_path(self, path):
        config = self.config
        ignore = config.preprocessing 
        for node in path.get_nodes():
            label = node.get_label()
            if config.preprocessing:
                if node.type != NODE_TYPE_NET:
                    label = label.replace("VIRUSSIGN.COM",rand_string()) 
                    label = label.replace("VIRUSSHARE",rand_string()) 
                    label = label.replace("INJECT-X86",rand_string()) 
                    label = re.sub(r"/USERS/(.*?)/","/USERS/*/", label)
                    if label.count("C:/") > 1:
                        index = label.index("C:/", 1)
                        label = label[0:index].strip()                
                    node.label = label               

                    if self.is_self(label):
                        ignore = False
                else:
                    node.label = node.dstip+":"+node.dstport
         
            if config.basename:
                if node.type == NODE_TYPE_FILE or node.type == NODE_TYPE_PROCESS:
                    node.label = get_basename(label)

            if config.abstract_name:
                if node.type == NODE_TYPE_FILE or node.type == NODE_TYPE_PROCESS:
                    windows_flag = is_windows(label)
                    max_index = 16 if windows_flag else 10
                    parts = node.get_label().split("/")
                    for i in range(0, len(parts)):
                        part = parts[i]
                        tokens = part.split(".")
                        if len(tokens) > 1:
                            parts[i] =  tokens[0][0:max_index]+"."+tokens[1]
                        else:
                            parts[i] = part[0:max_index]
                    node.label = "/".join(parts)
        
            if config.abstract_ip and node.type == NODE_TYPE_NET:
                node.label = replace_ip_parts(node.dstip, "*")         

        direction = config.direction
        if direction == "backward":
            path_new = Path()
            for edge in path.edges:
                if self.is_self(edge.dstNode.get_label()):
                    break
                path_new.add_edge(edge)
            path = path_new if path_new.get_length() > 0 else None 
        elif direction == "forward":
            path_new = Path()
            add_flag = False
            for edge in path.edges:
                if add_flag:
                    path_new.add_edge(edge)
                elif self.is_self(edge.srcNode.get_label()):
                    path_new.add_edge(edge)
                    add_flag = True
            path = path_new if path_new.get_length() > 0 else None
        

        return path if not ignore else None

import networkx as nx
class NodozeGraphLoader(PathDataLoader):
    
    def __init__(self, program_name, is_benign, base_path=_BASE_PATH):
        PathDataLoader.__init__(self, program_name, is_benign, base_path)

    def build_graph_from_paths(self, paths):
        g = nx.DiGraph()
        for path in paths:
            for edge in path.edges:
                srcNode = edge.srcNode
                dstNode = edge.dstNode
                g.add_edge(srcNode.get_label(), dstNode.get_label(), label=edge.get_label())
        return g

    def load_graphs(self, k, num=1, rand=False):
        res = []
        groups = self.load_path_groups(k, num, rand)
        for path_group in groups:
            graph = self.build_graph_from_paths(path_group)
            res.append(graph)
        return res


from networkx.drawing.nx_pydot import read_dot
import networkx.algorithms.dag as dag

class DotNode(object):
    def __init__(self, id, label, shape):
        self.id = id
        self.type = None
        if shape=="box":
            self.type = NODE_TYPE_PROCESS
            label = label.replace(",\\n","").strip()
        elif shape=="oval":
            self.type = NODE_TYPE_FILE
        elif shape=="diamond":
            self.type = NODE_TYPE_NET
        self.label = label

# Edge types: FILE_EXEC, PROC_CREATE, READ_WRITE, IP_CONNECTION_EDGE, PROC_END
class DotEdge(object):
    def __init__(self, label, srcNode=None, dstNode=None):
        self.label = label
        self.srcNode = srcNode
        self.dstNode =dstNode

class DotGraph(object):
    def __init__(self, program_name, path):
        self.program = program_name
        self.path = path
        g = read_dot(path)
        node_labels = nx.get_node_attributes(g,'label')
        node_shapes = nx.get_node_attributes(g,'shape')
        node_dict = dict()
        nodes = []
        for node_id in g.nodes:
            label = node_labels[node_id].replace('"','')
            node = DotNode(node_id, label, node_shapes[node_id])
            nodes.append(node)
            node_dict[node_id] = node
        
        self.nx_graph = g
        self.nodes = nodes
        self.node_dict = node_dict
        self.edges = self.process_edges(g)
        
        self.node_labels = node_labels
        self.node_shape = node_shapes

    def process_edges(self, g):
        node_dict = self.node_dict
        edges = []
        for e in g.edges:
            src = node_dict[e[0]]
            dst = node_dict[e[1]]
            data = g.get_edge_data(e[0], e[1])
            label = data[0]['__obj'].replace('"','')
            edge = DotEdge(label, src, dst)
            edges.append(edge)
        return edges

    def subgraph_edges(self):
        nodes = set()
        for key in self.node_dict:
            node = self.node_dict[key]
            label = get_basename(node.label)
            if label.lower().replace(".exe","") == self.program:
                children = dag.descendants(self.nx_graph, key)
                for child in children:
                    nodes.add(child)
        g = self.nx_graph.subgraph(nodes)
        edges = self.process_edges(g)
        return edges
    


class DotGraphLoader(object):

    def __init__(self, program_name, is_benign, base_path=_BASE_PATH):
        self.program = program_name
        self.is_benign = is_benign
        self.base_path = os.path.join(base_path, "benign" if is_benign else "anomaly")
        self.folder_path = os.path.join(self.base_path, program_name)
        self.file_names = None

    def get_files_in_folder(self):
        folder = self.folder_path
        return [os.path.join(folder, name) for name in os.listdir(folder) if name.endswith(".call")]

    def get_file_names(self):
        folder = self.folder_path
        if self.file_names:
            return self.file_names
        else:
            return [os.path.join(folder, name) for name in os.listdir(folder) if name.endswith(".call")]

    def load_graphs(self, cache=True):
        if cache:
            cache = "dotgraph_cache/" + ("benign" if self.is_benign else "anomaly") + "/"+self.program
            if os.path.exists(cache):
                return pickle.load(open(cache,"rb"))

        res = []
        names = self.get_file_names()
        count = 0
        for name in names:
            count+=1
            print("%s/%s %s" % (count, len(names), name))
            try:
                graph = DotGraph(self.program, name)
                res.append(graph)
            except Exception as e:
                print(e)
        return res

def print_dataset_statistics(names):
    for name in names:
        loader1 = PathDataLoader(name, True)
        loader2 = PathDataLoader(name, False)
        print("%s\t%s\t%s\t%s\t%s" % (name, loader1.get_used_file_count(), loader1.get_path_count(), loader2.get_used_file_count(), loader2.get_path_count() ))
