from datetime import datetime, date, timedelta
import calendar

# calculate dates
class PeriodService :

  def  __init__ (self, clientTimestamp):

    if type(clientTimestamp) == datetime:
      self.timestamp = clientTimestamp
    else :
      format = "%Y-%m-%d" if len(clientTimestamp) <=10 else "%Y-%m-%d %H:%M:%S"
      self.timestamp =  datetime.strptime(clientTimestamp, format )
  
    self.periods = {
      "today" : {
        "key" : 'today',
        "translateKey" : 'PERIODS.TODAY',
        "limit" : self.today(),
      },
      "week" : {
        "key" : 'week',
        "translateKey" : 'PERIODS.THIS_WEEK',
        "limit" : self.week(),
      },
      "month" : {
        "key" : 'month',
        "translateKey" : 'PERIODS.THIS_MONTH',
        "limit" : self.month(),
      },
      "year" : {
        "key" : 'year',
        "translateKey" : 'PERIODS.THIS_YEAR',
        "limit" : self.year(),
      },
      "yesterday" : {
        "key" : 'yesterday',
        "translateKey" : 'PERIODS.YESTERDAY',
        "limit" : self.today(1)
      },
      "lastWeek" : {
        "key" : 'lastWeek',
        "translateKey" : 'PERIODS.LAST_WEEK',
        "limit" : self.lastWeek(),
      },
      "lastMonth" : {
        "key" : 'lastMonth',
        "translateKey" : 'PERIODS.LAST_MONTH',
        "limit" : self.lastMonth(),
      },
      "lastYear" : {
        "key" : 'lastYear',
        "translateKey" : 'PERIODS.LAST_YEAR',
        "limit" : self.year(-1),
      },

      # components will make an exception for all time - no period has to be selected
      # on the server this simple removes the WHERE condition
      "allTime" : {
        "key" : 'allTime',
        "translateKey" : 'PERIODS.ALL_TIME',
      },
      "custom" : {
        "key" : 'custom',
        "translateKey" : 'PERIODS.CUSTOM',
        }
      }
 
  def lookupPeriod(self, key):
    return self.periods[key]

  def today(self, current=0) :
    today =self.timestamp  - timedelta(current)
    return { "start" : today, 'end' : today }

  def week(self) :
    today = self.timestamp
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return { "start" : start, "end" : end }

  def lastWeek(self) :
    today = self.timestamp
    end = today - timedelta(days=today.weekday() + 1 )
    start = end + timedelta(days=-6)
    return { "start" : start, "end" : end }

  def month(self) :
    start_date = self.timestamp
    lastDay = calendar.monthrange(start_date.year, start_date.month)[1] # number
    return { 
      "start" : date(start_date.year, start_date.month, 1), 
      "end" : date(start_date.year, start_date.month, lastDay) 
    }

  def year(self, current = 0) :
    start_date = self.timestamp
    return { 
      "start" : date(start_date.year - current, 1, 1), 
      "end" : date(start_date.year - current, 12, 31) 
    }

  def lastMonth(self) :
    start_date = self.timestamp
    days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
    last_month = start_date - timedelta(days=days_in_month)
    lastDay = calendar.monthrange(last_month.year, last_month.month)[1] # number
    return { 
      "start" : date(last_month.year, last_month.month, 1), 
      "end" : date(last_month.year, last_month.month, lastDay) 
    }
