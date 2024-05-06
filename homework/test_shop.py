"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity)
        assert product.check_quantity(0)
        assert product.check_quantity(product.quantity - 1)
        assert not product.check_quantity(product.quantity + 1)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(product.quantity - 1)
        assert product.quantity == 1

        product.buy(product.quantity)
        assert product.quantity == 0


    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_new_product(self, product, cart):
        cart.add_product(product)
        assert cart.products[product] == 1

    def test_add_existing_product(self, product, cart):
        cart.add_product(product)
        cart.add_product(product, product.quantity - 1)
        assert cart.products[product] == product.quantity

    def test_delete_product(self, product, cart):
        cart.add_product(product, 5)
        cart.remove_product(product, 2)
        assert cart.products[product] == 3

        cart.remove_product(product)
        assert product is not cart.products

        cart.add_product(product, 20)
        cart.remove_product(product, 100)
        assert product is not cart.products

    def test_clear_cart(self, product, cart):
        cart.add_product(product, 100)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, product, cart):
        cart.add_product(product, 5)
        assert cart.get_total_price() == 500


    def test_buy_cart(self, product, cart):
        cart.add_product(product, 100)
        cart.buy()
        assert product.quantity == 900

        product.quantity = 1000
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()

        product.quantity = 0
        cart.add_product(product, 2)
        with pytest.raises(ValueError):
            cart.buy()