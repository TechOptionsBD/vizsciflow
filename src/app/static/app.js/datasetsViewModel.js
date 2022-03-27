
function DatasetsViewModel() {
    var self = this;
    self.datasets = ko.observableArray();
    self.datasetsURI = '/datasets';
    self.datasetFilter = ko.observable("");
    self.filteredDatasets = ko.computed(function () {
        return this.datasets().filter(function (dataset) {
            if (!self.datasetFilter() || dataset.name.toLowerCase().indexOf(self.datasetFilter().toLowerCase()) !== -1
                || dataset.url.toLowerCase().indexOf(self.datasetFilter().toLowerCase()) !== -1
                || dataset.description.toLowerCase().indexOf(self.datasetFilter().toLowerCase()) !== -1)
                return dataset;
        });
    }, this);

    self.currentSelection = ko.observable(0);

    self.selectedSchema = {};

    self.addNew = function () {
        datasetAddViewModel.isUpdate(false);
        $('#dataSets-addNew-dialog').modal('show');
    };

    self.update = function (dataset) {

        if (!self.selectedSchema || !self.selectedSchema.id) {
            return;
        }
        dataset.id = self.selectedSchema.id;
        self.currentSelection(dataset.id);

        ajaxcalls.simple(self.datasetsURI, 'GET', { 'update': ko.toJSON(dataset), 'update_id': self.selectedSchema.id }).done(function () {
            self.load();
        });
    }

    self.saveNew = function (dataset) {

        ajaxcalls.simple(self.datasetsURI, 'GET', { 'save': ko.toJSON(dataset) })
            .done(function (data) {
                self.currentSelection(data.dataset.id);
                self.load();
            });
    }

    self.about = function () {
        window.open("static/biodsl-help.html#datasources", '_blank');
    };

    //ajax call to api to load the datasets
    self.load = function () {
        ajaxcalls.simple(self.datasetsURI, 'GET')
            .done(function (data) {

                self.datasets([]);
                $.each(data.datasets, function (i, s) {
                    var dataset = s.schema;
                    dataset.id = s.id;
                    self.datasets.push(dataset);
                });

            }).fail(function (jqXHR) {
                showXHRText(jqXHR);
            });
    };

    self.click = function (schema, element) {
        // $('.dataset-listview').removeClass('dataset-listview-selected');
        // $(element.currentTarget).addClass('dataset-listview-selected');
        self.currentSelection(schema.id); 
        self.selectedSchema = schema;
        showDatasetTab(schema);
    };

    self.deleteSchema = function () {

        if ($('.dataset-listview-selected').length == 0 || !self.selectedSchema || !self.selectedSchema.id) {
            return;
        }
        //api call to delete schema
        ajaxcalls.simple(self.datasetsURI, 'GET', { 'delete': self.selectedSchema.id }).done(function (data) {
            self.load();
        });
    };

    self.editSchema = function () {
        if ($('.dataset-listview-selected').length == 0) {
            return;
        }
        datasetAddViewModel.parseFileDataToViewModel(ko.toJSON(self.selectedSchema));
        $('#dataSets-addNew-dialog').modal('show');
        datasetAddViewModel.isUpdate(true);
    };

    self.load();
};

ko.bindingHandlers.searchTextMatch = {
    init: function (element, valueAccessor, allBindings, viewModel, bindingContext) {

        var searchText = ko.utils.unwrapObservable(datasetsViewModel.datasetFilter());
        var eleText = $(element).html();
        var refresheEleText = eleText.replace('<span class="highlight">', '').replace('</span>', '');

        if (!searchText) {
            $(element).html(refresheEleText);
            return;
        }

        var pattern = refresheEleText.match(new RegExp(searchText, 'gi'));  //new RegExp("(" + searchText + ")");
        var higlightedText = refresheEleText.replace(pattern, '<span class="highlight">' + pattern + '</span>');
        $(element).html(higlightedText);


    },
    update: function (element, valueAccessor, allBindings, viewModel, bindingContext) {

        var searchText = ko.utils.unwrapObservable(datasetsViewModel.datasetFilter());
        var eleText = $(element).html();
        var refresheEleText = eleText.replace('<span class="highlight">', '').replace('</span>', '');

        if (!searchText) {
            $(element).html(refresheEleText);
            return;
        }

        var pattern = refresheEleText.match(new RegExp(searchText, 'gi')); //new RegExp("(" + searchText + ")");
        var higlightedText = refresheEleText.replace(pattern, '<span class="highlight">' + pattern + '</span>');
        $(element).html(higlightedText);


    }
}

ko.bindingHandlers.datasetHover = {
    init: function (element, valueAccessor, allBindings, viewModel, bindingContext) {

        $(element).mouseover(function () {
            $('.dataset-listview').removeClass('dataset-listview-hover');
            $(element).addClass('dataset-listview-hover');
        });
        $(element).mouseleave(function () {
            $('.dataset-listview').removeClass('dataset-listview-hover');
        });
    }
};


ko.bindingHandlers.trigAddUpdateDataset = {
    init: function (element, valueAccessor, allBindings, viewModel, bindingContext) {  
        if (viewModel.id == bindingContext.$parent.currentSelection()) {
            datasetviewViewModel.load(viewModel);
        }
    },
    update: function (element, valueAccessor, allBindings, viewModel, bindingContext) {  
        if (viewModel.id == bindingContext.$parent.currentSelection()) {
            datasetviewViewModel.load(viewModel);
        }
    }
}
