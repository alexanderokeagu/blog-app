from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class BlogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@email.com', password='secret')
        self.post = Post.objects.create(title="a good title", body="nice body content", author=self.user)



    def test_string_representation(self):
        post = Post(title="a little test")
        self.assertEqual(str(post), post.title)



    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(),'/post/1/' )



    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'a good title')
        self.assertEqual(f'{self.post.body}', 'nice body content')
        self.assertEqual(f'{self.post.author}', 'testuser')


        

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'nice body content')
        self.assertTemplateUsed(response, 'blog/home.html')




    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'a good title')
        self.assertTemplateUsed(response, 'blog/post_detail.html')




    def test_post_create_view(self):
        response = self.client.post(reverse('post_view'), {
            'title': 'New title',
            'body' : 'New text',
            'author': self.user,

        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')
        self.assertTemplateUsed(response, 'blog/post_new.html')


    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
           'title': 'Updated title',
           'body' : 'Updated text', 
        })
        self.assertEqual(response.status_code, 302)
        


    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)

