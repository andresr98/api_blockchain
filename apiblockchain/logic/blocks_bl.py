from apiblockchain.models import Header, Block
from .transactions_bl import get_current_transactions, get_hash_current_transactions, save_current_transactions
from .headers_bl import get_last_header
from apiblockchain.logic.merkleRoot.node import Node 
from apiblockchain.logic.merkleRoot.merkle_tree import MerkleTree 
import hashlib
import random

def to_mine(difficult):
    last_header = get_last_header()
    hash_txs = get_hash_current_transactions()

    nodes = create_nodes(hash_txs)
    merkle = MerkleTree()
    merkle.build_tree(nodes)
    merkle_root = merkle.get_root()

    header = Header(prev_hash=last_header.own_hash, merkle_root=merkle_root, high=last_header.high + 1, difficult=difficult)
    block_string = str(header.prev_hash) + str(header.merkle_root) + str(header.high)
    block_string = concat_string_block(block_string, hash_txs)

    header.nonce, header.own_hash = proof_of_work(block_string, header.difficult)
    block = Block(header=header, own_hash=header.own_hash)

    try:
        header.save()
        block.save()
        result = save_current_transactions(block)

        if result:
            return True
        else:
            return False
    except Exception:
        return False


def mine_genesis_block(mine_address, quantity):
    transaction_hashs = get_hash_current_transactions()
    header = Header(prev_hash="0", merkle_root=transaction_hashs[0], high=0, difficult=4)

    block_string = str(header.prev_hash) + str(header.merkle_root) + str(header.high)
    block_string = concat_string_block(block_string, transaction_hashs)
    header.nonce, header.own_hash = proof_of_work(block_string, header.difficult)

    block = Block(header=header, own_hash=header.own_hash)

    try:
        header.save()
        block.save()
        result = save_current_transactions(block)

        if result:
            return True
        else:
            return False
    except Exception:
        return False

def proof_of_work(block_string, difficult=4):
    req_zeros = '0' * difficult
    nonce = 1
    final_string = (block_string + str(nonce)).encode()
    block_hash = hashlib.sha256(final_string).hexdigest()
    random.seed()
    while not block_hash.startswith(req_zeros):
        nonce = random.randint(1, 9223372036854775807) 
        final_string = (block_string + str(nonce)).encode()
        block_hash = hashlib.sha256(final_string).hexdigest()
    return nonce, block_hash

def concat_string_block(block_string, hash_transactions):
    final_string = block_string

    for tx in hash_transactions:
        final_string += tx
    return final_string

def create_nodes(hashs):
    nodes = []

    for hash_tx in hashs:
        node = Node(hash_tx)
        nodes.append(node)
    return nodes
