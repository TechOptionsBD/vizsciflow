function HandleModeViewModel() {
    var self = this;
    self.currentMode = ko.observable('wfMode');
    self.shouldProvElemShow = ko.observable(false);
    self.shouldGraphBtnShow = ko.observable(false);
    
    self.setMode = function(id) {
        if(self.currentMode() !== id){
            scriptViewModel.setPrevScript();
        }
        if(id == 'wfMode'){
            self.currentMode('wfMode')
            self.shouldProvElemShow(false)
            self.shouldGraphBtnShow(true)
            $("#provMode").removeClass("active-mode");
            $("#wfMode").addClass("active-mode");
            $("#exTabBiowl li:first a").tab('show').on('shown.bs.tab', function (param) {
                $("#exTabBiowl ul li:first").addClass('active');	
            });

            $('#liBrowserTab').show();
            $('#liOutput').show();
            $('#liProvenanceTab').hide();
            
            $('#liVisualTab').hide();
            $('#liMetadataTab').hide();
            $('#liFilterHistoryTab').hide();
            $('#liDataset').hide();

            $('#provplugins').hide();
        }
        else if(id == 'provMode'){
            self.currentMode('provMode')
            self.shouldProvElemShow(true)
            self.shouldGraphBtnShow(false)
            $("#wfMode").removeClass("active-mode");
            $("#provMode").addClass("active-mode");
            $("#exTabBiowl li:first a").tab('show').on('shown.bs.tab', function (param) {
                $("#exTabBiowl ul li:first").addClass('active');	
            });

            $('#liProvenanceTab').show();
            $('#liBrowserTab').hide();
            $('#liOutput').hide();

            $('#liVisualTab').hide();
            $('#liMetadataTab').hide();
            $('#liFilterHistoryTab').hide();
            $('#liDataset').hide();

            $('#provplugins').show();
        }
    }
    
    self.getMode = function(){
        return self.currentMode()
    }
}