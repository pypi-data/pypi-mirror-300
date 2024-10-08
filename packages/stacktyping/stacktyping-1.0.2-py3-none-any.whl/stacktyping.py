from typing import Any


def export(func):
    from sys import modules
    setattr(modules[__name__], func.__name__, func)
    return func


@export
class StackError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def detection_stack(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(stack, 'detection') and self.detection:
            self.detection()
            return func(self, *args, **kwargs)
        else:
            raise PermissionError('No permission')

    return wrapper


@export
class stack:
    """
    Stack is a type developed based on lists.

    You can create a stack like this:
    _var = stack(typing)

    The available types of typing are:
    str, int, float, bool, list, dict, tuple, set, stack...

    If you view the stack, it will be returned in the form of a list:
    Empty stack []
    Int stack [1, 2, 3, 4, 5]...

    Based on C++ -> Python.
    """

    def __new__(cls, *args, **kwargs):
        """ Create a new stack. """
        return super().__new__(cls)


    def __init__(self, typing):
        """ Initialize stack. """
        t = [str, int, float, bool, dict, stack, list, tuple, set]
        if (typing not in t) and not isinstance(typing, tuple(t[5:9])):
            raise StackError('Data type error')

        self.__typing = typing
        self.__stack: list[typing] = []

        if isinstance(typing, tuple(t[5:9])):
            try:
                self.__stack = list(typing)
            except (TypeError):
                raise StackError(
            type(typing).__name__ + ' type does not support conversion to stack'
                )


    def __str__(self):
        """ Convert stack to string. """
        from re import sub
        return sub(r'\[', '{', sub(']', '}', str(self.__stack)))


    def __repr__(self):
        """ Output Stack """
        from re import sub
        return sub(r'\[', '{', sub(']', '}', str(self.__stack)))


    def detection(self) -> None:
        """
        Check if the element types of the stack are consistent.

        In the class, the decorator 'detection_stack' can detect in real-time:
        @detection_stack
        def size(self) -> int: ...

        This function will not return anything.
        """

        if len(self.__stack) > 0:
            for item in self.__stack:
                if not isinstance(item, self.__typing):
                    raise StackError(
                        'Different element types')
        return


    @property
    @detection_stack
    def size(self) -> int:
        """ Return the number of elements in the stack. """
        return len(self.__stack)


    @detection_stack
    def pop(self) -> None:
        """ Pop up the top element of the stack. """
        del self.__stack[-1]


    @property
    @detection_stack
    def top(self) -> Any:
        """ Get the top element of the stack. """
        if len(self.__stack) <= 0:
            raise StackError(
                'The number of elements must be greater than or equal to 1')
        return self.__stack[-1]


    @property
    @detection_stack
    def empty(self) -> bool:
        """ Check if the stack is empty. """
        return len(self.__stack) == 0


    @detection_stack
    def push(self, _obj) -> None:
        """ Push elements onto the stack. """
        self.__stack.append(_obj)


    @detection_stack
    def swap(self, other) -> None:
        """ Swap the two stacks. """
        if not isinstance(other, stack):
            raise StackError('Type Error of ' + type(other).__name__)
        _T, _C = stack(int), self.__stack[:]
        while not other.empty:
            _T.push(other.top)
            other.pop()
        while _C:
            other.push(_C[-1])
            _C.pop()
        self.__stack = iters(_T)


    @detection_stack
    def _copy(self) -> Any:
        """ Save your stack as a copy """
        _stack = stack(self.__typing)
        for item in reversed(self.__stack):
            _stack.push(item)
        return _stack


@export
def clear(_Stack) -> None:
    """ Pop up all elements of the stack. """
    global stack
    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)

    while not _Stack.empty:
        _Stack.pop()


@export
def iters(_Stack, typing=list) -> list | tuple:
    """ Convert the stack into an iterable list. """
    global stack
    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)

    if typing not in [tuple, list]:
        raise StackError('Type Error of ' + type(typing).__name__)

    _StackIter, _T = [], _Stack._copy()

    while not _T.empty:
        _StackIter.append(_T.top)
        _T.pop()

    return typing(_StackIter)


@export
def move(_Stack, other) -> None:
    """ Move elements from one stack to another stack. """
    global stack
    if not isinstance(_Stack, stack) or not isinstance(other, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)

    while not _Stack.empty:
        other.push(_Stack.top)
        _Stack.pop()


@export
def news() -> None:
    """ Get news about stacktyping. """
    from stacktyping import NEW
    print(NEW)


@export
def seek(_Stack, *args) -> int | tuple[int, ...]:
    """ Find the position of an element from the stack. """
    global stack
    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)
    tup = []

    try:
        for s in args:
            if len(args) == 1:
                return iters(_Stack).index(s)
            tup.append(iters(_Stack).index(s))
        return tuple(tup)

    except Exception:
        return -1


@export
def sinfo(_Stack) -> dict:
    """ Get all the information of the stack """
    global stack
    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)

    return {
        '<stack {}>'.format(type(_Stack.top).__name__ if not _Stack.empty else 'N'): '__sk1__',
        'Element': sub(r'\{', '', sub('}', '', str(_Stack))),
        'Length': _Stack.size,
        'Top': _Stack.top if not _Stack.empty else ''
    }


@export
def stsum(_Stack) -> int:
    """ Calculate the sum of elements in an int stack. """
    global stack
    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)
    result, _T = 0, _Stack._copy()

    while not _T.empty:
        if not isinstance(_T.top, int):
            return -1
        result += _T.top
        _T.pop()

    return result


@export
def ssort(_Stack, rule='+') -> None:
    """ Stack ascending / descending sorting. """
    global stack
    r = {'+': 1, '-': -1, 1: 1, -1: -1}

    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)

    if rule not in r:
        raise StackError('The rules are unclear')

    _it = iters(_Stack)
    for i in range(len(_it)):
        for j in range(len(_it) - i - 1):
            if _it[j] > _it[j + 1]:
                _it[j], _it[j + 1] = _it[j + 1], _it[j]
    _it = _it[::r[rule]]

    clear(_Stack)
    for item in _it:
        _Stack.push(item)


@export
def update(_Stack, *args) -> None:
    """ Combine multiple stacks into one """
    global stack
    if not isinstance(_Stack, stack):
        raise StackError('Type Error of ' + type(_Stack).__name__)

    for s in args:
        if not isinstance(s, stack):
            raise StackError('Type Error of ' + type(s).__name__)
        while not s.empty:
            _Stack.push(s.top)
            s.pop()




__all__ = ['stack', 'iters', 'stsum', 'update', 'clear', 'ssort', 'sinfo', 'move', 'seek', 'news']