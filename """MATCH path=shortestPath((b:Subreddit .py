"""MATCH path=shortestPath((b:Subreddit {name:"boating"})-[*1..10]-(c:Subreddit {name:"houston"}))
RETURN path LIMIT 200"""