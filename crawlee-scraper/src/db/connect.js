import { MongoClient } from "mongodb";


export const getMongoDbConn = async () =>{
    const url = process.env.MONGO_DB_CONN_STRING;
    const client = new MongoClient(url);
    await client.connect();
    console.log("Connected to MongoDB Instance");
    const db = client.db('csct-db');
    return db
}
