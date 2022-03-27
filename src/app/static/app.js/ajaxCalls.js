
    var AjaxCalls = function(username, password) {
    	var self = this;
    	self.username = username;
    	self.password = password;
    	
    	self.form = function(uri, method, data, asyncParam = true) {
            var request = {
                    url: uri,
                    type: method,
                    async: asyncParam,
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: data,
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("Authorization", 
                            "Basic " + btoa(self.username + ":" + self.password));
                    },
                    error: function(jqXHR) {
                        showXHRText(jqXHR);
                    }
                };
                return $.ajax(request);
        }
        
        self.simple = function(uri, method, data, asyncParam = true) {
            var request = {
                    url: uri,
                    type: method,
                    async: asyncParam,
                    contentType: "application/json",
                    accepts: "application/json",
                    cache: false,
                    dataType: 'json',
                    data: data,
//                     beforeSend: function (xhr) {
//                         xhr.setRequestHeader("Authorization", 
//                             "Basic " + btoa(self.username + ":" + self.password));
//                     },
                    error: function(jqXHR, a, b) {
                        showXHRText(jqXHR);
                    }
                };
                return $.ajax(request);
        }

		self.simpleByteData = function(uri, method, data, asyncParam = true) {
            var request = {
                    url: uri,
                    type: method,
                    async: asyncParam,
                    contentType: "application/json",
                    accepts: "application/json",
                    cache: false,
                    data: data,
					dataType : 'binary',
					responseType: 'arraybuffer',
                    error: function(jqXHR, textStatus, error) {
                    	showXHRText(jqXHR);
                    }
             };
             return $.ajax(request);
        }
		
		self.simpleByteDataTest = function(uri, method, data, asyncParam = true, imageType) {
			
			var oReq = new XMLHttpRequest();
			oReq.open(method, uri + "?" + data, true);
			oReq.responseType = "arraybuffer";
			var imgType = "image/" + imageType;
			var url = "";
			oReq.onload = function(oEvent) {
				if (this.status == 200) {
					var arrayBuffer = oReq.response;
				
					// if you want to access the bytes:
					var byteArray = new Uint8Array(arrayBuffer);

					// If you want to use the image in your DOM:
					
					var blob = new Blob([arrayBuffer], {type: imgType});
					var url = URL.createObjectURL(blob);
					//someImageElement.src = url;
				}
			};

			oReq.send();
		}
    }
    