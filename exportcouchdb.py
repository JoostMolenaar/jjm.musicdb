import MySQLdb
import MySQLdb.cursors

from itertools import groupby

conn = MySQLdb.connect(user='root', passwd='mysqlroot', db='musicdb', use_unicode='True', charset='utf8')

cursor = conn.cursor(MySQLdb.cursors.DictCursor)
cursor.execute('SELECT * FROM `label`')

def query(sql, args=(), index_by=None, group_by=None):
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql, *args)
    result = cursor.fetchall()
    if index_by is not None:
        result = { row[index_by]: row for row in result }
    if group_by is not None:
        result = { key: list(rows) for (key, rows) in groupby(result, lambda row: row[group_by]) }
    return result

#labels = { row["LabelID"]: row for row in query("SELECT * FROM `label`") }
#artists = { row["ArtistID"]: row for row in query("SELECT * FROM `artist`") }
#formats = { row["FormatID"]: row for row in query("SELECT * FROM `format`") }
#artist_releases = query("SELECT * FROM `artist_release`")
#releases = { row["ReleaseID"]: row for row in query("SELECT * FROM `release`") }
#artist_groups = query("SELECT * FROM `artist_group`")

labels = query("SELECT * FROM `label`", index_by="LabelID")
artists = query("SELECT * FROM `artist`", index_by="ArtistID")
formats = query("SELECT * FROM `format`", index_by="FormatID")
releases = query("SELECT * FROM `release`", index_by="ReleaseID")

artist_releases = query("SELECT * FROM `artist_release`", group_by="ReleaseID")
artist_groups = query("SELECT * FROM `artist_group`", group_by="GroupID")

from pprint import pprint

#pprint(labels)
#pprint(artists)
#pprint(formats)
#pprint(releases)

#pprint(artist_releases)
#pprint(artist_groups)

json_release = [ 
    {
        "type": "release",
        "name": r["Name"],
        "label": labels[r["LabelID"]]["Name"],
        "catno": r["CatNo"],
        "format": formats[r["FormatID"]]["Name"],
        "artists": [ artists[ar["ArtistID"]]["Name"] for ar in artist_releases[r["ReleaseID"]] ],
        "year": r["Year"]
    } for r in releases.values() ]

pprint(json_release)

import couchdb
db = couchdb.Server()["musicdb"]

for x in json_release:
    print db.save(x)

# Release -
# 
# {
#     "name": "Soundboy's ashes get hacked up and spat out in disgust EP",
#     "artists": [
#         "Appleblim",
#         "Peverelist"
#     ],
#     "label": "Skull Disco",
#     "catno": "SKULL008",
#     "year": 2008,
#     "format": "12\""
# }
# 
# Label -
# 
# {
#     "name": "[i/cm]",
#     "parent": "Imbalance Recordings"
# }
# 
# Artist #1 -
# 
# {
#     "name": "Vladislav Delay",
#     "aliasfor": "Sasu Ripatti",
#     "ingroups": [
#         "Moritz Von Oswald Trio"
#     ]
# }
# 
# Artist #2 -
# 
# {
#     "name": "Moritz Von Oswald Trio",
#     "aliasfor": null,
#     "members": [
#         "Moritz Von Oswald",
#         "Vladislav Delay",
#         "Max Loderbauer"
#     ]
# }


