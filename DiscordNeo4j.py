# pip3 install neo4j-driver
# python3 example.py
from codecs import ignore_errors
import os
import csv
import re
from pandas import read_csv
from py2neo import Graph, Node, Relationship
import glob
from neo4j import GraphDatabase, basic_auth


graph = Graph("bolt://3.239.191.198:7687",
    auth=("neo4j", "blanks-prisons-activities"),)


DataFiles =  glob.glob("/Users/skalthoff/Code/DiscordDms/*.csv")


#print(DataFiles)

#print(type(DataFiles))

def ProcessFile(filename):
    filePath = filename
    with open(filePath, mode="r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mentionList = [s.split("#")[0] for s in re.findall('@([A-Za-z0-9_]+)', row["Content"])]
            
            
            
            if len(mentionList) > 0:
                
                
                a = Node("User", name=row["Author"].split("#")[0])
                #tx = graph.begin()
                #tx.create(a)
                for mention in mentionList:
                    b = Node("User", name=mention)
                    KNOWS = Relationship.type("KNOWS")
                    ab = Relationship(a, "MENTIONS", b)
                    #tx.create(ab)
                graph.merge(ab, "User", "name")
                #tx.commit()
                #create a node for the sender of the message if it doesn't exist and then create a relationship to the mentioned user if it doesn't exist, if it does exist, then just create the relationship

def breakout_mentions(file, outputFile):
    with open(file, mode="r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            mentionList = [ s.split("#")[0] for s in re.findall('@([A-Za-z0-9_]+)', row["Content"])]
            #remove item from list if it contains .com
            cleanList = [item for item in mentionList if ".com" not in item]
            mentionList = cleanList
            print(mentionList)
            if len(mentionList) > 0:
                for mention in mentionList:
                    with open(outputFile, 'a') as output:
                        writer = csv.DictWriter(output, fieldnames=["Author", "Mention"])
                        for mention in mentionList:
                            writer.writerow({"Author": row["Author"].split("#")[0], "Mention": mention})

def main():
    for file in DataFiles:
        if file.endswith(".csv"):
            breakout_mentions(file, "mentions.csv")
            print("Processing: " + file.split('/')[-1])


main()
#with driver.session(database="neo4j") as session:
