export API_TOKEN=YOUR_TOKEN_HERE

# Get birthdays of your friends in VK and export it in json file
# in {'name': 'first_name last_name', 'bdate': 'bdate'} format  
curl -XGET "https://api.vk.com/method/friends.get?v=5.131&access_token=${API_TOKEN}&fields=bdate" \
    | jq '[.response.items[] | {name: (.first_name + " " + .last_name), bdate: .bdate}]' > birthday.json

# Some of friends might have not specified their birthdays, so they are null in json file
# You can separate friends with specified and not specified birthdays to different files
cat birthdays.json | jq '[.[] | (if .bdate != null then . else empty end) ]' > friends_with_birthdays.json

cat birthdays.json | jq '[.[] | (if .bdate == null then . else empty end) ]' > friends_without_birthdays.json
