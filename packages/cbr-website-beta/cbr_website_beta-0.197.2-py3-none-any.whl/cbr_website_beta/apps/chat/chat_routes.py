from flask import render_template

from cbr_shared.config.Server_Config__CBR_Website               import server_config__cbr_website
from cbr_website_beta.apps.chat                                 import blueprint
from cbr_website_beta.cbr__flask.decorators.allow_annonymous    import allow_anonymous, admin_only


@blueprint.route('/stats')
@admin_only
def chat_stats():
    from cbr_athena.llms.storage.CBR__Chats__Analysis import CBR__Chats__Analysis
    title         = "Chat - Stats"
    content_view  = '/llms/chats/stats.html'
    template_name = '/pages/page_with_view.html'


    chats_stats = CBR__Chats__Analysis().chats_stats()

    return render_template( template_name_or_list = template_name ,
                            content_view          = content_view  ,
                            title                 = title         ,
                            stats                 = chats_stats   )

@blueprint.route('/history')
@admin_only
def chat_history():
    from cbr_athena.llms.storage.CBR__Chats_Storage__Local import CBR__Chats_Storage__Local
    title         = "Chat - History"
    content_view  = '/llms/chats/history.html'
    template_name = '/pages/page_with_view.html'


    cbr_chats_storage_local = CBR__Chats_Storage__Local().setup()
    #chat_ids = cbr_chats_storage_local.chats_ids()
    chats_latest = cbr_chats_storage_local.chats_latest()

    return render_template( template_name_or_list = template_name ,
                            content_view          = content_view  ,
                            title                 = title         ,
                            chats                 = chats_latest  )

@blueprint.route('/view/<path:path>/pdf')
@allow_anonymous
def chat_view__from_chat_id__pdf(path=None):
    from cbr_website_beta.cbr__flask.utils.current_server import current_server
    url_for_screenshot = f'{current_server()}web/chat/view/{path}'                 # todo: add path validation
    return url_for_screenshot

@blueprint.route('/view/<path:path>')
@allow_anonymous
def chat_view__from_chat_id(path=None):
    title             = "Chat - View past chat"
    content_view      = '/llms/chat_with_llms/view_chat_from_chat_id.html'
    template_name     = '/pages/page_with_view.html'
    url_athena        = server_config__cbr_website.target_athena_url()  + '/llms/chat/completion'
    url_chat_data     = server_config__cbr_website.target_athena_url()  + f'/llms/chat/view?chat_id={path}'
    platform = "Groq (Free)"
    provider = "1. Meta"
    model    = "llama3-70b-8192"

    return render_template( template_name_or_list = template_name ,
                            content_view          = content_view  ,
                            title                 = title         ,
                            url_athena            = url_athena    ,
                            platform              = platform      ,
                            provider              = provider      ,
                            model                 = model         ,
                            chat_id               = path          ,
                            url_chat_data         = url_chat_data )