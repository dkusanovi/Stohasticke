import numpy as np
import matplotlib.pyplot as plt

N1i = 10000      # Sb
N2i = 0          # Te

T_half_1 = 2.5   # 133Sb
T_half_2 = 12.5  # 133Te

lambda1 = np.log(2)/T_half_1
lambda2 = np.log(2)/T_half_2

print(lambda1)
print(lambda2)

def raspad(tmax, dt):
    tlist = [0]

    p1 = lambda1*dt
    p2 = lambda2*dt

    # ako je dt toliko velik da je p veći od 1, onda se sve raspadne u jednom koraku

    N1_list = [N1i]
    N2_list = [N2i]
    N3_list = [0]

    A1_list = [N1i]
    A2_list = [0]
    A3_list = [0]

    N1 = N1i
    N2 = N2i
    N3 = 0

    t = 0
    while t <= tmax:
        N1t = N1
        N2t = N2

        for i1 in range(N1t):
            r1 = np.random.rand()
            if r1 <= p1:
                N1 = N1 - 1
                N2 = N2 + 1

        for i2 in range(N2t):
            r2 = np.random.rand()
            if r2 <= p2:
                N2 = N2 - 1
                N3 = N3 + 1

        t = t + dt
        tlist.append(t)
        N1_list.append(N1)
        N2_list.append(N2)
        N3_list.append(N3)


        # analitički
        A1 = N1i*np.exp(-lambda1*t)
        A2 = N1i*(lambda1/(lambda2 - lambda1)) * (np.exp(-lambda1*t) - np.exp(-lambda2*t))
        A3 = N1i - A1 - A2
        A1_list.append(A1)
        A2_list.append(A2)
        A3_list.append(A3)

    return tlist, N1_list, N2_list, N3_list, A1_list, A2_list, A3_list



def graf():
    tlist, N1_list, N2_list, N3_list, A1_list, A2_list, A3_list = raspad(60, 0.1)[0], raspad(60, 0.1)[1], raspad(60, 0.1)[2], raspad(60, 0.1)[3], raspad(60, 0.1)[4], raspad(60, 0.1)[5], raspad(60, 0.1)[6]

    plt.figure(figsize=(10, 6))
    plt.plot(tlist, N1_list, label='N(133Sb) numerički', color='blue')
    plt.plot(tlist, N2_list, label='N(133Te) numerički', color='magenta')
    plt.plot(tlist, N3_list, label='N(133I) numerički', color='green')
    plt.plot(tlist, A1_list, '--', label='N(133Sb) analitički', color='blue')
    plt.plot(tlist, A2_list, '--', label='N(133Te) analitički', color='magenta')
    plt.plot(tlist, A3_list, '--', label='N(133I) analitički', color='green')
    plt.xlabel('Vrijeme (min)')
    plt.ylabel('Broj jezgara')
    plt.title('Lančani raspad dt = 0.1, t = 60 min')
    plt.grid(True)
    plt.legend()
    plt.show()

graf()

def usporedba():
    tlist1, N1_list1 = raspad(60, 0.2)[0], raspad(60, 0.2)[1]
    tlist2, N1_list2 = raspad(60, 0.5)[0], raspad(60, 0.5)[1]
    tlist3, N1_list3 = raspad(60, 1)[0], raspad(60, 1)[1]
    tlist4, N1_list4 = raspad(60, 2)[0], raspad(60, 2)[1]
    tlist5, N1_list5 = raspad(60, 5)[0], raspad(60, 5)[1]

    plt.figure(figsize=(10, 6))
    plt.plot(tlist1, N1_list1, label='N(133Sb) dt = 0.2')
    plt.plot(tlist2, N1_list2, label='N(133Sb) dt = 0.5')
    plt.plot(tlist3, N1_list3, label='N(133Sb) dt = 1')
    plt.plot(tlist4, N1_list4, label='N(133Sb) dt = 2')
    plt.plot(tlist5, N1_list5, label='N(133Sb) dt = 5')
    plt.xlabel('Vrijeme (min)')
    plt.ylabel('Broj jezgara')
    plt.title('Lančani raspad t = 60 min')
    plt.xlim(0, 6)
    plt.grid(True)
    plt.legend()
    plt.show()




usporedba()


