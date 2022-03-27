# scidatamanager-plugin
jquery plugin for dataset list 

**init plugin** 

```javascript
const datasets = $('target-element').datasetlist({ 
  	data: [], // required else returns false 
	searchBar: false, // default false, if set true, a search bar will apear at the top of the list
	searchBarClass: '', // provide class(s) for search bar, provide mutiple with space sperated
	itemClass: '', // provide class(s) applicable on the dataset each item, provide multiple classes with space separated
  	itemheaderClass: '', // provide class(s), provide mutiple with space sperated 
  	itemBodyClass: '', // provide class(s), provide mutiple with space sperated 
  	dataItemClass: '', // provide class(s), provide mutiple with space sperated 
  	onItemClick: callback handler, // callback for list item click event. callback recievs (event, data) as parameter 
  	onItemExpand: callback handler, // callback for list item expanding event. callback recievs (event, data) as parameter 
  	onItemExpanded: callback handler, // callback for list item after expanded event. callback recievs (event, data) as parameter 
  	onItemClosing: callback handler, // callback for list item closing event. callback recievs (event, data) as parameter
  	onItemClosed: callback handler, // callback for list item after closed event. callback recievs (event, data) as parameter 
	onItemRightClick: callback handler, // callback for list item right mouse button click
	onItemDrag: callback handler, // callback for list item drag event
	onDataItemDoubleClick: callback handler // callback for dataset data item double click event. callback recievs (event, data) as parameter 
	currentLoadedData: callback handler // callback for dataset lazy loaded data expand event. callback receives (datasetid, nodeid, loadedData) parameter
	 apiUrl: null, // set backend api base url
     secretKey: null, // set app secret key
     userName: null // set app user
});
```
after init call **renderList()** method to render list on UI

```javascript
	datasets.renderList(); //returns false if no data is supplied initially 
```

single dataset can be added after rendering the list

```javascript
	datasets.addNewDataset(data);
```

list header text can be updated anytime after initialization:

```javascript
	datasets.updateHeaderText(text);
```

callbacks can be assigned after the plugin is initialized:

```javascript
	datasets.onItemClick = function(event, data){
		// your logic goes here
	}
```

Every items in the **data[]** array should provide this:

```javascript
	{
		id: '', //unique,required. Otherwise this one won't be rendered on the UI
		name: '',
		path: '',
		groupName: '',
		datasetType: '',
		url: '',
		data: [], // array of data item
	}
```
**data** property in the above object is the list of dataset data items, every item should contain:

```javascript
	{
		id: '', // unique,required. Otherwise won't be rendered on the UI
		text: ''
	}
```
Every root node must provide this:

```javascript
{
    id: ''  //unique
    text: '',
    children: [
      {
        id: '', //unique
        text: "",
        children: boolean,
		type: '' // not required
      },
     
    ],
  },
```
Every child node must provide this:

```javascript
{
	[
      {
        id: '', //unique
        text: "",
        children: boolean,
		type: '' // not required
      },
     
    ],
  },
```

if dataset data properties are not provided in plugin initialization, can be added later 

```javascript 
    datasets.lazyLoadDatasetItems(dataset)
```




get any selected item data
```javascript
	datasets.getSelectedDataItem()
```
