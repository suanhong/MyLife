"""Read-only recovery inventory for the legacy Python 2.7 MyLife app.

This module is intentionally compatible with the legacy runtime. It does not
modify Post, UserImage, Settings, GCS objects, or counters.
"""
import hashlib
import json
import traceback

import webapp2

import filestore
from models.post import Post
from models.userimage import UserImage


class RecoveryInventoryHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        posts = Post.query().order(Post.date).fetch()
        images = UserImage.query().order(UserImage.filename).fetch()

        verify_bytes = self.request.get('verify', '0') == '1'
        result = {
            'read_only': True,
            'post_count': len(posts),
            'image_count': len(images),
            'posts': [],
            'images': [],
            'image_errors': []
        }

        for post in posts:
            result['posts'].append({
                'date': post.date_string(),
                'source': post.source,
                'has_images': bool(post.has_images),
                'images': list(post.images or []),
                'text_length': len(post.text or '')
            })

        for index, image in enumerate(images):
            item = {
                'index': index + 1,
                'filename': image.filename,
                'date': image.date.strftime('%Y-%m-%d') if image.date else None,
                'original_filename': image.original_filename,
                'original_size_key': image.original_size_key,
                'serving_size_key': image.serving_size_key,
                'backed_up_in_dropbox': bool(image.backed_up_in_dropbox)
            }
            if verify_bytes:
                try:
                    data = filestore.read(image.original_size_key)
                    item['readable'] = True
                    item['byte_size'] = len(data)
                    item['sha256'] = hashlib.sha256(data).hexdigest()
                except Exception:
                    item['readable'] = False
                    item['error'] = traceback.format_exc(3)
                    result['image_errors'].append({
                        'index': index + 1,
                        'filename': image.filename,
                        'error': item['error']
                    })
            result['images'].append(item)

        self.response.write(json.dumps(result, ensure_ascii=False, indent=2))
