//@ts-check

import { Rettiwt } from 'rettiwt-api';
import { config } from 'dotenv';
import express from 'express';
import { MongoClient } from 'mongodb';
config()

const app = express()
app.use(express.json())

const API_KEY = process.env.API_KEY;
const server_port = process.env.PORT || 3000;
// Creating a new Rettiwt instance
// Note that for accessing user details, 'guest' authentication can be used

const rettiwt = new Rettiwt({ apiKey: API_KEY });

/** @typedef {Object} User
 * @property {string} userName
 */
/** @typedef {Object} Tweet 
 * @property {string} id
 * @property {number} likeCount
 * @property {number} retweetCount
 * @property {string} createdAt
 * @property {User} tweetBy
 * @property {string} fullText
 * @property {string} lang
 * 
*/

/** @type {MongoClient} */
let mongo;

app.post('/scraper/ingest', async (req, res) => {
    try {
        const { limit: _limit, phrases } = req.body;
        const limit = _limit || 1000;
        let cursor = undefined;
        /** @type {Array<Tweet>} */
        let list = [];
        console.log('Fetching tweets', phrases, limit)
        while (true) {
            const response = await rettiwt.tweet.search({ includePhrase: phrases, language: 'en' }, 20, cursor)
            cursor = response.next.value;
            list = list.concat(response.list);

            if (list.length >= limit) {
                break;
            }
            /** @type {Array<Tweet>} */
            const currentItems = response.list;
            const toMongo = currentItems.map(item => ({
                author: item.tweetBy.userName,
                content: item.fullText,
                country: '',
                date_time: new Date(item.createdAt),
                id: item.id,
                language: item.lang,
                number_of_likes: item.likeCount,
                number_of_retweets: item.retweetCount,
            }))
            mongo.db('insights').collection('tweets').insertMany(toMongo).catch(e => {
                console.error('failed to insert', e);
            })
            console.log(`Fetched ${list.length} tweets`);
            if (response.list.length === 0) {
                break;
            }
            
        }
    res.status(200).send('OK');
    } catch (e) {
        console.error(e);
        res.status(500).send(e);

    }
});

app.get('/scraper/_health', (req, res) => {
    res.status(200).send('OK');
})

async function main() {
    const host = process.env.MONGO_HOST;
    const port = process.env.MONGO_PORT || 27017;
    const user = process.env.MONGO_USER;
    const password = process.env.MONGO_PASS;
    const uri = `mongodb://${user}:${password}@${host}:${port}/admin`;
    mongo = await MongoClient.connect(uri)
    console.log('Connected to MongoDB');

    app.listen(server_port, () => {
        console.log(`Server is running on port ${server_port}`);
    });
}

main().catch(e => console.error(JSON.stringify(e, null, 2)));
