# coding=UTF-8
""" Revision Tab extension """

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.helpers as h

# from ckan.controllers.package import PackageController

import logging
log = logging.getLogger(__name__)

# from logic import NotAuthorized

from routes.mapper import SubMapper

import pylons.config as pluginconf # to get the config setting for this plugin

from ckan.common import c
from ckan import authz as auth


class RTPlugin(p.SingletonPlugin):
    """RTPlugin

    Shows the list of revisions on a separate tab
    """

    tabtype = 'default'

    admin_only = False

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
            'tab_type': self.get_tab_type,
            'admin_only': self.admin_only
        }

    p.implements(p.IConfigurer)
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths
        tk.add_template_directory(config, 'templates')
        # inject custom scripts and css
        # tk.add_resource('fanstatic', 'revisiontab')


    # p.implements(p.IPackageController, inherit=True)
    # def before_view(self, pkg_dict):
    #     log.debug("xxxxxxxxxxxxxxxxxxxxxxxx Translating the package")
    #     return super(RTPlugin, self).before_view(pkg_dict)


    p.implements(p.IRoutes, inherit=True)
    def before_map(self, map):
        """
        Implements Iroutes.before_map
        Add our custom tab handler
        """

        self.admin_only = pluginconf.get('ckanext.revisiontab.admin_only', False)

        # if c and c.userobj and c.userobj.name:
        #     username = c.userobj.name
        # else:
        #     username = model.User.get(username)

        # if admin_only and auth.is_sysadmin(username):

        # admin-only setting
        # if admin_only and c and c.is_sysadmin:

        # add_tab = True
        # try:
        #     context = {'model': model, 'user': c.user, 'auth_user_obj': c.userobj}
        #     if admin_only and not tk.check_access('sysadmin', context):
        #         add_tab = False
        # except NotAuthorized:
        #     add_tab = False
        # if add_tab:

        # ckan.controllers.package:PackageController
        with SubMapper(map, controller='package') as m:
            m.connect('dataset_revision',
                '/dataset/revision/{id}',
                action='history',
                ckan_icon='sitemap'
            )

        return map
