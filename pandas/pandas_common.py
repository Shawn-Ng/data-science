
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
        raise ValueError('pandasDf must be a Pandas dataframe')
    
    result = pandasDf.head().append(pandasDf.tail())
    return result

