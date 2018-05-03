from flask import Flask, render_template, request, redirect, url_for
from flask_restplus import Api, Resource, fields
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
app = Flask(__name__)
api = Api(app)

engine = create_engine('sqlite:////tmp/pet.db')
Session= sessionmaker(bind=engine)



    
import os

port = os.getenv("PORT")
ns = api.namespace('cats', description='Cats operations')



cat = api.model('Cat', {
    'id': fields.Integer(readOnly=True, description='each cat has an id'),
    'nickname': fields.String(required=True, description='What is its nickname ?'),
    'age': fields.Integer(readOnly=True, description='How old is it ?'),
    'Hobby': fields.String(readOnly=True, description='What does it like to do ?')
})

class CatDAO(object):
    def __init__(self):
       self.counter = 0
       return

    def create(self, data):
        s = Session()
        newCat = data
        newCat['id'] = self.counter = self.counter + 1
        s.add(newCat)
        s.session.commit()
        s.close()
        return

    def get(self, id):
        
        api.abort(404, "Cat {} doesn't exist".format(id))

    def update(self, id, data):
        Cat = self.get(id)
        Cat.update(data)
        return Cat

    def delete(self, id):
        Cat = self.get(id)
        self.cats.remove(cat)
        
    def getAllCats(self):
        s = Session()
        cats=s.Cat.query.all()
        return cats
        
@api.route('/')
class CatList(Resource):
   
    @ns.doc('list_cats')
    @ns.marshal_list_with(cat)
    def get(self):
        '''List all cats'''
        return DAO.getAllCats()
            
   
    @ns.doc('cat')
    @ns.expect(cat)
    @ns.marshal_with(cat, code=201)
    def post(self):
        '''Create a new cat'''
        return DAO.create(api.payload), 201




@ns.route('/<int:id>')
@ns.response(404, 'Cat not found')
@ns.param('id', 'The cat id')
class Cat(Resource):
    '''Show a single cat item and lets you delete them'''
    @ns.doc('get_a_cat')
    @ns.marshal_with(cat)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_cat')
    @ns.response(204, 'Cat deleted')
    def delete(self, id):
        '''Delete a cat in the list'''
        
        return '', 204


    @ns.expect(cat)
    @ns.marshal_with(cat)
    def put(self):
        '''Update a cat in the list'''
        
        return '', 205
if __name__ == '__main__':
    DAO = CatDAO()
    app.run(host='0.0.0.0', port=port, debug=True)
    
    
    