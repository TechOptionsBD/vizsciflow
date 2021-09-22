function DatasetPluginViewModel() {
  var self = this;
  self.scidatamgrURI = 'https://p2irc-data-dev.usask.ca'
  self.datasetList = ko.observableArray();
  let datasetList;

  const initPlugin = function () {
    // initialize plugin
    datasetList = $("#datasetPlugin").datasetlist({
      data: self.datasetList(),
      searchBar: true, 
      searchBarPlaceholder: "Search dataset in list",
      headerText: 'SciDataManager Plugin Header Text',
      onItemClick: onItemClick,
      selectedDataItem: getSelectedDataItem, 
      getSelectedDataItem: getSelectedDataItem,
      onDataItemDoubleClick: onDataItemDoubleClick,
      onItemDrag: onDataItemDrag,
      onItemExpand: onItemExpand,
      onItemExpanded: onItemExpanded,
      headerClass: 'custom-dataset-header',
      itemHeaderClass: 'custom-dataset-item-header',
      itemBodyClass: 'custom-dataset-item-body',
      dataItemClass: 'custom-data-item',

      apiUrl: `${self.scidatamgrURI}/api/plugin/dataset/data?`, // set backend api for dataset data retrive
      secretKey: "6D59713374367639", //app secret key
      userName: username //current user
    });
    
    // render list on UI
    datasetList.renderList();
    datasetList.getSelectedDataItem()
  }

  self.renderDataset = function() {
    self.datasetList([]);

    // fetching api data
    ajaxcalls.simple(self.scidatamgrURI + '/api/plugin/datasets', 'GET', { secret_key: '6D59713374367639', username: username, pageNum: '1', numOfItems: '50' }).done(function(dataset) {    
      if (dataset === undefined)
        return;
      
      self.datasetList(dataset.data);
      initPlugin()
    }).fail(function(jqXHR) {
      showXHRText(jqXHR);
      initPlugin()
    });
  }

  self.reload = function () {
    $("#datasetPlugin").empty()
    self.renderDataset()
  }

  self.copyToEditor = function (url) {
      exmpl = `data = \'${url}\'`
      var pos = editor.selection.getCursor();
      editor.session.insert(pos, exmpl + "\r\n");
      editor.focus();
  }

  const onItemClick = function (e, data) {
    console.log('onItemClick');
  }

  const getSelectedDataItem = function (e, data) {
    console.log('getSelectedDataItem');
  }
    
  const onDataItemDoubleClick = function (e, dataset) {
    let path = dataset.path
    let pid = dataset.dataset.pid
    path = path.replace("Root node", "Data");
    path = `${self.scidatamgrURI}/${pid}${path}`
    self.copyToEditor(path)
  }

  const onDataItemDrag = function (e, dataset) {
    self.copyToEditor(dataset.path)
  }

  const onItemExpand = function (e, dataset) {
    datasetList.lazyLoadDatasetItems(dataset)
  }

  const onItemExpanded = function (e, data) {
    console.log('onItemExpanded');
  }
}

datasetViewModel = new DatasetPluginViewModel();