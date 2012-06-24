mongoimport -d kaggle-wp -c tu --type json --file data/trainUsers.json
mongoimport -d kaggle-wp -c tpt --type json --file data/trainPostsThin.json

#mongoimport -d kaggle-wp -c tp --type json --file data/trainPosts.json

