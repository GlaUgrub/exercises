(function (window) {
    var ajaxUtils = {};

    function createRequestObject() {
        if (window.XMLHttpRequest) {
            return new XMLHttpRequest();
        }
        else {
            window.alert("No support for AJAX!!!!");
        }
    }

    function sendGetRequest(URL, userDefinedHandler) {
        var request = createRequestObject();

        // set callback for request status changes
        request.onreadystatechange =
            function() {
                stateChangeHandler(request, userDefinedHandler);
            }


        request.open("GET", URL, true); // "true" is to make async request
        request.send(null); //"null" means no body in request
    }

    // calls user-defined callback only when
    // request processing is successfully completed
    function stateChangeHandler(request, userDefinedHandler) {
        if ((request.readyState == 4) &&
            (request.status == 200)) {
            var defaults = JSON.parse(request.responseText);
            userDefinedHandler(defaults);
        }
    }

    ajaxUtils.sendGetRequest = sendGetRequest;
    window.ajaxUtils = ajaxUtils;

})(window);
