import Node
class Node:
    '''node for a linked list'''
    def __init__(self, data) -> None:
        self.__x: int = data['x']
        self.__y: int = data['y']
        self.__parent: Node = None
        self.__child: Node = None

    def __str__(self) -> str:
        return f"({self.__x}:{self.__y})"
      
    def get_x(self) -> int:
        return self.__x

    def set_x(self, new_x: int) -> None:
        self.__x = new_x

    def get_y(self) -> int:
        return self.__y

    def set_y(self, new_y: int) -> None:
        self.__y = new_y

    def get_parent(self) -> Node:
        return self.__parent

    def set_parent(self, new_parent: Node) -> None:
        self.__parent = new_parent

    def get_child(self) -> Node:
        return self.__child

    def set_child(self, new_child: Node) -> None:
        self.__child = new_child
    
      