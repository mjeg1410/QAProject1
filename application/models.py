from application import db
from application import login_manager
from flask_login import UserMixin
from datetime import datetime
#--------------------------------------------------------------------------------------------
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_first_name = db.Column(db.String(15), nullable=False)
    character_last_name = db.Column(db.String(15), nullable=True)
    date_rolled = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False) 
    background = db.Column(db.String(500), nullable=True)
    questline = db.relationship('Instances', backref='rlpcs', lazy=True)

    def __repr__(self):
        return ''.join([
            'Player ID: ', self.player_id, '\r\n',
            'Character name: ', self.character_name, '\r\n', self.background
            ])
#--------------------------------------------------------------------------------------------
class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_name = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    quest = db.relationship('Instances', backref='world', lazy=True)
    setting = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return ''.join([
            'Player ID: ', self.player_id, '\r\n',
            'Campaign: ', self.campaign_name, '\r\n', self.setting
            ])
#--------------------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(id):
    return Players.query.get(int(id))
#--------------------------------------------------------------------------------------------
class Players(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    characters = db.relationship('Characters', backref='creator', lazy=True)
    campaigns = db.relationship('Campaigns', backref='dungeonmaster', lazy=True)
    def __repr__(self):
        return ''.join(['PlayerID: ', str(self.id), '\r\n',
        'Email: ', self.email, '\r\n',
        'Name: ', self.first_name, ' ', self.last_name])
#--------------------------------------------------------------------------------------------
class Instances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Instance_name = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return ''.join([
            'Instance ID: ', self.instance_id, '\r\n',
            'Instance: ', self.instance_name, '\r\n', self.location
            ])
#--------------------------------------------------------------------------------------------