function DatasetPluginViewModel(scidatapath, datasetCtrlParam, buildPath) {
  var self = this;
  self.scidatamgrURI = scidatapath;
  self.datasetList = ko.observableArray();
  self.datasetCtrl = datasetCtrlParam;
  self.buildPath = buildPath;
  let datasetList;
  self.selectedNode = null;

  const initPlugin = function () {
    // initialize plugin
    datasetList = $(self.datasetCtrl).datasetlist({
      data: self.datasetList(),
      searchBar: true,
      searchBarPlaceholder: "Search dataset in list",
      headerText: "SciDataManager Plugin Header Text",
      onItemClick: onItemClick,
      selectedDataItem: getSelectedDataItem,
      getSelectedDataItem: getSelectedDataItem,
      onDataItemDoubleClick: onDataItemDoubleClick,
      onItemDrag: onDataItemDrag,
      onItemExpand: onItemExpand,
      onItemExpanded: onItemExpanded,
      headerClass: "custom-dataset-header",
      itemHeaderClass: "custom-dataset-item-header",
      itemBodyClass: "custom-dataset-item-body",
      dataItemClass: "custom-data-item",

      apiUrl: `${self.scidatamgrURI}/api/plugin/dataset/data?`, // set backend api for dataset data retrive
      secretKey: "6D59713374367639", //app secret key
      userName: username, //current user
    });

    // render list on UI
    datasetList.renderList();
    datasetList.getSelectedDataItem();
  };

  self.renderDataset = function () {
    self.datasetList([]);

    // fetching api data
    ajaxcalls
      .simple(self.scidatamgrURI + "/api/plugin/datasets", "GET", {
        secret_key: "6D59713374367639",
        username: username,
        pageNum: "1",
        numOfItems: "50",
      })
      .done(function (dataset) {
        if (dataset === undefined) return;

        self.datasetList(dataset.data);
        initPlugin();
      })
      .fail(function (jqXHR) {
        showXHRText(jqXHR);
        initPlugin();
      });
  };

  self.download = $.debounce(500, function () {

    node = self.selectedNode;
    if (node === undefined) {
      return;
    }

    $.redirect("/datasources", { 'download': node.original.path }, "POST", "_blank");
  });


  self.reload = function () {
    $(self.datasetCtrl).empty();
    self.renderDataset();
  };

  self.addFolder = $.debounce(500, function () {
    node = self.datasetCtrl.datasetlist.getSelectedDataItem();

    if (node === undefined)
        return;
    ajaxcalls.simple("/datasources", 'GET', { 'addfolder': node.original.path }).done(function (data) {
        var newNodePosition = 'inside';
        var parentNode = node;
        var newNode = $('#tree').jstree().create_node(parentNode, data, newNodePosition, function () {
            $("#btnAddFolder").removeClass('active');
        });
        $('#tree').jstree("deselect_all");
        $("#tree").jstree(true).select_node(newNode);
    });
});

  self.about = function () {
    window.open("static/biodsl-help.html#datasources", '_blank');
  };
  self.beginFileUpload = function () {
    centerDialog($('#file-upload-dialog'));
    self.loadMetadataProperties();
    ko.cleanNode($("#file-upload-dialog")[0]);
    ko.applyBindings(dataSourceViewModel, $("#file-upload-dialog")[0]);
    $('#file-upload-dialog').modal('show');
  }

  self.beginUpdateMetadata = function () {
    //centerDialog($('#update-metadata-dialog'));
    var node = dataSourceViewModel.selectedNode().original;
    // var node = dataSourceViewModel.selectedNode();
    if (node === undefined)
      return;

    metadataViewModel.load(node.path);
    $('#update-metadata-dialog').modal('show');
  }

  self.loadMetadataProperties = function () {

    ajaxcalls.simple(metadataViewModel.metadataURI, 'GET', { 'properties': true }).done(function (data) {

      self.visualizers = ko.observableArray();
      $.each(data['visualizers'], function (key, value) {
        self.visualizers.push(ko.observable(key + ": " + value))
      });

      self.mimetypes = ko.observableArray();
      $.each(data['mimetypes'], function (key, value) {
        self.mimetypes.push(ko.observable(key + ": " + value))
      });

    }).fail(function (jqXHR, a, b) {
      showXHRText(jqXHR);
    });
  }

  self.load = function () {
    ajaxcalls.simple(self.scidatamgrURI, 'GET')
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


  self.copyToEditorDoubleClick = function (url) {
    // exmpl = `datassss = \'${url}\'`
    // var pos = editor.selection.getCursor();
    // editor.session.insert(pos, exmpl + "\r\n");
    // editor.focus();

    var pos = editor.selection.getCursor();
    text = editor.session.getLine(pos.row);
    if (text !== undefined && text.length != 0)
      editor.session.insert(pos, "'" + url + "'");
    else editor.session.insert(pos, "data = '" + url + "'\n");

    setTimeout(() => editor.focus(), 100)
    // editor.focus();
    // console.log(editor.getSession())
    // editor.getSession().reset();
    // $('#editor').get[0].reset()
   
  };

  self.copyToEditorDrag = function (url) {
    // exmpl = `\'${url}\'`;
    // var pos = editor.selection.getCursor();
    // editor.session.insert(pos, exmpl);
    // editor.focus();
    var pos = editor.selection.getCursor();
    text = editor.session.getLine(pos.row);
    if (text !== undefined && text.length != 0)
      editor.session.insert(pos, "'" + url + "'");
    else editor.session.insert(pos, "data = '" + url + "'\n");
    editor.focus();
    // editor.getSession().reset();
  };

  const onItemClick = function (e, data) {
    console.log("onItemClick");
  };

  const getSelectedDataItem = function (e, data) {
    console.log("getSelectedDataItem");
  };

  const onDataItemDoubleClick = function (e, dataset) {
    path = self.buildPath(self.scidatamgrURI, dataset?.dataset?.pid, dataset.path);
    self.copyToEditorDoubleClick(path);
  };

  const onDataItemDrag = function (e, dataset) {
    path = self.buildPath(self.scidatamgrURI, dataset?.dataset?.pid, dataset.path);
    var target = e.target;
    if (target.getAttribute('class') == 'ace_content'){
      self.copyToEditorDrag(path);
    }
    else {
      koobj = ko.dataFor(target);
      if (koobj) {
        koobj.value(path);
      }
    }
  };

  const onItemExpand = function (e, dataset) {
    datasetList.lazyLoadDatasetItems(dataset);
  };

  const onItemExpanded = function (e, data) {
    console.log("onItemExpanded");
  };
}
