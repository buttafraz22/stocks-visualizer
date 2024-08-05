import pytest
from datetime import datetime, timedelta
from faker import Faker
from worker.models import SymbolInformation, StockReportEntry

fake = Faker()

@pytest.fixture
def generate_dummy_stock_data(django_db_setup, django_db_blocker):
    """Fixture to generate dummy stock data for yesterday's date.
    500 Stock Reports Objects over 3 companies.
    """

    with django_db_blocker.unblock():
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        symbol_names = ['Millerson', 'Arbisoft', 'Hirenze']
        symbols = [
            SymbolInformation.objects.create(
                symbol_name=name,
                symbol_code = f'C0{i+1}',
                market_code = f'M0{i+1}'
            )
            for i, name in enumerate(symbol_names)
        ]

        for _ in range(500):
            StockReportEntry.objects.create(
                stock_id=fake.random_element(symbols),
                date_of_entyry=yesterday,
                settlement_type=fake.word(),
                order_reject_upper=fake.pyfloat(left_digits=3, right_digits=2, positive=True),
                order_reject_lower=fake.pyfloat(left_digits=3, right_digits=2, positive=True),
                last_day_close=fake.pyfloat(left_digits=3, right_digits=2, positive=True)
            )
