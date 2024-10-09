from datetime import datetime

import pytz

tz = pytz.country_timezones['IS'][0]
current_date_time = datetime.now(pytz.timezone(tz))

print(current_date_time.date())