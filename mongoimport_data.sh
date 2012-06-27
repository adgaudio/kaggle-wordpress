dbname="kaggle-wp"

mongoimport -d $dbname -c tu --type json --file data/trainUsers.json
mongoimport -d $dbname -c tpt --type json --file data/trainPostsThin.json
mongoimport -d $dbname -c tp --type json --file data/trainPosts.json

python clean_data.py

# Create indexes and preliminary data munging
#echo "db.tpt2.ensureIndex({'likes.uid': 1});" | mongo $dbname
#echo "db.tpt2.ensureIndex({post_id: 1});" | mongo $dbname
