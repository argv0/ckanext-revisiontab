""" Revision Tab extension """

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckan.controllers.package import PackageController
import ckan.lib.helpers as h

import re

import logging
log = logging.getLogger(__name__)


class RTPlugin(p.SingletonPlugin):
    """RTPlugin

    Shows inactive resources on a separate tab
    """

    tabtype = 'default'

    # ----------------
    # Template Helpers
    # ----------------
    def set_tab_type(self, string=None):
        self.tabtype = string
    def get_tab_type(self):
        return self.tabtype
    p.implements(p.ITemplateHelpers)
    def get_helpers(self):
        # add a new template helper
        return {
            'tab_type': self.get_tab_type
        }


    def check_tab_type(self):
        return re.search('/dataset/([^/]+)/(revision)$', h.full_current_url())


    p.implements(p.IConfigurer)
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        # inject custom scripts and css
        tk.add_resource('fanstatic', 'revisiontab')


    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IPackageController, inherit=True)

    def read(self, entity):
        return entity

    def create(self, entity):
        return entity

    def edit(self, entity):
        return entity

    def before_map(self, map):
        """Implements Iroutes.before_map
        Add our custom tab handler"""
        map.connect('dataset_revision',
                    '/dataset/{id}/revision',
                    controller='ckanext.revisiontab.plugin:RTController',
                    action='show',
                    ckan_icon='sitemap')
        return map

    def after_create(self, context, pkg_dict):
        return pkg_dict

    def after_update(self, context, pkg_dict):
        return pkg_dict

    def after_delete(self, context, pkg_dict):
        return pkg_dict

    def after_show(self, context, pkg_dict):
        return pkg_dict

    def before_search(self, search_params):
        return search_params

    def after_search(self, search_results, search_params):
        return search_results

    def before_index(self, pkg_dict):
        return pkg_dict

    def before_view(self, pkg_dict):
        """
        Filter out revision resources from normal resources
        Inactive resources are shown on their own tab
        """

        isRevisionView = self.check_tab_type()

        if isRevisionView:
            self.set_tab_type('revision')
            pkg_dict['resources'] = [ elem for elem in pkg_dict['resources'] if elem.get('state', False) != 'active' ]
        else:
            self.set_tab_type('default')
            pkg_dict['resources'] = [ elem for elem in pkg_dict['resources'] if elem.get('state', False) == "active" ]

        # log.info("pkg_dict: %s" % str(pkg_dict))

        return pkg_dict

    def read(self, entity):
        return entity



# -----------
# Controllers
# -----------

class RTController(PackageController):
    """ Revision Tab controller """

    def show(self, id):
        # do the default display for package controller "read" action
        return PackageController.read(self, id)

