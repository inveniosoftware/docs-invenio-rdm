# Administration reference guide

## Overview

This document provides a reference guide for all the attributes available for `invenio-administration` views.

## List View

### Attributes

- **name**                                 (*View class name*)                           - view's name used by Flask to create routing
- **resource_config**          *required*                                                - used to retrieve the resource (refers to extension attribute - check ext.py)
- **search_request_headers**               (*{ "Accept" :  "application/json" }*)        - used to request the resource
- **title**                    *required*                                                - displays a title in the list view page.
- **category**                 *required*                                                - places the menu entry under a category in the menu bar.
- **pid_path**                             (*"pid"*)                                     - used for accessing the unique identifier of a resource 
- **icon**                                                                               - displays an icon next to the menu's entry.
- **template**                             (*"invenio_administration/search.html"*)      - template to be rendered for the view. By default, it uses a predefined one. Can be overridden with a custom template.
- **display_search**                       (*True*)                                      - displays a searchbar in the list view.
- **display_delete**                       (*False*)                                     - displays a delete button for each resource.
- **display_edit**                         (*False*)                                     - displays an edit button for each resource.
- **item_field_list**          *required*                                                - list of fields to be rendered in the list view's table. Each field  corresponds to a column.
- **search_config_name**                   (*view's name*)                               - search app configuration name
- **search_facets_config_name**                                                          - displays facets in search table
- **search_sort_config_name**                                                            - displays sort options in search table
- **create_view_name**                                                                   - endpoint to create a resource directly from list view  
- **resource_name**                        (*pid_path*)                                  - displays a label in actions modals
- **display_read_only**                  (*True*)                                        - specifies if there should be a link to a details view

## Details View

### Attributes

- **name**                                 (*view class name*)                          - view's name used by Flask to create routing
- **url**                                  (*view's 'name'*)                            - url used to route the view.
- **resource_config**    *required*                                                     - used to retrieve the resource (refers to extension attribute - check ext.py)
- **pid_path**                             (*pid_path*)                                 - used for accessing the unique identifier of a resource 
- **api_endpoint**       *required*                                                     - used to update the resource.
- **title**              *required*        (*"Resource details"*)                       - displays a title in the view page.
- **list_view_name**     *required*                                                     - name of the resource's list view name, enables  navigation between detail view and list view.
- **form_fields**        *required*                                                     - fields to be displayed  in the detail form.
- **template**                             (*"invenio_administration/details.html"*)    - template to be rendered for the view. Can be overridden by a custom template.
- **search_request_headers**               (*{ "Accept" :  "application/json" }*)       - used to request the resource
- **display_edit** (*True*)                                                             - toggles Edit button in details view
- **display_delete** (*True*)                                                           - toggles Delete button in details view
- **item_field_list** *required*                                                        - list of items to be rendered in the details page

## Create View

### Attributes

- **name**                                 (*view class name*)                          - view's name used by Flask to create routing
- **url**                                  (*view's 'name'*)                            - url used to route the view.
- **resource_config**    *required*                                                     - used to retrieve the resource (refers to extension attribute - check ext.py)
- **pid_path**                             (*pid*)                                      - used for accessing the unique identifier of a resource 
- **api_endpoint**       *required*                                                     - used to execute POST request.
- **title**              *required*                                                     - displays a title in the view page.
- **list_view_name**     *required*                                                     - name of the resource's list view name, enables  navigation between create modal and list view.
- **form_fields**        *required*                                                     - fields to be displayed  in the creation form.
- **template**                             (*"invenio_administration/create.html"*)     - template to be rendered for the view. Can be overridden by a custom template.

## Edit View

### Attributes

- **name**                                 (*view class name*)                          - view’s name used internally by Flask
- **url**                                  (*view's 'name'*)                            - url used to route the view.
- **resource_config**    *required*                                                     - used to retrieve the resource (refers to extension attribute - check ext.py)
- **pid_path**                             (*pid_path*)                                 - used for accessing the unique identifier of a resource 
- **api_endpoint**       *required*                                                     - used to update the resource.
- **title**              *required*                                                     - displays a title in the view page.
- **list_view_name**     *required*                                                     - name of the resource's list view name, enables  navigation between edit view and list view.
- **form_fields**        *required*                                                     - fields to be displayed  in the edit form.
- **template**                             (*"invenio_administration/edit.html"*)       - template to be rendered for the view. Can be overridden by a custom template.
