import Node
class DLinkedList:

    def __init__(self) -> None:
        self.__head: Node = None
        self.__tail: Node = None
        self.__size: int = 0

    def __str__(self) -> str:
        result: str = ""
        if self.__size == 0:
            result = "list is empty"
        else:
            current: Node = self.__head
            while current != None:
                result += f"{current} "
                current = current.get_child()
        return result

    
    def front_push(self, new_head: Node) -> None:
        '''
        push new node on top of linked list, it is now the head 
        if only 1 element in linked list then old head become tail
        '''
        if self.__size == 0:
            self.__head = new_head
            self.__size += 1
          
        elif self.__size == 1:
            self.__head.set_parent(new_head)
            self.__tail = self.__head
            new_head.set_child(self.__head)
            self.__head = new_head
            self.__size += 1

        else:
            self.__head.set_parent(new_head)
            new_head.set_child(self.__head)
            self.__head = new_head

    def back_push(self, new_tail: Node) -> None:
        '''
        push new node at back of linked list, it is now the 
        tail, unless the list is empty then it's now the head'''
        if self.__size == 0:
            self.__head = new_tail
            self.__size += 1
          
        elif self.__size == 1:
            self.__head.set_child(new_tail)
            new_tail.set_parent(self.__head)
            self.__tail = new_tail
            self.__size += 1

        else:
            self.__tail.set_child(new_tail)
            new_tail.set_parent(self.__tail)
            self.__tail = new_tail

    def delete_tail(self) -> None:
        if self.__size == 0:
            print("list is empty")
          
        elif self.__size == 1:
            self.__head = None
            self.__size -= 1

        elif self.__size == 2:
            self.__head.set_child(None)
            self.__tail.set_parent(None)
            self.__tail == None
            self.__size -= 1    
          
        else:
            new_tail: Node = self.__tail.get_parent()
            new_tail.__tail.set_child(None)
            self.__tail.set_parent(None)
            self.__tail = new_tail
            self.__size -= 1

    def get_size(self) -> int:
        return self.__size

    def get_head(self) -> Node:
        return self.__head

    def get_tail(self) -> Node:
        return self.__tail
