import flet as ft
import requests
from database import API_BASE_URL, get_current_user
from baskets import add_to_basket
from orders import get_orders_page


def show_products_page(page):
    """Функция для отображения страницы с продуктами."""
    page.clean()

    def get_products():
        """Функция для получения списка продуктов."""

        response = requests.get(f"{API_BASE_URL}/app/product/")
        if response.status_code == 200:
            return response.json()['data']  # Возвращаем список продуктов
        else:
            return []

    # Получаем список продуктов
    products = get_products()

    page.title = "Продукты"

    # Разделение карточек на три части по ширине страницы
    rows = []
    for i in range(0, len(products), 3):
        row_items = products[i:i + 3]
        row = ft.Row(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.ALBUM),
                                    title=ft.Text(f"Продукт: {product['name']}"),
                                    subtitle=ft.Text(f"цена: {product['price']}"),
                                ),
                                ft.Row(
                                    [ft.ElevatedButton(text="Buy product",
                                                       on_click=lambda e, args=product: add_to_basket(
                                                           product=args,
                                                           page=page))],
                                    alignment="end",
                                ),
                            ]
                        ),
                        width=300,  # Ширина каждой карточки
                        padding=10,
                    )
                ) for product in row_items
            ],
            alignment="center",  # Выравнивание карточек в ряду
            spacing=20,  # Промежуток между карточками
        )
        rows.append(row)

    # Добавление всех рядов на страницу
    list_product = ft.Column(
        rows,
        spacing=20,  # Промежуток между строками
    )

    page.add(

    )

    # Очищаем страницу и добавляем продукты
    page.clean()
    page.add(
        ft.Column([
            ft.Text("Продукты", size=20),
            list_product,
            ft.ElevatedButton(text="Корзина", on_click=lambda e: page.go("/basket")),
            ft.ElevatedButton(text="Профиль", on_click=lambda e: page.go("/profile"))
            # Кнопка для возврата на главную страницу
        ], width=page.width, spacing=10, alignment="center", horizontal_alignment="center")
    )
    page.update()