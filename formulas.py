import pathlib
from typing import List
from itertools import product

Asignacion = List[bool]

class Formula:
    """
    Clase para representar fórmulas booleanas.
    """
    def __init__(self, izquierda, conectivo = None, derecha = None):
        """
        Constructor para la clase. En el caso de las variables,
        izquierda es el identificador de la variable, debe ser
        un entero, y conectivo y derecha deben ser None. El atributo
        conectivo debe ser un string, 'C'(onjunción), 'D'(isyunción),
        'I'(mplicación), 'N'(egación) o 'B'(icondicional). Para
        cualquier fórmula que no sea una variable, el atributo
        izquierda debe ser una fórmula, y para las fórmulas con
        conectivo distinto a 'N', el atributo derecho también tiene
        que ser una fórmula.
        """
        conectivos=['C','D','I','B','N']
        if (conectivo == None
                and not (isinstance(izquierda, int) and izquierda > -1)):
            raise TypeError("Las variables deben ser naturales")
        elif conectivo != None:
            if not isinstance(izquierda, Formula):
                raise TypeError("Los conectivos deben aplicarse a fórmulas")
            elif (conectivo == 'N' and derecha != None):
                raise TypeError("En la negación no debe existir fórmula derecha")
            elif (conectivo not in conectivos):
                raise ValueError("El conectivo es incorrecto")
            elif (conectivo != 'N' and not isinstance(derecha, Formula)):
                raise TypeError("Los conectivos deben aplicarse a fórmulas")
        self.izquierda = izquierda
        self.conectivo = conectivo
        self.derecha   = derecha

#-----------------------------FUNCIONES PRÁCTICA 1------------------------------
    def __repr__(self):
        """
        Representación en cadena, legible para humanos, de
        las fórmulas.
        """
        if self.conectivo == None:
            variable = 'x{}'.format(repr(self.izquierda))
            return variable
        elif self.conectivo == 'N':
            negacion = "(¬{0})".format(repr(self.izquierda))
            return negacion
        else:
            binaria = "({0} {1} {2})".format(repr(self.izquierda),'{0}',repr(self.derecha))

            if self.conectivo == 'C':
                binaria = binaria.format('∧')
            elif self.conectivo == 'D':
                binaria = binaria.format('∨')
            elif self.conectivo == 'I':
                binaria = binaria.format('→')
            elif self.conectivo == 'B':
                binaria = binaria.format('↔')

            return binaria

    def lista_variables(self):
        """
        Devuelve la lista de todas las variables que ocurren
        en una fórmula, en orden.
        """
        lista = []
        if self.izquierda  == None:
            return lista
        if self.conectivo == None:
            lista.append(self.izquierda)
            lista.sort()
            return lista
        if self.conectivo == 'N':
            return self.izquierda.lista_variables()

        lista2 = self.izquierda.lista_variables() + self.derecha.lista_variables()
        lista2.sort() #ordena la lista
        lista2 = list(dict.fromkeys(lista2)) #elimina elementos repetidos
        return lista2

    def ultima_variable(self):
        """
        Devuelve la última variable que ocurre en una fórmula.
        """
        lista = self.lista_variables()
        return lista.pop()

    def numero_conectivos(self):
        """
        Devuelve el número de conectivos que ocurren en la fórmula.
        """
        if self.conectivo == None:
            return 0
        if self.derecha == None:
            return self.izquierda.numero_conectivos() + 1
        return self.izquierda.numero_conectivos() + self.derecha.numero_conectivos() + 1


    def _evalua_aux(self, asignacion: Asignacion, posiciones: List[int]):
        """
        Función auxiliar para evaluar una fórmula. Recibe una lista de
        booleanos (una asignación de verdad), y una lista con las posiciones
        en las que ocurren las variables de la fórmula.
        """
        if len(asignacion) < len(posiciones):
            raise ValueError("La asignación no cubre todas las variables")
        if self.conectivo == None:
            valor = asignacion[posiciones.index(self.izquierda)]
        else:
            if self.conectivo == 'N':
                valor = 1 - self.izquierda._evalua_aux(asignacion, posiciones)
            elif self.conectivo == 'C':
                valor = (self.izquierda._evalua_aux(asignacion, posiciones))*(self.derecha._evalua_aux(asignacion, posiciones))
            elif self.conectivo == 'D':
                valor = max(self.izquierda._evalua_aux(asignacion, posiciones), self.derecha._evalua_aux(asignacion, posiciones))
            elif self.conectivo == 'I':
                if (self.izquierda._evalua_aux(asignacion, posiciones) and not self.derecha._evalua_aux(asignacion, posiciones)):
                    valor = 0
                else:
                    valor = 1
            elif self.conectivo == 'B':
                valor = 1 - abs(self.izquierda._evalua_aux(asignacion, posiciones) - self.derecha._evalua_aux(asignacion, posiciones))
        return valor

    def evalua(self, asignacion: Asignacion):
        """
        Devuelve el valor de verdad de la fórmula bajo una
        asignación dada, que recibe como entrada en la forma
        de una lista de booleanos.
        """
        posiciones = self.lista_variables()
        return self._evalua_aux(asignacion, posiciones)

    def aplana(self):
        """
        Devuelve una lista con la versión aplanada del árbol
        de sintáxis de la fórmula.
        """
        l = []
        #caso base para variables
        if self.conectivo == None:
            l.append(self)
        #caso para ir por la izquierda primero
        elif self.conectivo == 'N':
            l.extend(self.izquierda.aplana())
            l.append(self)
        #al terminar, ir por la derecha
        else:
            l.extend(self.izquierda.aplana())
            l.append(self)
            l.extend(self.derecha.aplana())
        return l

    def aplana_sin_variables(self):
        """
        Devuelve una lista con la versión aplananada del
        árbol de sintaxis de la fórmula, sin las hojas.
        """
        l = []
        #caso base para variables
        if self.conectivo == None:
            return l
        #caso para ir por la izquierda primero
        elif self.conectivo == 'N':
            l.extend(self.izquierda.aplana_sin_variables())
            l.append(self)
        #al terminar, ir por la derecha
        else:
            l.extend(self.izquierda.aplana_sin_variables())
            l.append(self)
            l.extend(self.derecha.aplana_sin_variables())
        return l

#-----------------------------FUNCIONES PRÁCTICA 2------------------------------
    def _evalua_sub_aux(self,
                        asignacion: Asignacion,
                        posiciones: List[int],
                        resultado):
        """
        Función auxiliar para evaluar a la fórmula y todas sus
        subfórmulas. Recibe como entrada una lista de booleanos
        (asignación de verdad), una lista con las posiciones en
        las que ocurren las variables, y una lista de las subfórmulas
        de la fórmula.   Este método devuelve un diccionario que asocia
        a cada subfórmula su valor de verdad bajo la asignación.
        """
        if len(asignacion) < len(posiciones):
            raise ValueError("La asignacion no cubre a todas las variables")
        if self.conectivo == None:
            resultado[self]= asignacion[posiciones.index(self.izquierda)]
        else:
            self.izquierda._evalua_sub_aux(asignacion, posiciones, resultado)

            if self.conectivo == 'N':
                resultado[self] = 1 - resultado[self.izquierda]
            else:
                self.derecha._evalua_sub_aux(asignacion, posiciones, resultado)

                if self.conectivo == 'C':
                    resultado[self] = (resultado[self.izquierda]*resultado[self.derecha])
                elif self.conectivo == 'D':
                    resultado[self] = max(resultado[self.izquierda], resultado[self.derecha])
                elif self.conectivo == 'I':
                    if (resultado[self.izquierda] and not resultado[self.derecha]):
                        resultado[self] = 0
                    else:
                        resultado[self] = 1
                else:
                    resultado[self] = 1 - abs(resultado[self.izquierda] - resultado[self.derecha])
        return resultado


    def evalua_sub(self, asignacion):
        """
        Recibe como entrada una lista de booleanos (asignación de verdad)
        y devuelve una lista de booleanos; las entradas de esta lista de
        booleanos corresponden con las posiciones de la lista de
        subfórmulas que genera la función aplana.   La finalidad de esta
        función es generar los renglones de la tabla de verdad de esta
        fórmula.   Sólo la primera ocurrencia está evaluada en la lista.
        """
        resultado = {}
        return self._evalua_sub_aux(asignacion,self.lista_variables(), resultado)

    def renglones_verdad(self):
        """
        Devuelve una lista con los renglones de la tabla de verdad de
        la fórmula.   Por diseño, los valores de las variables sólo
        ocurren en las primeras columnas de la tabla de verdad.
        """
        renglones = []
        asignaciones = product([0,1],repeat = len(self.lista_variables))
        for asignacion in asignaciones:
            renglon = list(asignacion)
            renglon.extend(self.evalua_sub(renglon))
            renglones.append(renglon)
        return renglones

    def tex_tabla(self):
        """
        Devuelve la fórmula con los separadores necesarios
        para crear la tabla en LaTeX.
        """
        if self.conectivo == None:
            return f"x_{{{self.izquierda}}}"
        else:
            if self.conectivo  == 'N':
                izquierda = ""
                conectivo = "\\lnot"
                derecha = self.izquierda.tex_tabla()
            else:
                izquierda = self.izquierda.tex_tabla()
                derecha = self.derecha.tex_tabla()
                if self.conectivo == 'C':
                    conectivo = "\\land"
                elif self.conectivo ==  'D':
                    conectivo = "\\lor"
                elif self.conectivo == 'I':
                    conectivo = "\\to"
                else:
                    conectivo = "\\leftrightarrow"

            cabezera = f"({izquierda} & {conectivo} & {derecha})"
            return cabezera

    def _cabecera_tabla(self):
        """
        Devuelve la cabecera de la tabla de verdad en formato
        de tabla de LaTeX.
        """
        cabecera = "  "
        for variable in self.lista_variables():
            cabecera += f"x_{{{variable}}} & "
        cabecera += self.tex_tabla()
        cabecera += " \\\\\n"
        return cabecera

    def _renglon_verdad(self,
                   asignacion):
        """
        Devuelve un renglón de la tabla de verdad de la fórmula,
        en formato de tabla de LaTeX, correspondiente a la
        asignación de verdad recibida.
        """
        renglon = "  "
        evaluacion = self.evalua_sub(asignacion)
        for valor in asignacion:
            renglon += f"{valor} & "

        for subformula in self.aplana_sin_variables():
            if self == subformula:
                renglon += f"& \\mathbf{{{evaluacion[subformula]}}} &"
            else:
                renglon += f" & {evaluacion[subformula]} & "
        renglon += "\\\\\n"
        return renglon

    def tabla_verdad(self):
        """
        Devuelve la tabla de verdad de la fórmula en formato
        LaTeX.
        """
        numero = (self.tex_tabla()).count('&') +1
        columna1 = 'c'*len(self.lista_variables())
        columma2 = 'c'*numero
        tabla = "\\begin{adjustbox}{max width=\\textwidth, array=" + columna1 + "|" + columma2 + "} \\\\\n"
        tabla += self._cabecera_tabla()
        tabla += "\\hline \n"
        asignaciones = product([0,1],repeat = len(self.lista_variables()))
        for asignacion in asignaciones:
            tabla += self._renglon_verdad(asignacion)
        tabla += "\\end{adjustbox}\n"
        return tabla

    def LaTeX(self, nombre_archivo):
        """
        Crea un archivo con nombre nombre_archivo.tex, que es un
        archivo mínimo en LaTeX para poder compilar la tabla de
        verdad asociada a la fórmula.
        """
        latex = open(nombre_archivo + ".tex",'w')
        tabla = "\\documentclass{article}\n\n"
        tabla += "\\usepackage{adjustbox}\n\n"
        tabla += "\\begin{document}\n\n"
        tabla += "\[ \n" + self.tabla_verdad() + "\]\n\n" + "\\end{document}"

        latex.write(tabla)
        latex.close()

x1 = Formula(1)
x2 = Formula(2)
x3 = Formula(3)
f1 = Formula(x1,'C',x2)
f2 = Formula(x3,'N')
f3 = Formula(f1, 'D', f2)
f4 = Formula(f2, 'C',f1)
f5 = Formula(f4, 'I', f3)
print(f3.tabla_verdad())
f3.LaTeX("prueba2")
