function CreateAceEditor(editorId, mode, height) {
    // configure ace.js for code editor
    var mapperArea = $(editorId);

    var mapperDiv = $('<div>', {
        position: 'absolute',
        id: 'aceeditor',
        width: '100%',
        height: height,//mapperArea.height(),
        'class': mapperArea.attr('class'),
        'css': 'border:2px solid black'
    }).insertBefore(mapperArea);

    mapperArea.css('visibility', 'hidden');
    var offset = mapperDiv.offset();
    mapperArea.attr('rows', 1);

    var mapperEditor = ace.edit(mapperDiv[0]);
    mapperEditor.renderer.setShowGutter(false);
    mapperEditor.getSession().setValue(mapperArea.val());
    mapperEditor.getSession().setMode(mode);
    mapperEditor.setOptions({ highlightSelectedWord: true, enableBasicAutocompletion: true });
    mapperEditor.renderer.setOptions({ showGutter: true, displayIndentGuides: true });
    //editor.setKeyboardHandler("ace/keyboard/vim");
    //editor.setTheme("ace/theme/idle_fingers");
    //editor.setTheme("ace/theme/twilight");
    mapperEditor.setTheme("ace/theme/iplastic");
    //             editor.setOptions({       
    //                 fontSize: "12pt"
    //               });

    return mapperEditor;
}