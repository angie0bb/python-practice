# Practice python, assignment 3
# linked list

# bring codes for the single linked list and stack from the lab and lecture slides.
class LList:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def __init__(self):
        self.head = None
        self.tail = None  # initializing the tail
        self.nVals = 0

    def addFront(self, val):
        new_node = self.Node(val, self.head)

        if self.head is None:  # If the linked list is empty, we should add a node and have both: the head and the tail pointing at it.
            self.tail = new_node

        self.head = new_node
        self.nVals += 1

    def getFront(self):
        if self.head is None:
            return None
        else:
            return self.head.val

    def removeFront(self):
        returned_value = self.head
        if self.head is not None:

            if self.tail == self.head:  # If the tail and the head is pointing to the same node, then the list has only one node. The reference must be removed from both: the tail and the head
                self.head = self.tail = None

            else:
                self.head = self.head.next
            self.nVals -= 1

        return returned_value.val  # return the removed value

    def toList(self):
        result_lst = []
        node = self.head
        while node is not None:
            result_lst.append(node.val)
            node = node.next
        # print(array)
        return result_lst

    # We modified the addBack() from the tutorial slides to make it O(1) instead of O(N)
    def addBack(self, val):
        if self.head is None:
            self.addFront(val)
        else:
            self.tail.next = self.Node(
                val)  # The while loop to reach the tail is not necessary anymore, we can be replace it with the tail node.
            self.tail = self.tail.next  # The tail must be changed to the last node that we just added to the end of the linked list
            self.nVals += 1

    def getBack(self):
        if self.tail is None:
            return None
        else:
            return self.tail.val

    def count(self):
        return self.nVals

##### Part 1: Creating Two Singly Linked List Functions #####

    def printSLL(self):
        node = self.head
        node_lst = []
        if node is None:
            print("Empty Linked List")
        else:
            while node is not None:
                node_lst.append(str(node.val))
                node = node.next
            node_lst_joined = ",".join(node_lst)
            print("[" + node_lst_joined + "]")

    def locate(self, item):
        node = self.head

        if node is None:
            print("Item was not located")
            return
        while node is not None:
            if item != node.val:
                node = node.next
            else:
                print("Item was located")
                return
        print("Item was not located")


# lst = LList()
# lst.addFront(2)
# lst.addFront(5)
# lst.addFront(1)
# lst.printSLL()
#
# lst.locate(2)
#

##### Part 2: Evaluating Postfix Expressions #####

class Stack:
    def __init__(self):
        self.llist = LList()

    def __len__(self):
        return self.llist.nVals

    def push(self, val):
        self.llist.addFront(val)

    def pop(self):
        return self.llist.removeFront()

    def peek(self):
        return self.llist.getFront()

    def getBack(self):
        return self.llist.getBack()

    def __len__(self):
        return self.llist.count()

    def toList(self):
        return list(reversed(self.llist.toList()))


def evalPostfix(e):  # e -> string
    is_error = False
    split_e = e.split()
    # print(split_e)

    # use Stack
    s = Stack()
    operators = ["+", "-", "*", "/"]

    for i in split_e:
        if i not in operators:
            s.push(int(i))
            # print(int(i))
        elif i in operators:
            # error checking
            if len(s) < 2:
                current_stack = s.toList()
                print(f'Error: {current_stack}')
                return
            operand1 = s.pop()
            operand2 = s.pop()

            if i == "+":
                s.push(operand2 + operand1)
            elif i == "-":
                s.push(operand2 - operand1)
            elif i == "*":
                s.push(operand2 * operand1)
            else:
                s.push(operand2 / operand1)

    # error checking
    if len(s) != 1:
        current_stack = s.toList()
        print(f'Error: {current_stack}')
    else:
        # non-error
        try:  # to get integer value if the result is x.0
            if s.peek().is_integer():
                print(int(s.peek()))
            else:
                print(s.peek())
        except:
            print(s.peek())


# evalPostfix("1 2 3 4 * - /")
# evalPostfix("20 5 - 3 / 2 *")
# evalPostfix("+")
# evalPostfix("1")











