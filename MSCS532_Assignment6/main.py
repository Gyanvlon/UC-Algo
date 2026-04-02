"""Entry-point examples for Assignment 6 implementations."""

from src.data_structures import DynamicArray, QueueArray, SinglyLinkedList, StackArray
from src.selection import deterministic_select, randomized_select


def demo_selection() -> None:
    arr = [12, 7, 5, 3, 7, 10, 1, 8]
    k = 4
    print("Array:", arr)
    print(f"{k}-th smallest (deterministic):", deterministic_select(arr, k))
    print(f"{k}-th smallest (randomized):", randomized_select(arr, k))


def demo_data_structures() -> None:
    dyn = DynamicArray[int]()
    for x in [1, 2, 3]:
        dyn.append(x)
    dyn.insert(1, 10)
    print("DynamicArray:", dyn.to_list())

    stack = StackArray[int]()
    stack.push(1)
    stack.push(2)
    print("Stack pop:", stack.pop())

    queue = QueueArray[int]()
    queue.enqueue(100)
    queue.enqueue(200)
    print("Queue dequeue:", queue.dequeue())

    ll = SinglyLinkedList[int]([4, 5, 6])
    ll.insert_front(3)
    ll.delete_value(5)
    print("LinkedList traverse:", ll.traverse())


def main() -> None:
    demo_selection()
    print()
    demo_data_structures()


if __name__ == "__main__":
    main()
