from pymongo import MongoClient

class db_connector:
    def __init__(self, db_name = "jam_db", drop_db = False):
        self.client = MongoClient('localhost', 27017)
        if drop_db:
            self.client.drop_database(db_name)
        self.db = self.client[db_name]
        self.jobs_table = self.create_table("jobs")
        # self.user_table = self.create_table("users")

    def create_table(self, collection_name):
        return self.db[collection_name]

    def insert(self, item, table):
        table.insert_one(item)

    def update_company_location_if_exists(self, item):
        # print(item["company"])
        result = self.jobs_table.find({"company": item["company"]})
        if result.count() == 0:
            self.jobs_table.insert_one(item)
        else:
            # Checks if city needs to be updated
            cities = result[0]['city']
            try:
                src_idx = cities.index(item["city"][0])
            except:
                cities.append(item["city"][0])
                self.jobs_table.update(
                    { "_id": result[0]["_id"] },
                    { "$set": {"city": cities} }
                )

            urls = result[0]['job_link']
            try:
                src_idx = cities.index(item["job_link"][0])
            except:
                cities.append(item["job_link"][0])
                self.jobs_table.update(
                    {"_id": result[0]["_id"]},
                    {"$set": {"job_link": urls}}
                )