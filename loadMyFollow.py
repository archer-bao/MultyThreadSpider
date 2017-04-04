from tumblpy import Tumblpy

t = Tumblpy('iA0ftYaCstAwyaRJLd3iVWkskv2d1BUeyko8UYvp4nF8SoqR9M',
            'OqHriLttTymLwNkvcmfke4B0Wuwi0mg7doccD2UxCJljEOiNP0',
            'P6cn3sxlx7TjEldPZVDxIHiJL7FvVUHHnRw1eQ4N18aknLTxZ1',
            'WqjOo4aZt5EiDlCqveqnbUxgdgs2mCUvKVtYHXyIv5UkQlXiKj')

f = open("blog_data.txt", "a", encoding="utf-8")

for i in range(0, 15):
    kw = {'offset': i * 20, 'limit': 20}
    print(kw)
    resp = t.following(kw)
    blogs = resp.get("blogs")
    for blog in blogs:
        print(blog.get("url"))
        f.write(blog.get("url") + "\n")
