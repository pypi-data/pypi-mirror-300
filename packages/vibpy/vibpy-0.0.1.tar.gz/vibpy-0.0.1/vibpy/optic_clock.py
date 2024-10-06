# @dependency libs——math,numpy,scipy
import math
import numpy as np
from scipy import signal
from scipy import io
import matplotlib.pyplot as plt

def tf_h(freq, types=1):
    """
    :param freq:
    :param types: 1 revised, 0 unrevised
    :return: value of tf_h at freq
    """
    tao=1
    h=(math.sqrt(2) * (math.sin(math.pi * freq * tao)) ** 2 / (math.pi * freq * tao)) ** 2
    if freq > 0.5 and types==1:
        h = (math.sqrt(2) / (math.pi * freq * tao)) ** 2
    return h


def v2acc(fs,vel,sen,options='g'):
    """
    Translate vel to acc in time domain
    :param fs:
    :param vel:
    :param sen:
    :param options:
    :return: array of acc default in g
    """
    g=9.8
    vel1 = vel/sen
    dt = 1/fs
    acc = (vel1[1:] - vel1[0:- 1])/dt ## 一阶差分
    if options == 'g':
        acc=acc/g
    return acc


def psd_v2acc(freq,psd_v,sen,options='g'):
    """
    Translate vel to acc in frequency domain
    :param freq:
    :param psd_v:
    :param sen: sensitivity of sensor
    :param options:
    :return: array of psd default in g^2/Hz
    """
    g=9.8
    psd_a = []
    for i in range(0,len(freq)):
        if options == 'g':
            psd_a.append(psd_v[i]*(2*math.pi*freq[i])**2/sen**2/g**2)
        else:
            psd_a.append(psd_v[i]*(2*math.pi*freq[i])**2/sen**2)
    return psd_a


def allan(freq, psd_a, types=1):
    """
    :param freq:
    :param psd_a:
    :param types: 1 revised tf_h, 0 unrevised tf_h
    :return:
            psd  value not including tf_h
            sigma  value including tf_h
    """
    sigma=0
    psd=0
    df=freq[2]-freq[1]
    for i in range(0,len(freq)):
        h = tf_h(freq[i], types)
        sigma = sigma + df * h * psd_a[i]
        psd = psd + df * psd_a[i]
    psd=math.sqrt(psd)
    sigma=math.sqrt(sigma)
    return psd, sigma


def inter_find(f,f_min,f_max):
    """
    find the index of f_min and f_max
    :param f:
    :param f_min:
    :param f_max:
    :return: index of start and end
    """
    nlist1 = np.size(np.where(f < f_min))
    nlist2 = np.size(np.where(f < f_max))
    return nlist1,nlist2


def read_mat(filedir,filename,var_name,var_str):
    """
    read data from .mat of matlab
    :param filedir:
    :param filename:
    :param var_name: struct name or variable name
    :param var_str: names in struct
    :return: y array data
    """
    filepath = filedir + '/' + filename
    data = io.loadmat(filepath)
    data_all = data[var_name]
    n=len(var_str)
    if n==0:
        y = data_all
    elif n==1:
        y = data_all[0,0][var_str[0]]
    else:
        y = data_all[0,0][var_str[0]][0,0][var_str[1]]
    return y


def psd_cal(filedir,filename,fs,sen,f_min,f_max,l_rate,types,options='g'):
    """
    calculate based on time domain data
    :param filedir:
    :param filename:
    :param fs: sampling freq
    :param sen: sensitivity of sensor
    :param f_min:
    :param f_max:
    :param l_rate: length rate for default window hann, example 0.1
    :param types: type of tf_h
    :param options: default g
    :return: f1 freq array
            p1 psd of g^2/Hz array
            rms  value not including tf_h
            sigma  value including tf_h
    """
    filepath=filedir+'/'+filename
    data=np.loadtxt(filepath)
    data = data - np.mean(data)
    data = v2acc(fs, data, sen, options)
    f1, p1 = signal.welch(data, fs, window='hann', nperseg=round(l_rate * len(data)), nfft=len(data), scaling='density')
    nlist1 = np.size(np.where(f1 < f_min))
    nlist2 = np.size(np.where(f1 < f_max))
    f1 = f1[nlist1:nlist2]
    p1 = p1[nlist1:nlist2]
    rms, sigma = allan(f1, p1, types)
   # print("{:e}".format(sigma))  ## 科学计数法
   # print("{:e}".format(psd))
    return f1,p1,rms,sigma


def fig_str(types='ASD',unit='g'):
    """
    special y_label and title
    :param types:
    :param unit:
    :return:
    """
    if types=='ASD' and unit=='g':
        str_unit=r'$g/\sqrt{Hz}$'
        y_label=types + ' [' + str_unit + ']'
        title_str='Amplitude Spectrum Density'
    elif types=='ASD' and unit=='m/s^2':
        str_unit=r'$m/s^2/\sqrt{Hz}$'
        y_label = types + ' [' + str_unit + ']'
        title_str='Amplitude Spectrum Density'
    elif types=='PSD' and unit=='g':
        str_unit='g^2/Hz'
        y_label = types + ' [' + str_unit + ']'
        title_str='Power Spectrum Density'
    elif types=='PSD' and unit=='m/s^2':
        str_unit='m/s^2/Hz'
        y_label = types + ' [' + str_unit + ']'
        title_str='Power Spectrum Density'
    else:
        str_unit=unit+'^2/Hz'
        y_label = types + ' [' + str_unit + ']'
        title_str=types
    return y_label, title_str

