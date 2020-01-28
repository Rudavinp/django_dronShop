from django.test import TestCase, Client
from django.urls import reverse
from product.models import Category

from dashboard.categories.forms import CategoryForm


def get_category_model():
    return Category.objects.create(name='testCat')


class TestDashboardCategories(TestCase):

    def test_category_list(self):
        url = reverse('dashboard:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_str_method(self):
        cat = get_category_model()
        self.assertTrue(isinstance(cat, Category))
        self.assertEqual(cat.__str__(), cat.name)

    def test_category_create(self):
        url = reverse('dashboard:category-add')
        data = {'name': 'testCat', 'description': 'Blabla'}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Category.objects.count()==1)

    def test_category_create_with_not_valid_name(self):
        url = reverse('dashboard:category-add')
        data = {'name': '', 'description': 'Blabla'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Category.objects.count()==0)

    def test_category_details(self):
        category = get_category_model()
        url = reverse('dashboard:category-detail',
                      kwargs={'pk': category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_cat_form_with_not_valid_name(self):
        data = {'name': '', 'description': 'Blabla'}
        form = CategoryForm(data, ancestor=None)
        self.assertFalse(form.is_valid())

    def test_create_sub_categories(self):
        cat_parent = get_category_model()
        url = reverse('dashboard:category-add',
                     kwargs={'root_pk': cat_parent.pk})
        data = {'name': 'cat_chield', 'description': 'Blabla'}
        response = self.client.post(url, data, follow=True)
        cat_parent.refresh_from_db()
        subcategories = cat_parent.get_children()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(subcategories), 1)
        self.assertTrue(Category.objects.count() == 2)

    def test_category_edit(self):
        category = get_category_model()
        url = reverse('dashboard:category-edit',
                      kwargs={'pk': category.pk})
        data = {'name': 'NewName',}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.all()[0].name, 'NewName')

    def test_category_delete(self):
        category = get_category_model()
        self.assertEqual(Category.objects.count(), 1)
        url = reverse(
            'dashboard:category-delete',
            kwargs={
                'pk': category.pk
            }
        )
        category.refresh_from_db()
        response = self.client.post(url, follow=True)
        self.assertEqual(Category.objects.count(), 0)