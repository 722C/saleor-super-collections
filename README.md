# saleor-super-collections

Tree Structure Plugin for [Saleor](https://github.com/mirumee/saleor)'s Built In Collections

This provides a (currently skeleton) implementation of a tree structure for managing Saleor's built in collections. This is currently built for the `v2018.6` tag of Saleor.

Adding this tree structure as a separate model removes/reduces the need to modify the original source.

---

## Installation

To install, `pip install` the package as such:

```bash
pip install git+git://github.com/722c/saleor-super-collections.git#egg='saleor-super-collections'
```

Or list the package in your `requirements.txt` as such:

```
git+git://github.com/722c/saleor-super-collections.git#egg='saleor-super-collections'
```

Alternatively, this can be installed as a Git submodule directly in the root directory of your Saleor instance.

## Configuration

Once you have installed the app, you will need to add a few things to your project:

Add the app to your installed apps (the order doesn't matter):

```python
INSTALLED_APPS = [
    ...

    # Saleor plugins
    'saleor-super-collections.super_collections',

    ...
]
```

Add the apps URLs to your root `urls.py` in the `translatable_urlpatterns` near the bottom (this will allow any native Saleor URLs to be matched beforehand):

```python
translatable_urlpatterns = [
    ...
    url(r'^search/', include((search_urls, 'search'), namespace='search')),

    # URLs for saleor-super-collections
    url(r'', include('saleor-super-collections.super_collections.urls')),

    url(r'', include('payments.urls'))
]
```

The frontend view lives at `/{language_code}/super-collections`.

Finally, add the link to the dashboard by importing the template tag in `templates/dashboard/base.html` and putting it where you want in the side nav:

```django
<!DOCTYPE html>
{% load staticfiles i18n %}
 ...

 <!-- This is template tag you will need to load. -->
{% load super_collections_side_nav from super_collections %}

...

<ul class="side-nav">
  <li class="nav-home">
    <a href="{% url 'dashboard:index' %}">
      {% trans "Home" context "Dashboard homepage" %}
    </a>
  </li>
  {% if perms.product.view_product or perms.product.view_categories %}
  <li class="side-nav-section" id="first">
    ...
  </li>
  {% endif %}

  <!-- Add in the saleor-super-collections where you want. -->
  {% super_collections_side_nav %}

  ...
</ul>

...
```
