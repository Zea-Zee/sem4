from bintrees import RBTree

def process_requests(commands):
    tree = RBTree()

    for command in commands:
        if command[0] == 1:
            # Добавляем новую заявку с приоритетом k
            k = command[1]
            if k in tree:
                tree[k] += 1  # Если такой приоритет уже есть, увеличиваем количество
            else:
                tree.insert(k, 1)
        elif command[0] == 0:
            # Нужно вывести i-й по важности приоритет
            i = command[1]
            # Преобразуем дерево в список и берем i-й элемент
            sorted_priorities = list(tree.keys())
            print(sorted_priorities[-i])
        elif command[0] == -1:
            # Удаляем заявку с приоритетом k
            k = command[1]
            if tree[k] == 1:
                tree.remove(k)
            else:
                tree[k] -= 1  # Уменьшаем количество, если таких приоритетов было несколько

def main():
    n = int(input("Введите количество заявок: "))
    commands = [list(map(int, input().split())) for _ in range(n)]
    process_requests(commands)

main()
