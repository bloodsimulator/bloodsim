'''
THIS IS THE LUMPED PARAMETER MODEL OF THE HEART WHICH IS TO BE GIVEN AS THE INPUT TO THE
ARTERY MODEL

The side functions are dfined first and the main function where the simulation
is done is described last

'''
# Importing the necessary library files
import numpy as np

valve, Aav, Amv, Apv, Atv, Gpw = np.zeros(6)
E_cardiopul, Elaa, Elab, Elva, Elvb, Eraa, Erab, Erva, Ervb, Epua, Epuc, Epuv, Epwa, Epwc, Epwv=np.zeros(15)
yL_cardiopul, yav, ymv, ypv, ytv, ypua, ypuc, ypuv, ypwa, ypwc, ypwv=np.zeros(11)
R_cardiopul, Ra, Raa, Rav, Rca, Rda, Rmv, Rpua, Rpuc, Rpuv, Rpv, Rpwa, Rpwc, Rpwv, Rtv, Rv, Rvc, bav, bmv, bpv, btv=np.zeros(21)
S_cardiopul, Spua, Spuc, Spuv, Spwa, Spwc, Spwv=np.zeros(7)
Z_cardiopul, Zpua, Zpuc, Zpuv, Zpwa, Zpwc, Zpwv=np.zeros(7)
C_peripheral, Caor, Cart, Ccap, Cven, Cvca=np.zeros(6)
yL_peripheral, yaor, yart, ycap, yven, yvca=np.zeros(6)
R_peripheral, Raor, Rart, Rcap, Rv, Rvc=np.zeros(6)
S_peripheral, Saor, Sart, Scap, Sven, Svca=np.zeros(6)
sdvsdqdvdq, dvq, P_0d=np.zeros(3)
dvdq_cardiopul, dv, v, dq, q=np.zeros(5)
cardiac_parameter, elv, ela, erv, era, cklr, ckrl, plv, prv, Sla, Slv, Sra, Srv, ppp, ppc, pit, qco, FL, FR1, STR=np.zeros(20)
R_cardiopulc, Rav0, Rmv0, Rpv0, Rtv0, bav0, bmv0, bpv0, btv0, Rav1, Rmv1, Rpv1, Rtv1, bav1, bmv1, bpv1, btv1=np.zeros(17)
Rav2, Rmv2, Rpv2, Rtv2, bav2, bmv2, bpv2, btv2, yav0, ymv0, ypv0, ytv0, yav1, ymv1, ypv1, ytv1, yav2, ymv2, ypv2, ytv2=np.zeros(20)
n_val, m_cvst, m_cvrg, n_vrg=np.zeros(4)
timestep, Tduration, ddt, tee, tcr, tac, tar, t, odic=np.zeros(9)


# MAIN FUNCTION TO SOLVE THE SYSTEM OF ODEs
def lumped(HR, ncyc, dt, *param):
    
    def Integrated_ode():
        global Aav, Amv, Apv, Atv, Gpw
        global Epua, Epuc, Epuv, Epwc, Epwv
        global yav, ymv, ypv, ytv, ypua, ypuc, ypuv, ypwa, ypwc, ypwv
        global Rav, Rmv, Rpua, Rpuc, Rpuv, Rpv, Rpwc, Rpwv, Rtv, bav, bmv, bpv, btv
        global Spua, Spuc, Spuv, Spwc, Spwv
        global Zpua, Zpuc, Zpuv, Zpwc, Zpwv
        global Caor, Cart, Ccap, Cven, Cvca
        global yaor, yart, ycap, yven, yvca
        global Raor, Rart, Rcap, Rv, Rvc
        global Saor, Sart, Scap, Sven, Svca
        global dvq, P_0d
        global dv, v, q
        global ela, era
        global plv, prv, Sla, Slv, Sra, Srv, ppc, pit, qco, Tduration, ddt, tcr
        dvq[0, 0] = q[0, 14] - q[0, 0]  # Venous volume  dvq(1)= q(15) - q(1);
        P_0d[0, 0] = v[0, 0] / Cven + Sven * dv[0, 0]  # Venous  Pressure
        dvq[0, 1] = (v[0, 0] / Cven + Sven * dv[0, 0] - Rv * q[0, 0] - v[0, 1] / Cvca - Svca * dv[
            0, 1]) / yven  # Venous flow
        dvq[0, 2] = q[0, 0] - q[0, 1]  # VC volume
        P_0d[0, 1] = v[0, 1] / Cvca + Svca * dv[0, 1]  # VC Pressure
        dvq[0, 3] = (v[0, 1] / Cvca - era * v[0, 2] - Rvc * q[0, 1] + Svca * dv[0, 1] - Sra * dv[
            0, 2] - ppc - pit) / yvca  # VC Flow
        qco = 0.0
        dvq[0, 4] = q[0, 1] + qco - q[0, 2]  # RA volume
        P_0d[0, 3] = era * v[0, 2] + Sra * dv[0, 2] + ppc + pit  # RA pressure
        dvq[0, 5] = (era * v[0, 2] - prv - Rtv * q[0, 2] - btv * q[0, 2] * np.abs(q[0, 2]) + Sra * dv[0, 2] - Srv * dv[
            0, 3]) / ytv  # TV flow
        dvq[0, 6] = q[0, 2] - q[0, 3]  # RV volume
        P_0d[0, 5] = prv + Srv * dv[0, 3] + ppc + pit  # RV pressure
        dvq[0, 7] = (prv - Epua * Zpua - Rpv * q[0, 3] - bpv * q[0, 3] * (np.abs(q[0, 3])) + Srv * dv[0, 3] - Spua * dv[
            0, 4] + ppc) / ypv  # PV flow
        dvq[0, 8] = q[0, 3] - q[0, 4] - q[0, 7]  # Pulmonary Artery volume
        P_0d[0, 7] = Epua * Zpua + Spua * dv[0, 4] + pit  # Pulmonary Artery Pressure
        dvq[0, 9] = (Epua * Zpua - Epuc * Zpuc - Rpua * q[0, 4] + Spua * dv[0, 4] - Spuc * dv[
            0, 5]) / ypua  # Pulmonary Artery Flow
        dvq[0, 10] = q[0, 4] - q[0, 5]  # Pulmonary Capillary volume
        P_0d[0, 9] = Epuc * Zpuc + Spuc * dv[0, 5] + pit  # Pulmonary Capillary Pressure
        dvq[0, 11] = (Epuc * Zpuc - Epuv * Zpuv - Rpuc * q[0, 5] + Spuc * dv[0, 5] - Spuv * dv[
            0, 6]) / ypuc  # Pulmonary Capillary Flow
        dvq[0, 12] = q[0, 5] - q[0, 6]  # Pulmonary Vein volume
        P_0d[0, 11] = Epuv * Zpuv + Spuv * dv[0, 6] + pit  # Pulmonary Vein Pressure
        dvq[0, 13] = (Epuv * Zpuv - ela * v[0, 9] - Rpuv * q[0, 6] + Spuv * dv[0, 6] - Sla * dv[
            0, 9] - ppc) / ypuv  # Pulmonary Vein flow
        if Gpw > 0:
            dvq[0, 14] = (Epua * Zpua - Epwc * Zpwc - q[0, 7] / gpw + Spua * dv[0, 4] - Spwc * dv[
                0, 7]) / ypwa  # Pulmonary Wedge ##Artery flow
        else:
            dvq[0, 14] = 0
        dvq[0, 15] = q[0, 7] - q[0, 8]  # Pulmonary Wedge capillary volume
        P_0d[0, 14] = Epwc * Zpwc + Spwc * dv[0, 7] + pit  # Pulmonary Wedge capillary Pressure
        dvq[0, 16] = (Epwc * Zpwc - Epwv * Zpwv - Rpwc * q[0, 8] + Spwc * dv[0, 7] - Spwv * dv[
            0, 8]) / ypwc  # Pulmonary Wedge capillary Flow
        dvq[0, 17] = q[0, 8] - q[0, 9]  # Pulmonary Wedge vein Volume
        P_0d[0, 16] = Epwv * Zpwv + Spwv * dv[0, 8] + pit  # Pulmonary Wedge vein Pressure
        dvq[0, 18] = (Epwv * Zpwv - ela * v[0, 9] - Rpwv * q[0, 9] + Spwv * dv[0, 8] - Sla * dv[
            0, 9] - ppc) / ypwv  # Pulmonary Wedge vein Flow
        dvq[0, 19] = q[0, 6] + q[0, 9] - q[0, 10]  # LA volume
        P_0d[0, 18] = ela * v[0, 9] + Sla * dv[0, 9] + ppc + pit  # LA Pressure
        dvq[0, 20] = (ela * v[0, 9] - plv - Rmv * q[0, 10] - bmv * q[0, 10] * np.abs(q[0, 10]) + Sla * dv[0, 9] - Slv *
                      dv[0, 10]) / ymv  # Mitral flow
        dvq[0, 21] = q[0, 10] - q[0, 11]  # LV volume
        P_0d[0, 20] = plv + Slv * dv[0, 10] + ppc + pit  # LV Pressure
        dvq[0, 22] = (plv - v[0, 11] / Caor - Rav * q[0, 11] - (bav * q[0, 11]) * np.abs(q[0, 11]) + Slv * dv[
            0, 10] - Saor * dv[0, 11] + ppc + pit) / yav  # Aortic Flow
        # Adjust the state of cardiac valve
        if Aav == 0.0 and q[0, 11] <= 0.000000001:
            dvq[0, 22] = 0.0
        if np.abs(tcr - Tduration) <= ddt * 0.5 or tcr < 0.1 or (Amv == 0.0 and q[0, 10] < 0.000000001):
            dvq[0, 20] = 0.0
        if Apv == 0.0 and q[0, 3] <= 0.00000001:
            dvq[0, 7] = 0.0
        if np.abs(tcr - Tduration) <= ddt * 0.5 or tcr < 0.1 or (Atv == 0.0 and q[0, 2] <= 0.000000001):
            dvq[0, 5] = 0.0
        dvq[0, 23] = q[0, 11] - q[0, 12]  # Aorta volume
        P_0d[0, 22] = v[0, 11] / Caor + Saor * dv[0, 11]  # Aorta Presuure
        dvq[0, 24] = (v[0, 11] / Caor + Saor * dv[0, 11] - q[0, 12] * Raor - v[0, 12] / Cart - Sart * dv[
            0, 12]) / yaor  # Aorta Flow
        dvq[0, 25] = q[0, 12] - q[0, 13]  # Artery Volume
        P_0d[0, 24] = v[0, 12] / Cart + Sart * dv[0, 12]  # Artery Pressure
        dvq[0, 26] = (v[0, 12] / Cart + Sart * dv[0, 12] - q[0, 13] * Rart - v[0, 13] / Ccap - Scap * dv[
            0, 13]) / yart  # Artery Flow
        dvq[0, 27] = q[0, 13] - q[0, 14]  # Capillarya Volume
        P_0d[0, 26] = v[0, 13] / Ccap + Scap * dv[0, 13]  # Capillary Pressure
        dvq[0, 28] = (v[0, 13] / Ccap + Scap * dv[0, 13] - q[0, 14] * Rcap - v[0, 0] / Cven - Sven * dv[
            0, 0]) / ycap  # Capillary Pressure
    
    def Ecal(EEE, ZZZ, vol):
        EcalR = EEE * np.exp(vol / ZZZ)
        return EcalR
    
    def Lvecal():
        global Elva, Elvb
        global elv, FL
        global tee, tcr
        tcal = tcr
        if tcal <= tee:
            elv = FL * Elva * 0.5 * (1.0 - np.cos(3.1415926 * tcal / tee)) + Elvb / FL
        else:
            if tcal <= 1.5 * tee:
                elv = FL * Elva * 0.5 * (1.0 + np.cos(3.1415926 * (tcal - tee) / (0.5 * tee))) + Elvb / FL
            else:
                elv = Elvb / FL
    
    def Laecal():
        global tcr, ela, Elaa, tac, tar, Tduration, Elab
        tcal = tcr
        teec = tar - tac
        teer = teec
        tap = tar + teer - Tduration
        if (tcal >= 0.0 and tcal <= tap):
            ela = Elaa * 0.5 * (1.0 + np.cos(3.1415926 * (tcal + Tduration - tar) / teer)) + Elab
        if (tcal > tap and tcal <= tac):
            ela = Elab
        if (tcal > tac and tcal <= tar):
            ela = Elaa * 0.5 * (1.0 - np.cos(3.1415926 * (tcal - tac) / teec)) + Elab
        # c if (tcal > tar. and.tcal <= (tar+teer)) then
        if (tcal > tar and tcal <= Tduration):
            ela = Elaa * 0.5 * (1.0 + np.cos(3.1415926 * (tcal - tar) / teer)) + Elab
    
    def Rvecal():
        global tcr, FR1, Erva, tee, Ervb
        global erv
        tcal = tcr
        if tcal <= tee:
            erv = FR1 * Erva * 0.5 * (1.0 - np.cos(3.1415926 * tcal / tee)) + Ervb / FR1
        else:
            if tcal <= 1.5 * tee:
                erv = FR1 * Erva * 0.5 * (1.0 + np.cos(2.0 * 3.1415926 * (tcal - tee) / tee)) + Ervb / FR1
            else:
                erv = Ervb / FR1
    
    def Raecal():
        global Eraa, Erab
        global tar, tac, tcr
        global era, Tduration
        teec = tar - tac
        teer = teec
        tcal = tcr
        tap = tar + teer - Tduration
        if 0 <= tcal <= tap:
            era = Eraa * 0.5 * (1.0 + np.cos(3.1415926 * (tcal + Tduration - tar) / teer)) + Erab
        if tap < tcal <= tac:
            era = Erab
        if tcal > tac and tcal <= tar:
            era = Eraa * 0.5 * (1.0 - np.cos(3.1415926 * (tcal - tac) / teec)) + Erab
        if tcal > tar and tcal <= Tduration:
            era = Eraa * 0.5 * (1.0 + np.cos(3.1415926 * (tcal - tar) / teer)) + Erab
    
    def AAav():
        global Caor, dv, v
        global plv, Slv, ppc
        intee = plv + Slv * dv[0, 10] + ppc - v[0, 11] / Caor
        if intee > 0.0:
            AAav = 4.0
        else:
            AAav = 0.0
        return AAav
    
    def AAmv():
        global v, ela, plv
        intee = ela * v[0, 9] - plv
        if intee > 0.0:
            AAmv = 4.0
        else:
            AAmv = 0.0
        return AAmv
    
    def AApv():
        global Epua, Zpua, prv
        intee = prv - Epua * Zpua
        if intee > 0.0:
            AApv = 4.0
        else:
            AApv = 0.0
        return AApv
    
    def AAtv():
        global era, v, prv
        intee = era * v[0, 2] - prv
        if intee > 0.0:
            AAtv = 4.0
        else:
            AAtv = 0.0
        return AAtv
    
    def cardiac_state(subresultcr):
        global Aav, Amv, Apv, Atv, dvq
        global dv, v, dq, q, ddt
        # call Integrated_ode % == == == == == = make a note........................
        Integrated_ode()
        # Declaration of variables
        dfl = np.zeros(shape=(2, 30))
        dq = np.zeros(shape=(2, 15))
        subrukuk = np.zeros(shape=(4, 29))
        inter = np.zeros(shape=(2, 29))
        newpara = np.zeros(shape=(2, 29))
        # -------------------------------------------------------------------------
        dfl[0, :29] = dvq[0, :29]
        dq[0, :7] = dfl[0, 1:14:2]
        dq[0, 7:15] = dfl[0, 14:29:2]
        dv[0, :7] = dfl[0, 0:13:2]
        dv[0, 7:14] = dfl[0, 15:28:2]
        for nrk in range(4):
            subrukuk[nrk, :29] = np.multiply(ddt, dfl[0, :29])
            if nrk == 0:
                Aav = AAav()
                Amv = AAmv()
                Apv = AApv()
                Atv = AAtv()
            if nrk < 3:
                inter[0, :29] = np.multiply(0.5, subrukuk[nrk, 0:29])
            else:
                inter[0, :29] = subrukuk[nrk, 0:29]
        inter[0, :29] = np.multiply(0.5, subrukuk[nrk, 0:29])
        newpara[0, 0:29] = np.add(subresultcr[0, 0:29], inter[0, 0:29])
        q[0, :7] = newpara[0, 1:14:2]
        q[0, 7:15] = newpara[0, 14:29:2]
        v[0, :7] = newpara[0, 0:13:2]
        v[0, 7:14] = newpara[0, 15:28:2]
        return subrukuk
    # End of function definition ----------------------------------
    
    global Aav, Amv, Apv, Atv, Gpw                        # valve, 
    global Elaa, Elab, Elva, Elvb, Eraa, Erab, Erva, Ervb, Epua, Epuc, Epuv, Epwa, Epwc, Epwv # E_cardiopul,
    global yav, ymv, ypv, ytv, ypua, ypuc, ypuv, ypwa, ypwc, ypwv # yL_cardiopul,
    global Ra, Raa, Rav, Rca, Rda, Rmv, Rpua, Rpuc, Rpuv, Rpv, Rpwa, Rpwc, Rpwv, Rtv, Rv, Rvc, bav, bmv, bpv, btv # R_cardiopul,
    global Spua, Spuc, Spuv, Spwa, Spwc, Spwv            # S_cardiopul,
    global  Zpua, Zpuc, Zpuv, Zpwa, Zpwc, Zpwv           # Z_cardiopul,
    global  Caor, Cart, Ccap, Cven, Cvca                 #
    global  yaor, yart, ycap, yven, yvca                 # yL_peripheral,
    global  Raor, Rart, Rcap, Rv, Rvc                    # R_peripheral,
    global  Saor, Sart, Scap, Sven, Svca                 # S_peripheral,
    global  dvq, P_0d                                    # sdvsdqdvdq
    global  dv, v, dq, q                                 # dvdq_cardiopul,
    global  elv, ela, erv, era, cklr, ckrl, plv, prv, Sla, Slv, Sra, Srv, ppp, ppc, pit, qco, FL, FR1, STR # cardiac_parameter,
    global  Rav0, Rmv0, Rpv0, Rtv0, bav0, bmv0, bpv0, btv0, Rav1, Rmv1, Rpv1, Rtv1, bav1, bmv1, bpv1, btv1 # R_cardiopulc,
    global Rav2, Rmv2, Rpv2, Rtv2, bav2, bmv2, bpv2, btv2, yav0, ymv0, ypv0, ytv0, yav1, ymv1, ypv1, ytv1, yav2, ymv2, ypv2, ytv2#
    global n_val, m_cvst, m_cvrg, n_vrg
    global timestep, Tduration, ddt, tee, tcr, tac, tar, t, odic
    
    v = np.zeros(shape=(2, 14))
    q = np.zeros(shape=(2, 21))
    dvq = np.zeros(shape=(2, 29))
    result = np.zeros(shape=(2, 101))
    P_0d = np.zeros(shape=(2, 101))
    diffv = np.zeros(shape=(2, 14))
    resultcr = np.zeros(shape=(2, 101))
    dv = np.zeros(shape=(2, 21))
    MyResult = np.zeros(shape=(100000, 28))
    MyResult1 = np.zeros(shape=(100000, 29))
    # initial values of all state equations (should be equal to number of equations in dvdqsdvdq.m file)
    odic = np.array(
        [1068.2371, 52.4983, 181.7233, -41.7618, 65.0625, 0, 122.6637, 0, 67.0272, -0.3118, 135.1100, -2.1737, 198.7568,
         -64.1791, 0, 2.7983, 0.1357, 2.7932, 1.1042, 68.8587, 0, 121.2539, 0, 67.3641, 41.8262, 22.0472, 56.6627,
         1.8539, 57.6473])
    Pit = -2.5
    pit = Pit
    jj = 0
    # --------------------------------------------------------------------------------
    br = param[0]
    cmp = param[1]
    ela = param[2]
    ind = param[3]
    res = param[4]
    ve = param[5]
    
    Elva = ela[10]                         # !Peak-systolic elastance of left ventricle
    Elvb = ela[3]                          # !Basic diastolic elastance of left ventricle
    Elaa = ela[8]                          # !Peak-systolic elastance of left atrium
    Elab = ela[9]                          # !Basic diastolic elastance of left atrium
    Erva = ela[6]                          # !Peak-systolic elastance of right ventricle
    Ervb = ela[7]                          # !Basic diastolic elastance of right ventricle
    Eraa = ela[4]                          # !Peak-systolic elastance of right atrium
    Erab = ela[5]                          # !Basic diastolic elastance of right atrium
    Vmax = 900                             # Reference volume of Frank-Starling law
    Es = 45.9                              # !Effective septal elastance
    Vpc0 = 380.0                           # !Reference total pericardial and cardiac volume old value 380
    Vpe = 30.0                             # !Pericardial volume of heart
    Vcon = 40.0                            # !Volume constant
    Sva0 = 0.0005                          # !Coefficient of cardiac viscoelasticity
    # Cardiac valve parameters
    # (aortic valve(AV),mitral valve(MV), tricuspid valve(TV),pulmonary valve(PV))
    bav = br[2]                            # !Bernoulli's resistance of AV
    bmv = br[0]                            # !Bernoulli's resistance of MV
    btv = br[3]                            # !Bernoulli's resistance of TV
    bpv = br[1]                            # !Bernoulli's resistance of PV
    Rav = res[8]                           # !Viscous resistance of AV
    Rmv = res[7]                           # !Viscous resistance of MV
    Rtv = res[2]                           # !Viscous resistance of TV
    Rpv = res[3]                           # !Viscous resistance of PV
    yav = ind[8]                           # !Inertance of AV
    ymv = ind[7]                           # !Inertance of MV
    ytv = ind[2]                           # !Inertance of TV
    ypv = ind[3]                           # !Inertance of PV
    #  Pulmonary circulation
    Epua0 = ela[1]
    Epuc0 = ela[2]
    Epuv0 = ela[0]
    Epwc0 = 0.7000
    Epwv0 = 0.7000
    Rpua = res[1]
    Rpuc = res[2]
    Rpuv = res[3]
    Rpwa = 0.0005
    Rpwc = 0.4
    Rpwv = 0.4
    ypua = ind[4]
    ypuc = ind[5]
    ypuv = ind[6]
    ypwa = 0.0005
    ypwc = 0.0005
    ypwv = 0.0005
    Zpua = 20.0
    Zpuc = 60.0
    Zpuv = 200.0
    Zpwa = 1.0
    Zpwc = 1.0
    Zpwv = 1.0
    Spua = ve[4]
    Spuc = ve[5]
    Spuv = ve[6]
    Spwa = 0.01
    Spwc = 0.01
    Spwv = 0.01
    #  Peripheral circulation
    Caor = cmp[2]
    Cart = cmp[1]
    Ccap = cmp[0]
    Cven = cmp[4]
    Cvca = cmp[3]
    yaor = ind[9]
    yart = 0.05
    ycap = ind[10]
    yven = ind[0]
    yvca = ind[1]
    Raor = res[9]
    Rart = 0.8
    Rcap = res[10]
    Rv = res[0]
    Rvc = res[1]
    Saor = ve[9]
    Sart = 0.01
    Scap = ve[10]
    Sven = ve[0]
    Svca = ve[1]
    qco = 0.0
    # ------------------------------------------------------------------------------------------------
    HR = HR
    Tduration = 60 / HR                                # input('Please specify cardiac duration(s)')
    dt = dt                                            # input'Please specify time step(s)')
    ncycle = ncyc
    tee = 0.3 * np.sqrt(Tduration)                     # !Moment when ventricular contractility reaches the peak
    tac = Tduration - 0.5 * tee - 0.02 * (
            Tduration / 0.855)                         # !Moment when atrium begins to contract
    tar = Tduration - 0.02 * (Tduration / 0.855)       # !Moment when atrium begins to relax
    ddt = dt
    ntotal = (ncycle * Tduration / dt)
    ntotal = int(ntotal)
    # ------------------------------------------------------------------------
    for nstep in range(ntotal):
        if nstep == 0:
            tcr = 0.0
            ppc = 0.0
            cn = 0
            for i in range(29):
                result[0, i] = odic[i]
            for i in np.arange(14):
                if i <= 6:
                    v[0, i] = result[0, 2 * i]
                else:
                    v[0, i] = result[0, 2 * i + 1]
            for i in np.arange(15):
                if i <= 6:
                    q[0, i] = result[0, 2 * i + 1]
                else:
                    q[0, i] = result[0, 2 * i]
            STR = 1.0
            FL = 1.0
            FR1 = 1.0
            Gpw = 0.0
            Aav = 0.0
            Amv = 0.0
            Apv = 0.0
            Atv = 0.0
            Pit = -2.5
        # ----------------------Start computation---------------------------
        ncount = 0
        ncountadd = ncount + 1
        cn += 1
        tcr = cn * dt % Tduration
        t = cn * dt
        # c.... Compute the pulmonary elastances
        Epua = Ecal(Epua0, Zpua, v[0, 4])
        Epuc = Ecal(Epuc0, Zpuc, v[0, 5])
        Epuv = Ecal(Epuv0, Zpuv, v[0, 6])
        Epwc = Ecal(Epwc0, Zpwc, v[0, 7])
        Epwv = Ecal(Epwv0, Zpwv, v[0, 8])
        # c.....Update nolinear cardiac parameters
        if tcr == 0.0:
            FL = 1.0 - (result[0, 21] / Vmax)        # Left ventricle scaling factor
            FR1 = 1.0 - (result[0, 6] / Vmax)        # Right ventricle scaling factor
        Lvecal()                                     # LV elastance function calling
        Laecal()                                     # LA elastance function calling
        Rvecal()                                     # RV elastance function calling
        Raecal()                                     # RA elastance function calling
        # Spetum cross talk pressure calculations
        cklr = erv / (Es + erv)
        ckrl = elv / (Es + elv)
        plv = ckrl * Es * v[0, 10] + ckrl * cklr * Es * v[0, 3] / (1.0 - cklr)
        prv = cklr * Es * v[0, 3] + ckrl * cklr * Es * v[0, 10] / (1.0 - ckrl)
        # All cardiac chambers viscoelastance calculation
        Sla = Sva0 * v[0, 9] * ela
        Slv = Sva0 * plv
        Sra = Sva0 * v[0, 2] * era
        Srv = Sva0 * prv
        # Pericardium pressure calculations
        ppp = (v[0, 2] + v[0, 3] + v[0, 9] + v[0, 10] + Vpe - Vpc0) / Vcon
        ppc = np.exp(ppp)
        # c....Update dv and state equation function calling
        Integrated_ode()  # = == == == == == == == == == == == == == = >> make a note.............................
        diffv[0, :7] = dvq[0, 0:13:2]
        diffv[0, 7:14] = dvq[0, 15:28:2]
        dv[0, :14] = diffv[0, :14]
        # c.....Implement fourth - order Runge - Kutta method
        resultcr[0, :101] = result[0, :101]
        rukuk = cardiac_state(resultcr)
        # c.....Update variables with Runge-Kutta method
        for j in np.arange(29):
            result[ncountadd, j] = result[ncount, j] + (
                    rukuk[0, j] + 2.0 * (rukuk[1, j] + rukuk[2, j]) + rukuk[3, j]) / 6.0
        delta = 0.00000001
        # update all four cardiac valve flow as zero when they were closed
        if Aav == 0.0 and resultcr[0, 22] <= delta:
            resultcr[0, 22] = 0.0
            result[ncountadd, 22] = 0.0
            q[0, 11] = 0.0
        if np.abs(tcr - Tduration) <= ddt * 0.5 or tcr < 0.1 or (Amv == 0.0 and resultcr[0, 20]) <= delta:
            resultcr[0, 20] = 0.0
            resultcr[ncountadd, 20] = 0.0
            q[0, 10] = 0.0
        if (Apv == 0.0) and (resultcr[0, 7] <= delta):
            resultcr[0, 7] = 0.0
            resultcr[ncountadd, 7] = 0.0
            q[0, 3] = 0.0
        if np.abs(tcr - Tduration) <= ddt * 0.5 or tcr < 0.1 or Atv == 0.0 and resultcr[0, 5] <= delta:
            resultcr[0, 5] = 0.0
            result[ncountadd, 5] = 0.0
            q[0, 2] = 0.0
        # c.....Update q() and v() to be used at next time
        v[0, :7] = result[ncountadd, 0:13:2]
        v[0, 7:14] = result[ncountadd, 15:28:2]
        q[0, : 7] = result[ncountadd, 1:14:2]
        q[0, 7: 15] = result[ncountadd, 14:29:2]
        q[0, 15: 21] = result[ncountadd, 29:35:1]
        result[0, :29] = result[1, :29]
        # load calculated hemodynamic variables in an array
        jj += 1
        # print('Value of JJ:', jj - 1)
        MyResult[jj - 1, :27] = P_0d[0, :27]
        MyResult1[jj - 1, :29] = result[0, :29]
        # Update the initial conditions for next cardiac cycle
        if nstep + 1 == ntotal:
            odic_new = result[0, :29]
    t = np.arange(0, 4.8, dt)
    T = t
    return MyResult1, T


if __name__ =="__main__":
    import time
    import matplotlib.pyplot as plt
    st = time.time()
    heart_br_para = [0.000016,0.000025, 0.000025, 0.000016]
    heart_cmp_para = [0.06, 0.3, 0.9, 30.0, 100.0]
    heart_ela_para = [0.0200,0.0200, 0.0200, 0.06, 0.055, 0.06, 0.52, 0.043, 0.07, 0.075, 2.87]
    heart_ind_para = [0.0005,0.0005,0.0002, 0.0005,0.005, 0.0005,
                            0.0005, 0.0002, 0.0005, 0.015, 0.0005]
    heart_res_para = [0.001, 0.07, 0.005, 0.005, 0.04, 0.04,
                                0.005, 0.005, 0.005, 0.08, 0.35]
    heart_ve_para = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01,
                                0.01, 0.01, 0.01, 0.01, 0.01]
    cda_dat = [ heart_br_para, heart_cmp_para, heart_ela_para, heart_ind_para, heart_res_para, heart_ve_para ]
    try:
        x, t = lumped(70, 5, 0.00015,*cda_dat)
    except Exception as e:
        print(str(e))
    end = time.time()
    print('Total time: ',(end-st))
    total = len(t)
    plt.plot(t, x[:total, 20])
    plt.show()