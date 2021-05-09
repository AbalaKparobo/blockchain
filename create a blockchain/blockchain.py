# -*- coding: utf-8 -*-
"""
Created on Sat May  8 20:54:44 2021

@author: kparobo.abala
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

class BlockChain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    
    def create_block(self, proof, previous_hash):    
        block = {
                'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash
                }    
        self.chain.append(block)
        return block
    
    
    def get_previous_block(self):
        return self.chain[-1]
    
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            proof_hash = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if proof_hash[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    
    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest( )
    
    
    def is_chain_valid(self, chain):
        current_index = 1
        while current_index < len(chain):
            previous_block = chain[current_index - 1]
            block = chain[current_index]
            if block['previous_hash'] != self.hash_block(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            proof_hash = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if proof_hash != '0000':
                return False
            current_index += 1
        return True
        
        
        
app = Flask(__name__)

blockchain = BlockChain()

@app.route('/mine-block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash_block(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)
    response = {
            'message': 'Congrats! you have successfully mined a block',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
            }
    return jsonify(response), 200        

@app.route('/get-chain', methods = ['GET'])
def get_chain():
    response = {
            'chain_length': len(blockchain.chain),
            'chain' : blockchain.chain
            }
    return jsonify(response), 200

@app.route('/check-chain-validity', methods = ['GET'])
def is_valid():
    response = {
            'chain_is_valid': blockchain.is_chain_valid(blockchain.chain),
            'chain_length': len(blockchain.chain)
            }
    
    return jsonify(response), 200
            
            
app.run(host = '0.0.0.0', port = 5000)
            
            
            
            
            
            
            
            
            
            
            
            
            