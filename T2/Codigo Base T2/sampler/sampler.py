from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames


class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.callContextTreeData = {}
        self.callers_stack = []
        
    def start(self):
        self.active = True
        self.t.start()

    
    def stop(self):
        self.active = False
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                self.callers_stack = []
                for index in range(len(stack)):
                    ##########################
                    """ if self.callers_stack:
                        current_caller = self.callers_stack[-1]
                        if current_caller != stack[index]:
                            self.callers_stack.append(stack[index])
                            
                    self.callers_stack.append(stack[index]) """
                    #########################
                    if index not in self.callContextTreeData:
                        self.callContextTreeData[index] = []
                        if self.callers_stack:
                            self.callContextTreeData[index].append({"name": stack[index], "caller": self.callers_stack[-1], "counter": 1 })
                        if len(self.callers_stack) == 0:
                            self.callContextTreeData[index].append({"name": stack[index], "caller": None, "counter": 1})

                    else:
                        elementExists = False
                        for element in self.callContextTreeData[index]:
                            if stack[index] == element["name"]:
                                element["counter"] += 1
                                elementExists = True
                        if not elementExists:
                            if self.callers_stack:
                                self.callContextTreeData[index].append({"name": stack[index], "caller": self.callers_stack[-1], "counter": 1})

                    
                    if index + 1 < len(stack):
                        self.callers_stack.append(stack[index])
                            

                #El contenido de CallContextTreeData es un diccionario donde la llave es el nivel del stack y el valor es una lista de diccionarios donde la llave es el nombre de la funcion y el valor es la cantidad de veces que se ha llamado. Algo como:
                """ 
                Para esta data (code1.py):
                [
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script'],
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'bar'],
    #################################
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'bar', mmethod1],
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'bar', mmethod1],
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'bar', mmethod1],
    #################################
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'zoo'],
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'zoo'],
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'zoo', 'bar'],
    #################################
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo', 'zoo', 'bar'],
    #################################
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo'],
    ['_bootstrap', '_bootstrap_inner', 'run', 'execute_script', '<module>', 'main', 'foo'],
                ]
                Da este resultado:
                {   
                    0: [{'_bootstrap': 7}],
                    1: [{'_bootstrap_inner': 7}],
                    2: [{'run': 7}],
                    3: [{'execute_script': 7}],
                    4: [{'<module>': 6}],
                    5: [{'main': 6}],
                    6: [{'foo': 6}],
                    7: [{'bar': 1}, {'zoo': 3}],
                    8: [{'bar': 1}]
                }
                Revisar si es conevniente de que se guarde todo como lista en lugar de diccionario para el call context tree. O sino hacer un trabajo previo para pasar la info del diccionario a una lista ordenada para crear el arbol con los niveles. Fijarse en los casos con ###. Hay que identificar quien llama a quien y en que nivel se encuentra. Sería bueno implementar un call stack para cada hilo y que se vaya actualizando a medida que se van llamando funciones. Algo como lo que se hizo para instrumentor
                """
                print(stack)  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def printReport(self):
        # Este metodo debe imprimir el reporte del call context tree
        
        # n_tabs = 1
        # print(f"total ({self.callContextTreeData[0][0]['counter']} seconds)")

        # for level, array in self.callContextTreeData.items():
            
        #     self.recursive_print(n_tabs, array)

        #     n_tabs+=1
        
        print(self.callContextTreeData)
        pass
        

    def recursive_print(self, n_tabs, array):
      # tab = "  "
      # for dict in array:
      #   print(f"{tab*n_tabs} {dict['name']} ({dict['counter']} seconds)" )
      # self.recursive_print(n_tabs + 1)
      pass