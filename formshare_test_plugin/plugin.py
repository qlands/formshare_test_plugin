import formshare.plugins as plugins
import formshare.plugins.utilities as u
from .views import MyPublicView, MyPrivateView
import sys
import os
from pyramid.httpexceptions import HTTPFound
from formshare.processes.odk.api import get_odk_path, get_form_schema
import csv
import uuid

def say_hello():
    pass


# noinspection PyMethodMayBeStatic,PyUnusedLocal
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
    plugins.implements(plugins.ILogOut)
    plugins.implements(plugins.IPartnerAuthentication)
    plugins.implements(plugins.IExport)
    plugins.implements(plugins.IAssistantAuthentication)
    plugins.implements(plugins.ICollaborator)
    plugins.implements(plugins.IFormFileGenerator)
    plugins.implements(plugins.IFormDataColumns)

    # IPartnerAuthentication
    def after_partner_login(self, request, partner):
        return True, ""

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
        templates_dir = os.path.join(
            config.registry.settings["formshare.test.directory"],
            *["resources", "plugin", "templates"]
        )

        u.add_templates_directory(config, templates_dir)

    def get_translation_directory(self):
        module = sys.modules["formshare_test_plugin"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "formshare_test_plugin"

    # IResources
    def add_libraries(self, config):
        resources_dir = os.path.join(
            config.registry.settings["formshare.test.directory"],
            *["resources", "plugin", "resources"]
        )

        libraries = [u.add_library("test_api", resources_dir)]
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

    def update_extendable_tables(self, tables_allowed):
        return tables_allowed

    def update_extendable_modules(self, modules_allowed):
        return modules_allowed

    # IProject
    def before_creating_project(self, request, user, project_data):
        return True, ""

    def after_creating_project(self, request, user, project_data):
        pass

    def before_editing_project(self, request, user, project, project_details):
        return True, ""

    def after_editing_project(self, request, user, project, project_data):
        pass

    def before_deleting_project(self, request, user, project):
        return True, ""

    def after_deleting_project(self, request, user, project, project_forms):
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

    def after_deleting_form(
        self, request, form_type, user_id, project_id, form_id, form_data
    ):
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

    def after_assistant_login(self, request, collaborator):
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

    def before_partner_download_private_product(
        self, request, partner, project, form, product, output, file_name, mime_type
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

    def before_partner_download_product_by_api(
        self, request, partner, project, form, product, output, file_name, mime_type
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
        return request.route_url("home")

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
    def before_processing_public_view(self, route_name, request):
        return True

    def after_processing_public_view(self, route_name, request, context):
        return context

    # ILogOut
    def before_log_out(self, request, user, continue_logout):
        return True

    def after_log_out(self, request, user, redirect_url, logout_headers):
        return redirect_url, logout_headers

    # IExport
    def has_export_for(self, request, export_type):
        if export_type == "TEST":
            return True

    def do_export(self, request, export_type):
        return HTTPFound(location=request.route_url("home"))

    # ICollaborator
    def before_adding_collaborator(self, request, project_id, collaborator_id):
        return True, ""

    def after_accepting_collaboration(self, request, project_id, collaborator_id):
        pass

    def before_removing_collaborator(self, request, project_id, collaborator_id, collaboration_details):
        return True, ""

    def after_removing_collaborator(self, request, project_id, collaborator_id, collaboration_details):
        pass

    # IFormFileGenerator
    def generate_form_file(self, request, user_id, project_id, form_id, file_name):
        if file_name == "generated.csv" or file_name == "generated_case.csv":
            odk_dir = get_odk_path(request)
            uid = str(uuid.uuid4())

            paths = ["tmp", uid]
            os.makedirs(os.path.join(odk_dir, *paths))

            paths = ["tmp", uid, file_name]
            temp_csv = os.path.join(odk_dir, *paths)
            outfile = open(temp_csv, "w")
            out_csv = csv.writer(outfile)
            if get_form_schema(request, project_id, form_id) is None:
                heading = ["list_name", "name", "label", "country_id"]
                out_csv.writerow(x for x in heading)
                row = ["projects", "001", "Test project", "UG"]
                out_csv.writerow(x for x in row)
            else:
                heading = ["list_name", "name", "label", "country_id"]
                out_csv.writerow(x for x in heading)
                row = ["projects", "001", "Test project", "UG"]
                out_csv.writerow(x for x in row)
                row = ["projects", "002", "Test project 2", "UG"]
                out_csv.writerow(x for x in row)
            outfile.close()
            return temp_csv
        return None

    # IFormDataColumns
    def filter_form_survey_columns(
            self, request, user_id, project_id, form_id, survey_columns
    ):
        pass

    def filter_form_choices_columns(
            self, request, user_id, project_id, form_id, choices_columns
    ):
        pass

    def add_to_form_survey_columns(
            self, request, user_id, project_id, form_id, survey_columns
    ):
        pass

    def add_to_form_choices_columns(
            self, request, user_id, project_id, form_id, choices_columns
    ):
        pass

    def get_form_survey_property_info(
            self,
            request,
            user_id,
            project_id,
            form_id,
            table_name,
            field_name,
            property_name,
    ):
        return property_name, False


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class FormShareTestAPIPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAPIRoutes)
    plugins.implements(plugins.IPrivateView)
    plugins.implements(plugins.IAssistantView)
    plugins.implements(plugins.IPartnerView)

    def after_api_mapping(self, config):
        # We don't add any routes before the host application
        custom_map = [
            u.add_route("api_before_map", "/before_map", MyPublicView, None),
        ]
        return custom_map

    def before_api_mapping(self, config):
        # We add here a new route /json that returns a JSON
        custom_map = [
            u.add_route("api_after_map", "/before_map", MyPublicView, None),
            u.add_route("api_after_map2", "/before_map2", MyPublicView, None),
        ]

        return custom_map

    def before_processing(self, route_name, request, class_data):
        pass

    def after_processing(self, route_name, request, class_data, context):
        return context

    def before_processing_assistant_view(self, route_name, request, context):
        pass

    def after_processing_assistant_view(self, route_name, request, context):
        return context

    def before_processing_partner_view(self, route_name, request, context):
        pass

    def after_processing_partner_view(self, route_name, request, context):
        return context


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class FormShareTestAssistantPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAssistant)
    plugins.implements(plugins.IFormAccess)

    def before_creating_assistant(self, request, user, project, assistant_data):
        return assistant_data, True, ""

    def after_creating_assistant(self, request, user, project, assistant_data):
        pass

    def before_editing_assistant(
        self, request, user, project, assistant, assistant_data
    ):
        return assistant_data, True, ""

    def after_editing_assistant(
        self, request, user, project, assistant, assistant_data
    ):
        pass

    def before_deleting_assistant(self, request, user, project, assistant):
        return True, ""

    def after_deleting_assistant(self, request, user, project, assistant):
        pass

    def before_assistant_password_change(
        self, request, user, project, assistant, password
    ):
        return True, ""

    def after_assistant_password_change(
        self, request, user, project, assistant, password
    ):
        pass

    # IFormAccess
    def before_giving_access_to_assistant(
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

    def after_giving_access_to_assistant(
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

    def before_editing_assistant_access(
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

    def after_editing_assistant_access(
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

    def before_revoking_assistant_access(
        self, request, user, project, form, assistant_project, assistant_id
    ):
        return True, ""

    def after_revoking_assistant_access(
        self, request, user, project, form, assistant_project, assistant_id
    ):
        pass


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class FormShareTestAssistantGroupPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAssistantGroup)
    plugins.implements(plugins.IFormGroupAccess)
    plugins.implements(plugins.IJSONSubmission)

    def before_creating_group(self, request, user, project, group_data):
        return group_data, True, ""

    def after_creating_group(self, request, user, project, group_data):
        pass

    def before_editing_group(self, request, user, project, assistant, group_data):
        return group_data, True, ""

    def after_editing_group(self, request, user, project, assistant, group_data):
        pass

    def before_deleting_group(self, request, user, project, group, group_data):
        return True, ""

    def after_deleting_group(self, request, user, project, group, group_data):
        pass

    # IFormGroupAccess
    def before_giving_access_to_group(
        self, request, user, project, form, group_project, assistant_group
    ):
        return True, ""

    def after_giving_access_to_group(
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


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class FormShareTestUserPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IUser)
    plugins.implements(plugins.IEnvironment)
    plugins.implements(plugins.IXMLSubmission)
    plugins.implements(plugins.IMediaSubmission)

    def before_creating_user(self, request, user_data):
        return user_data, True, ""

    def after_creating_user(self, request, user_data):
        pass

    def before_editing_user(self, request, user, user_data):
        return user_data, True, ""

    def after_editing_user(self, request, user, user_data):
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


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class FormShareTestPartnerPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IPartner)

    def before_creating_partner(self, request, partner_data):
        return partner_data, True, ""

    def after_creating_partner(self, request, partner_data):
        pass

    def before_editing_partner(self, request, partner_id, partner_data):
        return partner_data, True, ""

    def after_editing_partner(self, request, partner_id, partner_data):
        pass

    def before_deleting_partner(self, request, partner_id, partner_data):
        return True, ""

    def after_deleting_partner(self, request, partner_id):
        pass

    def before_partner_password_change(self, request, partner_id, password):
        return True, ""

    def after_partner_password_change(self, request, partner_id, password):
        pass
