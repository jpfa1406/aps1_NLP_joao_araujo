# aps1_joao_araujo

Sci-fi book recomendation and Search API

## Overview

This project is a FastAPI-based web application designed to help science fiction enthusiasts discover new books that match their interests. The idea for this project came to me as I was finishing *Children of Time* by Adrian Tchaikovsky and I wanted to find another book that could offer a similar experience.

The API uses TF-IDF (Term Frequency-Inverse Document Frequency) to analyze book descriptions and rank them by relevance based on user queries.

## Dataset
The dataset was taken from a [Kaggle dataset](https://www.kaggle.com/datasets/tanguypledel/science-fiction-books-subgenres?resource=download) consisting of multiple CSV files, each representing a different science fiction subgenre. These include:

 - Aliens
 - Alternate History
 - Alternate Universe
- Apocalyptic
- Cyberpunk
- Dystopia
- Military
- Robots
- Space Opera
- Steampunk
- Time Travel
Each file contains book titles, descriptions, and ratings. The data has been preprocessed and combined into a single dataset used by the application.

## Running the Project with Docker

```bash
docker build -t aps_jp .
docker run -d -p 1506:8888 aps_jp
```

### 1. Test That Yields 10 Results
- **Query**: `/query?query=blend of space exploration and evolution of intelligent species`
- **Expected Result**: This query should yield at least 10 results, as there are many Sci-fi books that fit the theme of large-scale space conflicts.
- **Comment**: Searching for "blend of space exploration and evolution of intelligent species" returns multiple results due to the common theme in science fiction of space battles and intergalactic wars.
- **Test Link**: [Query 'blend of space exploration and evolution of intelligent species'](http://10.103.0.28:1506/query?query=a%20large%20war%20in%20space)

### 2. Test That Yields Fewer Than 10 Results
- **Query**: `/query?query=hitchhiker`
- **Expected Result**: This query yields only 7 results because there are not enough relevant documents in the database related to "hitchhiker."
- **Comment**: All results refer to the famous book "The Hitchhiker's Guide to the Galaxy".
- **Test Link**: [Query for hitchhiker](http://10.103.0.28:1506/query?query=hitchhiker)

### 3. Test That Yields a Non-Obvious Result
- **Query**: `/query?query=julius cesar`
- **Expected Result**: Most of the Sci-fi books returned have themes around time trevelers, witch is expect to include "Julius Cesar" but "Repo Virtual" is in a cyberpunk setting, making it a non-obvious connection.
- **Comment**: The query "julius cesar" surfaces a book that connects through the name "Julius" even though the story is set in a futuristic cyberpunk world. This demonstrates the system's ability to find relevant but non-obvious matches.
- **Test Link**: [Query for julius cesar](http://10.103.0.28:1506/query?query=julius%20cesar)

## Authors

joao pedro farias araujo