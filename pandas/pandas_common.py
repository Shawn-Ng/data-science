#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def config_pandas_display():
    '''
    Configure Pandas display
    '''
    import pandas as pd
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_rows', 200)
    pd.set_option('display.expand_frame_repr', True)


def reset_pandas_display():
    '''
    Reset Pandas display
    '''
    import pandas as pd
    pd.set_option('display.max_columns', 20)
    pd.set_option('display.max_colwidth', 50)
    pd.set_option('display.max_rows', 60)
    pd.set_option('display.expand_frame_repr', True)


# PURE PYTHON FUNCTION
def clean_string_literal(aStr):
    '''
    Convert literal string to string
    
    Parameter
    ---------
    aStr: str
        The column to convert from string literal to string
    
    Return
    ------
    Cleansed string
    '''
    result = aStr
    
    if isinstance(aStr, (str)):
        result = aStr.strip("'\"")
    
    return result


def convert_string_to_number(aStr, numericType=''):
    '''
    Convert string number to number (int / float / bool)
    
    Parameter
    ---------
    aStr: str
        The column to convert from string to number
    
    Return
    ------
    Number
    '''
    result = aStr

    if isinstance(aStr, (str)):
        if numericType == 'int':
            result = int(clean_string_literal(aStr))

        if numericType == 'float':
            result = float(clean_string_literal(aStr))
        
    return result


def convert_string_to_boolean(aStr, booleanType='bool'):
    '''
    Convert string boolean to boolean (bool / int)
    
    Parameter
    ---------
    aStr: str
        The column to convert from string to boolean
    
    Note
    ----
    Do not use eval() as it's unsafe
    
    Return
    ------
    Boolean or integer
    '''
    import distutils.util

    result = aStr
    
    if booleanType == 'bool':
        if isinstance(aStr, (str)):
            # result = eval(clean_string_literal(aStr))
            result = bool(distutils.util.strtobool(clean_string_literal(aStr)))

    if booleanType == 'int':
        if isinstance(aStr, (bool)):
            result = int(aStr)
        if isinstance(aStr, (str)):
            # result = int(eval(clean_string_literal(aStr)))
            result = distutils.util.strtobool(clean_string_literal(aStr))
    
    return result


def convert_string_to_DL(aStr):
    '''
    Convert string dictionary/list to dictionary/list
        
    Parameter
    ---------
    aStr: str
        The column to convert from string to dictionary/list
    
    Return
    ------
    Dictionary / list
    '''
    import ast

    result = aStr
    if isinstance(aStr, (str)):
        result = ast.literal_eval(clean_string_literal(aStr))
    
    return result
    

# PANDAS FUNCTION
def add_type_columns(pandasDf):
    '''
    Return Pandas dataframe where each columns has their type column right next to it
    
    Parameter
    ---------
    pandasDf: pandas.core.frame.DataFrame
        One Pandas dataframe
    
    Return
    ------
    A Pandas dataframe
    '''    
    if not isinstance(pandasDf, (pd.DataFrame)):
        raise TypeError('Variable must be a pandas dataframe')

    suffix = '_type'
    for column in pandasDf.columns:
        # To prevent creating (1) duplicated column (2) column with ever-increasing suffix [xxx_type, xxx_type_type ...]
        newCol = column+suffix
        if not (newCol in pandasDf.columns or column.endswith(suffix)):
            newColLoc = pandasDf.columns.get_loc(column)+1
            newColValue = pandasDf[column].apply(lambda x: type(x))
            pandasDf.insert(newColLoc, column=newCol, value=newColValue)
            # pandasDf[newCol] = pandasDf[column].apply(lambda x: type(x))
    return pandasDf


def compare_all_list_items(aList):
    '''
    Print every comparison between list's 2 items
    
    Parameter
    ---------
    aList: list
        A list

    Return
    ------
    A Pandas dataframe
    '''
    import itertools
    import pandas as pd

    if not isinstance(aList, (list)):
        raise TypeError('Variable must be a list')

    result = []
    
    for a, b in itertools.combinations(aList, 2):
        # print(f"{repr(a)} == {repr(b)}: {a==b}")
        row = {'item1':repr(a), 'item2':repr(b), 'comparison':a==b}
        result.append(row)

    df = pd.DataFrame(result, columns=['item1','item2','comparison'])
    return df


def head_tail(pandasDf):
    '''
    Print the Pandas dataframe first n head and last n tail
    
    Parameter
    ---------
    pandasDf: pandas.core.frame.DataFrame
        One Pandas dataframe
        
    Return
    ------
    A Pandas dataframe
    '''
    import pandas as pd
    
    if not isinstance(pandasDf, (pd.DataFrame)):
        raise TypeError('Variable must be a pandas dataframe')
    
    result = pandasDf.head().append(pandasDf.tail())
    return result


def columns_to_dictionary(pandasDf):
    '''
    Create a dictionary {datatype: [columnNames]} from Pandas dataframe
    
    Parameter
    ---------
    pandasDf: pd.Dataframe
    
    Return
    ------
    A dictionary
    '''
    import pandas as pd
    
    if not isinstance(pandasDf, (pd.DataFrame)):
        raise TypeError('Variable must be a pandas dataframe')
    
    dataTypeDict = {}

    for index, value in pandasDf.loc[0].iteritems():
        dataType = type(value)
        if dataType not in dataTypeDict:
            dataTypeDict[dataType] = [index]
        else:
            dataTypeDict[dataType].append(index)

    return dataTypeDict


def index_marks(nrows, chunkSize):
    '''
    Determine the range given the (1) dataframe rows (2) desired chunk size
    
    Parameter
    ---------
    nrows: int
        The number of rows in a dataframe
    chunkSize: int
        The desire chunk size
    
    Return
    ------
    Python range
    '''
    if not all(isinstance(x, (int)) for x in [nrows, chunkSize]):
        raise ValueError('Variables 1 & 2 must be int')
    
    p1 = 1 * chunkSize
    p2 = (nrows // chunkSize + 1) * chunkSize
    p3 = chunkSize
    result = range(p1, p2, p3)

    return result


def split_pandas_dataframe(pandasDf, chunkSize):
    '''
    Split Pandas dataframe into dataframes with specific chunkSize
    
    Parameter
    ---------
    pandasDf: pd.Dataframe
    chunkSize: int
        The chunk size of each smaller dataframes
    
    Return
    ------
    Return list of dataframes
    '''
    import numpy as np    
    import pandas as pd
    
    indices = index_marks(pandasDf.shape[0], chunkSize)
    result = np.split(pandasDf, indices)
    
    return result


def excel_keep_url_string(filepath, pandasDf):
    '''
    Save Pandas dataframe as excel, without converting string to urls.
    - Excel auto converts string to urls
    - Excel limit of 65,530 urls per worksheet
    - Excel does not keep url > 255 characters
    
    Parameter
    ---------
    filepath: str
        File path
    pandasDf: pd.Dataframe
        The dataframe to export into excel

    Return
    ------
    Pandas dataframe => excel
    '''
    import pandas as pd
        
    if not isinstance(filepath, (str)):
        raise ValueError('Variable 1: must be non-empty str')

    if not isinstance(pandasDf, pd.DataFrame):
        raise TypeError('Variable 2: must be Pandas dataframe')

    writer = pd.ExcelWriter(filepath, engine='xlsxwriter', options={'strings_to_urls': False})
    pandasDf.to_excel(writer, index=False)
    writer.close()


def compare_before_after_dataframes(pandasDf, pandasDf2):
    '''
    Compare the before & after Pandas dataframe going through data transformation (DT)
    
    Parameter
    ---------
    pandasDf: pd.Dataframe
        The Pandas dataframe before DT
    pandasDf2: pd.Dataframe
        The Pandas dataframe after DT
    
    Return
    ------
    Output comparison between 2 dataframes
    '''
    import pandas as pd
    
    if not all(isinstance(x,( pd.DataFrame)) for x in [pandasDf, pandasDf2]):
        raise TypeError('Variables 1 & 2 must be pandas dataframe')
    
    print('-----------------------')
    print('PANDAS DATAFRAME LENGTH')
    print('-----------------------')
    print('df1: Dataframe before data transformation')
    print('df2: Dataframe after data transformation')
    print('df1 length: {}'.format(len(pandasDf)))
    print('df2 length: {}'.format(len(pandasDf)))
    print('The dataframes length change: {}'.format(len(pandasDf)==len(pandasDf2)))
    print()
    
    print('---------------')
    print('COMPARE COLUMNS')
    print('---------------')
    for column in pandasDf.columns:
        pdDf = pandasDf[pandasDf[column].notnull()]
        pdDf2 = None
        print('df1 non-null {}: {}'.format(column, len(pdDf)))

        try:
            pdDf2 = pandasDf2[pandasDf2[column].notnull()]
        except KeyError:
            print('df2 {}: does not exist'.format(column))

        if pdDf2 is not None:
            print('df2 non-null {}: {}'.format(column, len(pdDf2)))

            if len(pdDf) == len(pdDf2):
                print('df1 & df2 has the same length')
            elif len(pdDf2) > len(pdDf):
                print('df2 > df1, Check')
            else:
                strings = ['null', 'NA']
                pdDfNull = len(pandasDf[pandasDf[column].isnull()])
                pdDfString = len(pandasDf[pandasDf[column].isin(strings)])
                pdDfEmptyString = len(pandasDf[pandasDf[column].str.len()==0])
                pdDfRemoveNullEmpty = len(pandasDf) - pdDfNull - pdDfString - pdDfEmptyString
                print('df1 - null ({}) - string null ({}) - empty string ({}) = {} == df2 ({}): {}'                      .format(pdDfNull, pdDfString, pdDfEmptyString, pdDfRemoveNullEmpty,
                              len(pdDf2), pdDfRemoveNullEmpty==len(pdDf2)))
        print()
        

def value_counts_to_dataframe(pandasDf, column):
    '''
    Convert pandas.Series.value_counts() into pandas.Dataframe
    
    Parameter
    ---------
    pandasDf: pandas.Dataframe
    column: str
        The column to do value_counts()
        
    Return
    ------
    pandas.Dataframe
    '''
    import pandas as pd
    
    result = pandasDf[column].value_counts().rename_axis(column).reset_index(name='counts')
    return result


# How to hide specific cell in notebook: https://stackoverflow.com/a/48084050
