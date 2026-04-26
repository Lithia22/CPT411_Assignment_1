"""
CPT411 Assignment – L6: English Stop Words Finder
Pure DFA: explicit states for each stop word prefix.
Processes one character at a time.

Stop Words (25 words):
======================
Articles (3):     a, an, the
Prepositions (9): as, at, by, for, in, into, of, on, to
Conjunctions (5): and, but, if, or, so
Pronouns (5):     i, it, you, we, they
Modals (2):       be, can
Other (1):        is

Detects 25 English stop words and displays status, positions, counts, DFA trace, and highlighted text.
"""


class StopWordDFA:
    """Pure DFA with explicit states. State numbers map to q0, q1, etc."""

    # DFA Constants
    START = 0
    TRAP = -1

    # Accept States
    ACCEPT_STATES = {
        # Articles
        1: "a",
        2: "an",
        29: "the",

        # Prepositions
        4: "as",
        5: "at",
        10: "by",
        13: "for",
        16: "in",
        18: "into",
        22: "of",
        23: "on",
        31: "to",

        # Conjunctions
        3: "and",
        9: "but",
        15: "if",
        24: "or",
        26: "so",

        # Pronouns
        14: "i",
        20: "it",
        34: "you",
        36: "we",
        40: "they",

        # Modals
        7: "be",
        44: "can",

        # Other
        19: "is",
    }

    # ────────────────────────────────────────────────────────────────────────
    # Initialization
    # ────────────────────────────────────────────────────────────────────────
    def __init__(self):
        self._reset()
        self._build_transitions()

    def _reset(self):
        """Reset DFA state for a new text scan."""
        self.state = self.START
        self._word = ""
        self._word_start = 0
        self.matches = []
        self.trace = []

    def _format_state(self, state):
        """Convert numeric state to readable format (q0, q1, -1 for trap)."""
        if state == self.TRAP:
            return "-1"
        return f"q{state}"

    # ────────────────────────────────────────────────────────────────────────
    # Transition Table
    # ────────────────────────────────────────────────────────────────────────
    def _build_transitions(self):
        """Build δ(state, char) → next_state. Missing transitions go to TRAP."""
        self.transitions = {}

        # State 0: START
        self.transitions[0] = {
            'a': 1, 
            'b': 6, 
            'c': 42, 
            'f': 11, 
            'i': 14,
            'o': 21, 
            's': 25, 
            't': 27, 
            'w': 35, 
            'y': 32,
        }

        # ── a branch: a, an, and, as, at ─────────────────────────────────────
        self.transitions[1] = {'n': 2, 's': 4, 't': 5}
        self.transitions[2] = {'d': 3}
        self.transitions[3] = {}   # and
        self.transitions[4] = {}   # as
        self.transitions[5] = {}   # at

        # ── b branch: be, but, by ───────────────────────────────────────────
        self.transitions[6] = {'e': 7, 'u': 8, 'y': 10}
        self.transitions[7] = {}   # be
        self.transitions[8] = {'t': 9}
        self.transitions[9] = {}   # but
        self.transitions[10] = {}  # by

        # ── c branch: can ───────────────────────────────────────────────────
        self.transitions[42] = {'a': 43}
        self.transitions[43] = {'n': 44}
        self.transitions[44] = {}  # can

        # ── f branch: for ───────────────────────────────────────────────────
        self.transitions[11] = {'o': 12}
        self.transitions[12] = {'r': 13}
        self.transitions[13] = {}  # for

        # ── i branch: i, if, in, into, is, it ───────────────────────────────
        self.transitions[14] = {'f': 15, 'n': 16, 's': 19, 't': 20}
        self.transitions[15] = {}  # if
        self.transitions[16] = {'t': 17}
        self.transitions[17] = {'o': 18}
        self.transitions[18] = {}  # into
        self.transitions[19] = {}  # is
        self.transitions[20] = {}  # it

        # ── o branch: of, on, or ────────────────────────────────────────────
        self.transitions[21] = {'f': 22, 'n': 23, 'r': 24}
        self.transitions[22] = {}  # of
        self.transitions[23] = {}  # on
        self.transitions[24] = {}  # or

        # ── s branch: so ────────────────────────────────────────────────────
        self.transitions[25] = {'o': 26}
        self.transitions[26] = {}  # so

        # ── t branch: the (q29), they (q40), to (q31) ───────────────────────
        self.transitions[27] = {'h': 28, 'o': 31}
        self.transitions[28] = {'e': 29}
        self.transitions[29] = {'y': 40}   # "they" continues from "the"
        self.transitions[31] = {}          # "to"
        self.transitions[40] = {}          # "they"

        # ── w branch: we ────────────────────────────────────────────────────
        self.transitions[35] = {'e': 36}
        self.transitions[36] = {}  # we

        # ── y branch: you ───────────────────────────────────────────────────
        self.transitions[32] = {'o': 33}
        self.transitions[33] = {'u': 34}
        self.transitions[34] = {}  # you

    # ────────────────────────────────────────────────────────────────────────
    # Transition Function
    # ────────────────────────────────────────────────────────────────────────
    def _get_next_state(self, state, char):
        """δ(state, char) → next_state. Returns TRAP if no transition exists."""
        char = char.lower()
        if state == self.TRAP:
            return self.TRAP
        if state in self.transitions and char in self.transitions[state]:
            return self.transitions[state][char]
        return self.TRAP

    # ────────────────────────────────────────────────────────────────────────
    # Core DFA Simulation
    # ────────────────────────────────────────────────────────────────────────
    def transition(self, ch, index):
        """
        Process one character through the DFA.

        - Non-letters act as word boundaries → reset and check for matches
        - Letters follow transition function; TRAP kills the current word
        - Length check prevents substring matches (e.g., "and" in "android")
        """
        from_state = self.state
        display = "[space]" if ch == " " else "[newline]" if ch == "\n" else ch
        action = ""

        # Word boundary (non-letter)
        if not ch.isalpha():
            if self.state in self.ACCEPT_STATES and self._word:
                matched_word = self.ACCEPT_STATES[self.state]
                # Length check prevents "and" matching inside "android"
                if len(self._word) == len(matched_word):
                    self.matches.append({
                        "word": self._word,
                        "lower": matched_word,
                        "start": self._word_start,
                        "end": index - 1
                    })
                    action = f'✓ STOP WORD: "{self._word}"'
                else:
                    action = f'✗ Not a stop word: "{self._word}"'
            elif self.state != self.START and self.state != self.TRAP:
                action = f'✗ Not a stop word: "{self._word}"'
            else:
                action = f'Skipped: "{display}"'

            self.state = self.START
            self._word = ""
            self.trace.append({
                "char": display,
                "fromState": self._format_state(from_state),
                "toState": self._format_state(self.START),
                "action": action
            })
            return

        # Letter: transition through DFA
        ch_lower = ch.lower()
        next_state = self._get_next_state(self.state, ch_lower)

        if self.state == self.START:
            self._word_start = index
            self._word = ch
        else:
            self._word += ch

        if next_state == self.TRAP:
            action = f'No transition for "{ch}" → TRAP'
            self.state = self.TRAP
        else:
            action = f'Added "{ch}" → word: "{self._word}"'
            if next_state in self.ACCEPT_STATES:
                action += f' (possible: "{self.ACCEPT_STATES[next_state]}")'
            self.state = next_state

        self.trace.append({
            "char": display,
            "fromState": self._format_state(from_state),
            "toState": self._format_state(self.state),
            "action": action
        })

    # ────────────────────────────────────────────────────────────────────────
    # Full Text Processing
    # ────────────────────────────────────────────────────────────────────────
    def process(self, text):
        """Process entire text one character at a time."""
        self._reset()

        for i, ch in enumerate(text):
            self.transition(ch, i)

        # Handle final word at end of text (no trailing boundary)
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
                action = f'✗ Not a stop word at end: "{self._word}"'
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


# ────────────────────────────────────────────────────────────────────────
# Module Interface (for app.py)
# ────────────────────────────────────────────────────────────────────────
def run_dfa(text):
    """Entry point for Flask backend. Returns matches, count, and trace."""
    dfa = StopWordDFA()
    result = dfa.process(text)
    return {
        "count": result["total"],
        "matches": result["matches"],
        "trace": result["trace"]
    }