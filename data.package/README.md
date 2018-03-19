# Data Package
- [Doc](https://frictionlessdata.io/docs/data-package/)
- [Spec : Datapackage](https://frictionlessdata.io/specs/data-package/)
- [Spec : Identifier](https://frictionlessdata.io/specs/data-package-identifier/)
- [Spec : resources](https://frictionlessdata.io/specs/data-resource/)

# datapackage.json
```
{
  "name": "a-unique-human-readable-and-url-usable-identifier",
  "datapackage_version": "1.0-beta",
  "title": "A nice title",
  "description": "...",
  "version": "2.0",
  "keywords": ["name", "My new keyword"],
  "licenses": [{
    "url": "http://opendatacommons.org/licenses/pddl/",
    "name": "Open Data Commons Public Domain",
    "version": "1.0",
    "id": "odc-pddl"
  }],
  "sources": [{
    "name": "World Bank and OECD",
    "web": "http://data.worldbank.org/indicator/NY.GDP.MKTP.CD"
  }],
  "contributors":[ {
    "name": "Joe Bloggs",
    "email": "joe@bloggs.com",
    "web": "http://www.bloggs.com"
  }],
  "maintainers": [{
    // like contributors
  }],
  "publishers": [{
    // like contributors
  }],
  "dependencies": {
    "data-package-name": ">=1.0"
  },
  "resources": [
  	{
    	"schema":{
    		
    	}
    	// one of url or path should be present
    	"path": "relative-path-to-file", // e.g. data/mydata.csv
    	"url": "online url" // e.g http://mysite.org/some-data.csv
  	}
  ],
  // extend your datapackage.json with attributes that are not
  // part of the data package spec
  // we add a views attribute to display Recline Dataset Graph Views
  // in our Data Package Viewer
  "views" : [
    {
      ... see below ...
    }
  ],
  // you can add your own attributes to a datapackage.json, too
  "my-own-attribute": "data-packages-are-awesome",
}
```



