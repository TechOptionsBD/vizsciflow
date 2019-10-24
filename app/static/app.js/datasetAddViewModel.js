var DatasetSingularPropertyViewModel = [
    {
        name: ko.observable("name"),
        value: ko.observable("")
    }, {
        name: ko.observable("url"),
        value: ko.observable("")
    }, {
        name: ko.observable("description"),
        value: ko.observable("")
    }, {
        name: ko.observable("version"),
        value: ko.observable("")
    }, {
        name: ko.observable("text"),
        value: ko.observable("")
    }, {
        name: ko.observable("sourceOrganization"),
        value: ko.observable("")
    }, {
        name: ko.observable("license"),
        value: ko.observable("")
    }, {
        name: ko.observable("keywords"),
        value: ko.observable("")
    },
    {
        name: ko.observable("accessMode"),
        value: ko.observable("")
    },
    {
        name: ko.observable("about"),
        value: ko.observable("")
    }];

var DatasetAuthorViewModel = [
    {
        name: ko.observable("givenName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("familyName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("email"),
        value: ko.observable("")
    },
    {
        name: ko.observable("telephone"),
        value: ko.observable("")
    },
    {
        name: ko.observable("gender"),
        value: ko.observable("")
    }

];

var DatasetDatesViewModel = [
    {
        name: ko.observable("expires"),
        value: ko.observable("")
    }, {
        name: ko.observable("datePublished"),
        value: ko.observable("")
    }, {
        name: ko.observable("dateModified"),
        value: ko.observable("")
    }, {
        name: ko.observable("dateCreated"),
        value: ko.observable("")
    }
];

var DatasetPublisherViewModel = [
    {
        name: ko.observable("givenName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("familyName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("email"),
        value: ko.observable("")
    },
    {
        name: ko.observable("telephone"),
        value: ko.observable("")
    },
    {
        name: ko.observable("gender"),
        value: ko.observable("")
    }
];

var DatasetCreatorViewModel = [
    {
        name: ko.observable("givenName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("familyName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("email"),
        value: ko.observable("")
    },
    {
        name: ko.observable("telephone"),
        value: ko.observable("")
    },
    {
        name: ko.observable("gender"),
        value: ko.observable("")
    }
];

var DatasetEditorViewModel = [
    {
        name: ko.observable("givenName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("familyName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("email"),
        value: ko.observable("")
    },
    {
        name: ko.observable("telephone"),
        value: ko.observable("")
    },
    {
        name: ko.observable("gender"),
        value: ko.observable("")
    }

];

var DatasetProducerViewModel = [
    {
        name: ko.observable("givenName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("familyName"),
        value: ko.observable("")
    },
    {
        name: ko.observable("email"),
        value: ko.observable("")
    },
    {
        name: ko.observable("telephone"),
        value: ko.observable("")
    },
    {
        name: ko.observable("gender"),
        value: ko.observable("")
    }
];

function datasetSingularPropertyViewModelFileDataMapper(filedata) {
    DatasetSingularPropertyViewModel[0].value(filedata.name);
    DatasetSingularPropertyViewModel[1].value(filedata.url);
    DatasetSingularPropertyViewModel[2].value(filedata.description);
    DatasetSingularPropertyViewModel[3].value(filedata.version);
    DatasetSingularPropertyViewModel[4].value(filedata.text);
    DatasetSingularPropertyViewModel[5].value(filedata.sourceOrganization);
    DatasetSingularPropertyViewModel[6].value(filedata.license);
    DatasetSingularPropertyViewModel[7].value(filedata.keywords);
    DatasetSingularPropertyViewModel[8].value(filedata.accessMode);
    DatasetSingularPropertyViewModel[9].value(filedata.about);
};

function datasetDatesViewModelFileDataMapper(filedata) {
    DatasetDatesViewModel[0].value(filedata.expires);
    DatasetDatesViewModel[1].value(filedata.datePublished);
    DatasetDatesViewModel[2].value(filedata.dateModified);
    DatasetDatesViewModel[3].value(filedata.dateCreated);
};

function datasetAuthorViewModelFileDataMapper(fileAuthordata) {
    DatasetAuthorViewModel[0].value(fileAuthordata.givenName);
    DatasetAuthorViewModel[1].value(fileAuthordata.familyName);
    DatasetAuthorViewModel[2].value(fileAuthordata.email);
    DatasetAuthorViewModel[3].value(fileAuthordata.telephone);
    DatasetAuthorViewModel[4].value(fileAuthordata.gender);
};

function datasetCreatorViewModelFileDataMapper(fileCreatorData) {
    DatasetCreatorViewModel[0].value(fileCreatorData.givenName);
    DatasetCreatorViewModel[1].value(fileCreatorData.familyName);
    DatasetCreatorViewModel[2].value(fileCreatorData.email);
    DatasetCreatorViewModel[3].value(fileCreatorData.telephone);
    DatasetCreatorViewModel[4].value(fileCreatorData.gender);
};

function datasetEditorViewModelFileDataMapper(fileEditorData) {
    DatasetEditorViewModel[0].value(fileEditorData.givenName);
    DatasetEditorViewModel[1].value(fileEditorData.familyName);
    DatasetEditorViewModel[2].value(fileEditorData.email);
    DatasetEditorViewModel[3].value(fileEditorData.telephone);
    DatasetEditorViewModel[4].value(fileEditorData.gender);
};

function datasetPublisherViewModelFileDataMapper(filePublisherData) {
    DatasetPublisherViewModel[0].value(filePublisherData.givenName);
    DatasetPublisherViewModel[1].value(filePublisherData.familyName);
    DatasetPublisherViewModel[2].value(filePublisherData.email);
    DatasetPublisherViewModel[3].value(filePublisherData.telephone);
    DatasetPublisherViewModel[4].value(filePublisherData.gender);
};

function datasetProducerViewModelFileDataMapper(fileProducerData) {
    DatasetProducerViewModel[0].value(fileProducerData.givenName);
    DatasetProducerViewModel[1].value(fileProducerData.familyName);
    DatasetProducerViewModel[2].value(fileProducerData.email);
    DatasetProducerViewModel[3].value(fileProducerData.telephone);
    DatasetProducerViewModel[4].value(fileProducerData.gender);
}

function DatasetAddViewModel() {
    var self = this;
    self.isUpdate = ko.observable(false);
    self.uploadDatasetURI = '';


    self.dataset = {
        SingularProperty: DatasetSingularPropertyViewModel,
        AuthorProperty: DatasetAuthorViewModel,
        DateProperty: DatasetDatesViewModel,
        CreatorProperty: DatasetCreatorViewModel,
        EditorProperty: DatasetEditorViewModel,
        PublisherProperty: DatasetPublisherViewModel,
        ProducerProperty: DatasetProducerViewModel
    };


    self.parseFileDataToViewModel = function (filedata) {

        var jsObjectData = JSON.parse(filedata);

        datasetDatesViewModelFileDataMapper(jsObjectData);
        datasetAuthorViewModelFileDataMapper(jsObjectData.author);
        datasetCreatorViewModelFileDataMapper(jsObjectData.creator);
        datasetEditorViewModelFileDataMapper(jsObjectData.editor);
        datasetProducerViewModelFileDataMapper(jsObjectData.producer);
        datasetPublisherViewModelFileDataMapper(jsObjectData.publisher);
        datasetSingularPropertyViewModelFileDataMapper(jsObjectData);
    };

    self.uploadSchema = function () {

        var schemaFile = $("#fileSchemaUpload").get(0).files[0];

        var reader = new FileReader();
        reader.readAsText(schemaFile);

        reader.onload = function () {
            self.parseFileDataToViewModel(reader.result);
        };
    };

    self.moveUp = function (data) {
        var idx = self.filters.indexOf(data),
            tmp = self.filters.splice(idx, 1);

        self.filters.splice(idx - 1, 0, tmp[0]);
    };

    self.moveDown = function (data) {
        var idx = self.filters.indexOf(data),
            tmp = self.filters.splice(idx, 1);

        self.filters.splice(idx + 1, 0, tmp[0]);
    };


    self.convertToSchemaFormat = function () {

        var universalSchema = new Object();
        var authorProperties = new Object();
        var dateProperties = new Object();
        var creatorProperties = new Object();
        var producerProperties = new Object();
        var publisherProperties = new Object();
        var editorProperties = new Object();

        for (var i = 0; i < self.dataset.SingularProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.SingularProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.SingularProperty[i].value);
            universalSchema[key] = value;
        }

        for (var i = 0; i < self.dataset.AuthorProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.AuthorProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.AuthorProperty[i].value);
            authorProperties[key] = value;
        }

        for (var i = 0; i < self.dataset.CreatorProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.CreatorProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.CreatorProperty[i].value);
            creatorProperties[key] = value;
        }

        for (var i = 0; i < self.dataset.ProducerProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.ProducerProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.ProducerProperty[i].value);
            producerProperties[key] = value;
        }

        for (var i = 0; i < self.dataset.PublisherProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.PublisherProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.PublisherProperty[i].value);
            publisherProperties[key] = value;
        }

        for (var i = 0; i < self.dataset.EditorProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.EditorProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.EditorProperty[i].value);
            editorProperties[key] = value;
        }

        for (var i = 0; i < self.dataset.DateProperty.length; i++) {
            var key = ko.utils.unwrapObservable(self.dataset.DateProperty[i].name);
            var value = ko.utils.unwrapObservable(self.dataset.DateProperty[i].value);
            universalSchema[key] = value;
        }

        universalSchema.author = authorProperties;
        universalSchema.editor = editorProperties;
        universalSchema.creator = creatorProperties;
        universalSchema.publisher = publisherProperties;
        universalSchema.producer = producerProperties;

        return universalSchema;
    };

    self.saveNew = function () {

        var schema = self.convertToSchemaFormat();

        datasetsViewModel.saveNew(schema);
    };

    self.update = function () {
        var schema = self.convertToSchemaFormat();
        datasetsViewModel.update(schema);
    }

};

