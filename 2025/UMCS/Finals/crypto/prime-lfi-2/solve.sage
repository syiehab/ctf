from Crypto.Util.number import long_to_bytes

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)

p = 227297987279223760839521045903912023553
q = 2*p + 1
a = 120959747616429018926294825597988269841 
b = 146658155534937748221991162171919843659

Ep = EllipticCurve(GF(p), [a,b])
G = Ep(17893720394144624190734996627010047306,20616393484923697651758556205781302795)
rG = Ep(19217060046994255110057650585368369910,26446388616238423730513736256805860117)

p1 = SmartAttack(G,rG,p)

Eq = EllipticCurve(GF(q), [a,b])
H = Eq(252930125706437967551140406680743888116, 90401948497758473859433663310741660973)
sH = Eq(54048417678981224995645344071474696337, 70305325112326605006109742214678677722)

p2 = H.discrete_log(sH)

flag = long_to_bytes(p1) + long_to_bytes(p2)

print(flag.decode())


