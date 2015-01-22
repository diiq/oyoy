class Stream(object):
    def __init__(self, string):
        self.string = string
        self.index = 0
        self.line_stack = []
        self.position_stack = []

    def set_index(self, n):
        while self.line_stack and self.line_stack[-1][0] > n:
            self.line_stack.pop()

        while self.position_stack and self.position_stack[-1][0] > n:
            self.position_stack.pop()

        self.index = n

    def track_position(self):
        if self.string[self.index] == "\n":
            self.position_stack.append((self.index, 0))
            self.line_stack.append((self.index, self.line() + 1))
        else:
            self.position_stack.append((self.index, self.position()))

    def eof(self):
        return self.index >= len(self.string)

    def get(self):
        if self.eof():
            raise EOFError()

        self.track_position()
        ret = self.string[self.index]
        self.index +=1

        return ret

    def get_n(self, n):
        ret = []
        for i in range(n):
            ret.append(self.get())

        return "".join(ret)

    def position(self):
        if self.position_stack:
            return self.position_stack[-1][1]
        return 0

    def line(self):
        if self.line_stack:
            return self.line_stack[-1][1]
        return 0
