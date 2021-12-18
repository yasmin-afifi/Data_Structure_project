class Node:
    def __init__(self, z):
        self.z = z
        self.next = None


class Stack:
    def __init__(self):
        self.head = Node("head")
        self.size = 0
    def _str_(self):
        y = self.head.next
        output = ''
        while y:
            output=output+ str(y.z) + '->'
            y = y.next
        return output[:-3]
    def push(self, z):
        node = Node(z)
        node.next = self.head.next
        self.head.next = node
        self.size= self.size+ 1
    def pop(self):
        if self.is_empty():
            raise Exception('the stack is empty')
        r= self.head.next
        self.head.next = self.head.next.next
        self.size=self.size - 1
        return r.z
    def top(self):
        if self.is_empty():
            raise Exception('the stack is empty')
        return self.head.next.z
    def is_empty(self):
        return self.size == 0
    def get_size(self):
        return self.size
    
  