function ScriptViewModel() {
    var self = this;
    self.prevModeScript = ko.observable('')

    self.getPrevModeScript = function(){
        return self.prevModeScript()
    }
    self.setPrevScript = function(){
        var currentScript = editor.session.getValue()
        editor.session.setValue("");
        editor.session.insert(editor.selection.getCursor(), self.prevModeScript());
        editor.focus();
        self.prevModeScript(currentScript)
    }
}