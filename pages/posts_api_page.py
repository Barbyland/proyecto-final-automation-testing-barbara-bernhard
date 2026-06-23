import requests


class PostsApiPage:
    def __init__(self, url_base="https://jsonplaceholder.typicode.com"):
        self.url_base = url_base

    def get_post(self, post_id):
        return requests.get(f"{self.url_base}/posts/{post_id}", timeout=10)

    def create_post(self, title, body, user_id):
        data = {
            "title": title,
            "body": body,
            "userId": user_id,
        }
        return requests.post(f"{self.url_base}/posts", json=data, timeout=10)

    def delete_post(self, post_id):
        return requests.delete(f"{self.url_base}/posts/{post_id}", timeout=10)
