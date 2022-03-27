  function GridStackViewModel () {
    var self = this;
    self.newLayoutName = ko.observable();
    self.settingsURI = '/settings'
    self.grid = $('.grid-stack').data('gridstack');
    self.serialize = function () {
        return _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
            var node = $(el).data('_gridstack_node');
            return { id: $(el).attr('id'), x: node.x, y: node.y, width: node.width, height: node.height };
        });
    };

    self.isGridEnabled = ko.observable(false);

    self.defaultLayout = [
        {
            x: 0,
            y: 0,
            w: 3,
            h: 8,
            id: "datasourceStack"
        },
        {
            x: 0,
            y: 12,
            w: 3,
            h: 4,
            id: "searchHistoryStack"
        },
        {
            x: 0,
            y: 8,
            w: 3,
            h: 4,
            id: "jobHistoriesStack"
        },
        {
            x: 3,
            y: 0,
            w: 6,
            h: 11,
            id: "main"
        },
        {
            x: 3,
            y: 11,
            w: 6,
            h: 1,
            id: "executeSectionStack"
        },
        {
            x: 3,
            y: 12,
            w: 6,
            h: 3,
            id: "exTab2Stack"
        },
        {
            x: 9,
            y: 0,
            w: 3,
            h: 9,
            id: "servicesStack"
        },
        {
            x: 9,
            y: 9,
            w: 3,
            h: 5,
            id: "workflowsStack"
        }
        
    ];

    self.isGridEnabled.subscribe(function () {  
        self.gridLockToggle();
    });

    self.savedLayouts = ko.observableArray();

    self.selectDefaultLayout = function (data, e) {

        $.each(self.defaultLayout, function (index, component) { 
            var domNode = "#" + component.id;

            $(domNode).attr('data-gs-x', component.x);
            $(domNode).attr('data-gs-y', component.y);
            $(domNode).attr('data-gs-width', component.w);
            $(domNode).attr('data-gs-height', component.h);
            $(domNode).show();     
        });
    };

    self.saveCurrentLayout = function (data, e) {
        $('#saveLayout').modal('show'); 
    };

    self.addNewLayout = function () {  
        var gridComponents = $('.grid-stack-item');
        var layoutProperties = [];

        $.each(gridComponents, function (index, component) { 
             var componentObj = {};

             componentObj.x = $(component).attr('data-gs-x');//ko.observable();
             componentObj.y = $(component).attr('data-gs-y');//ko.observable();
             componentObj.w = $(component).attr('data-gs-width');//ko.observable();
             componentObj.h = $(component).attr('data-gs-height');//ko.observable();
             componentObj.id = $(component).attr('id');//ko.observable();

             layoutProperties.push(componentObj);
        });

        //saved in inmemory, corresponding api implementation needed
        self.savedLayouts.push({layoutName: ko.observable(self.newLayoutName()), properties: layoutProperties});
    };

    self.applyLayout = function (data, e) {

        data.properties.forEach(property => {
            
            var domNode = "#" + property.id;

            $(domNode).attr('data-gs-x', property.x);
            $(domNode).attr('data-gs-y', property.y);
            $(domNode).attr('data-gs-width', property.w);
            $(domNode).attr('data-gs-height', property.h);  
        });
    }
    
    self.move = function (stored) {
        if (!stored)
            stored = gridStackViewModel.defaultLayout;
        stored = GridStackUI.Utils.sort(stored, 1, 12);
        $.each(stored, function (key, node) {
            el = $('#' + node.id);
            self.grid.update(el, node.x, node.y, node.width, node.height);
        });
    }

    self.load = function () {
        if (!username)
            self.move();

        ajaxcalls.simple(self.settingsURI, 'GET', { 'load': username }).done(function (data) {
            
            self.move(data);

        }).fail(function (jqXHR) {
            
            showXHRText(jqXHR);
        });
    }

    self.save = function () {
        if (!username)
            return;
        value = JSON.stringify(self.serialize());
        ajaxcalls.simple(self.settingsURI, 'GET', { 'save': value }).done(function (data) {
            
        }).fail(function (jqXHR) {
            
            showXHRText(jqXHR);
        });
    };

    self.gridLockToggle = function () {  

        var grid = $('.grid-stack').data('gridstack');

        if(self.isGridEnabled()){
            grid.enable();
        }
        else{
            grid.disable();
        }

        return true;
    };
}
