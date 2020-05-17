# Chamber Registry Service

## Usage


```json 
{
	"data": "Content of the object"
	"message": "Description of what happened"
}
```

### List chambers

**Definition**

`GET /chambers`

**Response**

- `200 OK` on success

``` json
[
	{
		"id":12345,
		"door": true,
		"program": "Program 10",
		"volume": 100,
		"light": true,
		"air": true,
		"version": "1.0",
		"address":"192.168.1.10"
	},
	{
		"id": 12346,
		"door": false,
		"program": "Program 8",
		"volume": 100,
		"light": true,
		"air": true,
		"version": "1.0",
		"address":"192.168.1.12"
	},
	{
		"id": 12350,
		"door": true,
		"program": "Program 2",
		"volume": 100,
		"light": true,
		"air": true,
		"version": "1.0",
		"address":"192.168.1.15"
	}
]
```

### Registering a new chamber

**Definition**

`POST /devices`

**Arguments**

- `"id":int` a global unique id for the chamber
- `"door":boolean` door status
- `"program":string` identifier of the program that it is current playing 
- `"volume":int` volume of the program in percentage
- `"light":boolean` lights status
- `"air":boolean` air status
- `"version":string` version of the software on the chamber
- `"address":string` IP address to access the chamber

If a chamber with the given id already exists, it will override the existent one.

**Response**

- `201 Created` on success

``` json
{
	"id": 12350,
	"door": true,
	"program": "Program 2",
	"volume": 100,
	"light": true,
	"air": true,
	"version": "1.0",
	"address":"192.168.1.15"
}
```

### Fetch chamber details

`GET /chamber/<id>`

**Response**

- `404 Not found` if the device does not exist
- `200 OK` on Success

``` json
{
	"id": 12350,
	"door": true,
	"program": "Program 2",
	"volume": 100,
	"light": true,
	"air": true,
	"version": "1.0",
	"address":"192.168.1.15"
}
```

### Deleting chamber from database

**Definition**

`DELETE /chambers/<id>`

**Response**

- `404 Not Found` if the chamber does not exist
- `204 No content`


