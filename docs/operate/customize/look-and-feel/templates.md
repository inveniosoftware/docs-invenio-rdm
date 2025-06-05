# Change templates

Out of the box, the front page of your instance provides links on how to change it. Perhaps you got here following those links. So let's change it!

Note that InvenioRDM supports overriding pre-existing templates by placing custom ones with the same filepath in the `templates/` folder.

## Change the front page

The original template for the front page (`frontpage.html`) is located [here](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm/frontpage.html) and the configuration value that sets it is:

```python
THEME_FRONTPAGE_TEMPLATE = 'invenio_app_rdm/frontpage.html'
"""Frontpage template."""
```

There are 2 options to change this template:

1. Change the configuration value setting to the new template path. This way, you can place and name your template file as you see fit.
2. Create a file with the same path relative to `templates` as the original. This way, you can keep the same structure and organization as InvenioRDM for your template file.

In this guide, we will see how to customize the front page using the second option.

**Step 1** - Create the template

The new `frontpage.html` template needs to be placed in the right location i.e. the same relative location it has in invenio-app-rdm.

**In invenio-app-rdm**, its path is the following (split-up to emphasize the part to copy):

```
invenio-app-rdm/invenio_app_rdm/theme/templates
└── semantic-ui/invenio_app_rdm/frontpage.html
```

**In your instance**, the path should then be:

```
templates
└── semantic-ui/invenio_app_rdm/frontpage.html
```

Copy the original `frontpage.html` there.

!!! info "Jinja templates"

    All backend-rendered InvenioRDM templates are [Jinja templates](https://jinja.palletsprojects.com/en/3.1.x/). Look at the Jinja documentation to see all that can be done with such templates.

We will simply change the content to the following as an example:

``` html+jinja
{%- extends "invenio_theme/frontpage.html" %}

{%- block page_header %}
{%- include "invenio_app_rdm/header_frontpage.html" %}
{%- endblock page_header %}

{%- block page_body %}
{%- block first_section %}
<div class="get-started-section section-content white-bg">
<h2 class="section-title">
    Spud-lunk through an archive of potato records.
</h2>

<div class="ui container three column stackable grid center aligned vertically padded relaxed">
    <div class="rdm-goal column">
        <h3 class="section-title">
        <a href="{{ url_for('invenio_search_ui.search') }}" >Search and Explore</a>
        </h3>
        <div class="command-line">
        Unearth records.
        </div>
    </div>
    <div class="rdm-goal column">
        <h3 class="section-title">
        <a href="{{ url_for('invenio_app_rdm_records.deposit_create') }}" >Make new records</a>
        </h3>
        <div class="command-line">Plant your contribution.</div>
    </div>
    <div class="rdm-goal column">
    <h3 class="section-title">
        <a href="{{ url_for('invenio_communities.communities_frontpage') }}" >Join a community</a>
    </h3>
    <div class="command-line">
        Grow with others.
    </div>
    </div>
</div>
</div>
{%- endblock first_section %}
{%- endblock page_body %}
```

!!! info "Side-note: How to find routes"

    To find the value to use in `url_for`, you can list InvenioRDM's routes via this command:

    ```shell
    pipenv run invenio routes
    ```

**Step 2** - Restart your server

You just need to restart your development server to see the changes.

```
<Ctrl+C>
invenio-cli run
```

## Custom templates workflow

The same pattern applies for any page. Create a template in your instance's `templates/` folder with the same path and name as the one you want to override. This way, your file is chosen rather than the default one. For another example, having `templates/semantic-ui/invenio_app_rdm/records/detail.html` in your instance, will make that template be used for generating the record landing page.

Any template is fair game e.g. the footer can be customized by copying and editing `footer.html` from
[invenio-app-rdm/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm/](https://github.com/inveniosoftware/invenio-app-rdm/tree/master/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm) into your instance:


```
templates
└── semantic-ui/invenio_app_rdm/footer.html
```
