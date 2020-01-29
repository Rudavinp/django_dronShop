from django.test import TestCase, Client
from django.urls import reverse
from product.models import Product, Category
from core.models import Comment
from product.forms import CommentForm
from account.models import User

from core.views import add_product_comment
from dashboard.categories.forms import CategoryForm


def get_product_model():
    cat = Category.objects.create(name='cat')
    return Product.objects.create(category=cat, name='testProd', price=10)



class TestProductView(TestCase):

    def setUp(self) -> None:
        test_user = User.objects.create_user(email='lol@bk.ru', password='12345')
        test_user.save()
        form = CommentForm('asvas')

    def test_user_login(self):
        login = self.client.login(username='lol@bk.ru', password='12345')
        print(1234, login)

        prod = get_product_model()
        data = {'prod_id': prod.pk}
        url = reverse('core:comment', kwargs=data,)

        response = self.client.post(url,  follow=True)
        # print(12345, response.context)
        print(123456, Comment.objects.count())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'lol@bk.ru')
        self.assertTrue(Comment.objects.count()==1)