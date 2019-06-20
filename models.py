from flask_sqlalchemy import SQLAlchemy


# create a new SQLAlchemy object
db = SQLAlchemy()



class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


# Model for Node
class Node(Base):
    __table_name__ = 'node'
    content = db.Column(db.String(500))
    type = db.Column(db.String(100))
    belongsToDiag = db.Column(db.Integer, db.ForeignKey('diagram.id'))

    diagram = db.relationship('Diagram', foreign_keys=[belongsToDiag])


    # user friendly way to display the object
    def __repr__(self):
        return self.content

# Model for poll options
class Connection(Base):
    __table_name__ = 'connection'

    content = db.Column(db.String(500))
    sourceNodeID = db.Column(db.String(20), db.ForeignKey('node.id'))
    targetNodeID = db.Column(db.String(20), db.ForeignKey('node.id'))

    source = db.relationship('Connection', foreign_keys=[sourceNodeID])
    target = db.relationship('Connection',foreign_keys=[targetNodeID])
    belongsToDiag = db.Column(db.Integer, db.ForeignKey('diagram.id'))

    diagram = db.relationship('Diagram', foreign_keys=[belongsToDiag])




# Polls model to connect topics and options together
class Diagram(Base):
    __table_name__ = 'diagram'

    def __repr__(self):
        # a user friendly way to view our objects in the terminal
        return self.id