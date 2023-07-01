from app import app
from models import Post, User, db

db.drop_all()
db.create_all()

default_url = "https://www.thecountrycook.net/wp-content/uploads/2022/01/thumbnail-Big-Fat-Chewy-Chocolate-Chip-Cookies-200x200.jpg"

user1 = User(
    first_name="Tyson",
    last_name="Tran",
    image_url=default_url,
)
user2 = User(
    first_name="Mari",
    last_name="Weill",
    image_url=default_url,
)
user3 = User(
    first_name="Linda",
    last_name="Tran",
    image_url=default_url,
)
user4 = User(
    first_name="Lisa",
    last_name="Tran",
    image_url=default_url,
)
user5 = User(
    first_name="Trong",
    last_name="Tran",
    image_url=default_url,
)

post1 = Post(title="Banana", content="bananas are cool")

db.session.add_all([user1, user2, user3, user4, user5])
db.session.commit()

db.session.add_all([post1])
db.session.commit()
