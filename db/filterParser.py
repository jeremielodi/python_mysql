# eslint class-methods-use-this:off #
from  .period import PeriodService
import copy

RESERVED_KEYWORDS = ['limit', 'detailed']
DEFAULT_LIMIT_KEY = 'limit'
DEFAULT_UUID_PARTIAL_KEY = 'uuid'

'''
 @class FilterParser
 
 @description
 This library provides a uniform interface for processing filter `options`
 sent from the client to server controllers.
 It providers helper methods for commonly request filters like date restrictions
 and standardises the conversion to valid SQL.
 
 It implements a number of built in 'Filter Types' that allow column qurries
 to be formatted for tasks that are frequently required.
 
 Supported Filter Types:
 equals - a direct comparison
 text - search for text contained within a text field
 dateFrom - limit the query to records from a date
 dateTo - limit the query to records up until a date
 
 @requires lodash
 @requires moment
 '''

class FilterParser:
  # options that are used by all routes that shouldn't be considered unique filters
  def __init__(self, filters = {}, options = {}):
    # stores for processing options
    self._statements = []
    self._parameters = []

    self._filters = copy.copy(filters)

    # configure default options
    self._tableAlias = options.get('tableAlias') or None
    self._limitKey = options.get('limitKey') or DEFAULT_LIMIT_KEY
    self._order = ''
    self._parseUuids = True if hasattr(options, 'parseUuids') else options.get('parseUuids')

    self._autoParseStatements = False if hasattr(options, 'autoParseStatements') else options.get('autoParseStatements')
    self._group = ''

  '''
    @method text
   
    @description
    filter by text value, searches for value anywhere in the database attribute
    alias for _addFilter method
   
    @param {String} filterKey    key attribute on filter object to be used in filter
    @param {String} columnAlias  column to be used in filter query. This will default to
                                 the filterKey if not set
    @param {String} tableAlias   table to be used in filter query. This will default to
                                 the object table alias if it exists
   '''
  def fullText(self, filterKey, columnAlias=None, tableAlias=None) :
    columnAlias = filterKey if not columnAlias else columnAlias
    tableAlias =  self._tableAlias if not tableAlias else tableAlias
    tableString = self._formatTableAlias(tableAlias)

    if self._filters.__contains__(filterKey)  :
      searchString = "%" + self._filters.get("filterKey")
      preparedStatement = "LOWER(" + tableString + columnAlias + ") LIKE ? "

      self._addFilter(preparedStatement, searchString)
      del self._filters[filterKey]  


  def period(self, filterKey, columnAlias=None, tableAlias=None):
    columnAlias = filterKey if not columnAlias else columnAlias
    tableAlias =  self._tableAlias if not tableAlias else tableAlias
    tableString = self._formatTableAlias(tableAlias)

    if self._filters.__contains__(filterKey) :
      #if a client timestamp has been passed - this will be passed in here
      period = PeriodService(self._filters.get('client_timestamp'))
      targetPeriod = period.lookupPeriod(self._filters[filterKey])

      # specific base case - if all time requested to not apply a date filter

      if ( filterKey == 'allTime') or (filterKey == 'custom') :
        del self._filters[filterKey]
        return

      # st.get('limit')
      periodFromStatement = 'DATE(' + tableString + columnAlias + ') >= DATE(?)'
      periodToStatement = 'DATE(' + tableString + columnAlias + ') <= DATE(?)'

      self._addFilter(periodFromStatement, targetPeriod.get('limit').get('start'))
      self._addFilter(periodToStatement, targetPeriod.get('limit').get('end'))
      del self._filters[filterKey]
  
  '''
   @method dateFrom
   @param {String} filterKey    key attribute on filter object to be used in filter
   @param {String} columnAlias  column to be used in filter query. This will default to
                                the filterKey if not set
   @param {String} tableAlias   table to be used in filter query. This will default to
                                 the object table alias if it exists
   '''
  def dateFrom(self, filterKey, columnAlias=None, tableAlias=None) :
    columnAlias = filterKey if not columnAlias else columnAlias
    tableAlias =  self._tableAlias if not tableAlias else tableAlias
    tableString = self._formatTableAlias(tableAlias)

    if  self._filters.__contains__(filterKey)  :
      timestamp = self._filters[filterKey]
      preparedStatement = "DATE("+tableString + columnAlias +") >= DATE(?)"
      day = PeriodService(timestamp).lookupPeriod('today').get('limit').get('start')
      self._addFilter(preparedStatement, day)
      del self._filters[filterKey]

  '''
  @method dateTo
  
  @param {String} filterKey    key attribute on filter object to be used in filter
  @param {String} columnAlias  column to be used in filter query. This will default to
                                the filterKey if not set
  @param {String} tableAlias   table to be used in filter query. This will default to
                                the object table alias if it exists
  '''
  def dateTo(self, filterKey, columnAlias= None, tableAlias = None) :
    columnAlias = filterKey if not columnAlias else columnAlias
    tableAlias =  self._tableAlias if not tableAlias else tableAlias
    tableString = self._formatTableAlias(tableAlias)
    timestamp = self._filters[filterKey]

    if  hasattr(self._filters, filterKey) :
      preparedStatement = "DATE("+ tableString + columnAlias + ") <= DATE(?)"
      day = PeriodService(timestamp).lookupPeriod('today').get('limit').get('start')
      self._addFilter(preparedStatement, day)
      del self._filters[filterKey]

  def equals(self, filterKey, columnAlias = None, tableAlias = None, isArray = False) :
    columnAlias = filterKey if not columnAlias else columnAlias
    tableAlias =  self._tableAlias if not tableAlias else tableAlias
    tableString = self._formatTableAlias(tableAlias)

    if self._filters.__contains__(filterKey) :
      valueString = '?'
      preparedStatement = ''

      if isArray : # search in a list of values, example : where id in (1,2,3)
        preparedStatement = "" + tableString + columnAlias + " IN  (" + valueString +")"
      else : # seach equals one value , example : where id = 2
        preparedStatement = tableString + columnAlias +" = " + valueString

      self._addFilter(preparedStatement, self._filters[filterKey])
      del self._filters[filterKey]

  '''
   @method custom
   @public
   
   @description
   Allows a user to write custom SQL with either single or multiple
   parameters.  The syntax is reminiscent of db.exec() in dealing with
    arrays.
  '''
  def custom(self, filterKey, preparedStatement, preparedValue = None) :

    if self._filters.__contains__(filterKey) :
      
      searchValue = preparedValue or self._filters[filterKey]
      isParameterArray = isinstance(searchValue, list)

      self._statements.append(preparedStatement)

      #gracefully handle array-like parameters by spreading them
      if isParameterArray :
        self._parameters.extend(searchValue)
      else :
        self._parameters.append(searchValue)
  
      del self._filters[filterKey]

  '''
   @method setOrder
   
   @description
   Allows setting the SQL ordering on complex queries - this should be
   exposed through the same interface as all other filters.
  '''
  def setOrder(self, orderString) :
    self._order = orderString
  '''
    @method setGroup
    @description
    Allows setting the SQL groups in the GROUP BY statement.  A developer is expected to
    provide a valid SQL string.  This will be appended to the SQL statement after the
    WHERE clause.
  '''
  def setGroup(self, groupString) :
    self._group = groupString


  def applyQuery(self, sql) :
    # optionally call utility method to parse all remaining options as simple
    # equality filters into `_statements`
    limitCondition = self._parseLimit()

    if self._autoParseStatements :
      self._parseDefaultFilters()

    conditionStatements = self._parseStatements()
    order = self._order
    group = self._group
    
    return sql + " WHERE " +conditionStatements + " "+ group + " " + order + " "+ limitCondition


  def parameters(self) :
    return self._parameters


  # this method only applies a table alias if it exists
  def _formatTableAlias(self, table) :
    return table + "."  if  table else ''

  '''
   @method _addFilter

   @description
   Private method - populates the private statement and parameter variables
  '''
  def _addFilter(self, statement, parameter) :
    self._statements.append(statement)
    self._parameters.append(parameter)

  #remove options that represent reserved keys
  def ommit(self):
    for x in RESERVED_KEYWORDS :
      del self._filters[x]
    return self._filters

  '''
    @method _parseDefaultFilters
    @description
    Utility method for parsing any filters passed to the search that do not
    have filter types - these always check for equality
  '''

  def _parseDefaultFilters(self) :
    #remove options that represent reserved keys
    self._filters = self.ommit()

    for value, key in self._filters :
      valueString = "?"
      tableString = self._formatTableAlias(self._tableAlias)

      if self._parseUuids :
        # check to see if key contains the text uuid - if it does and parseUuids has
        # not been suppressed, automatically parse the value as binary
        if (key.__contains__(DEFAULT_UUID_PARTIAL_KEY)) :
          valueString = 'HUID(?)'

      ch = tableString + key + "=" + valueString
      self._addFilter(ch, value)


  def _parseStatements(self) :
    # this will always return true for a condition statement
    DEFAULT_NO_STATEMENTS = '1'
    return DEFAULT_NO_STATEMENTS if not self._statements else  ' AND '.join(str(x) for x in self._statements)
  

  def _parseLimit(self) :
    limitString = ''

    if hasattr(self._filters,self._limitKey ) :
      limit = str(self._filters[self._limitKey])
      limitString = "\nLIMIT "+limit

    return limitString
