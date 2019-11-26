function SamplesViewModel(sampleViewModel) {
    var self = this;
    self.samplesURI = '/samples';
    self.clicks = 0;
    self.timer = null;
    self.items = ko.observableArray();
    self.sampleViewModel = sampleViewModel;
    self.access = ko.observable("0");
    self.workflowFilter = ko.observable("");
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
        centerDialog($('#addSample'));
        return $('#addSample').modal('show');
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
                    access: ko.observable(s.access)
                });
            });
            
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        });
    }
}
