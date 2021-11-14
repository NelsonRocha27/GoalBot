from pymongo import MongoClient


class DataBase:
    cluster = None
    db = None
    collection = None
    listOfTeams = None

    def __init__(self, url):
        self.cluster = MongoClient(url)
        self.db = self.cluster["GoalBotDB"]
        self.collection = self.db["Teams"]

    def Add_Team(self, guild_id, team):
        guildIDQuery = {"_id": guild_id}
        if self.collection.count_documents(guildIDQuery) == 0:
            post = {"_id": guild_id, "team": [team]}
            self.collection.insert_one(post)
        else:
            guild = self.collection.find(guildIDQuery)
            for result in guild:
                listOfTeams = result["team"]
            listOfTeams.append(team)
            self.collection.update_one({"_id": guild_id}, {"$set": {"team": listOfTeams}})

    def List_Teams(self, guild_id):
        listOfTeamsArray = []
        for document in self.collection.find({"_id": guild_id, "team": {"$exists": True}}):
            listOfTeamsArray = document['team']

        if len(listOfTeamsArray) > 0:
            self.listOfTeams = "\n".join(listOfTeamsArray)
            return True
        else:
            return False
