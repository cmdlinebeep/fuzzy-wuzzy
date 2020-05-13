import os
from sqlalchemy import Column, String, Integer, Table, ForeignKey, relationship, backref
from flask_sqlalchemy import SQLAlchemy

# Ensure that setup.sh has been sourced. Fail if variables not set
if not os.getenv('DATABASE_URL'):
    raise RuntimeError("Environment variables are not set, did you source setup.sh?")

database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
    binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    # db.create_all()


'''NOTE: Relationship between Company and Policy is many-to-many.  Companies
can have many policies, and policies can belong to many companies.  Here we'll
choose to define the Company as the parent and Policy as the child.'''

class Company(db.Model):
    __tablename__ = 'Company'
    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    
    name = Column(String(80), unique=True, nullable=False)
    website =  Column(String(80), unique=True, nullable=False)

    # Here is where we link the associative table for the many-to-many relationship with Policy
    policies = relationship('Policy', secondary=company_policy_table, backref=backref('companies'))
    # 'secondary' links this to the associative (m2m) table
    # 'relationship' statement above allows us to make references like: company_obj.policies
    # 'backref' creates an attribute on Company objects so we can reference: policy_obj.companies

    def __repr__(self):
        return f"Company object with name: {self.name} and site: {self.website}"

    '''
    insert() method
    Creates a new company
    EXAMPLE
        new_co = Company(name="Green Cola, Inc.", website="gcola.com")
        new_co.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update() method
    Updates a row already in the database
    EXAMPLE
        co = Company.query.filter(name="Green Cola, Inc.")
        co.website = "gcola.biz.info.site"
        co.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete() method
    Deletes a row from the database
    EXAMPLE
        co = Company.query.get(co_id)
        co.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
class Policy(db.Model):
    __tablename__ = 'Policy'

    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    
    name = Column(String(80), unique=True, nullable=False)
    body =  Column(String(3000), nullable=False)

    # Association table for Policy to Company (many-to-many)
    # Defining the Policy as the child here, doesn't really matter
    company_policy_table = Table('company_policy_table',
        Column('policy_id', Integer, ForeignKey('Policy.id'), primary_key=True),
        Column('company_id', Integer, ForeignKey('Company.id'), primary_key=True)    
    )

    def __repr__(self):
        return f"Policy object with name: {self.name} and begins: {self.data[0:10]}"

    '''
    insert() method
    Creates a new policy
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update() method
    Updates a row already in the database
    '''
    def update(self):
        db.session.commit()

    '''
    delete() method
    Deletes a row from the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()