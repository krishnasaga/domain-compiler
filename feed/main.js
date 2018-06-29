var elasticsearch = require('elasticsearch');
var dummyjson = require('dummy-json');

var client = new elasticsearch.Client({
  host: 'localhost:9200',
  log: 'trace'
});


const hypersnapshotTemplate = `
  {
   "index": "vison",
   "type": "hypersnapshot",
   "id": {{randomInt 2000 4000}},
   "body": {
    "page": "flight_options",
	"codeHead": "{{guid}}",
	"featureMatches": {
	  "count": "2",
	  "features": [
	    { "name": "price_panel", 
		  "match": {{randomFloat 0.01 0.99}},
		  "position": {
		    "center": { "x": 100, "y": 100 },
		    "boundingBox": [
			{ "x": 200, "y": 200 },
			{ "x": 200, "y": 200 },
			{ "x": 200, "y": 200 },
			{ "x": 200, "y": 200 }]
		  }
		},
		{ "name": "selected_flight", 
		  "match": {{randomFloat 0.01 0.99}},
		  "position": {
		  "center": { "x": 100, "y": 100 },
		  "boundingBox": [
		  { "x": 200, "y": 200 },
		  { "x": 200, "y": 200 },
		  { "x": 200, "y": 200 },
		  { "x": 200, "y": 200 }]
		}}
		]
	},
	"screenSize": {
	  "height": 2000,
	  "width": 1024
	}
  }
}
`;


Array.from(Array(100).keys()).forEach((key) => {

  const query = JSON.parse(dummyjson.parse(hypersnapshotTemplate,{ 
   helpers: { randomInt: dummyjson.utils.randomInt, randomFloat: dummyjson.utils.randomFloat }}));
   const body = Object.assign({},query.body,{timeStamp: new Date(new Date().getTime() + key*1000 ).toISOString()});
   
   client.create(Object.assign({},query,{ body }));
  
});
