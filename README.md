
### Place Piece
```bash
curl -X POST -H "Content-Type: application/json" -d '{"col": 3}' http://localhost:5000/drop | jq '.game_status.board[]'
```
### Board State (without placing)
```bash
curl http://localhost:5000/board | jq '.game_status.board[]'
```
### Only Current Player
```bash
curl http://localhost:5000/board | jq '.game_status.current_player'
```
### Only Winner 
```bash
curl http://localhost:5000/board | jq '.game_status.winner'
```
