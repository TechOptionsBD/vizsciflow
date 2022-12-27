function SampleViewModel() {
    var self = this;
    self.samplesURI = '/samples';
    self.tasksURI = '/functions';
    self.workflowId = ko.observable(0);
    self.name = ko.observable("No Name");
    self.desc = ko.observable("No Description");
    self.access = ko.observable();
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();
    self.wfParams = ko.observableArray();
    self.wfReturns = ko.observableArray();
    self.wfArgs = ko.observableArray();
    self.wfReturnArgs = ko.observableArray();
    self.TList = ko.observableArray(['int', 'int[]','float','float[]','str','str[]','bool','bool[]','any','any[]']);
    self.sampleEditor = CreateAceEditor("#sample", "ace/mode/python", '40vh');
   
    self.clear = function(){
        self.workflowId(0);
        self.name("No Name");
        self.desc("No description");
        self.wfParams.removeAll();
        self.wfReturns.removeAll();
        self.wfArgs.removeAll();
        self.wfReturnArgs.removeAll();
        self.getCodeEditor().session.setValue("", 1);
    }

    self.copy = function(src){
        self.workflowId(src.workflowId());
        self.name(src.name());
        self.desc(src.desc());
        self.access(src.access());
        self.userList(src.userList());
        self.selectedSharingUsers(src.selectedSharingUsers());
        self.wfParams(src.wfParams());
        self.wfReturns(src.wfReturns());
        self.copyArgsFromParams(self.wfParams);
        self.copyReturnArgsFromReturns(self.wfReturns);
    }

    self.copyFromJson = function(data) {
        self.workflowId(parseInt(data["id"]));
        self.name(data['name']);
        self.desc(data['desc']);
        self.access(data['access']);
        self.wfParams.removeAll();
        if (Array.isArray(data['params'])){
            data['params'].forEach(function(param){
                self.wfParams.push(
                    ko.observableDictionary({
                        name: param['name'],
                        type: param['type'],
                        desc: param['desc'],
                        default: param['default'] === undefined ? "" : param['default']
                    })
                );
            });
        }

        self.wfReturns.removeAll();
        if (Array.isArray(data['params'])){
            data['returns'].forEach(function(param){
                self.wfReturns.push(
                    ko.observableDictionary({
                        name: param['name'],
                        type: param['type'],
                        desc: param['desc'],
                        default: param['default'] === undefined ? "" : param['default']
                    })
                );
            });
        }

        self.copyArgsFromParams(self.wfParams());
        self.copyReturnArgsFromReturns(self.wfReturns());
    }
    
    self.copyArgsFromParams = function(params){
        self.wfArgs.removeAll();
        ko.utils.arrayForEach(params, function(param) {
            self.wfArgs.push(
                ko.observableDictionary({
                    name: param['name'],
                    type: param['type'],
                    desc: param['desc'],
                    value: param['default'] === undefined ? "" : param['default']
                })
            );
        });
    }

    self.copyReturnArgsFromReturns = function(returnParams){
        self.wfReturnArgs.removeAll();
        ko.utils.arrayForEach(returnParams, function(returnParam) {
            self.wfReturnArgs.push(
                ko.observableDictionary({
                    name: returnParam['name'],
                    type: returnParam['type'],
                    desc: returnParam['desc']
                })
            );
        });
    }

    self.add = function() {
        $('#addSample').modal('hide');
        
        var formdata = new FormData();
        formdata.append('sample', self.sampleEditor.getSession().getValue());//you can append it to formdata with a proper parameter name
        
        formdata.append('id', self.workflowId() === undefined ? 0 : self.workflowId());

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

        if(self.wfParams() !== null){
            formdata.append('params', ko.toJSON(self.wfParams));
        }

        if(self.wfReturns() !== null){
            formdata.append('returns', ko.toJSON(self.wfReturns));
        }

        ajaxcalls.form(self.samplesURI, 'POST', formdata).done(function(data) {
            if (!$.isEmptyObject(data)) {
                data = JSON.parse(data);

                if (samplesViewModel.access() == data.access || samplesViewModel.access() == 3){
                    samplesViewModel.items.push({
                        id: ko.observable(data.id),
                        user:ko.observable(data.user),
                        name: ko.observable(data.name),
                        selected: ko.observable(false),
                        access: ko.observable(data.access),
                        isOwner: ko.observable(data.is_owner)
                    });
                }

                self.copyFromJson(data);

                // update view
                workflowId = data.id;
                editor.session.getUndoManager().markClean();
            }
        });
    }

    self.addParam = function () {
        self.wfParams.push(
            ko.observableDictionary({
                name: '',
                type: '',
                desc: '',
                default:''
            })
        );
    };
    
    self.removeParam = function (data, e) {
        self.wfParams.remove(data);
    };

    self.addReturns = function () {
        self.wfReturns.push(
            ko.observableDictionary({
                name: '',
                type: '',
                desc: ''
            })
        );
    };
    
    self.removeReturns = function (data, e) {
        self.wfReturns.remove(data);
    };

    self.getCodeEditor = function() { return self.sampleEditor; }

    self.getUsers = function () { 
        self.userList([]);
        self.selectedSharingUsers([]); 
        ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 1 }).done(function (data) {
            
            data = Array.isArray(data) ? data : JSON.parse(data);
            data.forEach(element => {
                e = JSON.parse(element);
                self.userList.push({id: parseInt(e[0]), name:  e[1]});
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
        $("#wfUserSelection").multiselect(newVal ? 'disable' : 'enable');
    });
}
