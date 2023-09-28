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
        self.callContextTree = None
        self.stackList = []

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
                """ print(stack) """

    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def printReport(self):

        self.callContextTree = self.throughFirstStack(self.stackList[0], 0)
        for stack in self.stackList[1:]:
            for level in range(len(stack)):
                self.createCallContextTree(stack, level, self.callContextTree)
        """ print(self.callContextTree) """
        self.printCallContextTree(self.callContextTree)

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

    def printCallContextTree(self, current_dict):
        if current_dict['level'] == 0:
            print(f"Total ({current_dict['counter']} seconds)")
        print(
            f"{' ' * (current_dict['level'] + 1)} {current_dict['name']} ({current_dict['counter']} seconds)")
        if current_dict['children']:
            for child in current_dict['children']:
                self.printCallContextTree(child)
