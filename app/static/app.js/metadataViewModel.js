function MetaDataViewModel() {
    var self = this;
    
    self.metadataURI = '/metadata';
    self.path =  new ko.observable();
    self.filename = new ko.observable();
    self.systemProperties = new ko.observableDictionary();
    self.visualizers = new ko.observableDictionary();
    self.annotations = new ko.observableDictionary(); // list of strings
    self.properties = new ko.observableDictionary(); // keyvalue
    self.mimetypes = new ko.observableDictionary();

    self.save = function() {
        
        var formdata = new FormData();

        formdata.append('save', self.path());
        formdata.append('filename', self.filename());
        formdata.append('visualizers', ko.toJSON(self.visualizers));
        formdata.append('annotations', ko.toJSON(self.annotations));
        formdata.append('mimetypes', ko.toJSON(self.mimetypes));
        formdata.append('properties', ko.toJSON(self.properties));

        ajaxcalls.form(self.metadataURI, 'POST', formdata).done(function(data) {

        }).fail(function (jqXHR, a,b) {
                       
        });
    } 
    
    self.load = function(path) {
        
        self.newPropCounter = 0;
        self.newVisCounter = 0;
        self.newAnntnCounter = 0;
        self.newMimeCounter = 0;

        self.path(path);
        self.filename(path.replace(/^.*[\\\/]/, ''));
        ajaxcalls.simple(self.metadataURI, 'GET', {'load': path}).done(function(data) {
            if (data == undefined)
                return;
            
            self.systemProperties.removeAll();
            $.each(data['sysprops'], function(key, value){
                   self.systemProperties.push(key, value);
            });
            
            self.visualizers.removeAll();
            $.each(data['visualizers'], function(key, value){
                self.visualizers.push(key, value);
            });
            
            self.annotations.removeAll();
            $.each(data['annotations'], function(key, value){
                self.annotations.push(key, value);
            })
            
            /* var observableAnnotations = ko.utils.arrayMap(data['annotations'], function(annotation) {
                return { name: ko.observable(annotation) }; 
            });
            self.annotations = ko.observableArray(observableAnnotations); */
            
            self.properties.removeAll();
            $.each(data['properties'], function(key, value){
                self.properties.push(key, value);
            });
            
            self.mimetypes.removeAll();
            $.each(data['mimetypes'], function(key, value){
                self.mimetypes.push(key, value);
            })
            
        }).fail(function(jqXHR) {
            showXHRText(jqXHR);
        }).always(function(x, textStatus, jqXHR){
            self.historyLoading = false;
        });
    };

    self.newPropCounter = 0;
    self.newVisCounter = 0;
    self.newAnntnCounter = 0;
    self.newMimeCounter= 0;

    self.addNewProperty = function () {  
        ++self.newPropCounter;
        self.properties.push('new key '+ self.newPropCounter , 'new value '+ self.newPropCounter);
    };

    self.removeProperty = function (data, ev) { 
        self.properties.remove(data.key());
    };

    self.addNewVisualizer = function () {  
        ++self.newVisCounter;
        self.visualizers.push('new key '+ self.newVisCounter , 'new value '+ self.newVisCounter);
    };

    self.removeVisualizer = function (data, ev) {  
        self.visualizers.remove(data.key());
    };

    self.addNewAnnotation = function () {  
        ++self.newAnntnCounter;
        self.annotations.push('new key '+ self.newAnntnCounter , 'new value '+ self.newAnntnCounter);
    };
    
    self.removeAnnotation = function (data, ev) {  
        self.annotations.remove(data.key());
    };

    self.addNewMimeType = function () {
        ++self.newMimeCounter;  
        self.mimetypes.push('new key '+ self.newMimeCounter , 'new value '+ self.newMimeCounter);
    };

    self.removeMimeType = function (data, ev) {  
        self.mimetypes.remove(data.key());
    };

}

var metadataViewModel = new MetaDataViewModel();
