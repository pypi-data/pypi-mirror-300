import math
import os

def rand_vib(n, f, amp_g2hz):  # random vibration curve
    f0, f1, f2, f3 = f[0], f[1], f[2], f[3]
    n1, n2 = n[0], n[1]  # up_rate and down_rate
    s1 = amp_g2hz
    s0 = s1 * math.pow((f0 / f1), n1 / (10 * math.log10(2)))
    s2 = s1 * math.pow((f3 / f2), n2 / (10 * math.log10(2)))
    a1 = (s1 * f1 / (n1 / 3 + 1)) * (1 - math.pow(f0 / f1, n1 / 3 + 1))
    a2 = s1 * (f2 - f1)
    if n2 == -3:
        a3 = 2.3 * s1 * f2 * math.log10(f3 / f2)
    else:
        a3 = (s1 * f2 / (-1 * n2 / 3 - 1)) * (1 - math.pow(f2 / f3, -1 * n2 / 3 - 1))
    a = a1 + a2 + a3
    rms = math.sqrt(a)
    return s0, s2, rms


def rand_rms2amp(rms):  # rms to amp_g2hz
     g2amp = 1.02 * pow(rms, 2) / 1980
     return g2amp


def rand_g2mm(f, amp_g2hz):  # amp_g2hz to amplitude(mm)
     amp = 1067 * pow(amp_g2hz / pow(f, 3), 1 / 2)
     return amp


def shock_vib(n, f, amp_g):  # shock vibration curve   N up_rate
    f0, f1 = f[0], f[1]
    s = amp_g
    s3 = s * math.pow((f0 / f1), n / (20 * math.log10(2)))
    return s3


def sin_amp2g(f, amp):  # calculate acceleration(g) based on frequency and amplitude(mm)
    """
    :param f: freq
    :param amp: unit mm
    :return: acc unit g
    """
    g = 9.8
    if type(f) == type(1):  # single value
        a = 1e-3 * amp * pow(2 * math.pi * f, 2) / g
    else:
        n = len(f)  # frequency array
        a = []
        for i in range(n):
            a.insert(i - 1, 1e-3 * amp * pow(2 * math.pi * f[i - 1], 2) / g)
    return a


def sin_g2amp(f, acc):  # calculate amplitude(mm) based on frequency and acceleration(g)
    """
    :param f: freq
    :param acc: unit g
    :return: aamp unit mm
    """
    g = 9.8
    if type(f) == type(1):  # single value
        amp = 1e3 * acc * g / pow(2 * math.pi * f, 2)
    else:
        n = len(f)  # frequency array
        amp = []
        for i in range(n):
            amp.insert(i - 1, 1e3 * acc * g * pow(2 * math.pi * f[i - 1], 2))
    return amp


def db_oct(f, amp_g2hz):  # calculate db/oct
    f1, f2 = f[0], f[1]
    s0, s1 = amp_g2hz[0], amp_g2hz[1]
    n = math.log10(f2 / f1) / math.log10(2)
    dboct = 10 * math.log10(s1 / s0) / n
    return dboct


def oct_cal(f):  # calculate oct
    f1, f2 = f[0], f[1]
    oct = math.log10(f2 / f1) / math.log10(2)
    return oct


def freq_cal(k, m):  # calculate natural frequency
    freq = pow(k / m, 1 / 2) / (2 * math.pi)
    return freq


def angle2rad(angle):  # degree to rad
    rad = angle * math.pi / 180
    return rad


def rad2angle(rad):  # rad to degree
    angle = rad * 180 / math.pi
    return angle


def mag2db(mag, options="amplitude"):  # power 10, voltage 20
    if options == "amplitude":
        mag = pow(mag, 2)
    else:
        mag = mag
    db = 10 * math.log10(mag)
    return db


def db2mag(db, options="amplitude"):
    if options == "amplitude":
        db = db / 20
    else:
        db = db / 10
    mag = math.pow(10, db)
    return mag


def sign(x):  # sign function
    if x == 0:
        y = 0
    else:
        y = x / abs(x)
    return y


def rotate_axis(x, y, theta, options="counterclockwise"):  # position after axis rotation
    theta = angle2rad(theta)
    if options == "clockwise":
        theta = -theta
    else:
        theta = theta
    x1 = x * math.cos(theta) + y * math.sin(theta)
    y1 = -x * math.sin(theta) + y * math.cos(theta)
    return x1, y1


def fst(x1, x2, delta, dt):  # function for derivation tracker
    d = delta * dt
    d0 = dt * d
    y = x1 + dt * x2
    a0 = math.sqrt(d ** 2 + 8 * delta * abs(y))
    if abs(y) > d0:
        a = x2 + 0.5 * (a0 - d) * sign(y)
    else:
        a = x2 + y / dt
    if abs(a) > d:
        f = -delta * sign(a)
    else:
        f = -delta * a / d
    return f


def d_tracker(v, r1_1, r2_1, delta, dt):  # derivation tracker
    r1 = r1_1 + dt * r2_1
    r2 = r2_1 + dt * fst(r1_1 - v, r2_1, delta, dt)
    return r1, r2


def rw_txt_econ(filedir_old,filedir_new):
    """
    delete invalid row of econ file and save a new one
    :param filedir_old:
    :param filedir_new:
    :return: none
    """
    filenames = os.listdir(filedir_old)
    for name in filenames:
        data_econ = []
        filepath = filedir_old+'/'+name
        with open(filepath,'r')as file:
            line=file.readlines()
            counts=18
            while counts<len(line):
                line[counts]=line[counts].strip('\n')
                data_econ.append(line[counts])
                counts+=1
            filepath_new = filedir_new + '/' + name
            np.savetxt(filepath_new, data_econ, '%s')
    return 0