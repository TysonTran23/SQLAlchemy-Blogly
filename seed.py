from app import app
from models import Post, PostTag, Tag, User, db

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

post1 = Post(title="Banana", content="bananas are cool", user_id=1)
post2 = Post(title="Cats", content="Simon is my son", user_id=2)
post3 = Post(title="Td", content="Td is for lyfe", user_id=3)
post4 = Post(title="Aritzia", content="omg so cute", user_id=4)
post5 = Post(title="Golf", content="tyson is better at golf", user_id=5)

post_tag1 = PostTag(post_id=1, tag_id=1)

tag1 = Tag(id=1, name="Tyson")
tag2 = Tag(id=2, name="Mari")
tag3 = Tag(id=3, name="Lisa")


db.session.add_all([user1, user2, user3, user4, user5])
db.session.commit()

db.session.add_all([post1, post2, post3, post4, post5])
db.session.commit()

db.session.add([tag1, tag2, tag3])
db.session.commit()

db.session.add(post_tag1)
db.session.commit()
