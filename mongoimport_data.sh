dbname="kaggle-wp"

mongoimport -d $dbname -c tu --type json --file data/trainUsers.json
mongoimport -d $dbname -c tpt --type json --file data/trainPostsThin.json

#mongoimport -d $dbname -c tp --type json --file data/trainPosts.json


# Create indexes

echo "mongo create index statement..." | mongo $dbname

