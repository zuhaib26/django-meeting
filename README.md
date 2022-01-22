# django-meeting

open terminal
go to django-meeting folder
create virtual environment 
```
python3 -m virtualenv meetingvenv
```
Run the following command to activate the virtual environment
```
source meetingvenv/bin/activate
```
see the requirement.txt file for package requirements
Create a MySql database named scheduler 
In settings.py file update 

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scheduler',
        'USER': 'root',
        'PASSWORD': 'gdateq54123',
        'HOST': 'localhost',
        'PORT': '3306',
    }

}

with user, password, host and port 

go to meeting directory 
Run:
```python manage.py makemigrations```
```python manage.py migrate```

Create a superuser for django admin
Run:
```python manage.py createsuperuser```
Enter username for superuser
Enter Password for superuser

Use command
```python manage.py runserver```
To run the application

You can use GraphQL playground for GraphQl queries which does not require authentication, For GraphQl queries which require authentication i suggest postman

To run the queries that need authentication run 
```
mutation{
    tokenAuth(username: "test",password: "test"){
        token
    }
}
```
copy the result, in postman go to header part of query add a key filed Authorization, in its value add JWT followed by space and past the result. Check attached Video.


Query to get user details from id
```
query{
  user(id:1){
    firstName
    lastName
    email
  }
}
```

Query to get logged in user details

```
query{
  selfUser{
    firstName
    lastName
    email
  }
}
```


Mutation to get authentication token. It takes username and password
```
mutation{
    tokenAuth(username: "test",password: "test"){
        token
    }
}
```

Mutation to verify authentication token
```
mutation{
  verifyToken(token:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NDI3NzM5MjEsIm9yaWdJYXQiOjE2NDI3NzM2MjF9.v-ebiQfWD0dbGn-86qSTziEOW_VZ1t0VO8bHFNSEIvs"){
    payload
  }
}
```

Mutation to refresh authentication token
```
mutation {
  refreshToken(token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2NDI3NzM5MjEsIm9yaWdJYXQiOjE2NDI3NzM2MjF9.v-ebiQfWD0dbGn-86qSTziEOW_VZ1t0VO8bHFNSEIvs") {
    token
  }
}
```

Query to get Available meeting slots from username for non logged in users
```
query{
  slots(username:"test"){
    id
    date
    startTime
    interval
    belongsTo {
      username
    }
  }
}
```

Mutation to book availabe slot for non logged in users. It takes slotId, email, name
```
mutation{
  createSchedule(slotId:13, email:"zuhaib33@test.com", name:"zuhaib3333"){
    schedule{
      name
      email
      slot{
        date
        startTime
        interval
      }
    }
  }
}
```


Mutation to create meeting slots. Only Authenticated users can create it. It needs three arguments date, startTime and interval
date should be in this format 2021-02-17 and time in this 11:30:00
```
mutation{
  createAvailableSlot(date:"2021-02-17",startTime:"11:30:00",interval:15){
    slot{
      id
      date
      startTime
      interval
      belongsTo{
        id
      }
    }
  }
}
```

Query to get slots of logged in user
```
query{
  userSlots{
    id
    date
    startTime
    interval
  }
}
```

Mutation to update slot(only authenticated users). It takes four arguments slotId, date, startTime and interval
```
mutation{
  updateSlot(slotId:2, date:"2022-02-14", startTime:"12:30:00", interval:15){
    slot{
      interval
      date
      startTime
    }
  }
}
```

Mutation to delete slot(only authenticated users). It takes one argument slotId
```
mutation{
  deleteSlot(slotId:9){
    ok
  }
}
```

Query to get meeting schedules of authenticated user
```
query{
  schedules{
    email
    name
    slot{
      id
      date
      startTime
      interval
    }
  }
}
```

Mutation to book a meeting. It takes three arguments slotId, email and name
```
mutation{
  createSchedule(slotId:13, email:"zuhaib33@test.com", name:"zuhaib3333"){
    schedule{
      name
      email
      slot{
        date
        startTime
        interval
      }
    }
  }
}
```
