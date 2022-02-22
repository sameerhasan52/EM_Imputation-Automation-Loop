import numpy as np
from impyute.util import find_null
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
import os

def em(data, loops=50):
    iteration = 0
    null_xy = find_null(data)  # stores row index and col index of missing data

    for x_i, y_i in null_xy:
        col = data[:, int(y_i)]
        mu = col[~np.isnan(col)].mean()
        std = col[~np.isnan(col)].std()
        col[x_i] = np.random.normal(loc=mu, scale=std)
        previous, i = 1, 1
        for i in range(loops):
            # Expectation Step (E-Step)
            mu = col[~np.isnan(col)].mean()
            std = col[~np.isnan(col)].std()
            # Maximization Step (M-Step)
            col[x_i] = np.random.normal(loc=mu, scale=std)
            delta = (col[x_i]-previous)/previous
            iteration = i
            if i > 5 and delta < 1e-08:
             data[x_i][y_i] = col[x_i]
             break
        data[x_i][y_i] = col[x_i]
        previous = col[x_i]

    result = {
        'X_imputed' : data,
        'Iteration' : iteration
    }

    return result

## Function to convert Categorical Values to Numeric Values

def spl_to_numeric(x):
    if x=='A': return 1
    if x=='C': return 2
    if x=='G': return 3
    if x=='N': return 4
    if x=='S': return 5
    if x=='T': return 6

def hov_to_numeric(x):
    if x=='n': return 1
    if x=='y': return 2

def c4_ttteg_to_numeric(x):
    if x == 'b': return 1
    if x == 'o': return 2
    if x == 'x': return 3

def mush_to_numeric(x):
    if x == 'a': return 1
    if x == 'b': return 2
    if x == 'c': return 3
    if x == 'd': return 4
    if x == 'e': return 5
    if x == 'f': return 6
    if x == 'g': return 7
    if x == 'h': return 8
    if x == 'k': return 9
    if x == 'l': return 10
    if x == 'm': return 11
    if x == 'n': return 12
    if x == 'o': return 13
    if x == 'p': return 14
    if x == 'r': return 15
    if x == 's': return 16
    if x == 't': return 17
    if x == 'u': return 18
    if x == 'v': return 19
    if x == 'w': return 20
    if x == 'x': return 21
    if x == 'y': return 22

## Function to convert Numeric Values to Categorical Values

def numeric_to_spl(x):
    if x<=1.5: return 'A'
    if x>1.5 and x<=2.5: return 'C'
    if x>2.5 and x<=3.5: return 'G'
    if x>3.5 and x<=4.5: return 'N'
    if x>4.5 and x<=5.5: return 'S'
    if x>5.5: return 'T'

def numeric_to_hov(x):
    if x <= 1.5: return 'n'
    if x>1.5: return 'y'

def numeric_to_c4_ttteg(x):
    if x<=1.5: return 'b'
    if x>1.5 and x<=2.5: return 'o'
    if x>2.5: return 'x'

def numeric_to_mush(x):
    if x <= 1.5: return 'a'
    if x>1.5 and x<=2.5: return 'b'
    if x>2.5 and x<=3.5: return 'c'
    if x>3.5 and x<=4.5: return 'd'
    if x>4.5 and x<=5.5: return 'e'
    if x>5.5 and x<=6.5: return 'f'
    if x>6.5 and x<=7.5: return 'g'
    if x>7.5 and x<=8.5: return 'h'
    if x>8.5 and x<=9.5: return 'k'
    if x>9.5 and x<=10.5: return 'l'
    if x>10.5 and x<=11.5: return 'm'
    if x>11.5 and x<=12.5: return 'n'
    if x>12.5 and x<=13.5: return 'o'
    if x>13.5 and x<=14.5: return 'p'
    if x>14.5 and x<=15.5: return 'r'
    if x>15.5 and x<=16.5: return 's'
    if x>16.5 and x<=17.5: return 't'
    if x>17.5 and x<=18.5: return 'u'
    if x>18.5 and x<=19.5: return 'v'
    if x>19.5 and x<=20.5: return 'w'
    if x>20.5 and x<=21.5: return 'x'
    if x > 21.5: return 'y'


prefix = ['4-gauss', 'Iris', 'Wine', 'Glass', 'Sheart', 'BUPA', 'Ionosphere', 'Sonar',  'BCW', 'PID', 'DERM', 'Difdoug',
          'CNP', 'Yeast', 'Spam', 'Letter','TTTTEG','HOV','MUSH','Splice','C4']

name = ["_AE_1", "_AE_5", '_AE_10', '_AE_20', '_AG_1', '_AG_5', '_AG_10', '_AG_20', '_AL_1', '_AL_5', '_AL_10',
        '_AL_20', '_AN_1', '_AN_5', '_AN_10', '_AN_20', '_AW_1', '_AW_5', '_AW_10', '_AW_20', '_C_1', '_C_5', '_C_10',
        '_C_20', '_NE_1', '_NE_5', '_NE_10', '_NE_20', '_NG_1', '_NG_5', '_NG_10', '_NG_20', '_NL_1', '_NL_5', '_NL_10',
        '_NL_20', '_NN_1', '_NN_5', '_NN_10', '_NN_20', '_NW_1', '_NW_5', '_NW_10', '_NW_20']

extension = '.xlsx'
for pre in prefix:
    Flag = False
    original = "C:\\Users\\Dell\\PycharmProjects\\dummy\\Original Datasets Without Labels\\" + pre + extension
    for x in name:
        count = 0
        dir = "C:\\Users\\Dell\\PycharmProjects\\dummy\\Incomplete Datasets Without Labels\\" + pre + '\\'
        namefile = dir + pre + x + extension
        missing = pd.read_excel(namefile, header=None)

        if pre == 'Splice' or pre == 'TTTTEG' or pre == 'HOV' or pre == 'MUSH' or pre == 'C4':
            Flag = True
            noOfCol = missing.columns
            total_columns = len(noOfCol)
            for i in range(0, total_columns):
                if pre == 'Splice':
                    missing[i] = missing[i].apply(spl_to_numeric)
                if pre == 'HOV':
                    missing[i] = missing[i].apply(hov_to_numeric)
                if pre == 'MUSH':
                    missing[i] = missing[i].apply(mush_to_numeric)
                if pre == 'TTTTEG' or pre == 'C4':
                    missing[i] = missing[i].apply(c4_ttteg_to_numeric)

        missing = missing.to_numpy()


        result_imputed = em(missing)

        output_imputed = result_imputed["X_imputed"]

        out = pd.DataFrame(output_imputed)

        if Flag == True:
           for i in range(0,total_columns):
               if pre == 'Splice':
                   out[i] = out[i].apply(numeric_to_spl)
               if pre == 'HOV':
                   out[i] = out[i].apply(numeric_to_hov)
               if pre == 'MUSH':
                   out[i] = out[i].apply(numeric_to_mush)
               if pre == 'TTTTEG' or pre == 'C4':
                   out[i] = out[i].apply(numeric_to_c4_ttteg)

        save_dir = "C:\\Users\\Dell\\PycharmProjects\\dummy\\result\\"+pre+"\\"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        finalfile = save_dir+pre+x+extension

        out.to_excel(finalfile, header=None, index=False)

        cdata = pd.read_excel(original, header=None)
        compdata = cdata.to_numpy()

        fname = pre + x
        print(fname)

        if Flag == False:
            meanSquaredError = mean_squared_error(compdata, out)

            NRMS = sqrt(meanSquaredError)
            print(NRMS)


            nameIter = fname + ' ' + str(NRMS) + ' iteration : ' + str(result_imputed["Iteration"]) + '\n'
            f = open(save_dir + "Output.txt", "a")
            f.write(nameIter)
            f.close()

            f = open(save_dir + "NRMS.txt", "a")
            f.write(str(NRMS) + '\n')
            f.close()


        f = open(save_dir + "Filename.txt", "a")
        f.write(fname + '\n')
        f.close()


        f = open(save_dir + "Iteration.txt", "a")
        f.write(str(result_imputed["Iteration"]) + '\n')
        f.close()

        if Flag == True:
            imputed_file = pd.read_excel(finalfile, header=None)
            imputed_file = imputed_file.to_numpy()
            for i in range(0, len(imputed_file)):
              for j in range(0, total_columns):
                if imputed_file[i][j] == compdata[i][j]:
                    count += 1

            AE = count / imputed_file.size
            print(count)
            print("AE : ", AE)

            f = open(save_dir + "AE.txt", "a")
            f.write(str(AE) + '\n')
            f.close()