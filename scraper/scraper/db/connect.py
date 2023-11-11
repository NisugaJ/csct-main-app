from mongoengine import connect, Document, StringField
import os


def connect_to_db():
    try:
        connect(
            # db=os.environ.get('MONGO_DB_NAME'),
            # username=os.environ.get('MONGO_DB_USERNAME'),
            # password=os.environ['MONGO_DB_PASSWORD'],
            host=f"mongodb+srv://{os.environ.get('MONGO_DB_USERNAME')}:{os.environ['MONGO_DB_PASSWORD']}@csct-cluster.7dbfc95.mongodb.net/{os.environ.get('MONGO_DB_NAME')}",
        )
        print("Pinged successfully. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)
