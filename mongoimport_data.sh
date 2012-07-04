dbname="kaggle-wp"

mongoimport -d $dbname -c tu --type json --file data/trainUsers.json
mongoimport -d $dbname -c tpt --type json --file data/trainPostsThin.json
mongoimport -d $dbname -c tp --type json --file data/trainPosts.json

python clean_data.py

# Create indexes and preliminary data munging
#echo "db.tp2.ensureIndex({'likes.uid': 1});" | mongo $dbname
echo "db.tp2.ensureIndex({uid: 1});" | mongo $dbname
echo "db.tp2.ensureIndex({author: 1});" | mongo $dbname
echo "db.tp2.ensureIndex({blog: 1});" | mongo $dbname
echo "db.tp2.ensureIndex({post_id: 1});" | mongo $dbname

echo "db.tu2.ensureIndex({uid: 1});" | mongo $dbname
echo "db.tu2.ensureIndex({inTestSet: 1});" | mongo $dbname
echo "db.tu2.ensureIndex({blog: 1});" | mongo $dbname
echo "db.tu2.ensureIndex({post_id: 1});" | mongo $dbname
