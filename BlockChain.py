import Block
def add_block(transaction):
    if not BlockChain:
        new_block = Block("Chancellor on the brink...", transaction)
        BlockChain.append(new_block)
    else:
        new_block = Block(BlockChain[-1].block_hash, transaction)
        BlockChain.append(new_block)

BlockChain=[]