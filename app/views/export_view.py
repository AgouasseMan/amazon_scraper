
import csv
from config import CSV_PATH


def exporter_csv(produits):
    if not produits:
        print("Aucun produit à exporter.")
        return

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    champs = ["nom", "prix", "note", "lien"]

    with open(
        CSV_PATH,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as fichier:

        writer = csv.DictWriter(
            fichier,
            fieldnames=champs,
            quoting=csv.QUOTE_ALL
        )

        writer.writeheader()

        for produit in produits:
            writer.writerow({
                "nom": produit.nom,
                "prix": produit.prix,
                "note": produit.note,
                "lien": produit.lien
            })

    print(f"Export terminé : {CSV_PATH}")

