from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Campaigns, Players, Characters, Instances
from application.forms import CharacterForm, CampaignForm, RegistrationForm, LoginForm, UpdateAccountForm, InstanceForm
from flask_login import login_user, current_user, logout_user, login_required
#---------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    characterData = Characters.query.all()
    campaignData = Campaigns.query.all()
    instanceData = Instances.query.all()
    return render_template('home.html', title='Home', Istances=instanceData, Characters = characterData, Campaigns = campaignData)
#---------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        player=Players.query.filter_by(email=form.email.data).first()
        if player and bcrypt.check_password_hash(player.password, form.password.data):
            login_user(player, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)
#---------------------------------------------------------------------------------------------------
@app.route('/CharacterCreation', methods=['GET', 'POST'])#POSTS SUBSTITUTED FOR CHARACTERS, SECOND MODULE ROUTE FOR CAMPAIGN CREATION WITH SIMILARITY
@login_required
def character():
    form = CharacterForm()
    if form.validate_on_submit():
        characterData = Characters(
            character_first_name=form.character_first_name.data,
            character_last_name=form.character_last_name.data,
            background=form.character_background.data,
            creator=current_user
        )

        db.session.add(characterData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('character.html', title='Character Creation', form=form)
#---------------------------------------------------------------------------------------------------
@app.route('/CampaignCreation', methods=['GET', 'POST'])#POSTS SUBSTITUTED FOR CHARACTERS, SECOND MODULE ROUTE FOR CAMPAIGN CREATION WITH SIMILARITY
@login_required
def campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaignData = Campaigns(
            campaign_name=form.campaign_name.data,
            setting=form.setting.data,
            dungeonmaster=current_user
        )

        db.session.add(campaignData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('campaign.html', title='Campaign Creation', form=form)
#---------------------------------------------------------------------------------------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        
        player = Players(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data,password=hash_pw)

        db.session.add(player)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
#---------------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
#---------------------------------------------------------------------------------------------------
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name        
        form.email.data = current_user.email        
    return render_template('account.html', title='Account', form=form)
#---------------------------------------------------------------------------------------------------
@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    player = current_user.id
    characters = Characters.query.filter_by(player_id=player) #posts substituted for characters and campaigns
    for character in characters:
            db.session.delete(character)
    campaigns = Campaigns.query.filter_by(player_id=player)
    for campaign in campaigns:
            db.session.delete(campaign)
    account = Players.query.filter_by(id=player).first()
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))
#---------------------------------------------------------------------------------------------------
@app.route('/InstanceCreation', methods=['GET', 'POST'])#POSTS SUBSTITUTED FOR CHARACTERS, SECOND MODULE ROUTE FOR CAMPAIGN CREATION WITH SIMILARITY
@login_required
def instance():
    campaigns = Campaigns.query.all()
    campaigns_id = []
    for campaign in campaigns:
        campaign_id.append(campaigns.id)
    form.campaign_id.choices = [campaigns_id]
    print ("-------------------------------------------------------------------------------------------------")
    print (campaign_id)
    characters = Characters.query.all()
    characters_id = []
    for character in characters:
        character_id.append(characters.id)
    form.character_id.choices = [characters_id]
    if form.validate_on_submit():
        instanceData = Instances(
            Instance_name=form.instance_name.data,
            location=form.instance_location.data,
            campaign_id=form.campaign_id.data,
            character_id=form.character_id.data
        )
        db.session.add(instanceData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)


    return render_template('instance.html', title='Instance Creation', form=form)