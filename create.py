from application import db
from application.models import Campaigns,Players,Characters #add tables for characters/campaigns/rulesets/intances etc
db.create_all()