function SamplesViewModel(sampleViewModel) {
    var self = this;
    self.samplesURI = '/samples';
    self.tasksURI = '/functions';
    self.clicks = 0;
    self.timer = null;
    self.items = ko.observableArray();
    self.sampleViewModel = sampleViewModel;
    self.access = ko.observable("0");
    self.workflowFilter = ko.observable("");
    self.wfList = ko.observableArray();
    self.selectedWfId1 = ko.observableArray();
    self.selectedWfId2 = ko.observableArray();
    self.wfVersionList = ko.observableArray();
    self.selectedWfVersionId1 = ko.observableArray();
    self.selectedWfVersionId2 = ko.observableArray();
     self.filteredWorkflows = ko.computed(function(){
        return this.items().filter(function(item){
            if(!self.workflowFilter() || item.name().toLowerCase().indexOf(self.workflowFilter().toLowerCase()) !== -1)
              return item;
        });
       },this);
     
   self.about = function() {
       
       window.open("static/biodsl-help.html#workflows", '_blank');
   }

    self.remove = function() {
        
        var item = self.firstSelectedItem();
        if (item == null)
            return;
        
        ajaxcalls.simple(self.samplesURI, 'POST', { 'delete': item.name }).done(function(data) {
            self.load();
        });
    }
    
    self.newwf = function() {
        self.saveCurrentLoadintoEditor(null);
    }
    
    self.beginAdd = function() {
        var script = editor.getSession().getValue();
        if (script.length > 0) {
            self.sampleViewModel.getCodeEditor().setValue(script, 1);
         }
        var scriptname = $('#script-name').text();
        if (scriptname.length <= 0) {
            scriptname = "No Name";
        }
        self.sampleViewModel.name(scriptname);
        sampleViewModel.getUsers();
        $('#addSample').modal('show');
    }
    
    self.firstSelectedItem = function() {
        var items = self.items();
        for (var i = 0; i < items.length; i++) {
            if (items[i].selected()){
                return items[i];
            }
        }
        return null;
    }
    
    self.saveNeeded = function() {
        var script = $.trim(editor.getSession().getValue());
        if (script)
            script = script.trim();
       if (!script && !workflowId) // || editor.session.getUndoManager().isClean())
              return false; // if script empty and workflowId not set, it means (empty) workflow is not set yet.
          
       return isDirty;
    }

    self.toggleExpand = function (item, event) {
        event.stopPropagation();
        self.clicks++;
        if (self.clicks !== 1) {
            $(".expandedWorkflow").remove();
            self.loadIntoEditor(item);
            self.clicks = 0
            return;
        }
        else {
            self.clicks= 0;
            var domItem = $(event.target);
            if (domItem.next().next('div .expandedWorkflow').length !== 0) {
                $(".expandedWorkflow").remove();
                return;
            } else {
                $(".expandedWorkflow").remove();

                tooltip = "<div class=\"expandedWorkflow\" style=\"margin-top: 40px \"> <p>Name: " + item.name() + "<br>Owner: " + item.user() + "<br>Selected: " + item.selected() + "</p>";
                tooltip += "</p>";
                tooltip += "<p>Double click item to insert into code editor.</p></div>";

                domItem.parents('.draggable-workflow').append(tooltip);
            }
        }
         
    };
    
    self.loadIntoEditor = function(item) {
        
        if (!item) {
            workflowId = 0;
            $('#script-name').text('New script');
            editor.session.setValue("");
            $('#args').val('');
            return;
        }
        
         ajaxcalls.simple(self.samplesURI, 'GET', {'sample_id': item.id}).done(function(data) {
            
               if ($.isEmptyObject(data))
                   return;
            
            editor.session.setValue(data['script']);
            editor.focus();

            workflowId = item.id();
            $('#script-name').text(item.name());
            $('#args').val('');
            
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.dropNLoadIntoEditor = function(item) {
         ajaxcalls.simple(self.samplesURI, 'GET', {'sample_id': item.id}).done(function(data) {
            if ($.isEmptyObject(data))
                return;
            
            var pos = editor.selection.getCursor();
            editor.session.insert(pos, data['script'] + "\r\n");
            editor.focus();

            workflowId = item.id();
            $('#script-name').text(item.name());
            $('#args').val('');
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }
    
    self.saveCurrentLoadintoEditor = function(item) {
        if (self.saveNeeded()) {
              centerDialog($('#save-needed'));
            $('#save-needed').modal('show')
                .on('click', '#save-needed-yes', function(e) {
                    var updateDlg = tasksViewModel.updateWorkflow(true);
                 if (updateDlg) {
                     updateDlg.on('hidden.bs.modal', function() 
                             { 
                                     self.loadIntoEditor(item); 
                                 }.bind(this));
                 }
                 else
                     self.loadIntoEditor(item);
                 
               }).on('click', '#save-needed-no', function(e) {
                   self.loadIntoEditor(item);
               });
           }
        else {
            self.loadIntoEditor(item);
        }
    }
    
    self.click = function(model){
           self.load();
           return true;
    }
    
    self.load = function() {
        ajaxcalls.simple(self.samplesURI, 'GET', {'access': self.access()}).done(function(data) {
            self.items([]);
            $.each(data.samples, function(i, s){
                self.items.push({
                    id: ko.observable(s.id),
                    user:ko.observable(s.user),
                    name: ko.observable(s.name),
                    selected: ko.observable(false),
                    access: ko.observable(s.access),
                    isOwner: ko.observable(s.is_owner)
                });
            });
            
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }

    self.compareWf = function() {
        self.getAllSavedWf();
        $('#versionCompare').hide();
        
        // self.selectedWfId1([])
        // self.selectedWfId2([])

        $('#wfCompareSelection').modal('show');
    }
    
    self.getAllSavedWf = function () {
        self.wfList([]);
        ajaxcalls.simple(self.samplesURI, 'GET', {'access': 3}).done(function (data) {
            data.samples.forEach(wf => {
                self.wfList.push({
                    id: wf.id,
                    name: wf.name
                }); 
            });
            self.initiateWfSelectionDdl();

        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });
    };
    
    self.initiateWfSelectionDdl = function () {
        $("#compareWf1").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });

        $("#compareWf2").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });
    };

    self.wfSelectionChange = function (obj, event) {
        if (self.selectedWfId1() !== undefined && ko.toJS(self.selectedWfId1()[0]) == ko.toJS(self.selectedWfId2()[0])) {
            //display versions selection ddl
            self.getAllVersion(self.selectedWfId1()[0]);

            // self.selectedWfVersionId1([])
            // self.selectedWfVersionId2([])
            
            $('#versionCompare').show();
        }
        else{
            $('#versionCompare').hide();
        }
    }

    self.wfVersionSelectionChange = function () {
        if (self.selectedWfVersionId1()[0] == self.selectedWfVersionId2()[0]) {
            $('#wfVersionSelectionAlert').show();
            $('#wfVersionSelectionAlert').text('Please select two different versions!');
        }
        else {
            $('#wfVersionSelectionAlert').hide();
            $('#wfVersionSelectionAlert').text('');
        }
    }

    self.compareSelectedWf = function () {
        let selectedWfId1 = ko.toJS(self.selectedWfId1()[0]);
        let selectedWfId2 = ko.toJS(self.selectedWfId2()[0]);
        
        if(selectedWfId1 !== selectedWfId2){
            //compare two workflow
            ajaxcalls.simple(self.tasksURI, 'GET', {'compare': selectedWfId1, 'with': selectedWfId2}).done(function (res) {
                $('#wfCompareSelection').modal('hide');
                $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                    $('#liProvenanceTab').show();
                });
                tasksViewModel.createCompView(res.view) 
            }).fail(function (jqXHR) {
                showXHRText(jqXHR);
            });
        }
        else{
            //compare two versions of selected workflow
            let selectedWfVersionId1 = ko.toJS(self.selectedWfVersionId1()[0]);
            let selectedWfVersionId2 = ko.toJS(self.selectedWfVersionId2()[0]);
            
            if(selectedWfVersionId1 !== selectedWfVersionId2){
                ajaxcalls.simple(self.tasksURI, 'GET', {'revcompare': true,'revision1': selectedWfVersionId1, 'revision2': selectedWfVersionId2}).done(function (res) {
                    $('#wfCompareSelection').modal('hide');
                    $('.nav-tabs a[href="#provenancetab"]').tab('show').on('shown.bs.tab', function () {
                        $('#liProvenanceTab').show();
                    });
                    tasksViewModel.createCompView(res) 
                }).fail(function (jqXHR) {
                    showXHRText(jqXHR);
                });
            }
        }
    }

    self.getAllVersion = function (workflowId) {
        self.wfVersionList([]);
        ajaxcalls.simple(self.samplesURI, 'GET', {'revisions': workflowId}).done(function (data) {
            console.log(data);
            
            //get the version list here & make dropdown from it
            data.forEach(wfVersion => {
                self.wfVersionList.push({
                    hex: wfVersion.hex,
                    name: wfVersion.summary
                }); 
            });
            
            self.initiateWfVersionSelectionDdl();
        }).fail(function (jqXHR) {
            showXHRText(jqXHR);
        });

        //remove these block while get the version list above
        data = [
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
              "summary": "create workflow 1489",
              "committer": "mredul",
              "time": "2020-09-27 18:09:53+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5392",
              "summary": "create workflow 1488",
              "committer": "mredul",
              "time": "2020-09-22 18:16:17+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5393",
              "summary": "create workflow 1487",
              "committer": "mredul",
              "time": "2020-09-16 11:36:02+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5394",
              "summary": "create workflow 1486",
              "committer": "mredul",
              "time": "2020-09-16 11:02:30+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5395",
              "summary": "create workflow 1485",
              "committer": "mredul",
              "time": "2020-09-16 10:44:54+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5396",
              "summary": "create workflow 1484",
              "committer": "mredul",
              "time": "2020-09-16 10:43:43+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5397",
              "summary": "create workflow 1483",
              "committer": "mredul",
              "time": "2020-09-15 14:24:17+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5398",
              "summary": "create workflow 1482",
              "committer": "mredul",
              "time": "2020-09-14 20:39:29+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5399",
              "summary": "create workflow 1481",
              "committer": "mredul",
              "time": "2020-09-14 20:27:06+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5310",
              "summary": "create workflow 1480",
              "committer": "mredul",
              "time": "2020-09-14 19:55:59+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5311",
              "summary": "create workflow 1479",
              "committer": "mredul",
              "time": "2020-09-14 18:06:27+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5312",
              "summary": "create workflow 1478",
              "committer": "mredul",
              "time": "2020-09-14 17:34:52+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5313",
              "summary": "create workflow 1477",
              "committer": "mredul",
              "time": "2020-09-14 16:54:18+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5314",
              "summary": "create workflow 1476",
              "committer": "mredul",
              "time": "2020-09-14 15:08:17+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5315",
              "summary": "create workflow 1475",
              "committer": "mredul",
              "time": "2020-09-14 14:32:53+06:00"
            },
            {
              "hex": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5316",
              "summary": "create workflow 1474",
              "committer": "mredul",
              "time": "2020-09-14 14:00:04+06:00"
            }
        ]
        data.forEach(wfVersion => {
            self.wfVersionList.push({
                hex: wfVersion.hex,
                name: wfVersion.summary
            }); 
        });
        
        self.initiateWfVersionSelectionDdl();
        //remove these block while get the version list above
    };

    self.initiateWfVersionSelectionDdl = function () {
        $("#compareWfVersion1").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });

        $("#compareWfVersion2").multiselect({
            includeSelectAllOption: true,
            inheritClass: true,
            buttonWidth: '100%',
            enableFiltering: true,
            maxHeight: 200
        });
    };

    //workflow delete button
    self.workflowToolbar = function (item, event) {
	    event.stopPropagation();
        
        function areYouSure(confirmation){
            if(confirmation == true){
                ajaxcalls.simple(self.samplesURI, 'GET', { 'workflow_id': item.id(), 'confirm':'true' }).done(function (data){               	          
                    if (data === undefined)
                            return;
                    
                    if (data.return == 'deleted'){
                        workflowDeleted();
                    }
                    else if (data.return == 'error')
                        alert("ERROR");
                    
                }).fail(function (jqXHR) {
                    alert("Status: "+jqXHR.status);
                });  
            }
            else
                return;
        }
 
	    function workflowDeleted(){
	    	alert("WORKFLOW DELETED!");
            
            //delete this service from obsarevalbe array                                                                
            index = self.items.indexOf(item);
            if (self.items()[index].id()== item.id()){
                self.items.splice( index, 1 );
            } 
	    }
	    
	    var x = $(event.target).attr('id');
	    if (x === "delete") {
	    	ajaxcalls.simple(self.samplesURI, 'GET', { 'workflow_id': item.id() }).done(function (data) {            
                // console.log(data);    
        		if (data === undefined)
                        return;        

                data = data.return;
                
                if(data == 'shared'){
                    confirmation = confirm("This is a shared workflow. You still want to delete "+item.name()+" workflow?");
                    areYouSure(confirmation);
                }
                else if (data == 'not_shared'){
                    confirmation = confirm("Do you want to delete "+item.name()+" workflow?");
                	areYouSure(confirmation);
                }       			
        		else if (data == 'error')
        			alert("ERROR");
                }).fail(function (jqXHR) {
                        alert("Status: "+jqXHR.status);
                }); 
            }
        
            else if (x === "copyProv") {
                var content = "workflow = Workflow.Get(id="+ item.id() +")"
                              +"\r\nprint(View.Graph(workflow))"; 
                
                var pos = editor.selection.getCursor();
                editor.session.insert(pos, content + "\r\n");
                editor.focus();
            }
    }
}
