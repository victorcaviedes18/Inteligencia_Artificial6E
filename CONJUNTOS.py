#Conjuntos en python

U = {1,2,3,4,5,6,7,8,9,10,11,12}
A = {1,2,3,10,12}
B = {4,3,5,7,11}
C = {5,14,12,2,8,1}

print('UNIVERSO',U)
print('CONJUNTO A',A)
print('CONJUNTO B',B)
print('CONJUNTO C',C)

#2. Subconjunto .issubset()
print('A ES UN SUBCONJUNTO DE B?',A.issubset(B))

D = A & C
print('EL SUBCONJUNTO DE A Y C ES',D)


#4. Ver superconjunto .union()
J = A | B
print('EL SUPERCONJUNTO DE A Y B ES',J)

#5. Conjunto vacio
#set {}

#6. Complemento
def complemento (a):
    return  U-a

print('EL COMPLEMENTO EN C ES',complemento(C))    
    

#7. Diferencia
DI = A - B
FI = A.difference(B)
print('LA DIFERENCIA DE A Y B ES',FI)

#8. Diferencia Simetrica
print('LA DIFERENCIA SIMETRICA DE A Y C ES',A.symmetric_difference(C))

#9. Producto Cartesiano
def producto_cartesiano(a,b):
    E = set()
    for i in a:
        for j in b:
            E.add((i,j))
        return E

PC = producto_cartesiano(A,B)
print('EL PRODUCTOR CARTESIANO DE A Y B ES',PC)



