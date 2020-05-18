import numpy as np
from typing import Tuple, TextIO

# Convenience Constant

PROVINCE_CODES = (
        ('10','NL'),
        ('11','PE'),
        ('12','NS'),
        ('13','NB'),
        ('24','QC'),
        ('35','ON'),
        ('46','MB'),
        ('47','SK'),
        ('48','AB'),
        ('59','BC'),
        ('60','NN') # NN is a combined code for NT, NU and YK
    )

# PART 1: PREPARATION

# Change data types to:
# - 'U2' for nominal
# - int for ordinal
# - float for interval
# - float for ratio

DATA_COLUMNS = [
('alcofreq', int),
('alcoweek', float),
('biosex', 'U2'),
('agegroup', int),
('education', int),
('fruitvegtot', float),
('stressgen', int),
('stresswork', int),
('healthphys', int),
('healthment', int),
('satisfaction', int),
('province', 'U2'),
('hasdoctor', 'U2'),
('bmi', float),
('height', float),
('weight', float),
('incomegroup', int),
('workhoursperweek', float),
('firstlanguage', 'U2'),
('yrsmokedaily', int)
]


# Fill out tuples with nominal, ordinal, interval, and ratio column names

NOMINAL = ('biosex',
           'province', 
           'hasdoctor', 
           'firstlanguage')
ORDINAL = ('alcofreq',
           'agegroup',
           'education',
           'stressgen', 
           'stresswork',
           'healthphys',
           'healthment',
           'satisfaction',
           'incomegroup'
           )
INTERVAL =('bmi',)            
RATIO = ('alcoweek',
         'fruitvegtot',
         'height', 
         'weight', 
         'workhoursperweek', 
         'yrsmokedaily')





# PART 2: FUNCTIONS

def replace_nominal_codes(data: np.array, column_name: str, codes: Tuple[Tuple[str, str]]) -> None:
    '''Precondition: column_name exists in data and is a nominal data measurement scale.
    codes is a tuple of tuples containing (old code, new code).

    Change all occurrences of old code to new code in column_name of data.
    
    >>> replace_nominal_codes(CCHS, 'biosex', (('1', 'M'),('2', 'F')))
    >>> CCHS['biosex'][0]
    'F'
    >>> CCHS['biosex'][-1]
    'M'
    '''
    #for i in range(len(data[column_name])):
        #for j in range(len(codes)):
            #if data[column_name][i] == codes[j][0]:
                #data[column_name][i] = codes[j][1]

    for code in codes:
        mask = data[column_name] == code[0]
        data[column_name][mask] = code[1]
        
        
        
def replace_missing_with_nan(data: np.array, column_name: str, missing_codes: Tuple[float]) -> None:
    '''Precondition: column_name exists in data and is a ratio data measurement scale.
    missing_codes is a tuple containing codes that denote missing data.
    Convert all values in column column_name of data that match the codes 
    in missing_codes to Not-A-Number values (np.nan)
    
    >>> replace_missing_with_nan(CCHS, 'alcoweek', (996,))
    >>> CCHS['alcoweek'][2]
    nan
    >>> CCHS['alcoweek'][-3]
    nan
    '''
    change_array = data[column_name]
    mask = change_array == missing_codes[0]
    change_array[mask] = np.nan
        
        
def write_categorical_csv(data: np.array, column_name: str, outfile: TextIO) -> None:
    '''Precondition: column_name exists in data and is nominal or ordinal data measurement scale.
    Write to outfile the label and counts of each category contained in column_name of data.
    
    >>> with open("csv/biosex.csv", 'w') as file:
            write_categorical_csv(CCHS, 'biosex', file)
    >>> with open("csv/biosex.csv", 'r') as check:
            for line in check:
                print(line.strip())
    biosex,count
    F,832
    M,668
    '''
    outfile.write(column_name + ',count\n')
    label, count = np.unique(data[column_name],return_counts=True)
    for i in range(len(label)):
        outfile.write(str(label[i]) + ',' + str(count[i]) + '\n')

                   
    



def write_column_summary_csv(data: np.array, column_name: str, outfile: TextIO) -> None:
    '''Precondition: column_name exists in data and is a non-nominal data measurement scale.
    Write to outfile a line containing comma-separated values as follows:
    - The column name
    - The median of values in the column
    - (if interval or ratio) The mean of values in the column, ignoring nan
    - (if interval or ratio) The standard deviation of values in the column, ignoring nan
    
    (Examples not required)
    
    '''
    median = np.nanmedian(data[column_name], axis = 0)
    mean = np.nanmean(data[column_name])
    standard = np.nanstd(data[column_name])
    if column_name in INTERVAL + RATIO:
        outfile.write(column_name + ',' + str(median) + ',' + str(mean) + ',' + str(standard) + '\n')
    else:
        outfile.write(column_name + ',' + str(median) + ','+',\n')
        


if __name__ == "__main__":
    

    CCHS = np.genfromtxt('CCHSX.csv', delimiter=',', skip_header=1, dtype=DATA_COLUMNS)

    

    replace_nominal_codes(CCHS, 'biosex', (('1','M'),('2','F')))
    replace_nominal_codes(CCHS, 'province', PROVINCE_CODES)
    replace_nominal_codes(CCHS, 'hasdoctor', (('1','Y'),('2','N')))
    replace_nominal_codes(CCHS, 'firstlanguage', (('1','EN'),('2','FR'),('3','EF'),('4','NO')))


    replace_missing_with_nan(CCHS, 'alcoweek', (996,))
    replace_missing_with_nan(CCHS, 'workhoursperweek', (996,))

    

    for c in NOMINAL + ORDINAL:
        with open('csv/'+c+'.csv', 'w') as f:
            write_categorical_csv(CCHS, c, f)

   

    with open("csv/summary.csv", 'w') as f:
        f.write("COLUMN,MEDIAN,MEAN,STDEV\n")
        for n in ORDINAL + INTERVAL + RATIO:
            write_column_summary_csv(CCHS, n, f)
