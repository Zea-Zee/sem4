def reverseList(head):
    if not head or not head.next:
        return head

    prev = None

    while head:
        next_node = head.next
        head.next = prev
        prev = head
        head = 

    return
