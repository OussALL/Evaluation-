import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

def make_graph(valeurs, qst_number, subject_id, classe_id):
    sections = [
        "Très insatisfaisant",
        "Insatisfaisant",
        "Moyen",
        "Satisfaisant",
        "Très satisfaisant"
    ]
    
    valeurs_non_zero = [v for v in valeurs if v > 0]
    labels_non_zero = [sections[i] for i, v in enumerate(valeurs) if v > 0]

    plt.figure(figsize=(6, 6))
    plt.pie(
        valeurs_non_zero, 
        labels=labels_non_zero, 
        autopct='%1.1f%%', 
        startangle=90, 
        textprops={'fontsize': 10}
    )
    plt.title(f"Répartition des réponses à la question Q{qst_number}", fontsize=14)
    plt.axis('equal')  
    plt.tight_layout()
    plt.savefig(f".venv/static/graphs/q{qst_number}_{subject_id}_{classe_id}.png")
    plt.close()  