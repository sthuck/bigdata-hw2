//@ts-check

import { Rettiwt } from 'rettiwt-api';
import {config} from 'dotenv';
config()

async function main() {
    const API_KEY = process.env.API_KEY;
    // Creating a new Rettiwt instance
    // Note that for accessing user details, 'guest' authentication can be used

    const rettiwt = new Rettiwt({apiKey: API_KEY});
    let cursor = undefined;
    let list = [];
    while (true) {
        const response = await rettiwt.tweet.search({includePhrase: 'real madrid'}, 20, cursor)
        cursor = response.next.value;
        list = list.concat(response.list);
        if (list.length >= 200) {
            break;
        }
    }
    console.log(list)
}

main().catch(e => console.error(JSON.stringify(e, null, 2)));
