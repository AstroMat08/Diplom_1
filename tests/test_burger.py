from unittest.mock import Mock

import pytest

from praktikum.burger import Burger

class TestBurger:
    """Тесты для класса Burger."""

    def test_burger_init_creates_empty_burger(self):
        """При создании бургера булочка не установлена, список ингредиентов пуст."""
        burger = Burger()

        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns(self):
        """set_buns устанавливает булочку в бургер."""
        burger = Burger()
        mock_bun = Mock()

        burger.set_buns(mock_bun)

        assert burger.bun == mock_bun

    def test_add_ingredient_appends_ingredient(self):
        """add_ingredient добавляет ингредиент в конец списка."""
        burger = Burger()
        mock_ingredient = Mock()

        burger.add_ingredient(mock_ingredient)

        assert burger.ingredients == [mock_ingredient]

    def test_add_multiple_ingredients_keeps_order(self):
        """Несколько ингредиентов добавляются в правильном порядке."""
        burger = Burger()
        first, second, third = Mock(), Mock(), Mock()

        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.add_ingredient(third)

        assert burger.ingredients == [first, second, third]

    def test_remove_ingredient_removes_by_index(self):
        """remove_ingredient удаляет ингредиент по указанному индексу."""
        burger = Burger()
        first, second, third = Mock(), Mock(), Mock()
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.add_ingredient(third)

        burger.remove_ingredient(1)

        assert burger.ingredients == [first, third]

    def test_move_ingredient_changes_position(self):
        """move_ingredient перемещает ингредиент на новую позицию."""
        burger = Burger()
        first, second, third = Mock(), Mock(), Mock()
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.add_ingredient(third)

        burger.move_ingredient(0, 2)

        assert burger.ingredients == [second, third, first]

    @pytest.mark.parametrize(
        "bun_price, ingredients_prices, expected_price",
        [
            (100, [], 200),
            (100, [50], 250),
            (100, [50, 30, 20], 300),
            (200.5, [10.25, 40.25], 451.5),
            (0, [], 0),
        ],
    )
    def test_get_price_calculates_correctly(
        self, bun_price, ingredients_prices, expected_price
    ):
        """get_price = 2 * цена булочки + сумма цен ингредиентов."""
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for price in ingredients_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)

        assert burger.get_price() == expected_price

    def test_get_receipt_format_without_ingredients(self):
        """Чек без ингредиентов содержит только булочку и цену."""
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 200
        burger.set_buns(mock_bun)

        expected = (
            "(==== white bun ====)\n"
            "(==== white bun ====)\n"
            "\n"
            "Price: 400"
        )

        assert burger.get_receipt() == expected

    def test_get_receipt_with_ingredients(self):
        """Чек содержит все ингредиенты в нужном формате."""
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)

        mock_sauce = Mock()
        mock_sauce.get_type.return_value = "SAUCE"
        mock_sauce.get_name.return_value = "hot sauce"
        mock_sauce.get_price.return_value = 100

        mock_filling = Mock()
        mock_filling.get_type.return_value = "FILLING"
        mock_filling.get_name.return_value = "cutlet"
        mock_filling.get_price.return_value = 100

        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)

        expected = (
            "(==== black bun ====)\n"
            "= sauce hot sauce =\n"
            "= filling cutlet =\n"
            "(==== black bun ====)\n"
            "\n"
            "Price: 400"
        )

        assert burger.get_receipt() == expected

    @pytest.mark.parametrize(
        "ingredient_type, ingredient_name, expected_line",
        [
            ("SAUCE", "hot sauce", "= sauce hot sauce ="),
            ("FILLING", "cutlet", "= filling cutlet ="),
        ],
    )
    def test_get_receipt_ingredient_type_is_lowercased(
        self, ingredient_type, ingredient_name, expected_line
    ):
        """Тип ингредиента в чеке печатается в нижнем регистре."""
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "bun"
        mock_bun.get_price.return_value = 0
        burger.set_buns(mock_bun)

        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = ingredient_type
        mock_ingredient.get_name.return_value = ingredient_name
        mock_ingredient.get_price.return_value = 0
        burger.add_ingredient(mock_ingredient)

        assert expected_line in burger.get_receipt()