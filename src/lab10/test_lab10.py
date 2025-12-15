"""
Тестер для лабораторной работы 10.
Проверяет корректность реализации Stack, Queue и SinglyLinkedList.
"""

import sys
import os
import time
from typing import List, Dict, Any

# Импортируем модули из текущей папки
try:
    from structures import Stack, Queue
    from linked_list import SinglyLinkedList, Node
    print("✅ Модули успешно импортированы")
except ImportError as e:
    print(f"❌ Ошибка импорта модулей: {e}")
    print("Убедитесь, что файлы находятся в текущей папке:")
    print("  - structures.py")
    print("  - linked_list.py")
    sys.exit(1)


def test_stack() -> Dict[str, Any]:
    """Тестирование Stack."""
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ STACK")
    print("="*60)
    
    results = {"passed": 0, "failed": 0, "errors": []}
    stack = Stack()
    
    tests = [
        ("Инициализация", lambda: str(stack) == "Stack([])"),
        ("Добавление элемента", lambda: (stack.push(1), len(stack) == 1)[1]),
        ("Peek первого элемента", lambda: stack.peek() == 1),
        ("Добавление второго элемента", lambda: (stack.push(2), len(stack) == 2)[1]),
        ("Peek после второго элемента", lambda: stack.peek() == 2),
        ("Pop (должен вернуть 2)", lambda: stack.pop() == 2),
        ("Pop (должен вернуть 1)", lambda: stack.pop() == 1),
        ("Проверка пустоты", lambda: stack.is_empty()),
        ("Проверка длины пустого стека", lambda: len(stack) == 0),
    ]
    
    # Тест исключения
    try:
        stack.pop()
        results["errors"].append("❌ Pop из пустого стека не вызвал исключение")
        results["failed"] += 1
    except IndexError:
        results["passed"] += 1
        print("✅ Pop из пустого стека вызывает IndexError")
    
    for name, test in tests:
        try:
            if test():
                print(f"✅ {name}")
                results["passed"] += 1
            else:
                print(f"❌ {name}")
                results["failed"] += 1
        except Exception as e:
            print(f"❌ {name}: Ошибка - {e}")
            results["failed"] += 1
            results["errors"].append(f"{name}: {e}")
    
    return results


def test_queue() -> Dict[str, Any]:
    """Тестирование Queue."""
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ QUEUE")
    print("="*60)
    
    results = {"passed": 0, "failed": 0, "errors": []}
    queue = Queue()
    
    tests = [
        ("Инициализация", lambda: str(queue) == "Queue([])"),
        ("Добавление элемента", lambda: (queue.enqueue("A"), len(queue) == 1)[1]),
        ("Peek первого элемента", lambda: queue.peek() == "A"),
        ("Добавление второго элемента", lambda: (queue.enqueue("B"), len(queue) == 2)[1]),
        ("Peek не изменился", lambda: queue.peek() == "A"),
        ("Dequeue (должен вернуть A)", lambda: queue.dequeue() == "A"),
        ("Peek после dequeue", lambda: queue.peek() == "B"),
        ("Dequeue (должен вернуть B)", lambda: queue.dequeue() == "B"),
        ("Проверка пустоты", lambda: queue.is_empty()),
    ]
    
    # Тест исключения
    try:
        queue.dequeue()
        results["errors"].append("❌ Dequeue из пустой очереди не вызвал исключение")
        results["failed"] += 1
    except IndexError:
        results["passed"] += 1
        print("✅ Dequeue из пустой очереди вызывает IndexError")
    
    # Тест FIFO порядка
    queue = Queue()
    items = ["first", "second", "third"]
    for item in items:
        queue.enqueue(item)
    
    try:
        for expected in items:
            actual = queue.dequeue()
            if actual != expected:
                raise AssertionError(f"Ожидалось '{expected}', получено '{actual}'")
        print("✅ Очередь работает по принципу FIFO")
        results["passed"] += 1
    except Exception as e:
        print(f"❌ Очередь не работает по принципу FIFO: {e}")
        results["failed"] += 1
        results["errors"].append(f"FIFO тест: {e}")
    
    for name, test in tests:
        try:
            if test():
                print(f"✅ {name}")
                results["passed"] += 1
            else:
                print(f"❌ {name}")
                results["failed"] += 1
        except Exception as e:
            print(f"❌ {name}: Ошибка - {e}")
            results["failed"] += 1
            results["errors"].append(f"{name}: {e}")
    
    return results


def test_linked_list() -> Dict[str, Any]:
    """Тестирование SinglyLinkedList."""
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ SINGLYLINKEDLIST")
    print("="*60)
    
    results = {"passed": 0, "failed": 0, "errors": []}
    lst = SinglyLinkedList()
    
    # Базовые тесты
    tests = [
        ("Инициализация пустого списка", lambda: len(lst) == 0 and lst.head is None and lst.tail is None),
        ("Append первого элемента", lambda: (lst.append(1), len(lst) == 1 and lst.head.value == 1 and lst.tail.value == 1)[1]),
        ("Append второго элемента", lambda: (lst.append(2), len(lst) == 2 and lst.head.value == 1 and lst.tail.value == 2)[1]),
        ("Prepend элемента", lambda: (lst.prepend(0), len(lst) == 3 and lst.head.value == 0 and lst.tail.value == 2)[1]),
        ("Итерация по списку", lambda: list(lst) == [0, 1, 2]),
    ]
    
    for name, test in tests:
        try:
            if test():
                print(f"✅ {name}")
                results["passed"] += 1
            else:
                print(f"❌ {name}")
                results["failed"] += 1
        except Exception as e:
            print(f"❌ {name}: Ошибка - {e}")
            results["failed"] += 1
            results["errors"].append(f"{name}: {e}")
    
    # Тест insert
    try:
        lst.insert(2, 1.5)  # Вставка между 1 и 2
        if list(lst) == [0, 1, 1.5, 2]:
            print("✅ Insert в середину")
            results["passed"] += 1
        else:
            print(f"❌ Insert в середину: ожидалось [0, 1, 1.5, 2], получено {list(lst)}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ Insert в середину: Ошибка - {e}")
        results["failed"] += 1
    
    # Тест remove_at
    try:
        lst.remove_at(0)  # Удаление первого элемента
        if list(lst) == [1, 1.5, 2] and lst.head.value == 1:
            print("✅ Remove_at из начала")
            results["passed"] += 1
        else:
            print(f"❌ Remove_at из начала: ожидалось [1, 1.5, 2], получено {list(lst)}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ Remove_at из начала: Ошибка - {e}")
        results["failed"] += 1
    
    # Тест remove по значению
    try:
        lst.remove(1.5)  # Удаление по значению
        if list(lst) == [1, 2] and lst.tail.value == 2:
            print("✅ Remove по значению")
            results["passed"] += 1
        else:
            print(f"❌ Remove по значению: ожидалось [1, 2], получено {list(lst)}")
            results["failed"] += 1
    except Exception as e:
        print(f"❌ Remove по значению: Ошибка - {e}")
        results["failed"] += 1
    
    # Тест некорректного индекса
    try:
        lst.insert(10, 99)
        print("❌ Insert с некорректным индексом не вызвал исключение")
        results["failed"] += 1
    except IndexError:
        print("✅ Insert с некорректным индексом вызывает IndexError")
        results["passed"] += 1
    except Exception as e:
        print(f"❌ Insert с некорректным индексом вызвал неправильное исключение: {e}")
        results["failed"] += 1
    
    return results


def benchmark() -> None:
    """Простой бенчмарк производительности."""
    print("\n" + "="*60)
    print("БЕНЧМАРК ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*60)
    
    n = 10000
    print(f"Тестирование с {n} элементами")
    
    # Stack бенчмарк
    print("\n1. Stack:")
    stack = Stack()
    start = time.time()
    for i in range(n):
        stack.push(i)
    push_time = time.time() - start
    
    start = time.time()
    for _ in range(n):
        stack.pop()
    pop_time = time.time() - start
    
    print(f"   push {n} элементов: {push_time:.6f} сек")
    print(f"   pop {n} элементов: {pop_time:.6f} сек")
    
    # Queue бенчмарк
    print("\n2. Queue:")
    queue = Queue()
    start = time.time()
    for i in range(n):
        queue.enqueue(i)
    enqueue_time = time.time() - start
    
    start = time.time()
    for _ in range(n):
        queue.dequeue()
    dequeue_time = time.time() - start
    
    print(f"   enqueue {n} элементов: {enqueue_time:.6f} сек")
    print(f"   dequeue {n} элементов: {dequeue_time:.6f} сек")
    
    # SinglyLinkedList бенчмарк
    print("\n3. SinglyLinkedList:")
    lst = SinglyLinkedList()
    start = time.time()
    for i in range(n):
        lst.append(i)
    append_time = time.time() - start
    
    lst2 = SinglyLinkedList()
    start = time.time()
    for i in range(n):
        lst2.prepend(i)
    prepend_time = time.time() - start
    
    print(f"   append {n} элементов: {append_time:.6f} сек")
    print(f"   prepend {n} элементов: {prepend_time:.6f} сек")
    
    # Сравнение
    print("\n" + "-"*60)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ:")
    
    # Находим минимальное ненулевое время для сравнения
    base_time = max(push_time, 0.000001)  # Защита от деления на ноль
    
    print(f"\nОтносительная производительность (база: Stack.push = 1.00x):")
    if base_time > 0:
        print(f"   Stack.push:               1.00x ({push_time:.6f} сек)")
        print(f"   Queue.enqueue:            {enqueue_time/base_time:.2f}x ({enqueue_time:.6f} сек)")
        print(f"   SinglyLinkedList.append:  {append_time/base_time:.2f}x ({append_time:.6f} сек)")
        print(f"   SinglyLinkedList.prepend: {prepend_time/base_time:.2f}x ({prepend_time:.6f} сек)")
    else:
        print("   Невозможно сравнить (время выполнения равно нулю)")


def main():
    """Основная функция."""
    print("\n" + "="*80)
    print("ТЕСТЕР ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ 10")
    print("Структуры данных: Stack, Queue, SinglyLinkedList")
    print("="*80)
    
    total_results = {"passed": 0, "failed": 0, "errors": []}
    
    # Запуск тестов
    stack_results = test_stack()
    queue_results = test_queue()
    linked_list_results = test_linked_list()
    
    # Сбор статистики
    for results in [stack_results, queue_results, linked_list_results]:
        total_results["passed"] += results["passed"]
        total_results["failed"] += results["failed"]
        total_results["errors"].extend(results["errors"])
    
    # Вывод итогов
    print("\n" + "="*80)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*80)
    
    total_tests = total_results["passed"] + total_results["failed"]
    print(f"\nВсего тестов: {total_tests}")
    print(f"✅ Успешно: {total_results['passed']}")
    print(f"❌ Провалено: {total_results['failed']}")
    
    if total_results["errors"]:
        print(f"\nОшибки ({len(total_results['errors'])}):")
        for error in total_results["errors"]:
            print(f"  - {error}")
    
    # Процент успешных тестов
    if total_tests > 0:
        success_rate = (total_results["passed"] / total_tests) * 100
        print(f"\n📊 Процент успешных тестов: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        elif success_rate >= 80:
            print("\n👍 Большинство тестов пройдено успешно")
        else:
            print("\n⚠️  Много проваленных тестов, требуется доработка")
    
    # Запуск бенчмарка если все тесты пройдены
    if total_results["failed"] == 0:
        answer = input("\nЗапустить бенчмарк производительности? (y/n): ")
        if answer.lower() in ['y', 'yes', 'да']:
            benchmark()
    else:
        print("\n⚠️  Бенчмарк не запущен из-за проваленных тестов")
    
    print("\n" + "="*80)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\n\nКритическая ошибка: {e}")
        import traceback
        traceback.print_exc()