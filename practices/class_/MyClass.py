# encoding=utf-8


class MyClass:
    a = {'z': 1}
    del a['x']
    b = list(a + i for i in range(10))
