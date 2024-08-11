from flask import Flask, jsonify, request
from blockchain import Blockchain
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
blockchain = Blockchain()

@app.route('/mine_block', methods=['POST'])
def mine_block():
    data = request.get_json().get('data', 'Sample Data')
    blockchain.add_block(data)
    return jsonify({"message": "Block mined", "block": blockchain.chain[-1].__dict__})

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify({"chain": chain_data, "length": len(chain_data)})

@app.route('/is_valid', methods=['GET'])
def is_valid():
    return jsonify({"is_valid": blockchain.is_chain_valid()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
