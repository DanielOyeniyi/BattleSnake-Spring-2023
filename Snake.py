import DLinkedList
import Node
class Snake:
    '''Snake class'''
    def __init__(self, data: dict):
        self.__id: str = data['id']
        self.__data: dict = data
        self.__body: DLinkedList = DLinkedList.DLinkedList()
      
        for item in data['body']:
            part: Node = Node.Node(item)
            self.__body.back_push(part)
          
        self.__size = self.__body.get_size()

    def __str__(self) -> str:
        return f"{self.__body}"

    def make_body(self) -> None:
        body: DLinkedList = DLinkedList.DLinkedList()
        for item in self.__data['body']:
            part: Node = Node.Node(item)
            body.back_push(part)
        self.__body = body
        self.__size = body.get_size()

    def move_to(self, location: dict) -> None:
        new_part: Node = Node.Node(location)
        self.__body.front_push(new_part)
        self.__body.delete_tail()

    def grow(self) -> None:
        new_tail: Node = self.__body.get_tail()
        self.__body.back_push(new_tail)

    def get_size(self) -> int:
        return self.__size
        
        