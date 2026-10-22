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

    
    def cargar_alumnos_txt(self):
        try:
            with open("alumnos.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")

                    if len(datos) != 7:
                        continue

                    cedula, nombre, correo, tipo_programa = datos[:4]

                    notas = []
                    for nota in datos[4:7]:
                        valor = float(nota)
                        if valor != 0:
                            notas.append(valor)

                    tipo = tipo_programa.strip().lower()

                    if tipo == "curso":
                        programa = Curso(tipo_programa)
                    elif tipo == "diplomado":
                        programa = Diplomado(tipo_programa)
                    elif tipo == "bootcamp":
                        programa = Bootcamp(tipo_programa)
                    else:
                        continue

                    alumno = Alumno(
                        cedula, nombre, correo, notas, programa
                    )
                    self.alumnos.append(alumno)

        except FileNotFoundError:
            pass


    def guardar_alumno_txt(self, alumno):
        archivo = open("alumnos.txt", "a")
        archivo.write(alumno.cedula + "," + alumno.nombre_completo + "," + alumno.correo + "," + alumno.nombre_programa + ",0,0,0\n")
        archivo.close()

    def actualizar_alumnos_txt(self):
        archivo = open("alumnos.txt", "w")

        for alumno in self.alumnos:
            notas = alumno.notas[:3]

            while len(notas) < 3:
                notas.append(0)

            archivo.write(
                alumno.cedula + "," +
                alumno.nombre_completo + "," +
                alumno.correo + "," +
                alumno.nombre_programa + "," +
                str(notas[0]) + "," +
                str(notas[1]) + "," +
                str(notas[2]) + "\n"
            )

        archivo.close()
   
    def buscar_alumno(self, cedula):
        for alumno in self.alumnos:
            if alumno.cedula == cedula:
                return alumno
        return None

    def registrar_profesor(self, profesor):
        self.profesores.append(profesor)
        
    def buscar_profesor(self, cedula):
        for profesor in self.profesores:
            if profesor.cedula == cedula:
                return profesor
        return None

    
    def cargar_profesores_txt(self):
        try:
            with open("profesores.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split(",")

                    if len(datos) != 5:
                        continue

                    cedula, nombre, correo, especialidad, materia = datos

                    profesor = Profesor(
                        cedula, nombre, correo, especialidad, materia
                    )

                    self.profesores.append(profesor)

        except FileNotFoundError:
            pass


    def guardar_profesor_txt(self, profesor):
        archivo = open("profesores.txt", "a", encoding="utf-8")
        archivo.write(profesor.cedula + "," + profesor.nombre_completo + "," + profesor.correo + "," + profesor.especialidad + "," + profesor.materia_asignada + "\n")
        archivo.close()

    def registrar_nota(self, alumno, nota):
        self.pila_notas.append((alumno, nota))

    def deshacer_ultima_nota(self):
        if len(self.pila_notas) == 0:
         return None

        alumno, nota = self.pila_notas.pop()
        alumno.notas.remove(nota)

        return nota    

    def revisar_aprobados(self):
        aprobados = []
        for alumno in self.alumnos:
            if alumno.esta_aprobado():
                aprobados.append(alumno)
        return aprobados

    def generar_certificados(self):
        self.cola_certificados = []
        aprobados = self.revisar_aprobados()

        for alumno in aprobados:
            self.cola_certificados.append(alumno)

        return self.cola_certificados

    
    def guardar_certificados_txt(self):
        with open("certificados_pendientes.txt", "w", encoding="utf-8") as archivo:
            archivo.write("REPORTE DE CERTIFICADOS\n")
            archivo.write("==============================\n")
            archivo.write("Total de graduandos: " + str(len(self.cola_certificados)) + "\n\n")

            for alumno in self.cola_certificados:
                archivo.write("Cedula: " + alumno.cedula + "\n")
                archivo.write("Nombre: " + alumno.nombre_completo + "\n")
                archivo.write("Programa: " + alumno.nombre_programa + "\n")
                archivo.write("Promedio: " + str(round(alumno.calcular_promedio(), 2)) + "\n")
                archivo.write("Estatus: APROBADO\n")
                archivo.write("------------------------------\n")

    
 
    def mostrar_reporte(self):
        print("=== REPORTE ACADEMICO ===")

        print("\nALUMNOS:")
        for alumno in self.alumnos:
            alumno.mostrar_datos()
            print("Promedio:", round(alumno.calcular_promedio(), 2))

            if alumno.esta_aprobado():
                print("Estatus: APROBADO")
            else:
                print("Estatus: REPROBADO")

            print("------------------------------")

        print("\nPROFESORES:")
        for profesor in self.profesores:
            profesor.mostrar_datos()
            print("------------------------------")


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
        self.actualizar_alumnos_txt()
        print("Saliendo del Sistema Académico...")
        return


def mostrar_menu():
    print("==================================================")
    print("SGA-DO: SISTEMA DIPLOMADOSONLINE")
    print("==================================================")
    print("1. Registrar Alumno")
    print("2. Registrar Profesor")
    print("3. Registrar Notas a un Alumno")
    print("4. Deshacer Último Registro de Nota")
    print("5. Generar Cola de Certificados")
    print("6. Mostrar Reporte General")
    print("7. Salir")
    print("==================================================")

sistema = SistemaAcademico()
sistema.cargar_alumnos_txt()
sistema.cargar_profesores_txt()

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    
    if opcion not in ["1", "2", "3", "4", "5", "6", "7"]:
        print("Error: ingrese una opción válida del 1 al 7.")
        continue
    
    if opcion == "7":
        sistema.salir()
        break

    if opcion == "1":
        cedula = input("Cédula: ")
        nombre = input("Nombre completo: ")
        correo = input("Correo: ")
        tipo_programa = input("Tipo de programa: ")

        if tipo_programa.lower() == "curso":
            programa = Curso("curso")
        elif tipo_programa.lower() == "diplomado":
            programa = Diplomado("diplomado")
        elif tipo_programa.lower() == "bootcamp":
            programa = Bootcamp("bootcamp")
        else:
            print("Error: el programa debe ser Curso, Diplomado o Bootcamp.")
            continue
        
        if sistema.buscar_alumno(cedula) is not None:
            print("Ya existe un alumno con esa cédula.")
        else:
            alumno = Alumno(cedula, nombre, correo, [], programa)
            sistema.registrar_alumno(alumno)
            sistema.guardar_alumno_txt(alumno)
            print("Alumno registrado correctamente.")

    if opcion == "2":
        cedula = input("Cédula: ")
        nombre = input("Nombre completo: ")
        correo = input("Correo: ")
        especialidad = input("Especialidad: ")
        materia = input("Materia asignada: ")

        
        if sistema.buscar_profesor(cedula) is not None:
            print("Ya existe un profesor con esa cédula.")
        else:
            profesor = Profesor(cedula, nombre, correo, especialidad, materia)
            sistema.registrar_profesor(profesor)
            sistema.guardar_profesor_txt(profesor)
            print("Profesor registrado correctamente.")

    if opcion == "3":
        cedula = input("Cédula del alumno: ")
        alumno = sistema.buscar_alumno(cedula)

        if alumno is None:
            print("Alumno no encontrado.")
        else:
            print("Alumno encontrado:", alumno.nombre_completo)

            if len(alumno.notas) >= 3:
                print("El alumno ya tiene las 3 notas permitidas.")
            else:
                try:
                    nota = float(input("Ingrese la nota: "))

                    if nota < 1 or nota > 20:
                        print("Error: la nota debe estar entre 1 y 20.")
                    else:
                        alumno.registrar_nota(nota)
                        sistema.registrar_nota(alumno, nota)
                        sistema.actualizar_alumnos_txt()
                        print("Nota registrada correctamente.")

                except ValueError:
                    print("Error: debes ingresar un número válido.")

    if opcion == "4":
        nota_eliminada = sistema.deshacer_ultima_nota()

        if nota_eliminada is None:
            print("No hay notas para deshacer.")
        else:
            print("Nota eliminada:", nota_eliminada)
        if nota_eliminada is not None:
            sistema.actualizar_alumnos_txt()

    if opcion == "5":
        sistema.generar_certificados()
        sistema.guardar_certificados_txt()
        print("Certificados generados correctamente.")
    
    if opcion == "6":
        sistema.mostrar_reporte()
           
        