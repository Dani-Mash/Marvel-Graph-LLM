"""
generate_data.py  –  Project Gene‑Forge dataset creator
------------------------------------------------------
Outputs:
  data/characters.csv   data/teams.csv       data/genes.csv      data/powers.csv
  data/char_team.csv    data/char_gene.csv   data/gene_power.csv data/char_power.csv
  data/text_snippets.json
  data/marvel_kg.graphml
  data/neo4j_load.cypher      # optional helper for Neo4j bulk import
"""

import csv, json, os, textwrap, networkx as nx
from pathlib import Path


# ────────────────────────────────────────────────────────────────────────────────
# 1.  Source‑of‑truth list  (edit / extend here)
# ────────────────────────────────────────────────────────────────────────────────
CHARACTERS = [
    dict(
        name="Wolverine",
        team="X‑Men",
        gene="Regenerative Mutation",
        powers=["Accelerated Healing", "Enhanced Senses"],
        snippet=(
            "Born as James Howlett in 19th‑century Canada, Wolverine endured Weapon X "
            "experiments that bonded adamantium to his skeleton. His healing factor, "
            "heightened senses, and combat mastery make him the X‑Men’s fiercest defender."
        ),
    ),
    dict(
        name="Cyclops",
        team="X‑Men",
        gene="Optic‑Blast",
        powers=["Optic Blasts"],
        snippet=(
            "Scott Summers unleashes concussive optic beams and leads the X‑Men with "
            "military precision. Ruby‑quartz visors let him control power that could "
            "otherwise shatter mountains."
        ),
    ),
    dict(
        name="Storm",
        team="X‑Men",
        gene="Weather Manipulation",
        powers=["Weather Control"],
        snippet=(
            "Ororo Munroe commands atmospheric forces, summoning hurricanes or gentle "
            "rains at will. Worshipped as a goddess in Africa, she balances power with "
            "deep empathy and meditation."
        ),
    ),
    dict(
        name="Jean Grey",
        team="X‑Men",
        gene="Omega Level Telepathy",
        powers=["Telepathy", "Telekinesis"],
        snippet=(
            "An omega‑level mutant, Jean Grey wields formidable telepathy and telekinesis. "
            "Her bond with the Phoenix Force makes her a symbol of rebirth and cosmic power."
        ),
    ),
    dict(
        name="Spider‑Man",
        team="Avengers",
        gene="Radioactive Spider Mutation",
        powers=["Superhuman Agility", "Enhanced Strength"],
        snippet=(
            "After a radioactive spider bite, Peter Parker gained wall‑crawling, spider‑sense, "
            "and super strength. Guided by the mantra ‘With great power comes great "
            "responsibility,’ he protects New York with wit and science."
        ),
    ),
    dict(
        name="Hulk",
        team="Avengers",
        gene="Gamma Radiation Mutation",
        powers=["Superhuman Strength"],
        snippet=(
            "Gamma radiation turned Bruce Banner into the Hulk, whose strength scales with "
            "anger. Feared as a walking cataclysm yet trusted by the Avengers in dire battles."
        ),
    ),
    dict(
        name="Captain America",
        team="Avengers",
        gene="Super‑Soldier Serum",
        powers=["Enhanced Strength"],
        snippet=(
            "Steve Rogers, enhanced to peak human condition by the Super‑Soldier Serum, "
            "wields an indestructible vibranium shield and serves as the moral compass of "
            "the Avengers."
        ),
    ),
    dict(
        name="Black Panther",
        team="Avengers",
        gene="Heart‑Shaped Herb",
        powers=["Enhanced Senses", "Enhanced Strength"],
        snippet=(
            "T’Challa, king of Wakanda, gains heightened abilities from the heart‑shaped herb "
            "and dons a vibranium‑woven suit, blending ancient tradition with futuristic tech."
        ),
    ),
    dict(
        name="Magneto",
        team="Brotherhood of Mutants",
        gene="Magnetokinesis",
        powers=["Magnetism Control"],
        snippet=(
            "Erik Lehnsherr manipulates magnetic fields on a planetary scale, driven by a "
            "resolve that mutants must never suffer oppression again."
        ),
    ),
    dict(
        name="Scarlet Witch",
        team="Avengers",
        gene="Chaos Magic",
        powers=["Reality Manipulation"],
        snippet=(
            "Wanda Maximoff’s chaos magic can rewrite reality itself. Her struggle for control "
            "makes her both invaluable ally and existential threat."
        ),
    ),
]


# ────────────────────────────────────────────────────────────────────────────────
# 2.  ID assignment helpers
# ────────────────────────────────────────────────────────────────────────────────
def next_id(counter: dict, key: str) -> int:
    counter.setdefault(key, len(counter) + 1)
    return counter[key]


team_ids, gene_ids, power_ids = {}, {}, {}
rows = {
    "characters": [],
    "teams": [],
    "genes": [],
    "powers": [],
    "char_team": [],
    "char_gene": [],
    "gene_power": [],
    "char_power": [],
}
snippets = []

for cid, hero in enumerate(CHARACTERS, start=1):
    # — Character node
    rows["characters"].append({"character_id": cid, "name": hero["name"]})

    # — Team
    tid = next_id(team_ids, hero["team"])
    if tid == len(rows["teams"]) + 1:  # new
        rows["teams"].append({"team_id": tid, "name": hero["team"]})
    rows["char_team"].append({"character_id": cid, "team_id": tid})

    # — Gene
    gid = next_id(gene_ids, hero["gene"])
    if gid == len(rows["genes"]) + 1:
        rows["genes"].append({"gene_id": gid, "name": hero["gene"]})
    rows["char_gene"].append({"character_id": cid, "gene_id": gid})

    # — Powers
    for power in hero["powers"]:
        pid = next_id(power_ids, power)
        if pid == len(rows["powers"]) + 1:
            rows["powers"].append({"power_id": pid, "name": power})
        rows["gene_power"].append({"gene_id": gid, "power_id": pid})
        rows["char_power"].append({"character_id": cid, "power_id": pid})

    # — Snippet
    snippets.append({"character": hero["name"], "snippet": hero["snippet"]})


# ────────────────────────────────────────────────────────────────────────────────
# 3.  Write CSVs + JSON
# ────────────────────────────────────────────────────────────────────────────────
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def write_csv(name: str, header_keys: list[str]):
    with open(DATA_DIR / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header_keys)
        writer.writeheader()
        writer.writerows(rows[name])

write_csv("characters", ["character_id", "name"])
write_csv("teams", ["team_id", "name"])
write_csv("genes", ["gene_id", "name"])
write_csv("powers", ["power_id", "name"])
write_csv("char_team", ["character_id", "team_id"])
write_csv("char_gene", ["character_id", "gene_id"])
write_csv("gene_power", ["gene_id", "power_id"])
write_csv("char_power", ["character_id", "power_id"])

# snippets
with open(DATA_DIR / "text_snippets.json", "w", encoding="utf-8") as f:
    json.dump(snippets, f, indent=2, ensure_ascii=False)

print("✓ CSVs & snippets written to ./data")


# ────────────────────────────────────────────────────────────────────────────────
# 4.  Build an in‑memory graph and export to GraphML
# ────────────────────────────────────────────────────────────────────────────────
G = nx.MultiDiGraph()

# Add nodes with actual entity names as IDs
for r in rows["characters"]:
    G.add_node(r["name"], label="Character", name=r["name"])
for r in rows["teams"]:
    G.add_node(r["name"], label="Team", name=r["name"])
for r in rows["genes"]:
    G.add_node(r["name"], label="Gene", name=r["name"])
for r in rows["powers"]:
    G.add_node(r["name"], label="Power", name=r["name"])

# Add edges using actual entity names
for r in rows["char_team"]:
    char_name = next(c["name"] for c in rows["characters"] if c["character_id"] == r["character_id"])
    team_name = next(t["name"] for t in rows["teams"] if t["team_id"] == r["team_id"])
    G.add_edge(char_name, team_name, type="MEMBER_OF")

for r in rows["char_gene"]:
    char_name = next(c["name"] for c in rows["characters"] if c["character_id"] == r["character_id"])
    gene_name = next(g["name"] for g in rows["genes"] if g["gene_id"] == r["gene_id"])
    G.add_edge(char_name, gene_name, type="HAS_MUTATION")

for r in rows["gene_power"]:
    gene_name = next(g["name"] for g in rows["genes"] if g["gene_id"] == r["gene_id"])
    power_name = next(p["name"] for p in rows["powers"] if p["power_id"] == r["power_id"])
    G.add_edge(gene_name, power_name, type="CONFERS")

for r in rows["char_power"]:
    char_name = next(c["name"] for c in rows["characters"] if c["character_id"] == r["character_id"])
    power_name = next(p["name"] for p in rows["powers"] if p["power_id"] == r["power_id"])
    G.add_edge(char_name, power_name, type="POSSESSES_POWER")

nx.write_graphml(G, DATA_DIR / "marvel_kg.graphml")
print("✓ GraphML written to ./data/marvel_kg.graphml")


# ────────────────────────────────────────────────────────────────────────────────
# 5.  Optional: generate Cypher loader
# ────────────────────────────────────────────────────────────────────────────────
#cypher = textwrap.dedent(
#    """
#    USING PERIODIC COMMIT 500
#    LOAD CSV WITH HEADERS FROM 'file:///characters.csv' AS row
#    MERGE (c:Character {id: toInteger(row.character_id)}) SET c.name = row.name;
#
#    LOAD CSV WITH HEADERS FROM 'file:///teams.csv' AS row
#    MERGE (t:Team {id: toInteger(row.team_id)}) SET t.name = row.name;
#
#    LOAD CSV WITH HEADERS FROM 'file:///genes.csv' AS row
#    MERGE (g:Gene {id: toInteger(row.gene_id)}) SET g.name = row.name;
#
#    LOAD CSV WITH HEADERS FROM 'file:///powers.csv' AS row
#    MERGE (p:Power {id: toInteger(row.power_id)}) SET p.name = row.name;
#
#    LOAD CSV WITH HEADERS FROM 'file:///char_team.csv' AS row
#    MATCH (c:Character {id: toInteger(row.character_id)}),
#          (t:Team {id: toInteger(row.team_id)})
#    MERGE (c)-[:MEMBER_OF]->(t);
#
#    LOAD CSV WITH HEADERS FROM 'file:///char_gene.csv' AS row
#    MATCH (c:Character {id: toInteger(row.character_id)}),
#          (g:Gene {id: toInteger(row.gene_id)})
#    MERGE (c)-[:HAS_MUTATION]->(g);
#
#    LOAD CSV WITH HEADERS FROM 'file:///gene_power.csv' AS row
#    MATCH (g:Gene {id: toInteger(row.gene_id)}),
#          (p:Power {id: toInteger(row.power_id)})
#    MERGE (g)-[:CONFERS]->(p);
#
#    LOAD CSV WITH HEADERS FROM 'file:///char_power.csv' AS row
#    MATCH (c:Character {id: toInteger(row.character_id)}),
#          (p:Power {id: toInteger(row.power_id)})
#    MERGE (c)-[:POSSESSES_POWER]->(p);
#    """
#).strip()

#with open(DATA_DIR / "neo4j_load.cypher", "w", encoding="utf‑8") as f:
#    f.write(cypher)
#print("✓ Cypher loader written to ./data/neo4j_load.cypher")
