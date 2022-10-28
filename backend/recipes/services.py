import os
from datetime import date

from django.conf import settings
from django.db.models import Sum

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from recipes.models import RecipeIngredient


def shopping_cart_to_pdf(user):
    PDF_FILE_PREFIX = 'shopping_cart'

    today = date.today()
    path_pattern = '%d%m%Y'
    data_pattern = '%d/%m/%Y'

    table_root = os.path.join(settings.PDF_ROOT, 'fonts')
    user_font = ttfonts.TTFont(
        'User_font',
        os.path.join(table_root, 'font.ttf')
    )
    pdfmetrics.registerFont(user_font)

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name='Date',
            fontSize=30,
            fontName='User_font',
            alignment=TA_CENTER,
        )
    )
    filename = (
        PDF_FILE_PREFIX
        + f'_{today.strftime(path_pattern)}.pdf'
    )
    pdf_filename = filename + '.pdf'
    pdf_path = os.path.join(settings.PDF_ROOT, pdf_filename)
    pdf_file = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=30,
        bottomMargin=18
    )
    shopping_cart = []

    logo = Image(settings.LOGO_IMAGE_FOR_PDF)
    list_image = Image(settings.LIST_IMAGE_FOR_PDF)

    data_time = Paragraph(today.strftime(data_pattern), styles['Date'])
    spacer = Spacer(1, 40)

    ingredients = RecipeIngredient.objects.filter(
        recipe__shopping_cart=user
    ).order_by(
        'ingredient__name'
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(
        amount=Sum('amount')
    )

    first_row = ['#', 'Ингредиент', 'Количество', 'Единицы']
    table_data = [
        [
            index + 1,
            ingredient['ingredient__name'],
            ingredient['amount'],
            ingredient["ingredient__measurement_unit"]
        ] for index, ingredient in enumerate(ingredients)
    ]
    table_data.insert(0, first_row)
    table = Table(table_data)
    table.setStyle(TableStyle((
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'User_font'),
        ('FONTSIZE', (0, 0), (-1, -1), 25),
        ('LEADING', (0, 0), (-1, -1), 35),
    )))

    footer = Paragraph('Приятного аппетита!', styles['Date'])

    content = [
        logo,
        list_image,
        data_time,
        spacer,
        table,
        spacer,
        footer
    ]
    for unit in content:
        shopping_cart.append(unit)

    pdf_file.build(shopping_cart)
    return pdf_path, filename


def add_ingredients_to_recipe(ingredients_data, recipe):
    for values_dict in ingredients_data:
        ingredient = values_dict['ingredient']['id']
        amount = values_dict['amount']
        ingredient_in_recipe, _ = RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
