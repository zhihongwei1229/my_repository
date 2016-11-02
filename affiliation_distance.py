from databaseConnection import Database

data = Database()
affiliation = data.getAffiliationToken()

print(affiliation)
