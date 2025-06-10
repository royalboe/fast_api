from app.schema.schema import PostResponse
from fastapi.testclient import TestClient

def test_get_all_posts(authorized_client: TestClient, test_posts):
    res = authorized_client.get("/api/posts/")
    data = res.json()
    post_models = [PostResponse(**post['Post']) for post in data]
    assert len(data) == len(test_posts)
    assert res.status_code == 200
    for i in range(len(test_posts)):
        assert post_models[i].title == test_posts[i].title
        assert post_models[i].content == test_posts[i].content
        assert post_models[i].id == test_posts[i].id
    