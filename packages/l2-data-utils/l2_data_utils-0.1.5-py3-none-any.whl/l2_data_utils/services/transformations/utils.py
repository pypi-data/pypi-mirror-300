from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_previous_partition_month(current_month, count):
    """Get the month that is 'count' months before the given 'YYYY-MM' formatted string."""
    current_date = datetime.strptime(current_month, '%Y-%m')
    previous_month_date = current_date - relativedelta(months=count)
    return previous_month_date.strftime('%Y-%m')