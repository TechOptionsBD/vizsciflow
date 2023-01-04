function DatasetPluginViewModel(scidatapath, datasetCtrlParam, buildPath) {
  var self = this;
  self.scidatamgrURI = scidatapath;
  self.dataSourcesURI = '/datasources';
  self.datasets = ko.observableArray();
  self.datasetCtrl = datasetCtrlParam;
  self.buildPath = buildPath;
  self.selectedPath = '';

  const initPlugin = function () {
    // initialize plugin
    datasetList = $(self.datasetCtrl).datasetlist({
      data: self.datasets(),
      searchBar: true,
      searchBarPlaceholder: "Search dataset in list",
      headerText: "SciDataManager Plugin Header Text",
      onItemClick: onItemClick,
      selectedDataItem: getSelectedDataItem,
      getSelectedDataItem: getSelectedDataItem,
      onDataItemDoubleClick: onDataItemDoubleClick,
      onItemDrag: onDataItemDrag,
      onSelectionChanged: onSelectionDataItemChanged,
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
    self.datasets([]);

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

        self.datasets(dataset.data);
        initPlugin();
      })
      .fail(function (jqXHR) {
        showXHRText(jqXHR);
        initPlugin();
      });
  };

  self.download = $.debounce(500, function () {

    if (!self.selectedPath)
      return;

    $.redirect(self.dataSourcesURI, { 'download': self.selectedPath }, "POST", "_blank");
  });


  self.reload = function () {
    $(self.datasetCtrl).empty();
    self.renderDataset();
  };

  self.addFolder = $.debounce(500, function () {
    // node = self.datasetCtrl.datasetlist.getSelectedDataItem();

    if (!self.selectedPath)
        return;
    ajaxcalls.simple(self.dataSourcesURI, 'GET', { 'addfolder': self.selectedPath}).done(function (data) {
      datasetList.addNewDataset(data);

        // var newNodePosition = 'inside';
        // var parentNode = node;
        // var newNode = $('#tree').jstree().create_node(parentNode, data, newNodePosition, function () {
        //     $("#btnAddFolder").removeClass('active');
        // });
        // $('#tree').jstree("deselect_all");
        // $("#tree").jstree(true).select_node(newNode);
    });
});

  self.about = function () {
    window.open("static/biodsl-help.html#datasources", '_blank');
  };
  self.beginFileUpload = function () {
    centerDialog($('#file-upload-dialog'));
    //self.loadMetadataProperties();
    ko.cleanNode($("#file-upload-dialog")[0]);
    ko.applyBindings(self, $("#file-upload-dialog")[0]);
    $('#file-upload-dialog').modal('show');
  }

  self.upload = function () {

    $('#file-upload-dialog').modal('hide');

    var files = $("#upload").get(0).files;
    var formdata = new FormData();
    formdata.append('upload', files[0]); //use get('files')[0]
    if (!self.selectedPath)
      return;
    formdata.append('path', self.selectedPath);//you can append it to formdata with a proper parameter name
    // formdata.append('filename', $("#inputFilename").val());
    // var visualizer = $("#inputVisualizer").val();
    // if (visualizer) {
    //     visualizer = visualizer.split(": ");
    //     visualizer = {
    //         [visualizer[0]]: visualizer[1]
    //     };
    //     formdata.append('visualizer', JSON.stringify(visualizer));
    // }
    // formdata.append('annotations', $("#inputAnnotations")[0].value);
    // mimetype = $("#inputMimeType").val();
    // if (mimetype) {
    //     mimetype = mimetype.split(": ");
    //     formdata.append('mimetype', JSON.stringify({ [mimetype[0].trim()]: mimetype[1].trim() }));
    // }

    ajaxcalls.form(self.dataSourcesURI, 'POST', formdata).done(function (data) {
        // var inputFileName = $("#inputFilename").val();
        // self.loadNewItem(node, inputFileName);
    });
  }

  self.beginUpdateMetadata = function () {
    if (!self.selectedPath)
      reuturn;
    metadataViewModel.load(self.selectedPath);
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

  const onSelectionDataItemChanged = function(e, dataset){
    self.selectedPath = dataset.path ?? '';
  }

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
