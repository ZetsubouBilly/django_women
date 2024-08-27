from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from .models import Women

# Create your tests here.

class GetPagesTestCase(TestCase):
    fixtures= ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']

    def setUp(self):
        "sad"
    
    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('women/index.html', response.template_name)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w_lst = Women.published.all().select_related("cat")
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], w_lst[:5])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by =5;
        response = self.client.get(path + f'?page={page}')
        w_lst = Women.published.all().select_related("cat")
        self.assertQuerysetEqual(response.context_data['posts'], w_lst[(page-1)*paginate_by:page*paginate_by])

    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)


    def tearDown(self):
        "aad"