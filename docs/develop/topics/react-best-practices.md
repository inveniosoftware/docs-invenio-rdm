# React best practices

## Components

✅ DO

```javascript
import React, {Component} from 'react';

class MyAccordion extends Component {}

  render(){
    <Accordion key={agg.title}/>  
  }
```


❌ DON'T

```javascript
import React, {Component} from 'react';

class MyAccordion extends Component {}
  render(){
    <div className="ui accordion" key={agg.title}></div>  
  }
```

Use dedicated react semantic ui components in react. The react version of semantic-UI components have normally implemented some logic, which is crucial for the component to work correctly. The plain CSS semantic UI might not have all the features available when you use them in react.  
