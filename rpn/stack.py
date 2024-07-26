class Stack:
    _id_counter = 0

    def __init__(self):
        Stack._id_counter += 1
        self.id = Stack._id_counter
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def _ensure_minimum_elements(self, count=2):
        if len(self.stack) < count:
            raise ValueError(f"Need at least {count} elements to perform this operation.")

    def add(self):
        self._ensure_minimum_elements()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)
        return self.stack[-1]

    def subtract(self):
        self._ensure_minimum_elements()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)
        return self.stack[-1]

    def multiply(self):
        self._ensure_minimum_elements()
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)
        return self.stack[-1]

    def divide(self):
        self._ensure_minimum_elements()
        b = self.stack.pop()
        a = self.stack.pop()
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        self.stack.append(a / b)
        return self.stack[-1]

    def clear(self):
        self.stack = []

    def __repr__(self):
        return f"Stack(id={self.id}, stack={self.stack})"

    def to_dict(self):
        return {
            'id': self.id,
            'stack': self.stack
        }
