from app import create_app, db
from app.models import User, Diary, Comment, Like, Follower
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import random

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

            # Create comments, likes, and followers
            for i in range(1, 4):
                comment = Comment(content=f'Comment {i} for {username}', user_id=user.user_id, diary_id=diary.diary_id)
                like = Like(user_id=user.user_id, diary_id=diary.diary_id)

                # Add comment and like to the session and commit
                db.session.add(comment)
                db.session.add(like)
                db.session.commit()

            # Create followers (following a random user in the list)
            if len(username_list) > 1:
                random_user = random.choice(username_list[:-1])
                follower_user = User.query.filter_by(username=random_user).first()
                follower = Follower(follower_user_id=follower_user.user_id, following_user_id=user.user_id)

                # Add follower to the session and commit
                db.session.add(follower)
                db.session.commit()

            print(f"User with username '{username}' created successfully with diary, comments, likes, and follower.")

if __name__ == '__main__':
    create_dummy_data()
