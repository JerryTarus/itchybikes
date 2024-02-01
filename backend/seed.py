from app import create_app, db
from app.models import User, Diary, Comment, Like, Follower
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import random

app = create_app()
app.app_context().push()

# Dummy data for testing
def create_dummy_data():

    def create_user(username, email):
        user = User(username=username, email=email)
        user.set_password('1234567')
        return user

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

            db.session.add(user)
            db.session.commit()

            # Diaries
            diary = Diary(date=datetime.strptime('2024-01-30', '%Y-%m-%d'), summary=f'Diary for {username}', user_id=user.user_id)

            db.session.add(diary)
            db.session.commit()

            for i in range(1, 4):
                comment = Comment(content=f'Comment {i} for {username}', user_id=user.user_id, diary_id=diary.diary_id)
                like = Like(user_id=user.user_id, diary_id=diary.diary_id)

                db.session.add(comment)
                db.session.add(like)
                db.session.commit()

            # Followers  to follow a random user in the list
            if len(username_list) > 1:
                random_user = random.choice(username_list[:-1])
                follower_user = User.query.filter_by(username=random_user).first()
                follower = Follower(follower_user_id=follower_user.user_id, following_user_id=user.user_id)

                db.session.add(follower)
                db.session.commit()

            print(f"User with username '{username}' created successfully with diary, comments, likes, and follower.")
    
    # Create comments, likes, and followers
    for user in User.query.all():
        for diary in user.diaries:
            # Create comments
            for i in range(1, 4):
                comment = Comment(content=f'Comment {i} for {user.username}', user_id=user.user_id, diary_id=diary.diary_id)
                db.session.add(comment)
                db.session.commit()

            # Create likes
            like = Like(user_id=user.user_id, diary_id=diary.diary_id)
            db.session.add(like)
            db.session.commit()

            # Create followers (following a random user in the list)
            if len(User.query.all()) > 1:
                random_user = random.choice(User.query.filter(User.user_id != user.user_id).all())
                follower = Follower(follower_user_id=user.user_id, following_user_id=random_user.user_id)
                db.session.add(follower)
                db.session.commit()

    # Print a message after creating dummy data
    print("Dummy data created successfully.")



# Here I am creating dummy comments just for testing
def create_comments(user_id, diary_id, num_comments=5):
    comments = []
    for i in range(num_comments):
        content = f"Comment {i+1} for user {user_id} on diary {diary_id}"
        comment = Comment(content=content, user_id=user_id, diary_id=diary_id)
        comments.append(comment)
    return comments

# Same here, dummy likes
def create_likes(user_id, diary_id, num_likes=7):
    likes = []
    for i in range(num_likes):
        like = Like(user_id=user_id, diary_id=diary_id)
        likes.append(like)
    return likes

# Here I am creating random followers
def create_followers(follower_user_id, following_user_id):
    follower = Follower(follower_user_id=follower_user_id, following_user_id=following_user_id)
    return follower

# res = make_response(
# jsonify(data), 200
# )

# return res

if __name__ == '__main__':
    create_dummy_data()
