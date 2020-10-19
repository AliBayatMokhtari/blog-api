from blog_api import app
from blog_api import services
from flask import request


@app.route('/')
def hello_world():
    return {
        'message': 'Hello. Welcome to flask'
    }


@app.route('/about')
def about():
    return {
        'message': 'You have a get request for: /about'
    }


# User routes
@app.route('/users', methods=['GET'])
def get_users():
    return services.get_all_users(), 200


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    response, status_code = services.create_user(user_data)
    return response, status_code


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return services.delete_user(user_id)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return services.get_user(user_id)


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = request.json
    return services.update_user(user_id, user)


@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    return services.get_user_posts(user_id)


@app.route('/users/<int:user_id>/likes', methods=['GET'])
def get_user_liked_posts(user_id):
    return services.get_user_liked_posts(user_id)


@app.route('/users/<int:user_id>/commented-posts')
def get_user_commented_posts(user_id):
    return services.get_user_commented_posts(user_id)


@app.route('/users/<int:user_id>/comments')
def get_user_comments(user_id):
    return services.get_user_comments(user_id)


# Post routes
@app.route('/posts', methods=['GET'])
def get_posts():
    return services.get_all_posts()


@app.route('/posts', methods=['POST'])
def create_post():
    req_body = request.json
    return services.create_post(req_body)


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    req_body = request.json
    return services.update_post(post_id, req_body)


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    return services.delete_post(post_id)


@app.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    return services.get_post_likes(post_id)


@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    return services.get_post_comments(post_id)


# Comment routes
@app.route('/comments', methods=['POST'])
def create_comment():
    req_body = request.json
    return services.create_comment(req_body)


@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.json
    return services.update_comment(comment_id, data)


@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    return services.delete_comment(comment_id)


# Like routes
@app.route('/likes', methods=['POST'])
def create_like():
    data = request.json
    return services.create_like(data)


@app.route('/likes/<int:like_id>', methods=['DELETE'])
def delete_like(like_id):
    return services.delete_like(like_id)
