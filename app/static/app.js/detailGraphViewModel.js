function detailGojsGraph()
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
    		            	layeringOption: go.LayeredDigraphLayout.LayerLongestPathSource
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
    		        var port = $$(go.Shape, "Rectangle",					//shape of "port"
    		          {
    		            fill: "gray",
    		            desiredSize: new go.Size(8, 8),					//size of "port"
    		            //portId: name,  									//declare this object to be a "port"
                        toMaxLinks: 1,  								// don't allow more than one link into a port
    		            cursor: "pointer"  								// show a different cursor to indicate valid link point
    		          });
    		        var lab = $$(go.TextBlock, name,						// the name of the port is empty
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
    		          port.portId = name;
    		          port.fill = 'orange';
    		          lab.margin = new go.Margin(1, 0, 0, 1);
    		          panel.alignment = go.Spot.TopLeft;
    		          panel.add(port);
    		          panel.add(lab);
    		        } else {
    		          port.fromSpot = go.Spot.Right;
    		          port.fromLinkable = true;
    		          port.portId = name;
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
    		            { width: 120, height: 90,								//size of nodes
    		              minSize: new go.Size(100, 70), maxSize: new go.Size(150,10)},							
    		            $$(go.Shape, "RoundedRectangle",						//shape of nodes
    		              {
    		                fill: background, stroke: null, strokeWidth: 0, 
    		                spot1: go.Spot.TopLeft, spot2: go.Spot.BottomRight
    		              }),
    		            $$(go.Panel, "Table",
    		              $$(go.TextBlock, 
    		                {
    		                  row: 0,
    		                  margin: 3,
    		                  maxSize: new go.Size(80, NaN),
    		                  stroke: "white",								//node value color
    		                  font: "bold 9pt sans-serif"					//node value font
    		                },
    		                new go.Binding("text", "name").makeTwoWay()
    		                ),
    		                //add an extra blank row in middle 
   		                	$$(go.TextBlock, 
    		                {
   		                	  text : "",
    		                  row: 1,
    		                  margin: 3,
    		                  maxSize: new go.Size(80, NaN)
    		                }),
    		              $$(go.TextBlock, typename,
    		                {
    		                  row: 2,
    		                  margin: 3,
    		                  maxSize: new go.Size(80, 40),
    		                  stroke: "white",								//node title color
    		                  font: "bold 6pt sans-serif"					//node title font
    		                },
    		                //new go.Binding("text", "name").makeTwoWay()),
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
    		    	[makePort("IN", true)],									//no inport
        	        [makePort("OUT", false)]);
        	      makeTemplate("Data", "SteelBlue",
        	        [makePort("IN 1", true)],
        	        [makePort("OUT 1", false)]);
//        	      makeTemplate("Service", "Teal",
//        	        [makePort("IN", true)],
//        	        [makePort("OUT", false)]);
//    		      makeTemplate("Output", "forestgreen",
//    		    	[makePort("", true)],
//    		        []);													//no outport

    		      Diagram.linkTemplate =
    		        $$(go.Link,
    		          {
    		            routing: go.Link.AvoidsNodes,							//link routing style 
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
    		      
    		      	var outport = 0;
    		      	var inport = 0;
    	            var listOfInputPorts = [];
    	            var listOfOutputPorts = [];
    	            
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
    		      		
    		      		self.linkDataArray.forEach(function(link) {
    		      		//input port definition
    		      			if(node.id == link.to){
		      					inport++;
		      					inport_lable = 'IN ' + inport;
		      					link.topid = inport_lable;
		      					var aNewInputPort = makePort(inport_lable,true);
		      	                listOfInputPorts.push(aNewInputPort);
		      				}
        		      		//output port definition
        		      			if(node.id == link.from){
        		      				outport++;
        		      				outport_lable = 'OUT ' + outport;
        		      				link.frompid = outport_lable;
        		      				var aNewOutputPort = makePort(outport_lable,false);
    		      	                listOfOutputPorts.push(aNewOutputPort);
        		      			}
        		      		});    		      		
    		      		    		      		
	    		      	//creating model for graph data 
	    		  		var graph_model_data = ({class: 'go.GraphLinksModel', nodeCategoryProperty: 'type', linkFromPortIdProperty: 'frompid', linkToPortIdProperty: 'topid', nodeDataArray: self.nodeDataArray, linkDataArray: self.linkDataArray});
	
	    		  		Diagram.model = go.Model.fromJson(JSON.stringify(graph_model_data));  //load()
	    		  		Diagram.model.isReadOnly = true;  									 // Disable adding or removing parts
    		      		
    		      		makeTemplate(label, color,
    		      				listOfInputPorts,
    		                    listOfOutputPorts);
    		      		
    		      		listOfInputPorts = [];
	                    listOfOutputPorts = [];
    		      		outport = 0; 
    		      		inport = 0;
      			  });   	    	
    		    }		
    		}
        
			detailgojsGraph = new detailGojsGraph(); 
      //=======================================
      //=============gojs graph end============
      //=======================================
       
      //=======================================
      //=============D3 graph starts===========
      //=======================================			
			
			function D3Graph()
		    {
		    	var self = this;
		   		self.width = 960;
		   		self.height = 500;
		   		self.colors = d3.scaleOrdinal(d3.schemeCategory10);

				self.show = function(rels) {
					self.nodes = [];
					self.links = [];
					
					rels.forEach(function(rel){
						var exists = self.nodes.filter(function(n)
							{
								return rel.source.id === n.id; 
							});
						if (exists.length == 0)
							self.nodes.push(rel.source);
						
						exists = self.nodes.filter(function(n)
							{
								return rel.target.id === n.id; 
							});
						if (exists.length == 0)
							self.nodes.push(rel.target);
					});
					
					rels.forEach(function(rel) { 
					    var sourceNode = self.nodes.filter(function(n) { return n.id === rel.source.id; })[0];
					    var targetNode = self.nodes.filter(function(n) { return n.id === rel.target.id; })[0];
					    self.links.push({source: sourceNode, target: targetNode, value: rel.type});
					});
					
//		 			// Compute the distinct nodes from the links.
//		 	   		self.links.forEach(function(link) {
//		 	   		  link.source = self.nodes[link.source] || (self.nodes[link.source] = link.source);
//		 	   		  link.target = self.nodes[link.target] || (self.nodes[link.target] = link.target);
//		 	   		});
					
					self.width = $("#graph").width();
					self.height = $("#graph").height();
					
//		 			var force = d3.layout.force()
//		 	   		    .nodes(d3.values(self.nodes))
//		 	   		    .links(self.links)
//		 	   		    .size([self.width, self.height])
//		 	   		    .linkDistance(60)
//		 	   		    .charge(-300)
//		 	   		    .friction(0.9)
//		 	   		    .on("tick", self.tick)
//		 	   		    .start();
					
					if (self.svg !== undefined && self.svg != null) {
						d3.select("svg")
							.selectAll("*")
							.remove();
						d3.select("svg").remove();
					}
					
					self.svg = d3.select("#graph").append("svg")
		   		    	.attr("width", self.width)
		   		    	.attr("height", self.height);
					
					self.svg.append('defs').append('marker')
				        .attrs({'id':'arrowhead',
				            'viewBox':'-0 -5 10 10',
				            'refX':13,
				            'refY':0,
				            'orient':'auto',
				            'markerWidth':13,
				            'markerHeight':13,
				            'xoverflow':'visible'})
				        .append('svg:path')
				        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
				        .attr('fill', '#999')
				        .style('stroke','none');
					
					self.simulation = d3.forceSimulation()
				        .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(100).strength(1))
				        .force("charge", d3.forceManyBody())
				        .force("center", d3.forceCenter(self.width / 2, self.height / 2));
					
					self.link = self.svg.selectAll(".link")
		            .data(self.links)
		            .enter()
		            .append("line")
		            .attr("class", "link")
		            .attr('marker-end','url(#arrowhead)');
						
			        self.link.append("title")
			            .text(function (d) {return d.type;});
		        	
					self.edgepaths = self.svg.selectAll(".edgepath")
			            .data(self.links)
			            .enter()
			            .append('path')
			            .attrs({
			                'class': 'edgepath',
			                'fill-opacity': 0,
			                'stroke-opacity': 0,
			                'id': function (d, i) {return 'edgepath' + i}
			            })
		            	.style("pointer-events", "none");

		        	self.edgelabels = self.svg.selectAll(".edgelabel")
			            .data(self.links)
			            .enter()
			            .append('text')
			            .style("pointer-events", "none")
			            .attrs({
			                'class': 'edgelabel',
			                'id': function (d, i) {return 'edgelabel' + i},
			                'font-size': 10,
			                'fill': '#aaa'
			            });

			        self.edgelabels.append('textPath')
			            .attr('xlink:href', function (d, i) {return '#edgepath' + i})
			            .style("text-anchor", "middle")
			            .style("pointer-events", "none")
			            .attr("startOffset", "50%")
			            .text(function (d) {return d.value});
			        
			       self.node = self.svg.selectAll(".node")
				        .data(self.nodes)
				        .enter()
				        .append("g")
				        .attr("class", "node")
				   	    .on("mouseover", self.mouseover)
					    .on("mouseout", self.mouseout)
				        .call(d3.drag()
				                .on("start", self.dragstarted)
				                .on("drag", self.dragged)
				                //.on("end", self.dragended)
				        );

				    self.node.append("circle")
				        .attr("r", 5)
				        .style("fill", function (d, i) {return self.colors(i);})
				
				    self.node.append("title")
				        .text(function (d) {return d.id;});
				
				    self.node.append("text")
				        .attr("dy", -3)
				        .text(function (d) {return d.name+":"+d.label;});

				    self.simulation
		   				.nodes(self.nodes)
		            	.on("tick", self.tick);

			        self.simulation.force("link")
			            .links(self.links);
				}
		   		
		   		self.tick = function() {
		   			self.link
		            .attr("x1", function (d) {return d.source.x;})
		            .attr("y1", function (d) {return d.source.y;})
		            .attr("x2", function (d) {return d.target.x;})
		            .attr("y2", function (d) {return d.target.y;});

		        	self.node.attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

			        self.edgepaths.attr('d', function (d) {
			            return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
			        });

			        self.edgelabels.attr('transform', function (d) {
			            if (d.target.x < d.source.x) {
			                /* var bbox = this.getBBox();
			                rx = bbox.x + bbox.width / 2;
			                ry = bbox.y + bbox.height / 2; */
			                rx=0;
			                ry=0;
			                return 'rotate(180 ' + rx + ' ' + ry + ')';
			            }
			            else {
			                return 'rotate(0)';
			            }
			        });
		  	  	}

		   		self.mouseover = function() {
		   		  d3.select(this).select("circle").transition()
		   		      .duration(750)
		   		      .attr("r", 16);
		   		}

		   		self.mouseout = function() {
		   		  d3.select(this).select("circle").transition()
		   		      .duration(750)
		   		      .attr("r", 8);
		   		}
		   		
		   		self.dragstarted = function(d) {
		   	        if (!d3.event.active)
		   	        	self.simulation.alphaTarget(0.3).restart()
		   	        d.fx = d.x;
		   	        d.fy = d.y;
		   	    }

		   	    self.dragged = function(d) {
		   	        d.fx = d3.event.x;
		   	        d.fy = d3.event.y;
		   	    }
		    }
		    
		    d3graph = new D3Graph();
		    
	      //=======================================
	      //=============D3 graph end==============
	      //=======================================			
