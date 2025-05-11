from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self.next_states: list[State] = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in self.next_states:
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")


class StartState(State):
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return True


class TerminationState(State):
    def __init__(self):
        super().__init__()

    def check_self(self, char):
        return False


class DotState(State):
    """
    state for . character (any character accepted)
    """
    def __init__(self):
        super().__init__()

    def check_self(self, char: str) -> bool:
        return True


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol

    def check_self(self, curr_char: str) -> bool:
        return self.symbol == curr_char


class AsciiClassState(State):
    """
    state for [a-zA-Z0-9] character
    """

    def __init__(self, symbols: str) -> None:
        super().__init__()
        self.symbols = self.__get_chars(symbols)

    def __get_chars(self, symbols: str) -> set[str]:
        size = len(symbols)
        i = 0
        new_syms = set()
        while i < size:
            if (i + 2) < size and symbols[i + 1] == '-':
                start, end = ord(symbols[i]), ord(symbols[i + 2])
                new_syms.update(chr(i) for i in range(start, end + 1))
                i += 3
                continue
            else:
                new_syms.add(symbols[i])
            i += 1
        return new_syms

    def check_self(self, curr_char: str) -> bool:
        return curr_char in self.symbols


class StarState(State):
    def __init__(self, checking_state: State):
        super().__init__()
        self.next_states.append(self)
        self.next_states.append(checking_state)
        self.checking_state = checking_state

    def check_self(self, char):
        return self.checking_state.check_self(char)


class PlusState(State):
    def __init__(self, checking_state: State):
        super().__init__()
        self.checking_state = checking_state
        self.next_states.append(self)
        self.next_states[0].next_states.append(checking_state)

    def check_self(self, char):
        return self.checking_state.check_self(char)


class RegexFSM:
    def __init__(self, regex_expr: str) -> None:
        if not set(regex_expr) <= set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.*+[]-'):
            raise AttributeError("Character is not supported")
        self.curr_state = StartState()

        prev_stars: set[State] = {self.curr_state}
        curr_state = self.curr_state

        size = len(regex_expr)
        i = 0
        while i < size:
            curr_char = regex_expr[i]
            j = 0
            if curr_char == '[':
                j = 1
                while regex_expr[i + j] != ']':
                    j += 1
                curr_char = regex_expr[i + 1:i + j]
            try:
                next_char = regex_expr[i + 1 + j]
            except IndexError:
                next_char = None
            tmp_next_state, skip = self.__init_next_state(curr_char, next_char)
            curr_state.next_states.append(tmp_next_state)
            prev_state = curr_state
            curr_state = tmp_next_state
            if prev_stars and not isinstance(prev_state, StartState | StarState) and (i + skip) < size:
                prev_stars.clear()
            for prev_star in prev_stars - {prev_state}:
                prev_star.next_states.append(tmp_next_state)
            # if isinstance(tmp_next_state, StarState):
            prev_stars.add(tmp_next_state)

            i += skip
        if not isinstance(curr_state, StarState):
            prev_stars.clear()

        for prev_star in prev_stars - {curr_state}:
            prev_star.next_states.append(TerminationState())
        curr_state.next_states.append(TerminationState())

    def __init_next_state(self, next_token: str, after_token: str | None = None) -> tuple[State, int]:
        if len(next_token) > 1 and after_token not in {'*', '+'}:
            new_state = AsciiClassState(next_token)
            return new_state, len(next_token) + 2

        if after_token == '*':
            state, j = self.__init_next_state(next_token)
            return StarState(state), 2 + j - 1

        if after_token == '+':
            state, j = self.__init_next_state(next_token)
            return PlusState(state), 2 + j - 1

        match next_token:
            case next_token if next_token == ".":
                new_state = DotState()
            case next_token if next_token.isascii():
                new_state = AsciiState(next_token)
            case _:
                raise AttributeError("Character is not supported")

        return new_state, 1

    def check_string(self, string: str) -> bool:
        """Function checks whether string is accepted by regex"""
        curr_states = self.curr_state.next_states
        next_states = []
        for char in string:
            for state in curr_states:
                if state.check_self(char):
                    next_states.extend(state.next_states)
            curr_states, next_states = next_states, []

        if any(isinstance(state, TerminationState) for state in curr_states):
            return True
        return False


if __name__ == "__main__":
    r = 'ab*'
    regex_compiled = RegexFSM(r)
    print(regex_compiled.check_string("a"))  # False

    regex_pattern = "a*4.+hi"

    regex_compiled = RegexFSM(regex_pattern)

    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))  # True
    print(regex_compiled.check_string("meow"))  # False