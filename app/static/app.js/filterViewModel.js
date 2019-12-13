function FilterViewModel() {
    var self = this;
    
    self.okText = ko.observable("Search");
    self.filterURI = '/filters'
    self.name = ko.observable();
    self.clicks = 0;
    self.timer = null;
    
    self.histories = ko.observableArray();
    self.savedFilters = ko.observableArray();
    self.selectedNodePath = ko.observable();
    self.sortOrders = ko.observableArray([
      {
          name: "None",
          id: 0
      },
      {
          name: "ASC",
          id: 1
      },
      {
          name: "DESC",
          id: 2
      }
    ]);

    self.toggleSort = function(data, event){

      var sort = data.sort();
      sort  = ++sort > 2? 0 : sort;

      for(var i =0 ; i < self.filters().length; i++){
          var filtersName =  ko.utils.unwrapObservable(self.filters()[i].name());
          if(filtersName == data.name()){
              self.filters()[i].sort(sort);
              break;
          }
      }
  }
   
    self.filters = ko.observableArray([
        {
            selected: ko.observable(false),
            name: ko.observable("Name"),
            value: ko.observable(""),
            sort: ko.observable(0)
        }, {
            selected: ko.observable(false),
            name: ko.observable("Size"),
            value: ko.observable(""),
            sort: ko.observable(0)
        }, {
            selected: ko.observable(false),
            name: ko.observable("Created"),
            value: ko.observable(""),
            sort: ko.observable(0),
        }, {
            selected: ko.observable(false),
            name: ko.observable("Modified"),
            value: ko.observable(""),
            sort: ko.observable(0),
        }, {
            selected: ko.observable(false),
            name: ko.observable("Accessed"),
            value: ko.observable(""),
            sort: ko.observable(0),
        }, {
            selected: ko.observable(false),
            name: ko.observable("key:value"),
            value: ko.observable(""),
            sort: ko.observable(0),
        }
    ]);
    
  self.setSortClass = function (sort) {
         switch (sort()) {
             case 0:
                 return 'fa fa-times fa-xs';

             case 1:
                 return 'fa fa-sort-asc filter-dialog-sortIcon';

             case 2:
                 return 'fa fa-sort-desc filter-dialog-sortIcon';

             default:
                 return 'fa fa-times fa-xs';
         }
     };

     self.moveUp = function(data) {
         var idx = self.filters.indexOf(data),
           tmp = self.filters.splice(idx, 1);

         self.filters.splice(idx - 1, 0, tmp[0]);
       };
       
     self.moveDown = function(data) {
         var idx = self.filters.indexOf(data),
           tmp = self.filters.splice(idx, 1);

         self.filters.splice(idx + 1, 0, tmp[0]);
       };

    self.selectNode = function () {  
        var treeNodes = $("#tree").jstree(true).get_json('#', { 'flat': true });

        for (var index = 0; index < treeNodes.length; index++) {
            var node = treeNodes[index];
            var targetNode = $("#tree").jstree(true).get_node(node.id);

            if (targetNode.original.path == self.selectedNodePath()) {
                $("#tree").jstree("deselect_all");
                $("#tree").jstree(true).select_node(targetNode);
                self.selectedNodePath('');
                break;
            }
        }
    }
       // apply the filters
      self.filterInternal = function(node, jsonFilters) {

             ajaxcalls.simple(self.filterURI, 'GET', { 'root': node, 'applyfilters': jsonFilters }).done(function(data) {
                 
                 try {
                     dataSourceViewModel.loadFromJSON(data.datasources);
                 }
                 catch(error) {
                     
                 }
                 self.loadHistory();
                           
             }).fail(function(jqXHR) {
                 showXHRText(jqXHR);
             });
             }
     
    self.copyToEditor = function(item) {
       
        if (!dataSourceViewModel.selectedNode())
            return;
        
        path = dataSourceViewModel.selectedNode().original.path;
        var pos = editor.selection.getCursor();
        
        $.ajax({
            url: self.filterURI + "?filterforscript=" + item.id() + "&path=" + path
        })
        .then(function(data) {
            editor.session.insert(pos, data["script"] + "\r\n");
              editor.focus();
        }, function(xhr, status, error) {
               // Upon failure... set the tooltip content to error
        });
    }

    self.closeFilter = function () {  
        $("#btnfilterToggle").trigger('click');
        self.okText('');
    };

    self.promptFilter = function (data, e) { 

        if(e.type == 'change' && (data.name()=='Name' || data.name() == 'Permission' || data.name()== 'key:value')){
            return;
        }

        if (!data.value()) {
            return;
        }

        ko.utils.arrayForEach(self.filters(), function (filter) {  
            if(filter.name() == data.name()){
                filter.selected(true);
            }
        });
        self.filter();
    }
  
    // apply the filters
      self.filter = function() {
          if (!dataSourceViewModel.selectedNode()){
              self.selectedNodePath("\/");
              self.filterInternal("\/", ko.toJSON(self.filters));
          }

          else if(self.okText() == "Save") {
              // save the filters
          ajaxcalls.simple(self.filterURI, 'GET', { 'name': self.name(), 'savefilters': ko.toJSON(self.filters) }).done(function(data) {
                 self.loadSavedFilters();
                           
             }).fail(function(jqXHR) {
                 showXHRText(jqXHR);
             });
          }
          else {
              self.selectedNodePath(dataSourceViewModel.selectedNode().original.path);
              self.filterInternal(dataSourceViewModel.selectedNode().original.path, ko.toJSON(self.filters));
          }
      }
      
    self.openSavedFilterDialog = function(item) {
        self.name(item.name());
        self.openFilterDialogInternal(true, ko.toJSON(item.value()));
    }
    
    self.openFilterDialog = function(isSave, item) {
        self.openFilterDialogInternal(isSave, item.value());
    };

    self.deleteSavedFilter = function (item, element) {
         ajaxcalls.simple(self.filterURI, 'GET', { 'delete': item.id()}).done(function (data) {
          self.loadSavedFilters();
         });
     };
    
   // opens the filters dialog to define filters
      self.openFilterDialogInternal = function(isSave, item) {

       historyFilters = JSON.parse(item);
       if (!historyFilters)
            return;
       
       self.filters().forEach(function(f){
          f.selected(false);
          f.value("");
          f.sort(0);
       });
       
      self.filters().forEach(function(f){
              
             historyFilter = historyFilters.find(x => x.name === f.name())
             if (historyFilter && (f.name() == historyFilter.name)) {
                 f.selected(historyFilter.selected);
                 f.value(historyFilter.value);
                 f.sort(historyFilter.sort);
              }
          });
      
      
      //self.name("");
         
         dataSourceViewModel.openFilterDialog(isSave);
      }
      
     self.toggleExpand = function() {
         
         self.toggleExpand = function(item, event) {
             event.stopPropagation();
             
             self.clicks++;
             if (self.clicks !== 1) {
                 clearTimeout(self.timer);
                 self.filterByHistory(item);
                 self.clicks = 0;
                 return;        		 
             }
             
             self.timer = setTimeout(function(){
                 self.clicks = 0;
                 event.preventDefault();
                 var domItem = $(event.target);
                 $(".expandedfilter").remove();
                 if (item.expanded()) {
                     item.expanded(false);
                   } else {
                     self.histories().forEach(function(candidateSample) {
                       candidateSample.expanded(item === candidateSample);
                       if (item === candidateSample){
                           
                           $.ajax({
                             url: self.filterURI + "?filtertip=" + item.id()
                         })
                         .then(function(content) {
                             // Set the tooltip content upon successful retrieval
                             content = JSON.parse(content);
                             content = "<div class=\'expandedfilter\' style=\'border:2px solid black;background-color:lightblue\'> <p>Name: " + content.name + "</p><p>Created: " + content.created_on + "<p>Filter: " + content.value  
                                  + "</p><p>Double click to filter data sources with this.</p></div>";
                                 
                             domItem.parent().append(content);

                         }, function(xhr, status, error) {
                             // Upon failure... set the tooltip content to error
                         });
                     }
                   });
               }
             }, 300);
         }
      }

     self.filterByHistory = function(item) {
         if (!dataSourceViewModel.selectedNode()){
            self.filterInternal('\/', ko.toJSON(item.value()));
            self.selectedNodePath('\/');
            return;
         } 
         
         self.selectedNodePath(dataSourceViewModel.selectedNode().original.path);
         self.filterInternal(dataSourceViewModel.selectedNode().original.path, ko.toJSON(item.value()));
      }
     
     self.loadHistory = function() {
      
         ajaxcalls.simple(self.filterURI, 'GET', { 'filterhistory': true }).done(function(data) {
          
             if (data === undefined)
              return;
             
             self.histories([]);
          $.each(data['histories'], function(i, s){
              self.histories.push({
                  id: ko.observable(s.id),
                  name: ko.observable(s.name),
                  value: ko.observable(s.value),
                  created_on: ko.observable(s.created_on),
                  expanded: ko.observable(false),
              });
          });
          
      }).fail(function(jqXHR) {
          showXHRText(jqXHR);
      });
     }
     
  self.loadSavedFilters = function() {
      
         ajaxcalls.simple(self.filterURI, 'GET', { 'filters': true }).done(function(data) {
          
             if (data === undefined)
              return;
             
             self.savedFilters([]);
          $.each(data['histories'], function(i, s){
              self.savedFilters.push({
                  id: ko.observable(s.id),
                  name: ko.observable(s.name),
                  value: ko.observable(s.value),
                  created_on: ko.observable(s.created_on),
                  expanded: ko.observable(false),
              });
          });
          
      }).fail(function(jqXHR) {
          showXHRText(jqXHR);
      });
     };
  
  self.about = function () {
      window.open("static/biodsl-help.html#datasources", '_blank');
  };

    self.formControlCustomization = function (element) {
        
        var ele = $(element);
        var filterType = ele.prev('td').text();

        switch (filterType) {
            
            case 'Size':
                var frmControl = ele.find('input');
                self.intitiateRangeSlider(frmControl);
                break;
            
            case 'Created':
            case 'Modified':
            case 'Accessed':
                var frmControl = ele.find('input');
                self.intitiateDateRangePicker(frmControl);
                break;

            default:
                break;
        }
    };

    self.intitiateDateRangePicker = function (frmControl) {  
       
        frmControl.daterangepicker({
            linkedCalendars: false,
            cancelClass : "btn-danger",
            maxSpan: {
                "days": 60
            },
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
            
        });

    };
    
    self.intitiateRangeSlider = function (frmControl) {

        frmControl.bootstrapSlider({
            tooltip: 'show',
            range: 'true',
            min: 0,
            max: 1024,
            formatter:  function (value) {
                
                if (Array.isArray(value)) {
                    value[0] = value[0] + ' KB';
                    value[1] = value[1] + ' KB';
                    return value;
                } 
            }
        });
    };

    self.customizeSlider = function (value) {
        
        // if(Array.isArray(value)){
        //     value[0] = value[0] + ' KB';
        //     value[1] = value[1] + ' KB';
        //     return value;
        // }
    };
     
}
 

ko.bindingHandlers.formControlCustomization = {
    init: function (element, valueAccessor, allBindings, viewModel, bindingContext) {  

    }, 
    update: function (element, valueAccessor, allBindings, viewModel, bindingContext) {  

    }
};



filterViewModel = new FilterViewModel();