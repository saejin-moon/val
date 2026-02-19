# api docs
## id
from match_ids.txt

## metadata
- `metadata.dateStarted` ex. "2026-02-19T04:22:39.834+00:00" (change to est and a more readable format {gotta be a python library for that right} and save that as a string as well as the utc seconds for easier csv storage)
- `metadata.mapName` map name
- `metadata.mapDetails.imageUrl` map image

## segments
### team summary
if `type` is "team-summary"
- `.metadata.name` team name (to identiy if player won based on what team they were on)
- `.metadata.hasWon` whether team won
- `.metadata.kills.value` total team kills
- `.metadata.deaths.value` total team deaths
- `.metadata.damage.value` total team damage
### round summary
if `type` is "round-summary"
### player summary
if `type` is "player-summary"
- `.partyId` which party they are in (to find if i'm in a party and who i'm in a party with)


# csv
## matches.csv
every entry is a match
- `match_id` | string
- `date_utc` | int (needs to be converted)
- `date_string` | string (needs to be converted)
- `map_name` | string
- `map_image` | string
- `match_win` | boolean

## [match id].csv
every entry is an event
- `round` | int
- `round_win` | boolean
- `spike_planted` | boolean
- `user_position` | string
- `friendly{n}_position` | string
- `enemy{n}_position` | string
- `gun` | string
- `damage_taken` | int