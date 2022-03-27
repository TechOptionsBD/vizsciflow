function DatasetviewViewModel() {
    var self = this;
    self.dataset = ko.observable();
    self.hasProperties = ko.observable(false);
    self.hasDates = ko.observable(false);
    self.hasAuthor = ko.observable(false);
    self.hasCreator = ko.observable(false);
    self.hasProducer = ko.observable(false);
    self.hasPublisher = ko.observable(false);
    self.hasEditor = ko.observable(false);

    self.name = ko.observable();
    self.text = ko.observable();
    self.url = ko.observable();
    self.about = ko.observable();
    self.version = ko.observable();
    self.text = ko.observable();
    self.description = ko.observable();
    self.license = ko.observable();
    self.sourceOrganization = ko.observable();
    self.keywords = ko.observable();
    self.accessMode = ko.observable();
    self.expires = ko.observable();
    self.datePublished = ko.observable();
    self.dateModified = ko.observable();
    self.dateCreated = ko.observable();

    self.authGivenName = ko.observable();
    self.authFamilyName = ko.observable();
    self.authEmail = ko.observable();
    self.authTelephone = ko.observable();
    self.authGender = ko.observable();

    self.crtGivenName = ko.observable();
    self.crtFamilyName = ko.observable();
    self.crtEmail = ko.observable();
    self.crtTelephone = ko.observable();
    self.crtGender = ko.observable();

    self.prdcGivenName = ko.observable();
    self.prdcFamilyName = ko.observable();
    self.prdcEmail = ko.observable();
    self.prdcTelephone = ko.observable();
    self.prdcGender = ko.observable();

    self.pblsGivenName = ko.observable();
    self.pblsFamilyName = ko.observable();
    self.pblsEmail = ko.observable();
    self.pblsTelephone = ko.observable();
    self.pblsGender = ko.observable();

    self.edtGivenName = ko.observable();
    self.edtFamilyName = ko.observable();
    self.edtEmail = ko.observable();
    self.edtTelephone = ko.observable();
    self.edtGender = ko.observable();



    self.load = function (schema) {
        self.hasProperties(false);
        self.hasPublisher(false);
        self.hasProducer(false);
        self.hasDates(false);
        self.hasAuthor(false);
        self.hasCreator(false);
        self.hasEditor(false);

        for (var key in schema) {
            if (schema.hasOwnProperty(key)) {
                var element = schema[key];
                if (key == 'author' || key == 'creator' || key == 'editor' || key == 'publisher' || key == 'producer')
                    continue;
                if (element !== "") {
                    self.hasProperties(true);
                    break;
                }
            }
        }

        for (var key in schema.author) {
            if (schema.author.hasOwnProperty(key)) {
                var element = schema.author[key];
                if (element !== "") {
                    self.hasAuthor(true);
                    break;
                }
            }
        }


        for (var key in schema.editor) {
            if (schema.editor.hasOwnProperty(key)) {
                var element = schema.editor[key];
                if (element !== "") {
                    self.hasEditor(true);
                    break;
                }
            }
        }

        for (var key in schema.producer) {
            if (schema.producer.hasOwnProperty(key)) {
                var element = schema.producer[key];
                if (element !== "") {
                    self.hasProducer(true);
                    break;
                }
            }
        }

        for (var key in schema.publisher) {
            if (schema.publisher.hasOwnProperty(key)) {
                var element = schema.publisher[key];
                if (element !== "") {
                    self.hasPublisher(true);
                    break;
                }
            }
        }

        for (var key in schema.creator) {
            if (schema.creator.hasOwnProperty(key)) {
                var element = schema.creator[key];
                if (element !== "") {
                    self.hasCreator(true);
                    break;
                }
            }
        }

        if (schema.expires !== '' || schema.dateCreated !== '' || schema.dateModified !== '' || schema.datePublished !== '') {
            self.hasDates(true);
        }

        self.dataset();

        self.name(schema.name);
        self.text(schema.text);
        self.url(schema.url);
        self.about(schema.about);
        self.version(schema.version);
        self.description(schema.description);
        self.license(schema.license);
        self.sourceOrganization(schema.sourceOrganization);
        self.keywords(schema.keywords);
        self.accessMode(schema.accessMode);

        self.expires(schema.expires);
        self.datePublished(schema.datePublished);
        self.dateModified(schema.dateModified);
        self.dateCreated(schema.dateCreated);

        self.authGivenName(schema.author.givenName);
        self.authFamilyName(schema.author.familyName);
        self.authEmail(schema.author.email);
        self.authTelephone(schema.author.telephone);
        self.authGender(schema.author.gender);

        self.crtGivenName(schema.creator.givenName);
        self.crtFamilyName(schema.creator.familyName);
        self.crtEmail(schema.creator.email);
        self.crtTelephone(schema.creator.telephone);
        self.crtGender(schema.creator.gender);

        self.prdcGivenName(schema.producer.givenName);
        self.prdcFamilyName(schema.producer.familyName);
        self.prdcEmail(schema.producer.email);
        self.prdcTelephone(schema.producer.telephone);
        self.prdcGender(schema.producer.gender);

        self.pblsGivenName(schema.publisher.givenName);
        self.pblsFamilyName(schema.publisher.familyName);
        self.pblsEmail(schema.publisher.email);
        self.pblsTelephone(schema.publisher.telephone);
        self.pblsGender(schema.publisher.gender);

        self.edtGivenName(schema.editor.givenName);
        self.edtFamilyName(schema.editor.familyName);
        self.edtEmail(schema.editor.email);
        self.edtTelephone(schema.editor.telephone);
        self.edtGender(schema.editor.gender);
    }
};