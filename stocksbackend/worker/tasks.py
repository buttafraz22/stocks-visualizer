from celery import shared_task
import requests, zipfile, io
from datetime import datetime, timedelta
import pandas as pd
from .models import *


# Define a basic URL
BASE_URL = 'https://dps.psx.com.pk/download/symbol_price/'


@shared_task()
def get_daily_reports(days=1)->None:
    """Generate Daily Stock Symbol Price Reports from the PSX Website.
    By design, the website does not define today's report. (e.g if today is 21-May-YYYY,
    the latest report on the website is of 20-May).

    Args:
    days: Backwards Time Interval for report retrieval. Default is 1 day from today (today - 1 day).
        On the Server, this script shall not run on Sunday and Monday.

    Returns:
        None
    """
    try:
        # Manufacture the URL
    
        date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
        manufactured_url = BASE_URL + date + '.zip'
        response = requests.get(manufactured_url)


        if response.status_code != 200: 
            return  # The market was closed or report didn't come.

        elif response.status_code == 200:
            # 'Assemble' the zip file by the response.content
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))

            # Iterate over the zip file's directory contents (UNIX equivalent: ls)
            for filename in zip_file.namelist():
                if filename.endswith('.txt'):
                    with zip_file.open(filename) as file:
                        
                        # Decipher the zip file contents.
                        text_file_content = file.readlines()

                        # Decode the contents of the text file inside the zip file.
                        # Perform some cleaning and stripping of the data.

                        decoded_lines = [line.decode('utf-8').replace("'", '').strip() for line in text_file_content]
                        del decoded_lines[1]  # This is an empty string in the data text file

                        # Manufacture a Pandas Dataframe from the data. Originally, this was
                        # done to test whether the code works fine by exporting a csv sheet
                        # of the manufactured data.

                        # However, Inserting data into database using a dataframe is much easier
                        # thanks to its iterrows method.
                        data = [item.split(',') for item in decoded_lines[1].split('\r')]
                        df = pd.DataFrame(data, columns=decoded_lines[0].split(','))

                        # Implement database insert functionality here.

                        for _, row in df.iterrows():
                            symbols = SymbolInformation.objects.filter(
                                symbol_code = row['SYMBOL_CODE'],
                                market_code = row['MARKET_CODE']
                            )
                            if symbols.exists():
                                symbol = symbols.first()
                            else:
                                symbol = SymbolInformation.objects.create(
                                    symbol_name = row['SYMBOL_NAME'],
                                    symbol_code = row['SYMBOL_CODE'],
                                    market_code = row['MARKET_CODE']
                                )
                            stock_object = StockReportEntry.objects.create(
                                stock_id = symbol,
                                date_of_entyry = date,
                                settlement_type = row['SETTLEMENT_TYPE'],
                                order_reject_upper = row['ORDER_REJECT_UPPER_PRICE'],
                                order_reject_lower = row['ORDER_REJECT_LOWER_PRICE'],
                                last_day_close = row['LAST_DAY_CLOSE_PRICE']
                            )
        
    except Exception as e:
        print(str(e))
        