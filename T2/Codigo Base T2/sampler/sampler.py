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
        """ self.markCounter = True """
        self.callContextTree = None
        self.stackList = []
        """ self.callContextTreeData = {} """
        """ self.dataTree = [] """
        """ self.callers_stack = [] """

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
                self.stackList.append(stack)
                print(stack)
                """ for index in range(len(stack)):
                    current_function = stack[index]
                    if not self.dataTree:
                        self.dataTree.append({"name": current_function, "counter": 1, "level": index, "index_in_parent_list": None  ,  "children": []})
                    else:
                        if not self.markCounter:
                            self.add_counter_function(current_function, index, self.dataTree)
                        if index > 0:
                            previous_function_name = stack[index - 1]
                            previous_level = index - 1
                            parent = self.search_parent(previous_function_name, previous_level, self.dataTree)
                            parent["children"].append({"name": current_function, "counter": 1, "level": index, "children": []})
                
                
                if self.markCounter:
                    self.markCounter = False """

                """ self.callers_stack = []
                for index in range(len(stack)):
                    if index not in self.callContextTreeData:
                        self.callContextTreeData[index] = []
                        if self.callers_stack:
                            self.callContextTreeData[index].append(
                                {"name": stack[index], "caller": self.callers_stack[-1], "counter": 1})
                        if len(self.callers_stack) == 0:
                            self.callContextTreeData[index].append(
                                {"name": stack[index], "caller": None, "counter": 1})
                    else:
                        elementExists = False
                        for element in self.callContextTreeData[index]:
                            if stack[index] == element["name"]:
                                element["counter"] += 1
                                elementExists = True
                        if not elementExists:
                            if self.callers_stack:
                                self.callContextTreeData[index].append(
                                    {"name": stack[index], "caller": self.callers_stack[-1], "counter": 1})
                    if index + 1 < len(stack):
                        self.callers_stack.append(stack[index]) """
                # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren

    """ def add_counter_function(self, name, level, array):
        if not array:
            return
        root = array[0]
        if root["name"] == name and root["level"] == level:
            root["counter"] += 1
            return
        else:
            for child in root["children"]:
                if child["name"] == name and child["level"] == level:
                    child["counter"] += 1
                    return
            for child in root["children"]:
                self.add_counter_function(name, level, child["children"]) """

    """ def search_parent(self, name, level, array):
        root = array[0]
        if root["name"] == name and root["level"] == level:
            return root
        else:
            for child in root["children"]:
                if child["name"] == name and child["level"] == level:
                    return child
            for child in root["children"]:
                result = self.search_parent(name, level, child["children"])
                if result is not None:
                    return result """

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
        """ print(self.callContextTreeData) """
        # Lleno el primer nivel del call context tree
        """  for stack in self.stackList:
            self.callContextTree = self.createCallContextTree(stack, 0)
        print(self.callContextTree) """
        # Primero se llena el primer nivel del call context tree
        self.callContextTree = self.throughFirstStack(self.stackList[0], 0)
        # Luego se llena el resto del call context tree
        for stack in self.stackList[1:]:
            for level in range(len(stack)):
                self.createCallContextTree(stack, level, self.callContextTree)

        print(self.callContextTree)

    # Método recursivo para llenar el primer nivel del call context tree
    def throughFirstStack(self, stack, level):
        name = stack[level]

        new_element = {"name": name, "counter": 1,
                       "level": level, "children": []}

        if level + 1 < len(stack):
            next_element = self.throughFirstStack(stack, level + 1)
            new_element['children'].append(next_element)

        return new_element

    def checkLevel(self, level, current_dict):
        if current_dict['level'] == level:
            return {'validated': True, 'dict': None}
        else:
            if current_dict['children']:
                last_child = current_dict['children'][-1]
                return self.checkLevel(level, last_child)
            else:
                return {'validated': False, 'dict': current_dict}

    def checkPosition(self, name, level, current_dict, parent_dict=None):
        # Buscamos en el nivel actual
        if current_dict['level'] == level:
            if parent_dict is not None:
                last_child = parent_dict['children'][-1]
                if last_child['name'] == name:
                    return {'validated': True, 'dict': last_child}
                else:
                    return {'validated': False, 'dict': parent_dict}
            else:
                if current_dict['name'] == name:
                    return {'validated': True, 'dict': current_dict}
                else:
                    return {'validated': False, 'dict': None}
        else:
            last_child = current_dict['children'][-1]
            parent_dict = current_dict
            return self.checkPosition(name, level, last_child, parent_dict)

    # Método recursivo para llenar el resto del call context tree, se asume que el primer nivel ya está lleno y por ende ya hay algo en el callContextTree
    def createCallContextTree(self, stack, level, callContextTree):

        name = stack[level]

        validated_level = self.checkLevel(level, callContextTree)

        if validated_level['validated']:
            validated_position = self.checkPosition(
                name, level, callContextTree)
            if validated_position['validated']:
                current_function = validated_position['dict']
                current_function['counter'] += 1
            else:
                last_dict = validated_position['dict']
                new_element = {"name": name, "counter": 1,
                               "level": level, "children": []}
                last_dict['children'].append(new_element)
        else:
            last_dict = validated_level['dict']
            new_element = {"name": name, "counter": 1,
                           "level": level, "children": []}
            last_dict['children'].append(new_element)

    def recursive_print(self, n_tabs, array):
        # tab = "  "
        # for dict in array:
        #   print(f"{tab*n_tabs} {dict['name']} ({dict['counter']} seconds)" )
        # self.recursive_print(n_tabs + 1)
        pass
