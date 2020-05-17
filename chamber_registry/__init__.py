import markdown
import os
import shelve

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


chamber_parser = reqparse.RequestParser()
chamber_parser.add_argument('id', type=int,required=True,help="id has to be int")
chamber_parser.add_argument('door', type=bool, help="door has to be bool")
chamber_parser.add_argument('program', type=str, help="program has to be str")
chamber_parser.add_argument('volume', type=int, help="volume has to be int")
chamber_parser.add_argument('light', type=bool, help="light has to be bool")
chamber_parser.add_argument('air', type=bool, help="air has to be bool")
chamber_parser.add_argument('version', type=str, help="version has to be string")
chamber_parser.add_argument('address', type=str, help="address has to be string")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("chambers.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


class Test(Resource):
    def get(self):
        return { "message": "Happy to serve you" }
    
class ChamberList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        chambers = []

        for key in keys:
            chambers.append(shelf[key])
        
        return {'message': 'Success', 'data': chambers}


    def post(self):

        args = chamber_parser.parse_args()

        shelf = get_db()
        if not (str(args['id']) in shelf):
            shelf[str(args['id'])] = args
            return {'message': 'Chamber registered', 'data': args}, 201
        else:
            oldargs = shelf[str(args['id'])]
            parameters = [ 'door', 'program', 'volume', 'light', 'air', 'version', 'address' ]
            for i in parameters:
                if args[i] is None:
                    args[i] = oldargs[i]
                
            shelf[str(args['id'])] = args
            return {'message': 'Chamber updated', 'data': args}, 201

class Chamber(Resource):
    def get(self, id):
        shelf = get_db()
        if not (str(id) in shelf):
            return {'message': 'Chamber not found', 'data': {}}, 404

        return {'message': 'Chamber found', 'data': shelf[str(id)]}, 200

    def delete(self, id):
        shelf = get_db()
        if not (str(id) in shelf):
            return {'message': 'Chamber not found', 'data': {}}, 404

        del shelf[str(id)]
        return '', 204 

api.add_resource(Test, '/test')
api.add_resource(ChamberList, '/chambers')
api.add_resource(Chamber, '/chamber/<int:id>')
