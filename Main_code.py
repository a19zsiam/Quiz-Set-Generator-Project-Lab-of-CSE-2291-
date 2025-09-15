import mysql.connector as MyConn
import random, copy

# Database connect
mydb = MyConn.connect(
    host="localhost",
    user="root",
    password="Siam is a good boy",  
    database="QuizDB"
)
cursor = mydb.cursor(dictionary=True)

# Bring Questions
cursor.execute("SELECT * FROM questions")
rows = cursor.fetchall()

# Making Row to List
questions = []
for row in rows:
    q = {
        "question": row["question_text"],
        "options": [row["option_a"], row["option_b"], row["option_c"], row["option_d"]],
        "correct_idx": row["correct_idx"]
    }
    questions.append(q)

labels = ["A", "B", "C", "D"]

def shuffle_options(q):
    opts = q["options"][:]
    idx = q["correct_idx"]
    pairs = list(enumerate(opts))
    random.shuffle(pairs)
    new_opts = [t for (_, t) in pairs]
    new_correct = next(i for i, (old, _) in enumerate(pairs) if old == idx)
    return new_opts, new_correct

# ==== User Input ====
num_sets = int(input("How many sets do you want?"))
# ====================

for s in range(1, num_sets + 1):
    print(f"\n===== Quiz Set {s} =====")

    q_copy = copy.deepcopy(questions)
    random.shuffle(q_copy)

    new_qs = []
    for q in q_copy:
        opts, corr = shuffle_options(q)
        new_qs.append({
            "question": q["question"],
            "options": opts,
            "correct_idx": corr
        })

    for i, q in enumerate(new_qs, 1):
        print(f"{i}. {q['question']}")
        for j, opt in enumerate(q["options"]):
            print(f"   {labels[j]}. {opt}")
        print()

    print("Answer Key:")
    for i, q in enumerate(new_qs, 1):
        print(f"{i}. {labels[q['correct_idx']]}")
