from fastapi.testclient import TestClient
import pytest

@pytest.fixture(name="first_vote")
def fixture_first_vote(authorized_client: TestClient, test_posts, test_user):
    """Fixture to create a vote for the first post."""
    post = next((post for post in test_posts if post.author_id != test_user['id']), None)
    assert post is not None, "No post found for voting"
    assert post.id is not None, "Post ID is None"
    payload = {
        "post_id": post.id,
        "dir": 1
    }
    authorized_client.post(f"/api/vote/", json=payload)
    return post

def test_vote_on_others_post(authorized_client: TestClient, test_posts, test_user):
    """Test voting on a post."""

    post = next((post for post in test_posts if post.author_id != test_user['id']), None)
    post_id = post.id
    payload = {
        "post_id": post_id,
        "dir": 1
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data['message'] == "Successfully upvoted post"

def test_vote_on_own_post(authorized_client: TestClient, test_posts, test_user):
    """Test voting on own post should raise 403 error."""
    
    post = next((post for post in test_posts if post.author_id == test_user['id']), None)
    post_id = post.id
    payload = {
        "post_id": post_id,
        "dir": 1
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 403
    data = res.json()
    assert data['detail'] == "You cannot vote on your own post"

def test_vote_on_post_not_exist(authorized_client: TestClient):
    """Test voting on a post that does not exist should raise 404 error."""
    
    payload = {
        "post_id": 99999999,
        "dir": 1
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 404
    data = res.json()
    assert data['detail'] == "Post not found"
  
def test_vote_on_post(authorized_client: TestClient, test_posts, test_user):
    """Test voting on a post."""

    post = next((post for post in test_posts if post.author_id != test_user['id']), None)
    assert post is not None, "No post found for voting"
    post_id = post.id
    payload = {
        "post_id": post_id,
        "dir": 1
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data['message'] == "Successfully upvoted post"


def test_vote_on_post_already_voted(authorized_client: TestClient, first_vote):
    """Test voting on a post that has already been voted on should raise 409 error."""
    
    payload = {
        "post_id": first_vote.id,
        "dir": 1
    }

    # Second vote should raise conflict
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 409
    data = res.json()
    assert data['detail'] == "You have already upvoted this post"


def test_vote_on_post_downvote(authorized_client: TestClient, test_posts, first_vote):
    """Test downvoting a post."""
    post_id = first_vote.id
    # Downvote
    payload = {
        "post_id": post_id,
        "dir": 0
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data['message'] == "Successfully downvoted post."

def test_vote_on_post_downvote_not_exist(authorized_client: TestClient, test_posts):
    """Test downvoting a post that does not exist should raise 404 error."""

    payload = {
        "post_id": 000000000000000,
        "dir": 0
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 404
    data = res.json()
    assert data['detail'] == "Post not found"

def test_vote_on_post_downvote_already_downvoted(authorized_client: TestClient, test_posts, test_user):
    """Test downvoting a post that has already been downvoted should raise 409 error."""

    post_id = next((post for post in test_posts if post.author_id != test_user['id']), None).id
    # Downvote
    payload = {
        "post_id": post_id,
        "dir": 0
    }
    res = authorized_client.post(f"/api/vote/", json=payload)
    assert res.status_code == 404
    data = res.json()
    assert data['detail'] == "Post not found"

def test_vote_unauthorized_user_vote(client: TestClient, test_posts):
    """Test voting on a post without authentication should raise 401 error."""
    
    post_id = next((post for post in test_posts if post.author_id != 1), None).id
    payload = {
        "post_id": post_id,
        "dir": 1
    }
    res = client.post(f"/api/vote/", json=payload)
    assert res.status_code == 401
    assert res.json() == {'detail': 'Not authenticated'}