Title: Using Protobuf instead of JSON to communicate with a frontend
Date: 2015-05-22
Short_summary: Protobuf (or others tools like Thrift) are very often used to communicate between services. Let's see how it would work to use it between a server and a javascript frontend
Category: Dev
Authors: Vincent

*Reading time: ~15 minutes.*  

Protobuf (or other binary serialization formats like Thrift) are widely used to communicate between services. JSON is overwhelmingly used for backend <-> frontend communication and for APIs.  
Let's see how a client/server using Protobuf would look like.
<!-- PELICAN_END_SUMMARY --> 

## What is Protobuf
[Protobuf](https://developers.google.com/protocol-buffers/docs/overview) is a binary serialization format from Google meant to serialize structured data. It has clients in most languages, including Python and Javascript which we are going to use in our toy app.  

Tools like Protobuf have a few advantages over JSON:

- smaller in size
- typed
- offer a common interface for all your services, you can just update your .proto or .thrift and share those with the services using it, as long as there is a client for that language

[Thrift](https://thrift.apache.org/) does more as it also allows you to define methods as well as structs.

## Example app
As an example we are going to make a small address book app. Coincidentally that's the example that the Python Protobuf doc is using as well but that wasn't on purpose I swear! The data is generated randomly on startup of the flask app.  
The repo is on our [github](https://github.com/WeAreWizards/protojson) if you want to try it yourself.  
As mentioned on the README, the Python client for Protobuf does not support Python3 (yet) so you will have to make a Python2 virtualenv if you decide to install the server.  
The server will deliver the content in JSON or Protobuf based on the `Accept` header.

### Server-side
Let's have a quick look at the server, it might not be new if you have already used Protobuf before but it is helpful for the rest (like me, I only used Thrift before).  
First we need to define our Protobuf schema, which is done in the [addressbook.proto](https://github.com/WeAreWizards/protojson/blob/master/addressbook.proto) file. Here is one of the model as example:

```protobuf
message Contact {
  required string first_name = 1;
  required string last_name = 2;
  optional Address address = 3;
  repeated Phone phone_numbers = 4;
};
```
In this model, `first_name` and `last_name` are required (controversial, I'll come back to that later), the address model is optional and we can have 0, 1 or n `phone_numbers`.  
Now, Python doesn't know about .proto files so we need to use the [python client](https://pypi.python.org/pypi/protobuf) to generate code that we can use. This is the [addressbook_pb2.py](https://github.com/WeAreWizards/protojson/blob/master/addressbook_pb2.py) file. You can then import that in your Python code and access the models defined in your .proto file.  
Have a look on the [data.py](https://github.com/WeAreWizards/protojson/blob/master/data.py) client to see an example. You can use those models as you would with a class and using kwargs for every attributes.  
You also need to serialize them before sending, using the `SerializeToString()` method in our app.  

### Client-side
The client is written in Angular purely as an example and because ng-repeat was exactly what I wanted here. The code is a quick prototype so don't expect it to be idiomatic.  
It uses [ProtoBuf.js](https://github.com/dcodeIO/ProtoBuf.js) as a Protobuf client.  
The first thing we do is a basic GET to get all our contacts which is trivial since you can just dump the response data into our scope variable. On the other hand, we need to handle Protobuf deserialization since looking at our network tab we receive binary data looking like:

```
.
MarlonSheets
7771 Eastern Avenue11239
,
HarleyMalloy60139"
(712)614-9303
Y
Mack  Hendricks3
9573 Kimridge Cove
7490 Orchard Hill Cove11239"
(802)466-7004

MadelineBowen87023
0
WillaSadler
693 Burlington Parkway43824
T
```
By default, this is more compact than JSON by quite a bit but once I turned on GZIP, the difference became much smaller: 851B for ProtoBuf and 942B for JSON.  

In the example I copied the .proto file in the static directory and created our [models](https://github.com/WeAreWizards/protojson/blob/master/static/main.js#L12-L15) following the ProtoBuf.js tutorial.  
Now the only two things left to do for our GET is to add a `responseType: 'arraybuffer'` in our HTTP requests (which would be done in the config for a proper angular app) and decode the data we received using `MyModel.decode(data)`.  
Creating an instance looks like a class in javascript as well:

```js
var contact = new Contact({
  first_name: _contact['firstName'],
  last_name: _contact['lastName'],
});
```
Note that supplying an incorrect param such as an unknown field will result in a runtime error.  

POSTing is a bit more complex as Angular tries to be too clever and forces us to do some changes in the HTTP request:

```js
// The transformRequest is needed
var req = {
  method: 'POST',
  url: '/api/contacts',
  responseType: 'arraybuffer',
  transformRequest: function(r) { return r;},
  data: contact.toArrayBuffer(),
  headers: {
    'Content-Type': 'binary/octet-stream'
  }
};
```

## Conclusion
While I see the need for Protobuf and Thrift for services communication, I don't really see the point of using it instead of JSON for the frontend. 
First, the network tab becomes pretty much unusable and I use it very often.  
Since Protobuf doesn't use setters, you can screw up your object and it will only throw an error much later, but earlier than with vanilla javascript. Using [Typescript](http://www.typescriptlang.org/) or [Flow](http://flowtype.org/) with good definitions would solve many issues at compile time.  
Another point I raised earlier is that Google recommends to mark every field as optional in Protobuf, which is better in terms of compatibility but means you can send imcomplete data.  
Has any of you used a binary serialization for that successfully? Let us know in the comments or send us a tweet [@WeAreWizardsIO](https://twitter.com/WeAreWizardsIO).  

