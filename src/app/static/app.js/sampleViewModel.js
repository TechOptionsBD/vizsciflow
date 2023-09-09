function SampleViewModel(editor) {
    var self = this;
    self.samplesURI = '/samples';
    self.tasksURI = '/functions';
    self.workflowId = ko.observable(0);
    self.name = ko.observable("No Name");
    self.desc = ko.observable("No Description");
    self.access = ko.observable(0); // public access by default
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();
    self.wfParams = ko.observableArray();
    self.wfReturns = ko.observableArray();
    self.wfArgs = ko.observableArray();
    self.wfReturnArgs = ko.observableArray();
    self.TList = ko.observableArray();
    self.sampleEditor = editor ?? CreateAceEditor("#sample", "ace/mode/python", '40vh');
   
    self.isPublic = ko.computed(function()
    {
        return self.access() == 0;
    });
    
    self.loaddatatypes = function(){
        self.TList.removeAll();
        ajaxcalls.simple(self.tasksURI, 'GET', { 'datatypes': '' }).done(function (data) {
            $(data["datatypes"]).each((index, element)=> {
                self.TList.push(element);
            });
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }
    
    self.loaddatatypes();

    self.clear = function(){
        self.workflowId(0);
        self.name("No Name");
        self.desc("No description");
        self.access(0);
        self.userList.removeAll();
        self.selectedSharingUsers.removeAll();
        self.wfParams.removeAll();
        self.wfReturns.removeAll();
        self.wfArgs.removeAll();
        self.wfReturnArgs.removeAll();
        self.sampleEditor.session.setValue("", 1);
    }
    
    self.copy = function(src){
        self.clear();
        
        self.workflowId(src.workflowId());
        self.name(src.name());
        self.desc(src.desc());
        self.access(src.access());
        self.userList(src.userList());
        self.selectedSharingUsers(src.selectedSharingUsers());      
        self.wfParams(src.wfParams());
        self.wfReturns(src.wfReturns());
        self.wfArgs(src.wfArgs());
        self.wfReturnArgs(src.wfReturnArgs());
        self.TList(src.TList());
    }

    self.isEqualParamsJson = function(params, json){
        if (params.length != json.length) {
            return false;
        }

        json.forEach(function(param, index){
            if (params[index]['name'] != param['name'])
                return false;
            if (params[index]['type'] != param['type'])
                return false;
            if (params[index]['desc'] != param['desc'])
                return false;
        });

        return true;
    }

    self.copyFromJson = function(data) {
        self.workflowId(parseInt(data["id"]));
        self.name(data['name']);
        self.desc(data['desc']);
        self.access(parseInt(data['access']));
        if (!self.isEqualParamsJson(self.wfParams, data['params'])) {
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
                self.copyArgsFromParams(data['params']);
            }
        }
        if (!self.isEqualParamsJson(self.wfReturns, data['returns'])) {
            self.wfReturns.removeAll();
            if (Array.isArray(data['returns'])){
                data['returns'].forEach(function(param){
                    self.wfReturns.push(
                        ko.observableDictionary({
                            name: param['name'],
                            type: param['type'],
                            desc: param['desc']
                        })
                    );
                });
                self.copyReturnArgsFromReturns(data['returns']);
            }
        }
    }
    
    self.copyArgsFromParams = function(params){
        self.wfArgs.removeAll();
        params.forEach(function(param){
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
        returnParams.forEach(function(returnParam){
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
        
        if (self.name() === undefined)
            return;
        
        var formdata = new FormData();
        formdata.append('sample', self.sampleEditor.getSession().getValue());//you can append it to formdata with a proper parameter name
        
        formdata.append('id', self.workflowId() ?? 0);

        formdata.append('name', self.name());
        
        if (self.desc() !== undefined)
            formdata.append('desc', self.desc());
        
        if (self.access()) {
            formdata.append('access', 0);
        }
        else{
            if (self.selectedSharingUsers()) {
                formdata.append('access', 1);
                formdata.append('sharedusers', self.selectedSharingUsers());
            }
            else {
                formdata.append('access', 2);
            }
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
                access = parseInt(data.access);
                if (samplesViewModel.access() == access || samplesViewModel.access() == 3){
                    samplesViewModel.items.push({
                        id: ko.observable(data.id),
                        user:ko.observable(data.user),
                        name: ko.observable(data.name),
                        selected: ko.observable(false),
                        access: ko.observable(access),
                        isOwner: ko.observable(data.is_owner)
                    });
                }

                if (sampleViewModel) {
                    sampleViewModel.copyFromJson(data);
                    sampleViewModel.sampleEditor.session.getUndoManager().markClean();
                }
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
