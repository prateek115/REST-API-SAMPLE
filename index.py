from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'                           #creating DB for data storage
db = SQLAlchemy(app)

class projectModel(db.Model):                                                             #Creating model/Table
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Project(name={name}, type={type}, owner={owner})"

# app.app_context().push()                                                                  #creating DB (only run one time)
# db.create_all()

project_put_args = reqparse.RequestParser()                                                                         #parsing args sent by user to validate in put method
project_put_args.add_argument('name', type=str, help='Name of Project cannot left empty', required=True)            #parsing args sent by user to validate in put method
project_put_args.add_argument('type', type=str, help='Type of Project cannot left empty', required=True)            #parsing args sent by user to validate in put method
project_put_args.add_argument('owner', type=str, help='Owner of Project cannot left empty', required=True)          #parsing args sent by user to validate in put method

project_update_args = reqparse.RequestParser()
project_update_args.add_argument('name', type=str, help='Name of Project cannot left empty')                    #parsing value for patch method
project_update_args.add_argument('type', type=str, help='Type of Project cannot left empty')                     #parsing value for patch method
project_update_args.add_argument('owner', type=str, help='Owner of Project cannot left empty')                   #parsing value for patch method


# @app.route('/')
# def index_page():
#     return "Hello world"


resource_fields = {                                                        #Creating marshal to seriallize the object return from DB
    'id' : fields.Integer,
    'name' : fields.String,
    'type' : fields.String,
    'owner' : fields.String
}

class project(Resource):                                #Creating methods body with encapsulation
    
    @marshal_with(resource_fields)                      #initiating marshal to parse object
    def get(self, project_id):
        
        # try:
        #     result = projectModel.query.filter_by(id=project_id).first()
        # except:                                                                                   #used try/except method in get
        #     abort(404, message='Could not find the project')
        
        # return result
    
        result = projectModel.query.filter_by(id=project_id).first()
        if not result:
            abort(404, message='Could not find the project')
        return result

    @marshal_with(resource_fields)
    def put(self, project_id):
        args = project_put_args.parse_args()
        
        result = projectModel.query.filter_by(id=project_id).first()
        if result:
            abort(409, message='Project id already exist')

        project = projectModel(id = project_id, name=args['name'], type=args['type'], owner=args['owner'])
        db.session.add(project)
        db.session.commit()                                                                                     #Committing to DB after creation
        return project, 201
    
    
    @marshal_with(resource_fields)
    def patch(self, project_id):                                        #To update data value in DB
        args = project_update_args.parse_args()
        result = projectModel.query.filter_by(id=project_id).first()
        if not result:                                                              
            abort(404, message='Could not find the project')

        if args['name']:
            result.name = args['name']

        if args['type']:
            result.type = args['type']

        if args['owner']:
            result.owner = args['owner']

        db.session.commit()                                     #There is no neeed of add method if data is in DB already. Commit will work

        return result


    @marshal_with(resource_fields)
    def delete(self, project_id):
        result = projectModel.query.filter_by(id=project_id).first()
        if not result:
            abort(204,message='The record has been deleted.')
        else:
            db.session.delete(result)                                                                 #Delete method from DB with DELETE  protocol
            db.session.commit()


api.add_resource(project, "/project/<int:project_id>")          #defining URL


if __name__ == "__main__":              #running function from main
    app.run(debug=True)