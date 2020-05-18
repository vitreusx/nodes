# Overview

## `/net` endpoints

```http
GET /net/groups
Payload: auth
Result: List[str]
> 200 OK
> 401 Unauthorized
```
Get a list of groups for the node.

```http
PUT /net/group
Payload: name
> 201 Created
> 400 Bad Request [when group exists?]
> 401 Unauthorized
```
Create a new group.

```http
DELETE /net/group
Payload: name
> 200 OK
> 204 No Content
> 401 Unauthorized
```
Delete the group.

```http
GET /net/group/members
Payload: group
Result: Dict[str, str] (member name -> member addr)
> 200 OK
> 401 Unauthorized
```
List members of a group.

```http
PUT /net/group/member
Payload: group, name, addr
> 201 Created
> 400 Bad Request [when member exists?]
> 401 Unauthorized
```
Add a node to the group.

```http
DELETE /net/group/member
Payload: group, name
> 200 OK
> 204 No Content
> 401 Unauthorized
```
Remove a node from a group.

```http
POST /net/group/leave
Payload: group
> 200 OK
> 401 Unauthorized
```
Leave a group.

```http
POST /net/proxy
Payload: group, member, endpoint, payload
Result: any
> 200 OK
> 401 Unauthorized
```
Execute command at endpoint with a specified payload for a given member in a given group. [[Need to revise?]]

## `/tasks` endpoints

```http
GET /tasks/list
Result: List[str] (list of endpoints?)
> 200 OK
> 401 Unauthorized
```
Lists available tasks.

```http
GET /tasks/info
Payload: endpoint
Result: { endpoint: ..., name: ..., description: ... } or something like that?
> 200 OK
> 401 Unauthorized
```
Gets additional info about a task.

```http
POST /tasks/task
Payload: endpoint
> 200 OK
> 401 Unauthorized
```
Instructs server to perform a specified task.

## Notes

- All methods should be accessible from other node modules;
- Authorization: token based via Authorization HTTP header? need to think about it;
- How to automatically notify dashboard of the changes?;
- Do we want voice API (like turning on/off etc?);
