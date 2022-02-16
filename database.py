from pymongo import MongoClient


class DataBase:
    cluster = None
    db = None
    collection = None
    listOfTeams = []

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
        for document in self.collection.find({"_id": guild_id, "team": {"$exists": True}}):
            self.listOfTeams = document['team']

        if len(self.listOfTeams) > 0:
            return True
        else:
            return False

    def Define_Text_Channel(self, guild_id, channel_id):
        self.collection.update_one({"_id": guild_id}, {"$set": {"textChannelID": channel_id}})

    def Get_Text_Channel(self, guild_id):
        id = None
        for document in self.collection.find({"_id": guild_id, "textChannelID": {"$exists": True}}):
            id = document['textChannelID']

        if id is None:
            return None
        else:
            return id

    def Get_List_Teams_As_String(self, guild_id):
        if self.List_Teams(guild_id):
            return '\n'.join(self.listOfTeams)

    def Get_List_Teams(self, guild_id):
        if self.List_Teams(guild_id):
            return self.listOfTeams
