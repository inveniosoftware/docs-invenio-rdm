# Customization

As we just saw, overriding configured values is an easy and common way of customizing your instance to your needs. Sometimes, however, you need to provide custom files too: logos, templates... We show how to perform these custom changes.

## Update the logo

We are going to change the logo. Take an *svg* file and copy it to your **local** static files. You can use the [invenio color logo](https://github.com/inveniosoftware/invenio-theme/raw/master/invenio_theme/static/images/invenio-color.svg):

``` bash
cp ./path/to/new/color/logo.svg static/images/logo.svg
```

Then, use the `update` command:

``` bash
invenio-cli update --no-install-js
```
``` console
# Summarized output
Collecting statics and assets...
Collect static from blueprints.
Created webpack project.
Copying project statics and assets...
Symlinking assets/...
Building assets...
Built webpack project.
```

Passing the `--no-install-js` option, skips re-installation of JS dependencies.

Go to the browser [*https://localhost:5000/*](https://localhost:5000) or refresh the page. And voilà! The logo has been changed!

!!! warning "That evil cache"
    If you do not see it changing, check in an incognito window; the browser might have cached the logo.

## Change colors

You might also be wondering: *How do I change the colors so I can make my instance look like my institution's theme?*

We are going to change the top header section in the frontpage to apply our custom background color. Open the `assets/scss/<your instance shortname>/variables.scss` file and edit it as below:

``` scss
$navbar_background_image: unset;
$navbar_background_color: #000000; // Note this hex value is an example. Choose yours.
```

Then, run the `invenio-cli update` command as above and refresh the page! You should be able to see your top header's color changed! You can find all the available styling variables that you can change [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/scss/invenio_app_rdm/variables.scss).

## Change search results

Changing how your results are presented in the search page is also something quite common.

We are going to update the search result template so we can show more text in the result's description. Create a file called `ResultsItemTemplate.jsx` inside `assets/templates/search` folder and then edit it as below:

```js
import React from 'react';
import {Item} from 'semantic-ui-react';
import _truncate from 'lodash/truncate';

export function ResultsItemTemplate(record, index) {
  return (
    <Item key={index} href={`/records/${record.id}`}>
      <Item.Content>
        <Item.Header>{record.metadata.titles[0].title}</Item.Header>
        <Item.Description>
          {_truncate(record.metadata.descriptions[0].description, { length: 400 })}
        </Item.Description>
      </Item.Content>
    </Item>
  )
};
```

Then, run the `invenio-cli update` command as above and refresh the page! You should be able to see more text in each result's description! You can find all the available templates [here](https://github.com/inveniosoftware/invenio-app-rdm/tree/master/invenio_app_rdm/theme/assets/templates/search).

## Change the record landing page

When you click on a search result, you navigate in the details page of a specific record. This section shows you how to change the way the information is displayed in the details page.

We are going to configure our instance to use our template for displaying the information in the record's landing page. Open the `invenio.cfg` file and add the below:

```python
from invenio_rdm_records.config import RECORDS_UI_ENDPOINTS
RECORDS_UI_ENDPOINTS['recid'].update(template='my_record_landing_page.html')
```

Then, we create a file `my_record_landing_page.html` inside the `templates` folder and edit it as below:

```jinja
{%- extends 'invenio_rdm_records/record_landing_page.html' %}

{%- block page_body %}
<!-- // Paste your code here -->
{%- endblock page_body %}
```

Inside the `page_body` block you can restructure the page as you want! You can check the default record landing page template [here](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/theme/templates/invenio_rdm_records/record_landing_page.html).

Since we modified `invenio.cfg`, we need to re-start the server to see our changes take effect:

```bash
^C
Stopping server and worker...
Server and worker stopped...
```
```bash
invenio-cli run
```

## Change functionality

Need further customizations? Have you thought of creating your own extensions?

How to make an extension and add it to your InvenioRDM instance is explained in the [Extensions section](../extensions/custom.md).
