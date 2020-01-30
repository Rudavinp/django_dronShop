from django.test import TestCase
from django.urls import reverse
from product.models import Product, Category
from core.models import Comment
from account.models import User



class TestAddProdComment(TestCase):

    @classmethod
    def setUpTestData(cls):
        cat = Category.objects.create(name='cat')
        return Product.objects.create(category=cat, name='testProd', price=10)

    def setUp(self) -> None:
        test_user = User.objects.create_user(email='lol@bk.ru', password='12345')
        test_user.save()

    def test_logged_user_can_create_comment(self):
        self.client.login(username='lol@bk.ru', password='12345')
        prod = Product.objects.get(name='testProd')
        url = reverse('core:comment', kwargs={'prod_id': prod.pk},)
        response = self.client.post(url, {'text': 'blabla'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'lol@bk.ru')
        self.assertTrue(Comment.objects.count() == 1)
        self.assertRedirects(response, '/product/testProd-{}/'.format(prod.pk).lower(),
                             status_code=301)

    def test_logged_user_cant_create_empty_comment(self):
        self.client.login(username='lol@bk.ru', password='12345')
        prod = Product.objects.get(name='testProd')
        url = reverse('core:comment', kwargs={'prod_id': prod.pk}, )
        response = self.client.post(url, {'text': ''}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'lol@bk.ru')
        self.assertTrue(Comment.objects.count() == 0)

    def test_not_logged_user_cant_create_comment(self):
        prod = Product.objects.get(name='testProd')
        url = reverse('core:comment', kwargs={'prod_id': prod.pk}, )
        self.client.post(url, {'text': 'bla'}, follow=True)

        self.assertTrue(Comment.objects.count() == 0)