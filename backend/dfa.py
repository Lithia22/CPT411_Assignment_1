"""
CPT411 Assignment – L6: English Stop Words Finder
Pure DFA: explicit states for each stop word prefix.
Processes one character at a time.

States: q0=START, q1-q18=prefix states, q𝜙=trap/dead state
Stop words: and, the, then, so, into, if, with
"""

class StopWordDFA:
    """Pure DFA with explicit states. State numbers map to q0, q1, etc."""

    START = 0
    TRAP = -1

    # Accept states and their corresponding stop words
    ACCEPT_STATES = {
        3: "and",    # a → n → d
        6: "the",    # t → h → e
        7: "then",   # t → h → e → n
        9: "so",     # s → o
        13: "into",  # i → n → t → o
        14: "if",    # i → f
        18: "with",  # w → i → t → h
    }

    def __init__(self):
        self._reset()
        self._build_transitions()

    def _format_state(self, state):
        """Convert numeric state to readable format"""
        if state == self.TRAP:
            return "q𝜙" 
        return f"q{state}"

    def _reset(self):
        self.state = self.START
        self._word = ""
        self._word_start = 0
        self.matches = []
        self.trace = []

    def _build_transitions(self):
        """Build transition table δ(state, char) → next_state"""
        self.transitions = {}

        # State 0: START
        self.transitions[0] = {
            'a': 1,   # start of "and"
            't': 4,   # start of "the"/"then"
            's': 8,   # start of "so"
            'i': 10,  # start of "into"/"if"
            'w': 15,  # start of "with"
        }

        # "and" branch: a → n → d
        self.transitions[1] = {'n': 2}
        self.transitions[2] = {'d': 3}
        self.transitions[3] = {}

        # "the"/"then" branch: t → h → e → n
        self.transitions[4] = {'h': 5}
        self.transitions[5] = {'e': 6}
        self.transitions[6] = {'n': 7}
        self.transitions[7] = {}

        # "so" branch: s → o
        self.transitions[8] = {'o': 9}
        self.transitions[9] = {}

        # "into"/"if" branch: i → n → t → o  OR  i → f
        self.transitions[10] = {'n': 11, 'f': 14}
        self.transitions[11] = {'t': 12}
        self.transitions[12] = {'o': 13}
        self.transitions[13] = {}
        self.transitions[14] = {}

        # "with" branch: w → i → t → h
        self.transitions[15] = {'i': 16}
        self.transitions[16] = {'t': 17}
        self.transitions[17] = {'h': 18}
        self.transitions[18] = {}

    def _get_next_state(self, state, char):
        """Transition function δ(state, char) → next_state"""
        char = char.lower()
        if state == self.TRAP:
            return self.TRAP
        if state in self.transitions and char in self.transitions[state]:
            return self.transitions[state][char]
        return self.TRAP

    def transition(self, ch, index):
        """Process one character. Core DFA simulation."""
        from_state = self.state
        display = "[space]" if ch == " " else "[newline]" if ch == "\n" else ch
        action = ""

        if not ch.isalpha():
            # Non-letter: word boundary
            if self.state in self.ACCEPT_STATES and self._word:
                matched_word = self.ACCEPT_STATES[self.state]
                if len(self._word) == len(matched_word):
                    self.matches.append({
                        "word": self._word,
                        "lower": matched_word,
                        "start": self._word_start,
                        "end": index - 1
                    })
                    action = f'✓ STOP WORD: "{self._word}"'
                else:
                    action = f'✗ Not stop word: "{self._word}"'
            elif self.state != self.START and self.state != self.TRAP:
                action = f'✗ Not stop word: "{self._word}"'
            else:
                action = f'Skipped non-letter: "{display}"'
            self.state = self.START
            self._word = ""
            self.trace.append({
                "char": display,
                "fromState": self._format_state(from_state),
                "toState": self._format_state(self.state),
                "action": action
            })
            return

        # Letter: transition through DFA
        ch_lower = ch.lower()
        next_state = self._get_next_state(self.state, ch_lower)

        if next_state == self.TRAP:
            action = f"Invalid transition '{ch}' → TRAP"
            self.state = self.TRAP
        else:
            if self.state == self.START:
                self._word_start = index
                self._word = ch
                action = f'Started word: "{ch}"'
            else:
                self._word += ch
                action = f'Added "{ch}" → word: "{self._word}"'
            self.state = next_state

        self.trace.append({
            "char": display,
            "fromState": self._format_state(from_state),
            "toState": self._format_state(self.state),
            "action": action
        })

    def process(self, text):
        """Process entire text one character at a time."""
        self._reset()
        for i, ch in enumerate(text):
            self.transition(ch, i)

        # Check final word at end of text
        if self.state in self.ACCEPT_STATES and self._word:
            matched_word = self.ACCEPT_STATES[self.state]
            if len(self._word) == len(matched_word):
                self.matches.append({
                    "word": self._word,
                    "lower": matched_word,
                    "start": self._word_start,
                    "end": len(text) - 1
                })
                action = f'✓ STOP WORD at end: "{self._word}"'
            else:
                action = f'✗ Not stop word at end: "{self._word}"'
            self.trace.append({
                "char": "[END]",
                "fromState": self._format_state(self.state),
                "toState": self._format_state(self.START),
                "action": action
            })

        return {
            "status": "ACCEPTED" if self.matches else "REJECTED",
            "total": len(self.matches),
            "matches": self.matches,
            "trace": self.trace
        }


def run_dfa(text):
    """Called by server.py"""
    dfa = StopWordDFA()
    result = dfa.process(text)
    return {
        "count": result["total"],
        "matches": result["matches"],
        "trace": result["trace"]
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python dfa.py <textfile.txt>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()
    result = StopWordDFA().process(text)
    print(f"Status: {result['status']}, Total: {result['total']} stop words")
    for m in result['matches']:
        print(f"  {m['word']} at position {m['start']}-{m['end']}")