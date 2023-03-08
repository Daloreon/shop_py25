from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from product.models import Category
from product.views import CategoryAPIView, ProductModelViewSet
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryTest(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        category = [
            Category(title='c1'),
            Category(title='c2'),
            Category(title='c3'),
        ]
        Category.objects.bulk_create(category)
        # bulk_create -  с помощью него мы разом добавили за раз 3 обькта в базы данных
        self.setup_user()

    def setup_user(self):
        self.user = User.objects.create_user(
            email = 'test@test.com',
            password = 'test123',
            is_active = True,
        )

    def test_get_category(self):
        request = self.factory.get('api/v1/product/category/')
        view = CategoryAPIView.as_view({'get':'list'})
        response = view(request)
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]['title'] == 'c1'



    def test_post_category(self):
        data = {
            'title': 'c4',
        }

        request = self.factory.post('api/v1/product/category/', data)
        force_authenticate(request, self.user)
        view = CategoryAPIView.as_view({'post':'create'})
        response = view(request)
        assert response.status_code == 201
        assert Category.objects.filter(title = 'c4').exists()

        #.exist() выводит там False or True проверяя заданное условие

class ProductTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.setup_user()
    @staticmethod
    def setup_category():
        category = [
            Category(title='c1'),
            Category(title='c2'),
            Category(title='c3'),
        ]
        Category.objects.bulk_create(category)


    def setup_user(self):
        self.user = User.objects.create_user(
            email = 'test@test.com',
            password = 'test123',
            is_active = True,
        )

    def test_post_product(self):
        data = {
            'owner' : self.user.id,
            'category' : Category.objects.first(),
            'title' : 'test_product',
            'price' : 20,
            'amount' : 20,
            'image' : '',
        }
        request = self.factory.post('api/v1/product/modelviewset_crud', data)
        force_authenticate(request ,self.user   )
        view = ProductModelViewSet.as_view({'post':'create'})
        response = view(request)
        print(response.data)