from .node import Node
import hashlib

class MerkleTree:
    def __init__(self):
        self.root = None
    
    def get_root(self):
        return self.root.data

    def build_tree(self, nodes):

        #If there is only one hash on nodes, it will be the root of merkle tree
        if len(nodes) == 1:
            self.root = nodes[0]
            return
        parenths = []

        for i in range(0, len(nodes), 2):
            left_node = nodes[i]

            #In case just remain one transaction, append it to the end.
            if i == (len(nodes) - 1):
                parenths.append(left_node)
                break

            rigth_node = nodes[i + 1]
            #Take the info of 2 tx and generate their parent as a new hash.
            final_string = (left_node.data + rigth_node.data).encode()
            hash_txs = hashlib.sha256(final_string).hexdigest()

            #Create a new node and append to the end of the list
            new_root_node = Node(hash_txs)
            left_node.root = new_root_node
            rigth_node.root = new_root_node
            parenths.append(new_root_node)
        
        return self.build_tree(parenths)