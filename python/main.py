class Persona:
    def __init__(self, cedula, nombre_completo, correo):
       self.cedula = cedula
       self.nombre_completo = nombre_completo
       self.correo = correo
    def mostrar_datos(self):
        print("cedula:", self.cedula)
        print("nombre:", self.nombre_completo)
        print("correo:", self.correo) 


class Profesor(Persona):
    def __init__(self, cedula, nombre_completo, correo, especialidad, materia_asignada):
        super().__init__(cedula, nombre_completo, correo)
        self.especialidad = especialidad
        self.materia_asignada = materia_asignada
    def mostrar_datos(self):
        super().mostrar_datos()
        print("especialidad:", self.especialidad)
        print("materia asignada:", self.materia_asignada)



class Alumno(Persona):
    def __init__(self, cedula, nombre_completo, correo, notas, programa_asignado):
        super().__init__(cedula, nombre_completo, correo)
        self.notas = notas
        self.programa_asignado = programa_asignado  
        self.nombre_programa = programa_asignado.nombre_programa
    def mostrar_datos(self):
        super().mostrar_datos()
        print("notas:", self.notas)
        print("programa asignado:", type(self.programa_asignado).__name__)
        print("nombre programa:", self.nombre_programa)
    def registrar_nota(self, nota):
        if len(self.notas) < 3:
            self.notas.append(nota)
    def calcular_promedio(self):
        if len(self.notas) == 0:
            return 0
        return sum(self.notas) / len(self.notas)
    def esta_aprobado(self):
        return self.programa_asignado.evaluar_aprobacion(self.notas)        



class ProgramaAcademico:
    def __init__(self, nombre_programa):
        self.nombre_programa = nombre_programa
    def evaluar_aprobacion(self, notas):
        return False


class Curso(ProgramaAcademico):
    def __init__(self, nombre_programa):
        super().__init__(nombre_programa)
        self.promedio_minimo = 10
    def evaluar_aprobacion(self, notas):
        if len(notas) == 0:
            return False
        return sum(notas) / len(notas) >= self.promedio_minimo


class Diplomado(ProgramaAcademico):
    def __init__(self, nombre_programa):
        super().__init__(nombre_programa)
        self.promedio_minimo = 14
    def evaluar_aprobacion(self, notas):
        if len(notas) == 0:
            return False
        return sum(notas) / len(notas) >= self.promedio_minimo


class Bootcamp(ProgramaAcademico):
    def __init__(self, nombre_programa):
        super().__init__(nombre_programa)
        self.nota_minima_individual = 14
    def evaluar_aprobacion(self, notas):
        if len(notas) == 0:
            return False
        return all(nota >= self.nota_minima_individual for nota in notas)




class SistemaAcademico:
    def __init__(self):
        self.alumnos = []
        self.profesores = []
        self.pila_notas = []
        self.cola_certificados = []
    def registrar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def registrar_profesor(self, profesor):
        self.profesores.append(profesor)

    def registrar_nota(self, nota):
        self.pila_notas.append(nota)

    def deshacer_ultima_nota(self):
        if len(self.pila_notas) == 0:
            return None
        return self.pila_notas.pop()

    def revisar_aprobados(self):
        aprobados = []
        for alumno in self.alumnos:
            if alumno.esta_aprobado():
                aprobados.append(alumno)
        return aprobados

    def generar_certificados(self):
        aprobados = self.revisar_aprobados()
        for alumno in aprobados:
            certificado = "Certificado de aprobación - " + alumno.nombre_completo
            self.cola_certificados.append(certificado)            
        return self.cola_certificados
    
    def mostrar_reporte(self):
        print("=== REPORTE ACADEMICO ===")
        print("ALUMNOS:")
        for alumno in self.alumnos:
            alumno.mostrar_datos()
        print("PROFESORES:")
        for profesor in self.profesores:
            profesor.mostrar_datos()

    def guardar_datos_txt(self):
        archivo = open("datos.txt", "w")
        for alumno in self.alumnos:
            notas_texto = "-".join(str(nota) for nota in alumno.notas)
            archivo.write(alumno.cedula + "," + alumno.nombre_completo + "," + alumno.correo + "," + alumno.nombre_programa + "," + notas_texto + "\n")
        archivo.close()    
    
    def cargar_datos_txt(self):
        archivo = open("datos.txt", "r")
        for linea in archivo:
            datos = linea.strip().split(",")
            cedula = datos[0]
            nombre_completo = datos[1]
            correo = datos[2]
            nombre_programa = datos[3]
            notas = datos[4]
            notas = notas.split("-")
            notas = [int(nota) for nota in notas]
            programa = Diplomado(nombre_programa)
            alumno = Alumno(cedula, nombre_completo, correo, notas, programa)
            self.alumnos.append(alumno)
        
        archivo.close()
        return self.alumnos
    
    def salir(self):
        print("Saliendo del Sistema Académico...")
        return

profesor1 = Profesor("P-101", "Mario Castañeda", "mariocastañeda@gmail.com", "programacion", "python")
profesor1.mostrar_datos()

diplomado1 = Diplomado("Programacion")
alumno1 = Alumno("A-101", "Peter Parker", "peterparker@gmail.com", [], diplomado1)
alumno1.registrar_nota(15)
alumno1.registrar_nota(14)
alumno1.registrar_nota(16)
alumno1.mostrar_datos()
print("promedio:", alumno1.calcular_promedio())
print("aprobado:", alumno1.esta_aprobado())
curso1 = Curso("Curso de python")
print("curso aprobado:", curso1.evaluar_aprobacion([12, 11, 10]))
diplomado_prueba = Diplomado("Diplomado de Python")
print("diplomado aprobado:", diplomado_prueba.evaluar_aprobacion([15, 14, 16]))
bootcamp1 = Bootcamp("Bootcamp de Python")
print("bootcamp aprobado:", bootcamp1.evaluar_aprobacion([15, 14, 16]))

sistema = SistemaAcademico()
sistema.registrar_alumno(alumno1)
sistema.registrar_profesor(profesor1)
aprobados = sistema.revisar_aprobados()
print("cantidad de aprobados:", len(aprobados))
sistema.registrar_nota(18)
sistema.registrar_nota(12)
print("pila de notas:", sistema.pila_notas)
print("nota eliminada:", sistema.deshacer_ultima_nota())
certificados = sistema.generar_certificados()
print("certificados:", certificados)
sistema.mostrar_reporte()
sistema.guardar_datos_txt()
sistema.alumnos = []
sistema.cargar_datos_txt()

print("ALUMNOS CARGADOS DESDE TXT:")
for alumno in sistema.alumnos:
    alumno.mostrar_datos()
sistema.salir()
