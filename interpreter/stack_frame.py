class StackFrame():
    def __init__(self, instructions, env):
        self.instructions = instructions
        self.env = env
        self.new_env = None

    def next(self):
        if self.instructions == []:
            return None
        return self.instructions.pop()

    def push(self, instruction):
        self.instructions.append(instruction)
