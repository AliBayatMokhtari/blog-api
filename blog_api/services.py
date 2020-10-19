from blog_api import db
from blog_api.models import User, Post, Comment, Like


# public function
def serialize_list(_list):
    data = []
    for _list_item in _list:
        _list_item = _list_item.__dict__
        _list_item.pop('_sa_instance_state')
        data.append(_list_item)
    return data


def not_found_response():
    return {'error': 'not found', 'success': False}, 404


def server_error_response():
    return {'error': 'server error', 'success': False}, 500


# User services
def get_all_users():
    users = User.query.all()
    users = serialize_list(users)
    return {
        'users': users,
        'success': True,
        'error': None
    }


def get_user(user_id):
    if not user_id:
        return {'error': 'invalid id', 'success': False}
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        user = {'username': user.username, 'email': user.email,
                'image_file': user.image_file, 'id': user.id}
        return {'success': True, 'error': None,
                'result': user}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def create_user(user):
    if not user.get('username') or not user.get(
            'email') or not user.get('password'):
        return {'error': 'invalid input', 'success': False}, 400
    new_user = User(username=user.get('username'),
                    email=user.get('email'),
                    password=user.get('password'))
    db.session.add(new_user)
    try:
        db.session.commit()
        created_user = {'username': new_user.username,
                        'email': new_user.email,
                        'image_file': new_user.image_file,
                        'id': new_user.id}
        return {'error': None, 'success': True,
                'result': created_user}, 201
    except Exception as e:
        print(e)
        return server_error_response()


def update_user(user_id, req_body):
    if not user_id or not req_body.get('id') or req_body.get(
            'id') != user_id:
        return {
            'error': 'invalid id in route or in request body',
            'success': False}
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        if not req_body.get('username') or not req_body.get(
                'email'):
            return {'error': 'invalid input',
                    'success': False}, 400
        user.username = req_body.get('username')
        user.email = req_body.get('email')
        db.session.commit()
        user = {'username': user.username, 'email': user.email,
                'image_file': user.image_file, 'id': user.id}
        return {'success': True, 'error': None,
                'result': user}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def delete_user(user_id):
    if not user_id:
        return {'error': 'invalid id', 'success': False}
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        user = {'username': user.username, 'email': user.email,
                'image_file': user.image_file, 'id': user.id}
        return {'error': None, 'success': True,
                'result': user}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def get_user_posts(user_id):
    if not user_id:
        return {'error': 'invalid id', 'success': False}
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        user_posts = serialize_list(user.posts)
        user = {'username': user.username, 'email': user.email,
                'id': user.id, 'image_file': user.image_file}
        response_data = {'success': True, 'error': None,
                         'user': user, 'user_posts': user_posts}
        return response_data, 200
    except Exception as e:
        print(e)
        return server_error_response()


def get_user_liked_posts(user_id):
    if not user_id:
        return {'success': False, 'error': 'invalid id'}, 400
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        liked_posts = []
        for like in user.likes:
            liked_post = Post.query.get(like.post_id)
            liked_posts.append(liked_post)
        liked_posts = serialize_list(liked_posts)
        user = {'username': user.username, 'email': user.email, 'image_file': user.image_file,
                'id': user.id}
        return {'success': True, 'error': None, 'user': user, 'liked_posts': liked_posts}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def get_user_commented_posts(user_id):
    if not user_id:
        return {'success': False, 'error': 'invalid id'}
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        commented_posts = []
        for comment in user.comments:
            commented_post = Comment.query.get(comment.post_id)
            commented_posts.append(commented_post)
        commented_posts = serialize_list(commented_posts)
        user = {'username': user.username, 'email': user.email, 'image_file': user.image_file,
                'id': user.id}
        return {'success': True, 'error': None, 'user': user, 'commented_posts':
            commented_posts}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def get_user_comments(user_id):
    if not user_id:
        return {'success': False, 'error': 'invalid id'}
    try:
        user = User.query.get(user_id)
        if not user:
            return not_found_response()
        user_comments = user.comments
        user_comments = serialize_list(user_comments)
        user = {'username': user.username, 'email': user.email, 'image_file': user.image_file,
                'id': user.id}
        return {'success': True, 'error': None, 'user': user, 'user_comments': user_comments}, 200
    except Exception as e:
        print(e)
        return server_error_response()


# Post services
def get_all_posts():
    try:
        posts = Post.query.all()
        posts = serialize_list(posts)
        return {'success': True, 'error': None,
                'posts': posts}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def create_post(post):
    if not post.get('title') or not post.get(
            'content') or not post.get('user_id'):
        return {'error': 'invalid input', 'success': False}, 400
    if not User.query.get(post.get('user_id')):
        return {'success': False,
                'error': 'user id not found'}, 404
    new_post = Post(title=post.get('title'),
                    content=post.get('content'),
                    user_id=post.get('user_id'))
    db.session.add(new_post)
    try:
        db.session.commit()
        created_post = {'username': new_post.title,
                        'email': new_post.content,
                        'image_file': new_post.user_id,
                        'id': new_post.id}
        return {'error': None, 'success': True,
                'result': created_post}, 201
    except Exception as e:
        print(e)
        return server_error_response()


def update_post(post_id, req_body):
    if not post_id or not req_body.get('id') or req_body.get('id') != post_id:
        return {'error': 'invalid id in route or in request body', 'success': False}
    try:
        post = Post.query.get(post_id)
        if not post:
            return not_found_response()
        if not req_body.get('title') or not req_body.get('content') or not req_body.get('user_id'):
            return {'error': 'invalid input', 'success': False}, 400
        post.title = req_body.get('title')
        post.content = req_body.get('content')
        post.user_id = req_body.get('user_id')
        # post.date_posted = req_body.get('date_posted') if req_body.get(
        #     'date_posted') else post.date_posted
        db.session.commit()
        post = {'title': post.title, 'content': post.content, 'date_posted': post.date_posted,
                'id': post.id, 'user_id': post.user_id}
        return {'success': True, 'error': None, 'result': post}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def delete_post(post_id):
    if not post_id:
        return {'error': 'invalid id', 'success': False}
    try:
        post = Post.query.get(post_id)
        if not post:
            return not_found_response()
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        post = {'title': post.title, 'content': post.content,
                'date_posted': post.date_posted, 'id': post.id, 'user_id': post.user_id}
        return {'error': None, 'success': True, 'result': post}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def get_post_likes(post_id):
    if not post_id:
        return {'success': False, 'error': 'invalid id'}
    try:
        post = Post.query.get(post_id)
        if not post:
            return not_found_response()
        post_likes = serialize_list(post.likes)
        post = {'title': post.title, 'content': post.content, 'date_posted': post.date_posted,
                'id': post.id, 'user_id': post.user_id}
        return {'success': True, 'error': None, 'post': post, 'post_likes': post_likes}, 200
    except Exception as e:
        print(e)
        return server_error_response()


def get_post_comments(post_id):
    if not post_id:
        return {'success': False, 'error': 'invalid id'}
    try:
        post = Post.query.get(post_id)
        if not post:
            return not_found_response()
        post_comments = serialize_list(post.comments)
        post = {'title': post.title, 'content': post.content, 'date_posted': post.date_posted,
                'id': post.id, 'user_id': post.user_id}
        return {'success': True, 'error': None, 'post': post, 'post_comments': post_comments}, 200
    except Exception as e:
        print(e)
        return server_error_response()


# Comment services
def create_comment(req_body):
    if not req_body or not req_body.get('title') or not req_body.get('text'):
        return {'success': False, 'error': 'invalid input'}, 400

    user_id = req_body.get('user_id')
    post_id = req_body.get('post_id')
    title = req_body.get('title')
    text = req_body.get('text')

    if not user_id or not post_id:
        return {'success': False, 'error': 'user_id and post_id are required'}, 400

    try:
        user = User.query.get(user_id)
        post = Post.query.get(post_id)
        if not user:
            return {'success': False, 'error': 'User not found'}, 404
        if not post:
            return {'success': False, 'error': 'Post not found'}, 404

        comment = Comment(title=title, text=text, user_id=user_id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        comment = {'id': comment.id, 'title': comment.title, 'text': comment.text, 'user_id':
            comment.user_id, 'post_id': comment.post_id}
        return {'success': True, 'error': None, 'comment': comment}
    except Exception as e:
        print(e)
        return server_error_response()


def update_comment(comment_id, data):
    if not comment_id:
        return {'success': False, 'error': 'invalid id'}, 400
    if not data or not data.get('title') or not data.get('text') or not data.get('id'):
        return {'success': False, 'error': 'invalid input'}, 400
    if comment_id != data.get('id'):
        return {'success': False, 'error': 'ids must be the same'}, 400
    if data.get('user_id') or data.get('post_id'):
        return {'success': False, 'error': 'you can not change the post or user of comment'}, 400

    comment = Comment.query.get(comment_id)
    comment.title = data.get('title')
    comment.text = data.get('text')
    db.session.commit()
    comment = {'title': comment.title, 'text': comment.text, 'user_id': comment.user_id,
               'post_id': comment.post_id, 'id': comment.id}
    return {'success': True, 'error': None, 'comment': comment}, 200


def delete_comment(comment_id):
    if not comment_id:
        return {'success': False, 'error': 'invalid id'}, 400
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return {'success': False, 'error': 'comment not found'}, 400
        Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
        return {'success': True, 'error': None}, 200
    except Exception as e:
        print(e)
        return server_error_response()


# Like services
def create_like(data):
    if not data or not data.get('user_id') or not data.get('post_id'):
        return {'success': False, 'error': 'invalid input'}
    try:
        user_id = data.get('user_id')
        post_id = data.get('post_id')
        like = Like(user_id=user_id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        like = {'id': like.id, 'user_id': like.user_id, 'post_id': like.post_id}
        return {'success': True, 'error': None, 'like': like}
    except Exception as e:
        print(e)
        return server_error_response()


def delete_like(like_id):
    if not like_id:
        return {'success': False, 'error': 'invalid id'}, 400
    try:
        like = Like.query.filter_by(id=like_id)
        if not like:
            return not_found_response()
        like.delete()
        db.session.commit()
        return {'success': True, 'error': None}, 200
    except Exception as e:
        print(e)
        return server_error_response()
