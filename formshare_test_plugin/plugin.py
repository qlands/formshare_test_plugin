import formshare.plugins as plugins
import formshare.plugins.utilities as u
from .views import MyPublicView, MyPrivateView
import sys
import os


def say_hello():
    pass


class FormShareTestPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IResource)
    plugins.implements(plugins.IPluralize)
    plugins.implements(plugins.ISchema)
    plugins.implements(plugins.IDatabase)
    plugins.implements(plugins.IProject)
    plugins.implements(plugins.IForm)
    plugins.implements(plugins.IRegistration)
    plugins.implements(plugins.IUserAuthentication)
    plugins.implements(plugins.IUserAuthorization)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IProduct)
    plugins.implements(plugins.IImportExternalData)
    plugins.implements(plugins.IRepository)
    plugins.implements(plugins.IPublicView)
    plugins.implements(plugins.IDashBoardView)
    plugins.implements(plugins.IProjectDetailsView)
    plugins.implements(plugins.IFormDetailsView)
    plugins.implements(plugins.ILogOut)

    # IRoutes
    def before_mapping(self, config):
        # We don't add any routes before the host application
        custom_map = [
            u.add_route("before_map", "/before_map", MyPublicView, None),
        ]
        return custom_map

    def after_mapping(self, config):
        # We add here a new route /json that returns a JSON
        custom_map = [
            u.add_route("before_map", "/before_map", MyPublicView, None),
            u.add_route(
                "plugin_mypublicview", "/mypublicview", MyPublicView, "public.jinja2"
            ),
            u.add_route(
                "plugin_myprivateview",
                "/user/{userid}/myprivateview",
                MyPrivateView,
                "private.jinja2",
            ),
        ]

        return custom_map

    # IConfig
    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "/opt/formshare_plugins/templates")

    def get_translation_directory(self):
        module = sys.modules["formshare_test_plugin"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "formshare_test_plugin"

    # IResources
    def add_libraries(self, config):
        libraries = [u.add_library("test_api", "/opt/formshare_plugins/resources")]
        return libraries

    def add_js_resources(self, config):
        my_plugin_js = [u.add_js_resource("test_api", "test_js", "test.js", None)]
        return my_plugin_js

    def add_css_resources(self, config):
        my_plugin_css = [u.add_css_resource("test_api", "test_css", "test.css", None)]
        return my_plugin_css

    # IPluralize
    def pluralize(self, noun, locale):
        return noun

    # ISchema
    def update_schema(self, config):
        return [u.add_field_to_form_schema("test_field", "Testing field")]

    # IDatabase
    def update_orm(self, metadata):
        pass

    # IProject
    def before_create(self, request, user, project_data):
        return project_data, True, ""

    def after_create(self, request, user, project_data):
        pass

    # IForm
    def after_odk_form_checks(
        self,
        request,
        user,
        project,
        form,
        form_data,
        form_directory,
        survey_file,
        create_file,
        insert_file,
        itemsets_csv,
    ):
        return True, ""

    def before_adding_form(
        self, request, form_type, user_id, project_id, form_id, form_data
    ):
        return True, "", form_data

    def after_adding_form(
        self, request, form_type, user_id, project_id, form_id, form_data
    ):
        pass

    def before_updating_form(
        self, request, form_type, user_id, project_id, form_id, form_data
    ):
        return True, "", form_data

    def after_updating_form(
        self, request, form_type, user_id, project_id, form_id, form_data
    ):
        pass

    def before_deleting_form(self, request, form_type, user_id, project_id, form_id):
        return True, ""

    def after_deleting_form(self, request, form_type, user_id, project_id, form_id):
        pass

    # IRegistration
    def before_register(self, request, registrant):
        return registrant, True, ""

    def after_register(self, request, registrant):
        return None

    # IUserAuthentication
    def after_login(self, request, user):
        return True, ""

    def on_authenticate_user(self, request, user_id, user_is_email):
        return None, {}

    def on_authenticate_password(self, request, user_data, password):
        return None, None

    def after_collaborator_login(self, request, collaborator):
        return True, ""

    # IUserAuthorization
    def before_check_authorization(self, request):
        return True

    def custom_authorization(self, request):
        return True, "qlands"

    # ITemplateHelpers
    def get_helpers(self):
        return {"say_hello": say_hello}

    # IProduct
    def register_products(self, config):
        return [
            {
                "code": "test",
                "hidden": False,
                "icon": "fas fa-box-open",
                "metadata": {"for": "testing "},
            }
        ]

    def get_product_description(self, request, product_code):
        if product_code == "test":
            return "Testing"
        else:
            return None

    def before_download_private_product(
        self, request, project, form, product, output, file_name, mime_type
    ):
        return True

    def before_download_public_product(
        self, request, project, form, product, output, file_name, mime_type
    ):
        return True

    def before_download_product_by_api(
        self, request, project, form, product, output, file_name, mime_type
    ):
        return True

    # IImportExternalData
    def import_external_data(
        self,
        request,
        user,
        project,
        form,
        odk_dir,
        form_directory,
        schema,
        assistant,
        temp_dir,
        project_code,
        geopoint_variable,
        project_of_assistant,
        import_type,
        post_data,
        ignore_xform,
    ):
        return None

    # IRepository
    def before_creating_repository(
        self, request, user, project, form, cnf_file, create_file, insert_file, schema
    ):
        return True

    def on_creating_repository(self, request, user, project, form, task_id):
        pass

    def custom_repository_process(
        self,
        request,
        user,
        project,
        form,
        odk_dir,
        form_directory,
        schema,
        primary_key,
        cnf_file,
        create_file,
        insert_file,
        create_xml_file,
        repository_string,
    ):
        pass

    # IPublicView
    def before_processing(self, request):
        return None

    def after_processing(self, request, context):
        return context

    # IDashBoardView
    def after_dashboard_processing(self, request, class_data, context):
        return context

    # IProjectDetailsView
    def after_project_details_processing(self, request, class_data, context):
        return context

    # IFormDetailsView
    def after_form_details_processing(self, request, class_data, context):
        return context

    # ILogOut
    def before_log_out(self, request, user, continue_logout):
        return True

    def after_log_out(self, request, user, redirect_url, logout_headers):
        pass


class FormShareTestAPIPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAPIRoutes)
    plugins.implements(plugins.IPrivateView)

    def before_mapping(self, config):
        # We don't add any routes before the host application
        custom_map = [
            u.add_route("api_before_map", "/before_map", MyPublicView, None),
        ]
        return custom_map

    def after_mapping(self, config):
        # We add here a new route /json that returns a JSON
        custom_map = [
            u.add_route("api_after_map", "/before_map", MyPublicView, None),
            u.add_route("api_after_map2", "/before_map2", MyPublicView, None),
        ]

        return custom_map

    def before_processing(self, request, class_data):
        pass


class FormShareTestAssistantPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAssistant)
    plugins.implements(plugins.IFormAccess)

    def before_create(self, request, user, project, assistant_data):
        return assistant_data, True, ""

    def after_create(self, request, user, project, assistant_data):
        pass

    def before_edit(self, request, user, project, assistant, assistant_data):
        return assistant_data, True, ""

    def after_edit(self, request, user, project, assistant, assistant_data):
        pass

    def before_delete(self, request, user, project, assistant):
        return True, ""

    def after_delete(self, request, user, project, assistant):
        pass

    def before_password_change(self, request, user, project, assistant, password):
        return True, ""

    def after_password_change(self, request, user, project, assistant, password):
        pass

    # IFormAccess
    def before_giving_access(
        self,
        request,
        user,
        project,
        form,
        assistant_project,
        assistant_id,
        privilege_data,
    ):
        return privilege_data, True, ""

    def after_giving_access(
        self,
        request,
        user,
        project,
        form,
        assistant_project,
        assistant_id,
        privilege_data,
    ):
        pass

    def before_editing_access(
        self,
        request,
        user,
        project,
        form,
        assistant_project,
        assistant_id,
        privilege_data,
    ):
        return privilege_data, True, ""

    def after_editing_access(
        self,
        request,
        user,
        project,
        form,
        assistant_project,
        assistant_id,
        privilege_data,
    ):
        pass

    def before_revoking_access(
        self, request, user, project, form, assistant_project, assistant_id
    ):
        return True, ""

    def after_revoking_access(
        self, request, user, project, form, assistant_project, assistant_id
    ):
        pass


class FormShareTestAssistantGroupPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAssistantGroup)
    plugins.implements(plugins.IFormGroupAccess)
    plugins.implements(plugins.IJSONSubmission)

    def before_create(self, request, user, project, group_data):
        return group_data, True, ""

    def after_create(self, request, user, project, group_data):
        pass

    def before_edit(self, request, user, project, assistant, group_data):
        return group_data, True, ""

    def after_edit(self, request, user, project, assistant, group_data):
        pass

    def before_delete(self, request, user, project, group, group_data):
        return True, ""

    def after_delete(self, request, user, project, group, group_data):
        pass

    # IFormGroupAccess
    def before_giving_access(
        self, request, user, project, form, group_project, assistant_group
    ):
        return True, ""

    def after_giving_access(
        self, request, user, project, form, group_project, group_id
    ):
        pass

    # IJSONSubmission
    def before_processing_submission(
        self, request, user, project, form, assistant, json_file
    ):
        return 0, ""

    def after_processing_submission_in_repository(
        self, request, user, project, form, assistant, submission, error, json_file
    ):
        pass

    def after_processing_submission_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file
    ):
        pass


class FormShareTestUserPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IUser)
    plugins.implements(plugins.IEnvironment)
    plugins.implements(plugins.IXMLSubmission)
    plugins.implements(plugins.IMediaSubmission)

    def before_create(self, request, user_data):
        return user_data, True, ""

    def after_create(self, request, user_data):
        pass

    def before_edit(self, request, user, user_data):
        return user_data, True, ""

    def after_edit(self, request, user, user_data):
        pass

    # IEnvironment
    def after_environment_load(self, config):
        pass

    # IXMLSubmission
    def before_processing_submission(
        self, request, user, project, form, assistant, xml_file
    ):
        return True, 0

    def after_processing_submission(
        self, request, user, project, form, assistant, error, xml_file
    ):
        pass

    # IMediaSubmission
    def after_storing_media_in_repository(
        self, request, user, project, form, assistant, submission, json_file, media_file
    ):
        pass

    def after_storing_media_not_in_repository(
        self, request, user, project, form, assistant, submission, json_file, media_file
    ):
        pass


class FormShareTestObserverPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IPluginObserver)

    def before_load(self, plugin):
        pass

    def after_load(self, service):
        pass

    def before_unload(self, plugin):
        pass

    def after_unload(self, service):
        pass
