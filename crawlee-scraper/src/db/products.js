import { getMongoDbConn } from "./connect.js"

const collectionName = 'product'

const productExists = async (product_id)=>{
    const db = await getMongoDbConn()

    const matchedItems = await db.collection(collectionName).find({
        product_id: product_id
    }).toArray()

    if (matchedItems.length > 0) 
        return true
    else 
        return false
}


export {
    productExists
}