function GojsControlFlow() {
	//user info required for rtc
	var user_name = "";
	var user_email = "";

	//IMPORTANT
	//this id remain unique throughout the pipeline for a module
	var unique_module_id = 1;

	//TODO: NEED TO MAKE IT RELATIVE
	var WORKFLOW_OUTPUTS_PATH = '/home/ubuntu/Webpage/app_collaborative_sci_workflow/workflow_outputs/';
	//TODO: GET IT FROM USER (WORKFLOW NAME FIELD)
	var THIS_WORKFLOW_NAME = 'test_workflow';

	var self = this;
	self.width = 960;
	self.height = 500;
	var controlDiagram = '';
	var $$ = go.GraphObject.make;


	self.show = function () {	

		canvasIntialize();
		
		controlDiagram.toolManager.linkingTool.linkValidation = validateSameDataTypeOfModules;

		//init node & port
		makeTemplate("Project", "white",
					[makePort("xml", "Potential Clones", true)],
					[makePort("xml", "XML ", false)]);	
		
		linkTemplate();
		
		//starts diagram events
		diagramEvents();
	}
	//=================show() ENDS================

	function canvasIntialize(){
		self.nodeDataArray = [];
		self.linkDataArray = [];
		
		controlDiagram =
			$$(go.Diagram, "visual",
				{
					initialContentAlignment: go.Spot.Center,
					initialAutoScale: go.Diagram.UniformToFill,
					"undoManager.isEnabled": true
				}
			);
		controlDiagram.grid.visible = true;

		//creating model for graph data 
		var graph_model_data = ({ class: 'go.GraphLinksModel', nodeCategoryProperty: 'type', linkFromPortIdProperty: 'frompid', linkToPortIdProperty: 'topid', nodeDataArray: self.nodeDataArray, linkDataArray: self.linkDataArray });
		controlDiagram.model = go.Model.fromJson(JSON.stringify(graph_model_data));  //load()

		// create the Overview and initialize it to show the main Diagram
		var myOverview =
			$$(go.Overview, "visualDiagramOverview",
				{ observed: controlDiagram });
		myOverview.grid.visible = false;

		controlDiagram.model.undoManager.isEnabled = false;				//turn off undo/redo

	} 
	//=================canvasIntialize() ENDS================
		
	// validate if the linking modules have the same (compatible) data type
	function validateSameDataTypeOfModules(fromnode, fromport, tonode, toport) {

		var portOneDataType = fromport.portId.split('.')[fromport.portId.split('.').length - 1];
		var portTwoDataType = toport.portId.split('.')[toport.portId.split('.').length - 1];

		if (portOneDataType == 'any') return true;
		if (portOneDataType == portTwoDataType) return true; //the linking datatype is same, so allow

		return false;
	}

	function makePort(portDataType, portIdentifier, leftside) {
		var port = $$(go.Shape, "Rectangle",
					{
					fill: "#FF5733", stroke: null,
					desiredSize: new go.Size(8, 8),
					//portId: portDataType,  // declare this object to be a "port"
					toMaxLinks: 1,  // don't allow more than one link into a port
					cursor: "pointer"  // show a different cursor to indicate potential link point
					});

		var lab = $$(go.TextBlock, portIdentifier + ' ('+ portDataType +') ',  // the name of the port
					{ font: "8pt sans-serif", stroke: "black", maxSize: new go.Size(130, 40),margin: 0 });

		var panel =$$(go.Panel, "Horizontal",
					{ margin: new go.Margin(2, 0) });

		// set up the port/panel based on which side of the node it will be on
		if (leftside) {
		port.toSpot = go.Spot.Left;
		port.toLinkable = true;
		port.portId = portIdentifier + '.'+ portDataType;
		port.fill = 'orange';
		lab.margin = new go.Margin(1, 0, 0, 1);
		panel.alignment = go.Spot.TopLeft;
		panel.add(port);
		panel.add(lab);
		} else {
		port.fromSpot = go.Spot.Right;
		port.fromLinkable = true;
		port.portId = portIdentifier+ '.'+ portDataType;
		lab.margin = new go.Margin(1, 1, 0, 0);
		panel.alignment = go.Spot.TopRight;
		panel.add(lab);
		panel.add(port);
		}
		return panel;
	}

	function makeTemplate(typename, background, inports, outports) {
		var node = $$(go.Node, "Spot",
			$$(go.Panel, "Auto",
				{ width: 290, height: 130 },
				$$(go.Shape, "RoundedRectangle",
					{
						fill: background, stroke: "black", strokeWidth: 2,
						spot1: go.Spot.TopLeft, spot2: go.Spot.BottomRight
					}),
				$$(go.Panel, "Table",
					$$(go.TextBlock,
						{
							row: 0,
							margin: 3,
							maxSize: new go.Size(150, 40),
							stroke: "black",
							font: "bold 11pt sans-serif"
						},
						new go.Binding("text", "name").makeTwoWay()),
					//add an extra blank row in middle 
					$$(go.TextBlock, 
						{
							text : "",
							row: 1,
							margin: 3,
							maxSize: new go.Size(80, NaN)
						}),
					//add another extra blank row in middle 
					$$(go.TextBlock, 
						{
							text : "",
							row: 2,
							margin: 3,
							maxSize: new go.Size(80, NaN)
						}),
					//add another extra blank row in middle 
					$$(go.TextBlock, 
						{
							text : "",
							row: 3,
							margin: 3,
							maxSize: new go.Size(80, NaN)
						}),
					$$(go.TextBlock,
						{
							row: 4,
							margin: 3,
							maxSize: new go.Size(150, NaN),
							stroke: "black",
							font: "bold 8pt sans-serif"
						},
						new go.Binding("text", "module_id").makeTwoWay())
				),
				$$(go.Shape, "Circle",
					{ row: 3, fill: "white", strokeWidth: 0, name: "jobStatus", width: 13, height: 13 })
			),
			$$(go.Panel, "Vertical",
				{
					alignment: go.Spot.Left,
					alignmentFocus: new go.Spot(0, 0.5, 8, 0)						
				},
				inports),
			$$(go.Panel, "Vertical",
				{
					alignment: go.Spot.Right,
					alignmentFocus: new go.Spot(1, 0.5, -8, 0)
				},
				outports)
		);
		controlDiagram.nodeTemplateMap.add(typename, node);
	}

	function linkTemplate(){
		controlDiagram.linkTemplate =
			$$(go.Link,
				{
					routing: go.Link.AvoidsNodes, corner: 10,
					relinkableFrom: false, relinkableTo: false, curve: go.Link.JumpGap
				},				
				$$(go.Shape, { stroke: "#00bfff", name: "datalink", strokeWidth: 2.5 }),
				$$(go.Shape, { stroke: "#00bfff", name: "datalinkArrow", fill: "#00bfff", toArrow: "Standard" })

				// $$(go.Shape, { stroke: "gray", name: "datalink", strokeWidth: 2 }),
				// $$(go.Shape, { stroke: "gray", name: "datalinkArrow", fill: "gray", toArrow: "Standard" })
			);
		}

	function addNewLinkToWorkflowObject(newLinkInformation) {
		controlDiagram.startTransaction("add link");
		var newlink = { from: newLinkInformation.from, frompid: newLinkInformation.frompid, to: newLinkInformation.to, topid: newLinkInformation.topid };
		controlDiagram.model.addLinkData(newlink);
		controlDiagram.commitTransaction("add link");
	}


	function workflowObjSelectionMoved(selectionNewLocationInfo) {
		controlDiagram.startTransaction('selection moved');
		var movedNode = controlDiagram.findNodeForKey(selectionNewLocationInfo.key);
		movedNode.location = new go.Point(selectionNewLocationInfo.x, selectionNewLocationInfo.y);
		controlDiagram.commitTransaction('selection moved');
	}


	function workflowObjRemoveNode(nodeInfoForRemoval) {
		controlDiagram.startTransaction('node removed');
		var nodeTargetedForDeletion = controlDiagram.findNodeForKey(nodeInfoForRemoval.key);
		controlDiagram.remove(nodeTargetedForDeletion);
		controlDiagram.commitTransaction('node removed');
	}

	function workflowObjRemoveLink(linkInfoForRemoval) {
		var linksTargetedForDeletion = controlDiagram.findLinksByExample({ 'from': linkInfoForRemoval.from, 'frompid': linkInfoForRemoval.frompid, 'to': linkInfoForRemoval.to, 'topid': linkInfoForRemoval.topid });

		for (var iter = linksTargetedForDeletion; iter.next();) {
			aLink = iter.value;
			controlDiagram.startTransaction('link removed');
			controlDiagram.remove(aLink);
			controlDiagram.commitTransaction('link removed');
		}

	}

	//=======================================
	//=============gojs graph end============
	//=======================================


	//===========================>>>>>>>>>>>>>>>>>>>>>>>>
	// Diagram Events Start
	//===========================>>>>>>>>>>>>>>>>>>>>>>>>
	
	function diagramEvents(){

		//show the corresponding module details on any module click
		controlDiagram.addDiagramListener("ObjectSingleClicked",
		function (e) {
			var part = e.subject.part;
			if (!(part instanceof go.Link)) {
				var clickedModuleID = part.data.key; // Module_1
				//clickedModuleID = clickedModuleID.split('_')[1]; // 1
				$(".module").hide();
				$("#" + clickedModuleID).show();
			}
		}
		);

		//show the corresponding module details on any module click
		controlDiagram.addDiagramListener("ObjectDoubleClicked",
		function (e) {
			var part = e.subject.part;
			if (!(part instanceof go.Link)) {
				var clickedModuleID = part.data.key; // Module_1

				//@@USER_STUDY
				console.log(user_email + "=>MODULE_CONFIG_OPENED=>" + "moduleID:" + part.data.key);

				$(".module").hide();
				$("#" + clickedModuleID).show();

				$("#modal_module_configs").css('display', 'block');
			}
		}
		);

		//remove all corresponding module details on background click
		controlDiagram.addDiagramListener("BackgroundSingleClicked",
		function (e) {
			//$(".module").hide();
			//@@USER_STUDY
			console.log(user_email + "=>BACKGROUND_SINGLE_CLICKED");

			$("#modal_module_configs").css('display', 'none');
		}
		);

		$(document).on('click', '.close', function () {
		//alert('close clicked');
		//@@USER_STUDY
		console.log(user_email + "=>MODULE_CONFIG_CLOSED");

		$("#modal_module_configs").css('display', 'none');
		$("#myModal").css('display', 'none');
		});


		//attempting Workflow Diagram Part (link/node) deletion.
		controlDiagram.addDiagramListener("SelectionDeleting",
		function (e) {
			//alert("SelectionDeleting");
			for (var iter = controlDiagram.selection.iterator; iter.next();) {
				var part = iter.value;
				if (part instanceof go.Node) {
					//alert(part.data.key);


					//@@USER_STUDY
					console.log(user_email + "=>MODULE_DELETED" + "=>module_id:" + part.data.key);



					var nodeInfoForRemoval = { 'key': part.data.key };
					// notifyAll("workflow_obj_selection_node_delete", nodeInfoForRemoval);
				}
				if (part instanceof go.Link) {
					//alert(part.data.from);
					//alert(part.data.topid);

					var thisPortInput = part.data.to + '_NO_INPUT_SOURCE_SELECTED_' + part.data.topid;
					var referenceVariable = part.data.topid.split('.')[part.data.topid.split('.').length - 2];
					thisPortInput = referenceVariable + '="' + WORKFLOW_OUTPUTS_PATH + THIS_WORKFLOW_NAME + '/' + thisPortInput + '"';

					$("#" + part.data.to + ' .' + referenceVariable).val(thisPortInput).trigger('change');



					//@@USER_STUDY
					console.log(user_email + "=>DATALINK_DELETED" + "=>" + 'from:' + part.data.from + '*frompid:' + part.data.frompid + '*to:' + part.data.to + '*topid:' + part.data.topid);

					var linkInfoForRemoval = { 'from': part.data.from, 'frompid': part.data.frompid, 'to': part.data.to, 'topid': part.data.topid };
					// notifyAll("workflow_obj_selection_link_delete", linkInfoForRemoval);
				}
			}
		}
		);

		//event called on creating new link on the workflow object
		controlDiagram.addDiagramListener("LinkDrawn",
		function (e) {
			var part = e.subject.part;
			if (part instanceof go.Link) {
				//alert("Linked From: "+ part.data.from + " To: " + part.data.to);

				//$("#module_id_1 ."+part.data.topid).val("var='this should be new value'");
				//var toModuleId = part.data.to.split('_')[1]; // ie., x in Module_x
				//toModuleId = '#module_id_'+ toModuleId;

				var toPortClass = part.data.topid.split('.')[part.data.topid.split('.').length - 2];
				//var fromPortClass = part.data.frompid.split('.')[part.data.frompid.split('.').length - 2];
				//toPortClass = ' .' + toPortClass;

				$('#' + part.data.to + ' .' + toPortClass).val(toPortClass + "='" + WORKFLOW_OUTPUTS_PATH + THIS_WORKFLOW_NAME + '/' + part.data.from + '_' + part.data.frompid + "'").trigger('change');

				//@@USER_STUDY
				console.log(user_email + "=>DATALINK_ADDED" + "=>" + 'from:' + part.data.from + '*frompid:' + part.data.frompid + '*to:' + part.data.to + '*topid:' + part.data.topid);

				//alert("To " + part.data.to);
				//alert(part.data.topid.split('(')[part.data.topid.split('(').length - 2]);

				var newLinkInformation = { 'from': part.data.from, 'frompid': part.data.frompid, 'to': part.data.to, 'topid': part.data.topid };
				// notifyAll("workflow_obj_new_link_drawn", newLinkInformation);

			}
		}
		);

		//event called on selection (Node) changes...
		controlDiagram.addDiagramListener("SelectionMoved",
		function (e) {
			//alert("Selection Moved");
			for (var iter = controlDiagram.selection.iterator; iter.next();) {
				var part = iter.value;
				if (part instanceof go.Node) {
					//alert(part.data.key + " x: " + part.location.x + " y: " + part.location.y);


					//@@USER_STUDY
					console.log(user_email + "=>MODULE_MOVED" + "=>" + 'key:' + part.data.key + '*x:' + part.location.x + '*y:' + part.location.y);


					var nodeNewLocationInformation = { 'key': part.data.key, 'x': part.location.x, 'y': part.location.y };
					//notifyAll('workflow_obj_selection_moved', nodeNewLocationInformation);
				}
			}

		}
		);
	}
	
	//===========================>>>>>>>>>>>>>>>>>>>>>>>>
	// Diagram Events Ends
	//===========================>>>>>>>>>>>>>>>>>>>>>>>>		


	//========================================================
	//================== WORKFLOW CONTROL CODE STARTS ========
	//========================================================


		function getNextUniqueModuleID() {
			return unique_module_id;
		}

		function updateNextUniqueModuleID() {
			unique_module_id = unique_module_id + 1;
		}

		function Galaxy_Pear() {
			data = {
				"toolInputs": [{ "label": "Fastq File", "referenceVariable": "forward_fastq", "dataFormat": "f" },
				{ "label": "Fastq File", "referenceVariable": "reverse_fastq", "dataFormat": "fq" }
				],
				"toolOutputs": [{ "label": "Quality Analysis HTML", "referenceVariable": "assembled", "dataFormat": "fq" },
				{ "label": "Quality Analysis ZIP", "referenceVariable": "discarded", "dataFormat": "fq" },
				{ "label": "Quality Analysis ZIP", "referenceVariable": "forward_unassembled", "dataFormat": "fq" },
				{ "label": "Quality Analysis ZIP", "referenceVariable": "reverse_unassembled", "dataFormat": "fq" }
				],
				"toolConfigurations": [],
				"toolDocumentation": []
			};
			return JSON.stringify(data);
		}

		//adds the module to the pipeline. moduleID is unique throughout the whole pipeline
		//moduleName is the name of the module like: rgb2gray, medianFilter and so on
		function addModuleToPipeline(moduleID, moduleName, inportData, outportData) {	
			var moduleSourceCode_html = '';

			console.log(moduleID + " & " + moduleName);

			console.log(inportData)
			console.log(outportData)

			var listOfInputPorts = [];
			var listOfOutputPorts = [];

			//input port definition
			if(inportData !== ''){
				inportData = JSON.parse(inportData);
				for (var k in inportData) {
					if (inportData[k] instanceof Object) {
						var name = inportData[k]['name'];
						var type = inportData[k]['type'];

						var aNewInputPort = makePort(type, name, true);
						listOfInputPorts.push(aNewInputPort);
					}
				}
			}

			//output port definition
			outportData = JSON.parse(outportData);

			if(outportData.length !== 0){
				var name = '';
				var type = '';
								
				//if defaultOutputParam not empty
				if(outportData[0]['name'] !== undefined && outportData[0]['type'] !== undefined){
					for (var k in outportData) {
						if (outportData[k] instanceof Object) {
							name = outportData[k]['name'];
							type = outportData[k]['type'];

							var aNewOutputPort = makePort(type, name, false);
							listOfOutputPorts.push(aNewOutputPort);
						}
					}
				}
				
				//if defaultOutputParam empty
				else{
					// if(outportData[0] !== undefined)
					// 	name = outportData[0]['name'];
					
					if(outportData[0] !== undefined)			
						type = outportData[0]['type'];
					
					var aNewOutputPort = makePort(type, name, false);
					listOfOutputPorts.push(aNewOutputPort);
				}
			}
			
			makeTemplate(moduleName, "White",
				listOfInputPorts,
				listOfOutputPorts);

			controlDiagram.startTransaction("add node");
			// have the Model add the node data
			var newnode = { "key": "module_id_" + moduleID, "type": moduleName, "name": moduleName, "module_id": "Module " + moduleID };
			controlDiagram.model.addNodeData(newnode);
			// locate the node initially where the parent node is
			// diagram.findNodeForData(newnode).location = node.location;
			// and then add a link data connecting the original node with the new one
			// var newlink = { from: node.data.key, to: newnode.key };
			// diagram.model.addLinkData(newlink);
			// finish the transaction -- will automatically perform a layout
			controlDiagram.commitTransaction("add node");
		}//End of addModuleToPipeline()

		//handling any pipeline module addition on click using class for generalisation			   
		//newly added for control flow diagram			
		self.addNewNode = function (newModuleName, inportData, outportData) {

			var newModuleID = getNextUniqueModuleID();
			// var newModuleName = $(this).attr("id"); //getting the ID of service			

			addModuleToPipeline(newModuleID, newModuleName, inportData, outportData);

			//prepare the next valid unique module id
			updateNextUniqueModuleID();
		}

		//========================================================
		//================== WORKFLOW CONTROL CODE ENDS ==========
		//========================================================
	
}

gojsControlFlow = new GojsControlFlow();

