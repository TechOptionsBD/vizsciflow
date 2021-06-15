// get jstree core plugin
const getJsTreePlugins = () => [
  "json_data",
  "dnd",
  "themes",
  "types",
  "search",
  "massload",
  "crrm",
];

// get folder first expand's http request query string
const getJsTreeApiRequestQueryString = (nodeId, datasetId, settings) => {
  return {
    data_id: nodeId === "#" ? -1 : nodeId,
    dataset_id: datasetId,
    page_num: 1,
    secret_key: settings.secretKey,
    username: settings.userName,
    _: 1622973566266
  };
};

// get common used api response
const getCommonApiResObj = (parsedData) => {
  // console.log(parsedData, "getCommonApiResObj")
  const nodeLength = parsedData.itemCount;
  const hasMore = parsedData.hasMore;
  const pageNum = parsedData.pageNum;
  const loadNodeId = parsedData.loadNodeId;
  return { nodeLength, loadNodeId, pageNum, hasMore };
};

// get folder first expand's http request response with filtered data
const getLoadMoreNodeWithRootResponse = (datasetId, commonObj, parsedData) => {
  // console.log( datasetId, commonObj, parsedData, "filterApiResponse");
  const { nodeLength, hasMore, pageNum, loadNodeId } = commonObj;
  
  if (parsedData && parsedData.nodes && hasMore && parsedData.nodes.children) {
    parsedData.nodes.children.push({
      id: `${loadNodeId}`,
      text: "load more",
      icon: "jstree-loading",
      // icon: loadNodeId
    });
  } else if (hasMore) {
    parsedData.nodes.push({
      id: `${loadNodeId}`,
      text: "load more",
      icon: "jstree-loading",
      // icon: loadNodeId,
    });
  }
  if (hasMore) {
    store.dispatch(setDatasetRootNodeStateAction(datasetId, {loadNodeId, hasMore, pageNum, nodeLength}))
    // setSelctedNodesStatus(datasetId, { loadNodeId, loading, startIndex, nodeLength });
  }
  // parsedData.nodes.id="#"
  // console.log(JSON.stringify(parsedData.nodes), "in get more")
  return parsedData.nodes;
};

const getSelctedNodesStatus = (datasetId, selectedNode) =>{
  const storedData = store.getState();
  const currentExpandedDataset = storedData[datasetId];
  if(currentExpandedDataset)
  return currentExpandedDataset[selectedNode]

  // const currentSavedDatasetStatus = JSON.parse(localStorage.getItem(datasetId));
  // return currentSavedDatasetStatus[selectedNode]
}

const setSelctedNodesStatus = (datasetId,{
  loadNodeId,
  loading,
  startIndex,
  nodeLength,
}) => {
  // localStorage.setItem(
  //   loadNodeId,
  //   JSON.stringify({ loading, startIndex, nodeLength })
  // );
  const loadNodeStatus = {[loadNodeId]: {loading, startIndex, nodeLength }}
  // const savedItem = JSON.parse(localStorage.getItem(datasetId));
  // if(savedItem !== null){
    
  //   const c = {...savedItem, ...loadNodeStatus};
  // localStorage.setItem(datasetId, JSON.stringify(c))
  // }else{

  //   localStorage.setItem(datasetId, JSON.stringify(loadNodeStatus))
  // }
};

const getCustmonApiUrlWithQueryString = (url, nodeId, datasetId, pageNum, settings) =>
  `${url}&data_id=${
    nodeId === "#" ? -1 : nodeId
  }&dataset_id=${datasetId}&page_num=${pageNum + 1}&secret_key=${settings.secretKey}&username=${settings.userName}&_=1622973566266`;

const getLoadMoreNodes = (url, nodeId, datasetId, pageNum, settings, cb) => {
  $.get(
    getCustmonApiUrlWithQueryString(url, nodeId, datasetId, pageNum, settings),
    function (data, status) {
      data = JSON.parse(data)
      cb({ commonApiObj: getCommonApiResObj(data), loadedData: data.nodes});
    }
  );
};

const appendLoadedChild = (nodes, loadNodeId, datasetId) => {
  nodes && nodes.length && nodes.forEach((d) => {
    $(`#card-body-${datasetId}`).jstree(
      "create_node",
      loadNodeId,
      d,
      "before",
      function () {
        console.log("node added succesfully");
      },
      false,
      true
    );
  });
};

const deleteLoadeMoreNode = (datasetId, nodeId) => {
  var node = $(`#card-body-${datasetId}`).jstree(true).get_node(nodeId);
  $(`#card-body-${datasetId}`).jstree("delete_node", node);
};
