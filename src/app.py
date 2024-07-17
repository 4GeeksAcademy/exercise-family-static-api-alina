"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')

def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])

def getAllMembers():

    allMembers = jackson_family.get_all_members()
    if (allMembers == None):
        return jsonify({"msg": "Miembros no encontrado"}), 404
    return jsonify(allMembers), 200


@app.route('/members/<int:member_id>', methods=['GET'])

def getSingleMember(member_id):

    singleMember = jackson_family.get_member(member_id)
    if (singleMember == None):
        return jsonify({"msg": "Miembro no encontrado"}), 404
    return jsonify(singleMember), 200


@app.route('/members', methods=['POST'])

def addMember():
    newMember = jackson_family.add_member(request.json)
    return jsonify(newMember), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])

def deleteSingleMember(member_id):
    for member in jackson_family._members:
        if member["id"] == member_id:
            deleteMember = jackson_family.delete_member(member_id)
            return jsonify(deleteMember), 200
    return jsonify({"msg": "Miembro no encontrado"}), 404
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
