function SampleViewModel() {
    var self = this;
    self.samplesURI = '/samples';
    self.tasksURI = '/functions';
    self.name = ko.observable("No Name");
    self.desc = ko.observable("No Description");
    self.access = ko.observable();
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();

    self.sampleEditor = CreateAceEditor("#sample", "ace/mode/python", '40vh');

    self.addSample = function(task) {
        $('#addSample').modal('hide');
        
        var formdata = new FormData();
        formdata.append('sample', self.sampleEditor.getSession().getValue());//you can append it to formdata with a proper parameter name
        
        if (self.name() === undefined)
            return;
        formdata.append('name', self.name());
        
        if (self.desc() !== undefined)
            formdata.append('desc', self.desc());
        
        if (self.access()) {
            formdata.append('publicaccess', self.access());
        }
        else{
            formdata.append('sharedusers', self.selectedSharingUsers());
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

    self.getUsers = function () { 
        self.userList([]);
        self.selectedSharingUsers([]); 
        ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 1 }).done(function (data) {
            
            JSON.parse(data).forEach(element => {
                self.userList.push({id: element[0], name:  element[1]});
            });

            self.initiateMultiselectUser();
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    };

    self.initiateMultiselectUser = function () {  
        $("#wfUserSelection").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            dropUp: true,
            maxHeight: 200
        });
    };

    self.access.subscribe(function(newVal){
        
        if (newVal) {
            $("#wfUserSelection").multiselect('disable');
        } else {
            $("#wfUserSelection").multiselect('enable');
        }
    });
}
