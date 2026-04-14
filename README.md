# CPT411 Assignment 1 – DFA Recognizer

**Course:** CPT411 – Automata Theory & Formal Languages
**Language:** English Stop Words Finder

**Team Members:**

- Kavitashini A/P Seluvarajoo
- Lithia A/P Kisnen
- Neeshaneir A/P K Gangadharan

---

## What It Does

A Deterministic Finite Automaton (DFA) that reads text **one character at a time** to detect English stop words (and, the, then, so, into, if, with).

**Outputs:**

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
