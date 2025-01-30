function SampleViewModel(editor) {
    var self = this;
    self.samplesURI = '/samples';
    self.tasksURI = '/functions';
    self.workflowId = ko.observable(0);
    self.name = ko.observable("No Name");
    self.desc = ko.observable("No Description");
    self.access = ko.observable(0); // public access by default
    self.isPublic = ko.observable(true);
    self.userList = ko.observableArray();
    self.selectedSharingUsers = ko.observableArray();
    self.wfParams = ko.observableArray();
    self.wfReturns = ko.observableArray();
    self.wfArgs = ko.observableArray();
    self.wfReturnArgs = ko.observableArray();
    self.TList = ko.observableArray();
    self.chatMessages = ko.observableArray([]);
	self.newMessage = ko.observable("");
    self.sampleEditor = editor ?? CreateAceEditor("#sample", "ace/mode/python", '40vh');
       
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
        self.isPublic(true);
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
        self.isPublic(src.isPublic());
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
        self.isPublic(parseInt(data['access']) == 0);
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
        
        if (self.isPublic()) {
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
        ajaxcalls.simple(self.tasksURI, 'GET', { 'users': 0 }).done(function (data) {
            
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

    self.sendMessage = function(message) {
        if (self.workflowId() === 0 || message === "")
            return;
        
        try {
            if (!socket.connected) {
                socket.connect(); 
            }

            socket.emit('message', {'workflow_id': self.workflowId(), 'message': self.newMessage()});
            self.newMessage("");
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    self.leavechat = function() {
        if (self.workflowId() === 0)
            return;

        if (socket.connected) {
            socket.emit('leavechat', self.workflowId());
        }
    }

    self.joinchat = function() {
        if (self.workflowId() === 0)
            return;

        if (!socket.connected) {
            socket.connect();
        }
        ajaxcalls.simple(self.tasksURI, 'GET', {'chathistory': self.workflowId()}).done(function (chats) {
            self.chatMessages.removeAll();
            if (chats !== undefined && chats !== null && Array.isArray(chats)){
                chats.forEach(chat => {
                    self.chatMessages.push({'user': chat.user, 'message': chat.message});
                });
            }
            
            var objDiv = $("#chatMessages");
            objDiv.scrollTop(objDiv.prop("scrollHeight"));
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
        
        socket.emit('joinchat', self.workflowId());
    }

    self.aboutcollab = function() {
        window.open("static/biodsl-help.html#collab", '_blank');
    }

    self.collabmerge = function() {
        ajaxcalls.simple(self.samplesURI, 'GET', {'merge': self.workflowId(), 'script': $.trim(editor.getSession().getValue())}).done(function (res) {
            samplesViewModel.loadIntoEditor(item.id());

            $('#wfVersionSelectionAlertV').show();
            $('#wfVersionSelectionAlertV').text('Workflow merged successfully!');
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.collabpush = function() {
        if (!confirm("Are you sure you want to push this workflow? It will overwrite the changes by other collaborators."))
            return;
        ajaxcalls.simple(self.samplesURI, 'GET', {'push': self.workflowId(), 'script': $.trim(editor.getSession().getValue())}).done(function (res) {
            $('#wfVersionSelectionAlertV').show();
            $('#wfVersionSelectionAlertV').text('Workflow pushed and successfully!');
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.collabcompare = function() {
        self.getAllVersion(self.workflowId());
        $('#collabPanel').hide();
        $('#wfVersionCompareSelection').show();
    }

    self.collabclose = function() { 
        self.leavechat();
    }

    self.collabopen = function() {
        self.joinchat();
    }

    self.shouldSendEnabled = ko.computed(function() {
        return self.newMessage().length !== 0;
    });

    self.wfVersionSelectionChange = function () {
        if (self.selectedWfVersionId1()[0] == self.selectedWfVersionId2()[0]) {
            $('#wfVersionSelectionAlertV').show();
            $('#wfVersionSelectionAlertV').text('Please select two different versions!');
        }
        else {
            $('#wfVersionSelectionAlertV').hide();
            $('#wfVersionSelectionAlertV').text('');
        }
    }

    self.compareSelectedWf = function () {
        //compare two versions of selected workflow
        let selectedWfVersionId1 = ko.toJS(self.selectedWfVersionId1()[0]);
        let selectedWfVersionId2 = ko.toJS(self.selectedWfVersionId2()[0]);
        
        if (selectedWfVersionId1 === undefined || selectedWfVersionId2 === undefined){
            self.wfVersionSelectionChange();
            return;
        }
            
        if(selectedWfVersionId1 !== selectedWfVersionId2){
            ajaxcalls.simple(self.samplesURI, 'GET', {'revcompare': true,'revision1': selectedWfVersionId1, 'revision2': selectedWfVersionId2}).done(function (res) {
                $('#wfVersionCompareSelection').modal('hide');
                $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                    $('#liProvenanceTab').show();
                });
                tasksViewModel.createCompView(res) 
            }).fail(function (jqXHR) {
                showXHRText(jqXHR);
            });
        }
    }

    self.getAllVersion = function (workflowId) {
        self.wfVersionList([]);
        ajaxcalls.simple(self.samplesURI, 'GET', {'revisions': workflowId}, true).done(function (data) {
            //get the version list here & make dropdown from it
            if (data !== undefined && data !== null && Array.isArray(data)){
                data.forEach(wfVersion => {
                    self.wfVersionList.push({
                        hex: wfVersion.hex,
                        name: wfVersion.summary,
                        committer: wfVersion.committer,
                        time: wfVersion.time
                    }); 
                });
                
                self.initiateWfVersionSelectionDdl();
            }
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    };

    self.initiateWfVersionSelectionDdl = function () {
        $("#compareWfVersion1V").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });

        $("#compareWfVersion2V").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });
    };
}
