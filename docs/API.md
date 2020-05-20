# SITREP

## `/net` endpoints

```http
GET /net/groups
Result: List[str]
```
Get a list of groups (or rather their names) for the node.

```http
PUT /net/g/<group>
```
Create a new group.

```http
DELETE /net/g/<group>
```
Delete a group.

```http
GET /net/g/<group>
Result: Dict[str, str] (member name -> member addr)
```
List members of a group.

```http
PUT /net/g/<group>/m/<member>
```
Add a node to the group.

```http
DELETE /net/g/<group>/m/<member>
```
Remove a node from a group.

```http
POST /net/g/<group>/leave
```
Leave a group.

```http
POST /net/proxy
Payload: targets, endpoint, payload
Result: any?
```
Execute command at endpoint with a specified payload for given targets. [[Need to revise?]]

### Notes:
- there are also private endpoints (not sure whether we should document them).
