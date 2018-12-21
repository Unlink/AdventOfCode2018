##Netusim co to robí :)
# 12935354 16777215
# 1282132
# 15814028
# 5768211
# 14303887
# 547815
# 16331450

r0Values = list()

r0 = 0
r5 = 0
while True: #r5 != r0:
    r1 = r5 | 65536             #r1 = 65536
    r5 = 10678677
    
    while True:
        r4 = r1 & 255               #r4 = 0
        r5 = r5 + r4                #r5 = 10678677
        r5 = r5 & 16777215          #r5 = 10678677
        r5 = r5 * 65899             #r5 = 703714135623   or -660500921
        r5 = r5 & 16777215          #r5 = 10587719

        if 256 <= r1:
            r4 = 0
            r3 = 1
            while r3 <= r1:
                r3 = r4 + 1
                r3 = r3 * 256
                r4 = r4 + 1 
            r1 = r4-1
        else:
            break
    print(str(len(r0Values)+1)+":"+str(r5))
    if r5 in r0Values:
        break
    r0Values.append(r5)
