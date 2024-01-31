from app import create_app, db
from app.models import User, Diary, Comment, Like, Follower
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Create an app context before interacting with the database
app = create_app()
app.app_context().push()

# Create dummy data for testing
def create_dummy_data():
    # Create users

    def create_user(username, email):
        user = User(username=username, email=email)
        user.set_password('1234567')
        return user

    # Create users with error handling for duplicate usernames
    username_list = ['jerrytarus', 'billarnold', 'frankmarozva', 'izzienjeri', 'solomonkitonyi', 
                     'kaimwanyumba', 'steveotieno', 'crotonnsuites', 'itchyboots', 'marquesbrownless', 
                     'mkbhd', 'stevenbartlett', 'jerryrig', 'derrickuria', 'anisamuema', 'angiemithi',
                     'carolrugut', 'taliamar', 'mylojay']
    
    for username in username_list:
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            print(f"User with username '{username}' already exists.")
        else:
            user = create_user(username, f'{username}@gmail.com')

            # Add user to the session and commit
            db.session.add(user)
            db.session.commit()

            # Create diaries
            diary = Diary(date=datetime.strptime('2024-01-30', '%Y-%m-%d'), summary=f'Diary for {username}', user_id=user.user_id)

            # Add diary to the session and commit
            db.session.add(diary)
            db.session.commit()

            print(f"User with username '{username}' created successfully.")

if __name__ == '__main__':
    create_dummy_data()
