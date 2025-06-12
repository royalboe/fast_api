from app.schema.schema import PostResponse
from fastapi.testclient import TestClient
import pytest

def test_get_all_posts(authorized_client: TestClient, test_posts):
    res = authorized_client.get("/api/posts/")
    data = res.json()
    post_models = [PostResponse(**post['Post']) for post in data]
    data_length = len(data)
    assert data_length > 0
    assert data_length == len(test_posts)
    assert res.status_code == 200
    for i in range(data_length):
        assert post_models[i].title == test_posts[i].title
        assert post_models[i].content == test_posts[i].content
        assert post_models[i].id == test_posts[i].id

def test_get_post_by_id(authorized_client: TestClient, test_posts):
    post_id = test_posts[0].id
    res = authorized_client.get(f"/api/posts/{post_id}/")
    data = res.json()
    post_model = PostResponse(**data['Post'])
    assert res.status_code == 200
    assert post_model.id == post_id
    assert post_model.title == test_posts[0].title
    assert post_model.content == test_posts[0].content

def test_unauthorised_user_get_all_posts(client: TestClient):
    res = client.get("/api/posts/")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client: TestClient):
    res = authorized_client.get("/api/posts/99999999/")
    assert res.status_code == 404

def test_get_my_posts(authorized_client: TestClient, test_posts, test_user):
    res = authorized_client.get("/api/posts/user-posts/")
    data = res.json()
    post_models = [PostResponse(**post) for post in data]
    data_length = len(data)
    expected_data = [post for post in test_posts if post.author_id == test_user["id"]]
    expected_length = len(expected_data)
    assert data_length == expected_length
    assert res.status_code == 200
    for i in range(data_length):
        assert post_models[i].title == expected_data[i].title
        assert post_models[i].content == expected_data[i].content
        assert post_models[i].id == expected_data[i].id

@pytest.mark.parametrize("search_query", ["Test Post", "test post"])
def test_search_posts(authorized_client: TestClient, test_posts, search_query):
    res = authorized_client.get(f"/api/posts/?search={search_query}")
    data = res.json()
    post_models = [PostResponse(**post['Post']) for post in data]
    assert res.status_code == 200
    # assert len(data) > 0
    for post in post_models:
        assert search_query.lower() in post.title.lower()

@pytest.mark.parametrize("title, content, status_code", [
    ("New Post Title", "This is the content of the new post.", 201),
    ("Another Post", "Content for another post.", 201),
    ("Yet Another Post", "Content for yet another post.", 201),
    ("Test Post", "This is the content of the test post.", 201),
])
def test_authorised_user_create_post(authorized_client: TestClient, test_user, title, content, status_code):
    """Test creating a new post with various title and content combinations."""
    user_data = {
        "title": title,
        "content": content
    }
    res = authorized_client.post("/api/posts/", json=user_data)
    data = res.json()
    post_model = PostResponse(**data)
    assert res.status_code == status_code
    assert post_model.title == title
    assert post_model.content == content
    assert post_model.published
    assert post_model.author_id == test_user['id']

def test_authorised_user_create_post_with_empty_title(authorized_client: TestClient, test_user):
    """Test creating a new post with an empty title."""
    user_data = {
        "title": "",
        "content": "This is the content of the new post."
    }
    res = authorized_client.post("/api/posts/", json=user_data)
    assert res.status_code == 422

def test_authorised_user_create_post_with_empty_content(authorized_client: TestClient, test_user):
    """Test creating a new post with an empty title."""
    user_data = {
        "title": "This is a new post",
        "content": ""
    }
    res = authorized_client.post("/api/posts/", json=user_data)
    assert res.status_code == 422

def test_unauthorised_user_create_post(client: TestClient):
    """Test creating a new post without authentication."""
    user_data = {
        "title": "New Post Title",
        "content": "This is the content of the new post."
    }
    res = client.post("/api/posts/", json=user_data)
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}


def test_authorised_user_delete_own_post(authorized_client: TestClient, test_posts, test_user):
    """Test deleting a post with authentication."""
    own_post = next((post for post in test_posts if post.author_id == test_user['id']), None)
    assert own_post is not None, f"No post found with author_id {test_user['id']}"
    post_id = own_post.id
    print(own_post.author_id)
    res = authorized_client.delete(f"/api/posts/{post_id}/")
    assert res.status_code == 204

def test_authorised_user_delete_post_not_exist(authorized_client: TestClient):
    """Test deleting a non-existent post with authentication."""
    res = authorized_client.delete("/api/posts/99999999/")
    assert res.status_code == 404
  
def test_unauthorised_user_delete_post(client: TestClient, test_posts):
    """Test deleting a post without authentication."""
    post_id = test_posts[0].id
    res = client.delete(f"/api/posts/{post_id}/")
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_authorised_user_delete_other_post(authorized_client: TestClient, test_posts, test_user):
    """Test deleting a post that belongs to another user."""
    not_own_post = next((post for post in test_posts if post.author_id != test_user['id']), None)
    post_id = not_own_post.id
    res = authorized_client.delete(f"/api/posts/{post_id}/")
    assert res.status_code == 403
    assert res.json() == {'detail': 'Not authorized to perform requested action'}


def test_authotised_user_update_own_post(authorized_client: TestClient, test_posts, test_user):
    """Test updating a post with authentication."""
    own_post = next((post for post in test_posts if post.author_id == test_user['id']), None)
    assert own_post is not None, f"No post found with author_id {test_user['id']}"
    post_id = own_post.id
    user_data = {
        "title": "Updated Post Title",
        "content": "This is the updated content of the post."
    }
    res = authorized_client.put(f"/api/posts/{post_id}/", json=user_data)
    data = res.json()
    post_model = PostResponse(**data)
    assert res.status_code == 202
    assert post_model.title == user_data["title"]
    assert post_model.content == user_data["content"]

def  test_authotised_user_update_post_not_exist(authorized_client: TestClient):
    """Test updating a non-existent post with authentication."""
    user_data = {
        "title": "Updated Post Title",
        "content": "This is the updated content of the post."
    }
    res = authorized_client.put("/api/posts/99999999/", json=user_data)
    assert res.status_code == 404


def test_unauthorised_user_update_post(client: TestClient, test_posts):
    """Test updating a post without authentication."""
    post_id = test_posts[0].id
    user_data = {
        "title": "Updated Post Title",
        "content": "This is the updated content of the post."
    }
    res = client.put(f"/api/posts/{post_id}/", json=user_data)
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}

def test_authorised_user_update_other_post(authorized_client: TestClient, test_posts, test_user):
    """Test updating a post that belongs to another user."""
    not_own_post = next((post for post in test_posts if post.author_id != test_user['id']), None)
    post_id = not_own_post.id
    user_data = {
        "title": "Updated Post Title",
        "content": "This is the updated content of the post."
    }
    res = authorized_client.put(f"/api/posts/{post_id}/", json=user_data)
    assert res.status_code == 403
    assert res.json() == {'detail': 'Not authorized to perform requested action'}