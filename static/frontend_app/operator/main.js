
var global_token;
var x;
var returned_data;

(function (){
    function init_variables(){
        global_token = Cookies.get("csrftoken");
    }

    function get_request(url, data, token){
        data.csrfmiddlewaretoken = global_token;
        $.post(
            url,
            data,
            function(data, status){
                    if (status === 'success'){
                        returned_data = JSON.parse(JSON.stringify(data));
                        console.log(returned_data);
                    }
                }
            );
    }
    // call init functions
    init_variables();
    x = get_request('/operator/get-clients', {}, global_token);
    //
    // console.log('асд');
    // console.log(global_token);

})();
// populateClientList();
