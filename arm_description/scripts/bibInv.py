#!/usr/bin/env python
# Dieser Skript dient dazu, die Gelenkenposition fuer die entsprechend eingegebene Koordinaten zu berechnen.
import math
import numpy as np
def calc_inv_kin(pose):
    # Konstante (Laenge der Gelenken) [mm]
    l1 = 26
    l2 = 76
    l3 = 47
    l45= 103

    # Die erwuenschte Pose des Endeffektors:
    # [x, y, z, x, y, z], [mm, mm, mm, rad, rad, rad]
    pose = np.array([120, 0, 120, 0, 0, 0])
    x_ref =  np.array([[pose[0]], [pose[1]], [pose[2]]])
    # Definition np.arrayvon "Ellbogen" und "Handgelenk"
    elbow=-1 # 1: Ellbogen nach oben, -1: Ellbogen nach unten
    wrist=1 # 1: Handgelenk nach oben, -1: Handgelenk nach unten

    # theta 1= atan2(y5, x5)
    th1 = math.atan2(pose[1], pose[0]) 
    s1 = math.sin(th1)
    c1 = math.cos(th1)

    # Berechnung der z Axis des Endeffektors [3x1]
    Rx = np.array([[1, 0, 0], [0, c1, -s1], [0, s1, c1]])
    Ry = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    Rz = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
    Rz5 = np.matmul(Ry, Rz)
    Rz5 = np.matmul(Rz5, Rx)

    z5 = np.array([[Rz5[0,2]], [Rz5[1,2]], [Rz5[2,2]]])
    z4 = z5
    # Koordinaten des Handgelenkzentrums
    o0c = np.subtract(x_ref, (l45)*z5)
    # Hilfeparameter
    R = math.sqrt(o0c[0]*o0c[0]+o0c[1]*o0c[1])
    S = float(o0c[2])-l1
    V = math.sqrt(R*R+S*S)

    # theta_3, theta_2
    c3 = (V*V-(l2*l2+l3*l3))/(2*l2*l3)

    th3 = elbow*math.atan2(math.sqrt(1-c3*c3), c3)
    th2 = math.atan2(S,R) - elbow*math.atan2(l3*math.sqrt(1-c3*c3),l2+l3*c3)
    q23 = th2+th3
    s23 = math.sin(q23)
    c23 = math.cos(q23)

    x3 = np.array([[c1*c23], [s1*c23], [s23]])
    y3 = np.array([[-c1*s23], [-s1*c23], [c23]])
    # theta_4
    z4T = z4.T
    th4 = math.atan2(np.matmul(z4T, x3), -np.matmul(z4T, y3))

    # theta_5
    th5 = 0
    # Mappen die berechnete Werte auf din Rviz-Simulator    
    print(th1, th2-3.14/2, th3, th4-3.14/2, th5)

    return_value = np.array([th1, th2-3.14/2, th3, th4-3.14/2, th5])

    return return_value
