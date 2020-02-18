function SampleViewModel() {
    var self = this;
    self.samplesURI = '/samples';
    
    self.name = ko.observable("No Name");
    self.desc = ko.observable("No Description");
    self.access = ko.observable("2");
    self.users = ko.observable();

    self.sampleEditor = CreateAceEditor("#sample", "ace/mode/python", 300);

    self.addSample = function(task) {
        $('#addSample').modal('hide');
        
        var formdata = new FormData();
        formdata.append('sample', self.sampleEditor.getSession().getValue());//you can append it to formdata with a proper parameter name
        
        if (self.name() === undefined)
            return;
        formdata.append('name', self.name());
        
        if (self.desc() !== undefined)
            formdata.append('desc', self.desc());
        
        if (self.access() !== undefined) {
            formdata.append('access', self.access());
        
            if (self.access() == 1) {
                formdata.append('users', self.users());
            }
        }

        ajaxcalls.form(self.samplesURI, 'POST', formdata).done(function(data) {
            if (!$.isEmptyObject(data)) {
                data = JSON.parse(data);
                 workflowId = data.id;
                 $('#script-name').text(data.name);
                 editor.session.getUndoManager().markClean();
             }
            
            samplesViewModel.load();
        });
    }
    
    self.getCodeEditor = function() { return self.sampleEditor; }
}
