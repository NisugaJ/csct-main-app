import { BlobServiceClient } from "@azure/storage-blob";
import { v1  } from "uuid";
import getSimpleDateTime from "./datetime.js";


const pushFileToBlobStorage = async (filePath) => {
    
    try {
        const AZURE_STORAGE_CONNECTION_STRING = process.env.AZURE_STORAGE_CONNECTION_STRING;

        if (!AZURE_STORAGE_CONNECTION_STRING) {
        throw Error('Azure Storage Connection string not found');
        }

        // Create the BlobServiceClient object with connection string
        const blobServiceClient = BlobServiceClient.fromConnectionString(
            AZURE_STORAGE_CONNECTION_STRING
        );
        
        const containerName = "scraped-data";
        const containerClient = blobServiceClient.getContainerClient(containerName);
        containerClient.createIfNotExists();

        const blobName = `scraped_${getSimpleDateTime()}_` + v1() + '.json';
        const blockBlobClient = containerClient.getBlockBlobClient(blobName);
        await blockBlobClient.uploadFile(filePath);

        console.log(`Blob ${blobName} uploaded to Azure Blob Storage`);

    } catch (err) {
        console.log(`Error: ${err.message}`);
    }
}

export default pushFileToBlobStorage