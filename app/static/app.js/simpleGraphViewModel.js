function simpleGojsGraph()
        {			
        	var self = this;

       		//refactoring data for gojs graph
    		self.show = function(rels) {
    			self.nodes = [];
    			self.links = [];			
    			self.nodeDataArray = [];
    			self.linkDataArray = [];
    			
    			//remove duplicate values 
    			rels = rels.filter((rels, index, self) =>
    			  index === self.findIndex((t) => (
    			    t.source.id === rels.source.id && t.target.id === rels.target.id
    			  ))
    			)
    			
    			rels.forEach(function(rel){
    				var exists = self.nodes.filter(function(n)
    					{
    						return rel.source.id === n.id; 
    					});
    				if (exists.length == 0)
    					{
    						self.nodes.push(rel.source);
    						self.nodeDataArray.push({key: rel.source.id, type: rel.source.label, name: rel.source.name});
    					}
    				
    				exists = self.nodes.filter(function(n)
    					{
    						return rel.target.id === n.id; 
    					});
    				if (exists.length == 0)
    					{
    						self.nodes.push(rel.target);
    						self.nodeDataArray.push({key: rel.target.id, type: rel.target.label, name: rel.target.name});
    					}					
    			});
    			
    			rels.forEach(function(rel) {
    				
    				var sourceNode = self.nodes.filter(function(n) { return n.id === rel.source.id; })[0];
    			    var targetNode = self.nodes.filter(function(n) { return n.id === rel.target.id; })[0];
    			    self.links.push({source: sourceNode, target: targetNode, value: rel.type});
    			    self.linkDataArray.push({from: sourceNode.id, frompid: 'OUT', to: targetNode.id, topid: 'IN', value: rel.type});
    			});
    			    			
//    			console.log(JSON.stringify(self.linkDataArray))
//    			console.log(JSON.stringify(self.nodeDataArray))
    			
		    	//reload the graph
    			var graphdiv = document.getElementById("graph");
    			if (graphdiv !== null) {
    			    var olddiag = go.Diagram.fromDiv(graphdiv);
    			    if (olddiag !== null) 
    			    	olddiag.div = null;
    			}
  		      
  		    	//reload the overview
      			var overviewdiv = document.getElementById("DiagramOverview");
      			if (overviewdiv !== null) {
      			    var oldoverview = go.Diagram.fromDiv(overviewdiv);
      			    if (oldoverview !== null) 
      			    	oldoverview.div = null;
      			}      			
      			
    			//gojs graph
    			var $$ = go.GraphObject.make;
    			
	    		      Diagram =
	    		        $$(go.Diagram, "graph",
	    		          {   		        	
	    		            initialContentAlignment: go.Spot.Center,		//display the graph at center initially
	    		            initialAutoScale: go.Diagram.UniformToFill,
	    		            layout: $$(go.LayeredDigraphLayout,				//graph layout is Layered
	    		              { direction: 0,								//graph will extend towards Right direction
	    		            	layeringOption: go.LayeredDigraphLayout.LayerLongestPathSink
	    		              }),							
	    		            "undoManager.isEnabled": true,
	    		            "animationManager.isEnabled": true
	    		          }
	    		        );    		      
	    		      
    		      // create the Overview and initialize it to show the main Diagram
    			  var myOverview =
    			    $$(go.Overview, "DiagramOverview",
    			      { observed: Diagram });
    			    myOverview.grid.visible = true;
	    			    
    		      function makePort(name, leftside) {
    		        var port = $$(go.Shape, "Rectangle",				//shape of "port"
    		          {
    		            fill: "LightSeaGreen", stroke: null,
    		            desiredSize: new go.Size(8, 8),					//size of "port"
    		            portId: name,  									//declare this object to be a "port"
                        toMaxLinks: 1,  								// don't allow more than one link into a port
    		            cursor: "pointer"  								// show a different cursor to indicate valid link point
    		          });
    		        var lab = $$(go.TextBlock, '',						// the name of the port is empty
    		          { 
    		        	stroke: "white", 								//port text color
    		        	font: "bold 6pt arial" 							//port text font
    		           }); 					
    		        var panel = $$(go.Panel, "Horizontal",
    		          { margin: new go.Margin(2, 0) });
    		        
    		        // set up the port/panel based on which side of the node it will be on
    		        if (leftside) {
    		          port.toSpot = go.Spot.Left;
    		          port.toLinkable = true;
    		          port.fill = 'orange';
    		          lab.margin = new go.Margin(1, 0, 0, 1);
    		          panel.alignment = go.Spot.TopLeft;
    		          panel.add(port);
    		          panel.add(lab);
    		        } else {
    		          port.fromSpot = go.Spot.Right;
    		          port.fromLinkable = true;
    		          lab.margin = new go.Margin(1, 1, 0, 0);
    		          panel.alignment = go.Spot.TopRight;
    		          panel.add(lab);
    		          panel.add(port);
    		        }
    		        return panel;
    		      }
	    		      
    		      function makeTemplate(typename, background, inports, outports) {
    		        var node = $$(go.Node, "Spot",
    		           { selectionAdorned: false },  
    		          $$(go.Panel, "Auto",
    		            { width: 70, height: 90,							//size of nodes
    		              minSize: new go.Size(50, 50)},							
    		            $$(go.Shape, "TriangleRight",						//shape of nodes
    		              {
    		                fill: background, stroke: null, strokeWidth: 0, 
    		                spot1: go.Spot.TopLeft, spot2: go.Spot.BottomRight
    		              }),
    		            $$(go.Panel, "Table",
    		            		{
    		            			alignment: go.Spot.Left,
    		            			margin: 5
    		            		}, 
    		            	$$(go.TextBlock, 
    		                {
    		                  row: 0,
    		                  maxSize: new go.Size(80, NaN),
    		                  stroke: "white",								//node value color
    		                  font: "bold 8pt sans-serif"					//node value font
    		                },
    		                new go.Binding("text", "name").makeTwoWay()
    		                ),
    		              $$(go.TextBlock, typename,
    		                {
    		                  row: 1,
    		                  maxSize: new go.Size(80, 40),
    		                  stroke: "white",								//node title color
    		                  font: "bold 5pt sans-serif"					//node title font
    		                }
    		                )
    		            )
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
    		        Diagram.nodeTemplateMap.set(typename, node);
    		      }
	    		      
    		      //making nodes with data binding (label, color, inports, outports) 
    		      makeTemplate("Workflow", "CadetBlue",
    		    	[makePort("IN", true)],									
        	        [makePort("OUT", false)]);
    		      makeTemplate("Data", "SteelBlue",
        	        [makePort("IN", true)],
        	        [makePort("OUT", false)]);

    		      Diagram.linkTemplate =
    		        $$(go.Link,
    		          {
    		            routing: go.Link.Normal,							//link routing style 
    		            corner: 5,
    		            relinkableFrom: true, 
    		            relinkableTo: true
    		          },
    		          $$(go.Shape, { stroke: "gray", strokeWidth: 2 }),
    		          $$(go.Shape, { stroke: "gray", fill: "gray", toArrow: "Standard" }),
    			      $$(go.TextBlock,                        
    			        new go.Binding("text", "value"), 					//link label data binding
    			        {font: "bold 6pt sans-serif"})						//link label font
    		        );
    		      
    		      	//create nodes using model data
    	            self.nodes.forEach(function(node) {
    		      		label = node.label;
    		      		name = node.name;
    		      		
    		      		switch(label) {
	    		      	  case "Workflow":
		    		      		color = 'CadetBlue';
		    		      	    break;
		    		      	  case "Data":
		    		      		color = 'SteelBlue';
		    		      	    break;
		    		      	case "Service":
		    		      		color = 'Teal';
		    		      		break;
		    		      	default:
		    		      		color = 'SteelBlue';
	    		      	}
    		      		
	    		      	//creating model for graph data 
	    		  		var graph_model_data = ({class: 'go.GraphLinksModel', nodeCategoryProperty: 'type', linkFromPortIdProperty: 'frompid', linkToPortIdProperty: 'topid', nodeDataArray: self.nodeDataArray, linkDataArray: self.linkDataArray});
	
	    		  		Diagram.model = go.Model.fromJson(JSON.stringify(graph_model_data));  //load()
	    		  		Diagram.model.isReadOnly = true;  									 // Disable adding or removing parts
    		      		
	    		  		if(label == "Workflow")
	    		  			makeTemplate(label, color,
    		      				[],
    		                    [makePort("OUT", false)]);	
	    		  		else
	    		  			makeTemplate(label, color,
	    		      			[makePort("IN", true)],
	    		                [makePort("OUT", false)]);	
      			  });
	            
		    }		
		}
        
        simplegojsGraph = new simpleGojsGraph(); 
      //=======================================
      //=============gojs graph end============
      //=======================================
        
        

	    