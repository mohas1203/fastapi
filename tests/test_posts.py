from fastapi.testclient import TestClient
from typing import List
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauth_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_unauth_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_one_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")

    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("First title", "First content", True),
    ("Second title", "Second content", True),
    ("Third title", "Third content", False),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    create_post = schemas.Post(**res.json())

    assert res.status_code == 202
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published


def test_unauth_create_posts(client, test_posts):
    res = client.post(
        "/posts/", json={"title": 'lakjsdflaksjdf', "content": "jalsdjflaskjfd"})

    assert res.status_code == 401


def test_unauth_delete_posts(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_posts(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_none_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/9999999")

    assert res.status_code == 404


def test_delete_other_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
