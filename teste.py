
d = {
    "amigo" : [
        "Oi",
        "Tchau",
        "Oie"
    ],

    "inimigo": [
        "Perdeu",
        "Ganhou"
    ]
}

for (item, _) in d.items():
    if item in "amigo legal":
        print(item)