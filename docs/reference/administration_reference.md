# Administration reference guide

*Introduced in InvenioRDM v10*

## Overview

This document provides a reference guide for all the attributes available for `invenio-administration` views.

## List View

### Attributes
| Attribute                     | Required   | Default                                | Description                                                                                                          |
|-------------------------------|------------|----------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| **name**                      |            | *View class name*                      | view's name used by Flask to create routing                                                                          |
| **resource_config**           | *required* |                                        | used to retrieve the resource (name of the resource attribute of the flask extension - available in ext.py)          |
| **search_request_headers**    |            | *{ "Accept" :  "application/json" }*   | specifies resource-specific headers to add during REST API request                                                   |
| **title**                     | *required* |                                        | displays a title in the list view page                                                                               |
| **category**                  |            |                                        | places the menu entry under a category in the menu bar                                                               |
| **pid_path**                  |            | *"pid"*                                | used for accessing the unique identifier of a resource                                                               |
| **icon**                      |            |                                        | displays an icon next to the menu's entry                                                                            |
| **template**                  |            | *"invenio_administration/search.html"* | template to be rendered for the view. By default, it uses a predefined one. Can be overridden with a custom template |
| **display_search**            |            | *True*                                 | displays/hides a searchbar in the list view                                                                          |
| **display_delete**            |            | *False*                                | displays/hides a delete button for each resource                                                                     |
| **display_edit**              |            | *False*                                | displays/hides an edit button for each resource                                                                      |
| **item_field_list**           | *required* |                                        | list of fields to be rendered in the list view's table. Each field  corresponds to a column                          |
| **search_facets_config_name** |            |                                        | defines which facet configuration to use in the search view                                                          |
| **search_sort_config_name**   |            |                                        | defines which sort configuration to use in the search view                                                           |
| **create_view_name**          |            |                                        | endpoint to create a resource directly from list view                                                                |
| **resource_name**             |            | *pid_path*                             | defines a path to human-readable attribute of the resource (title/name etc.)                                         |
| **display_read**              |            | *True*                                 | specifies if there should be a link to a details view                                                                |


## Details View

### Attributes

| Attribute                  | Required   | Default                                 | Description                                                                                                 |
|----------------------------|------------|-----------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **name**                   |            | *view class name*                       | view's name used by Flask to create routing                                                                 |
| **url**                    |            | *view's 'name'*                         | url used to route the view.                                                                                 |
| **resource_config**        | *required* |                                         | used to retrieve the resource (name of the resource attribute of the flask extension - available in ext.py) |
| **pid_path**               |            | *pid_path*                              | used for accessing the unique identifier of a resource                                                      |
| **api_endpoint**           | *required* |                                         | used to indicate API endpoint of update the resource                                                        |
| **title**                  | *required* | *"Resource details"*                    | displays a title in the view page.                                                                          |
| **list_view_name**         | *required* |                                         | name of the resource's list view name, enables  navigation between detail view and list view.               |
| **form_fields**            | *required* |                                         | fields to be displayed  in the detail form.                                                                 |
| **template**               |            | *"invenio_administration/details.html"* | template to be rendered for the view. Can be overridden by a custom template.                               |
| **search_request_headers** |            | *{ "Accept" :  "application/json" }*    | used to request the resource                                                                                |
| **display_edit**           |            | *True*                                  | toggles Edit button in details view                                                                         |
| **display_delete**         |            | *True*                                  | toggles Delete button in details view                                                                       |
| **item_field_list**        | *required* |                                         | list of items to be rendered in the details page                                                            |

## Create View

### Attributes

| Attribute           | Required   | Default                                | Description                                                                                                 |
|---------------------|------------|----------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **name**            |            | *view class name*                      | view's name used by Flask to create routing                                                                 |
| **url**             |            | *view's 'name'*                        | url used to route the view.                                                                                 |
| **resource_config** | *required* |                                        | used to retrieve the resource (name of the resource attribute of the flask extension - available in ext.py) |
| **pid_path**        |            | *pid*                                  | used for accessing the unique identifier of a resource                                                      |
| **api_endpoint**    | *required* |                                        | used to execute POST request.                                                                               |
| **title**           | *required* |                                        | displays a title in the view page.                                                                          |
| **list_view_name**  | *required* |                                        | name of the resource's list view name, enables  navigation between create modal and list view.              |
| **form_fields**     | *required* |                                        | fields to be displayed  in the creation form.                                                               |
| **template**        |            | *"invenio_administration/create.html"* | template to be rendered for the view. Can be overridden by a custom template.                               |

## Edit View

### Attributes

| Attribute           | Required   | Default                               | Description                                                                                                 |
|---------------------|------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **name**            |            | *view class name*                     | view’s name used internally by Flask                                                                        |
| **url**             |            | *view's 'name'*                       | url used to route the view.                                                                                 |
| **resource_config** | *required* |                                       | used to retrieve the resource (name of the resource attribute of the flask extension - available in ext.py) |
| **pid_path**        |            | *pid_path*                            | used for accessing the unique identifier of a resource                                                      |
| **api_endpoint**    | *required* |                                       | used to update the resource.                                                                                |
| **title**           | *required* |                                       | displays a title in the view page.                                                                          |
| **list_view_name**  | *required* |                                       | name of the resource's list view name, enables  navigation between edit view and list view.                 |
| **form_fields**     | *required* |                                       | fields to be displayed  in the edit form.                                                                   |
| **template**        |            | *"invenio_administration/edit.html"*  | template to be rendered for the view. Can be overridden by a custom template.                               |


## Custom view

### Attributes

| Attribute      | Required | Default    | Description                                                                                                                                         |
|----------------|----------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| **name**       |          |            | Name of the view                                                                                                                                    |
| **category**   |          | *None*     | Menu entry that contains the view                                                                                                                   |
| **template**   |          |            | Path to the custom template.                                                                                                                        |
| **url**        |          | *viewname* | URL used to route the view.                                                                                                                         |
| **menu_label** |          |            | Label that will be displayed in the menu.                                                                                                           |
| **order**      |          |            | Order of the menu entry.                                                                                                                            |
| **icon**       |          |            | The optional icon that the menu entry might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/). |
