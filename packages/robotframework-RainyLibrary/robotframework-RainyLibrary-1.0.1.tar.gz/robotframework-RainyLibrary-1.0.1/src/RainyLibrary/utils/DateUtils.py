from robot.api.deco import keyword,not_keyword
from robot.api import logger
from datetime import datetime, timezone, timedelta,date
import calendar
import datetime
tz = timezone(timedelta(hours = 7))

class DateUtils():
    @not_keyword
    def thai_month_in_short(self,int_month):
        switcher = {
            1: "ม.ค.",
            2: "ก.พ.",
            3: "มี.ค.",
            4: "เม.ย.",
            5: "พ.ค.",
            6: "มิ.ย.",
            7: "ก.ค.",
            8: "ส.ค.",
            9: "ก.ย.",
            10: "ต.ค.",
            11: "พ.ย.",
            12: "ธ.ค."

        }
        return switcher.get(int_month,"Invalid month")

    @keyword()
    def get_current_date_and_short_month_in_thai(self,plusdate=0,want_thai_year=True,with_leading_zero=True):
        """Return current or date delta from arguments in thai

           EX. 05 พ.ค 2564
        """
        today = datetime.today()
        date  = today + timedelta(days=plusdate)

        if with_leading_zero and date.day in range(1,10):
            date_str = str(0) + str(date.day)
        else:
            date_str = str(date.day)

        if want_thai_year:
            year_str = str(date.year + 543)
        else:
            year_str = str(date.year)

        month_thai = self.thai_month_in_short(date.month)
        print(date_str + ' ' + month_thai + ' ' + year_str)
        d_m_y_string = str(date_str + ' ' + month_thai + ' ' + year_str)
        return d_m_y_string

    @keyword()
    def get_number_of_days_in_month(self,month=None,year=None):
        if year and month:
            number_of_days_in_month = calendar.monthrange(year, month)[1]
        else:
            now = datetime.datetime.now()
            number_of_days_in_month = calendar.monthrange(now.year, now.month)[1]
        
        print(number_of_days_in_month)
        return number_of_days_in_month
    
    @keyword()
    def get_days_remaining_in_current_month(self):
        now = datetime.datetime.now()
        number_of_days_in_month = calendar.monthrange(now.year, now.month)[1]
        return int(number_of_days_in_month-now.day)