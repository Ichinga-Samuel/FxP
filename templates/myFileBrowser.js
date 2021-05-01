
function myFileBrowser (field_name, url, type, win) {
    var cmsURL = '{% url 'media_list_editor' %}';

    if (cmsURL.indexOf("?") < 0) {
        cmsURL = cmsURL + "?type=" + type;
    }
    else {
        cmsURL = cmsURL + "&type=" + type;
    }

    tinyMCE.activeEditor.windowManager.open({
        file : cmsURL,
        title : 'Bilddatenbank',
        width : 800,
        height : 600,
        resizable : "yes",
        inline : "yes",
        close_previous : "no"
    }, {
        window : win,
        input : field_name
    });
    return false;

}