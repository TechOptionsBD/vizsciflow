const setDatasetRootNodeStateAction = (datasetId, commonApiObj) => {
  return {
    type: "SET_EXPANDS_NODE_STATUS",
    payload: { datasetId, commonApiObj },
  };
};

const setDatasetChildNodeStateAction = (datasetId, commonApiObj) => {
  return {
    type: "SET_EXPANDED_NODE_CHILD_NODE_STATUS",
    payload: { datasetId, commonApiObj },
  };
};

const setDatasetStateReducer = (state = {}, action) => {
  const hasMore = action?.payload?.commonApiObj?.hasMore;
  const pageNum = action?.payload?.commonApiObj?.pageNum;
  const nodeLength = action?.payload?.commonApiObj?.nodeLength;
  switch (action.type) {
    case "SET_EXPANDS_NODE_STATUS":
      if (state[action.payload.datasetId]) {
        return {
          ...state,

          [action.payload.datasetId]: {
            ...state[action.payload.datasetId],
            [action.payload.commonApiObj.loadNodeId]: {
              hasMore,
              pageNum,
              nodeLength,
            },
          },
        };
      } else {
        return {
          ...state,

          [action.payload.datasetId]: {
            [action.payload.commonApiObj.loadNodeId]: {
              hasMore,
              pageNum,
              nodeLength,
            },
          },
        };
      }

    case "SET_EXPANDED_NODE_CHILD_NODE_STATUS":
      const datasetIdInfo = state[action.payload.datasetId];
      if (
        datasetIdInfo &&
        datasetIdInfo[action.payload.commonApiObj.loadNodeId]
      ) {
        return {
          ...state,
          [action.payload.datasetId]: {
            ...state[[action.payload.datasetId]],
            [action.payload.commonApiObj.loadNodeId]: {
              hasMore,
              pageNum,
              nodeLength,
            },
          },
        };
      }

    default:
      return state;
  }
};

// const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = Redux.createStore(
  setDatasetStateReducer,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
