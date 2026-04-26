# CPT411 Assignment 1 – DFA Recognizer

**Team Members:**

- Kavitashini A/P Seluvarajoo
- Lithia A/P Kisnen
- Neeshaneir A/P K Gangadharan

---

## Language Description

The DFA recognizes 25 English stop words across multiple categories:

| Category     | Words                                 |
| ------------ | ------------------------------------- |
| Articles     | a, an, the                            |
| Prepositions | as, at, by, for, in, into, of, on, to |
| Conjunctions | and, but, if, or, so                  |
| Pronouns     | i, it, you, we, they                  |
| Modals       | be, can                               |
| Other        | is                                    |

---

## DFA Specifications

- **Start State:** q0
- **Trap State:** -1 (dead state)
- **States:** q0 to q44 (45 states)
- **Processes text one character at a time** from left to right
- **Non-letters act as word boundaries** (spaces, commas, periods, etc.)
- **Undefined transitions go to trap state**

The DFA reads text **character by character**, detects word boundaries using spaces and punctuation, and moves to the trap state (-1) when no valid transition exists.

---

## Outputs

1. Status (ACCEPTED / REJECTED)
2. Stop word found
3. Position (start–end index)
4. Number of occurrences
5. Boldface visualization (yellow highlight in text)
6. Character-by-character process trace

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Lithia22/CPT411_Assignment_1.git
cd CPT411_Assignment_1
```

### 2. Set up backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3. Open in browser

Go to `http://localhost:5000`
