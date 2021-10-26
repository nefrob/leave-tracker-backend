'''
Sets up and runs RESTful API server
'''

from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from backend.models.db import db
from backend.schemas.ma import ma
from backend.resources.leave import LeaveList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # use memory for debug

bluePrint = Blueprint('api', __name__)
api = Api(bluePrint)
app.register_blueprint(bluePrint)

api.add_resource(LeaveList, '/all')


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(404)
def handle_404(e):
    return jsonify({'message': 'Not found'}), 404


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


def main():
    app.logger.info('Starting backend...')

    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)


if __name__ == "__main__":
    main()