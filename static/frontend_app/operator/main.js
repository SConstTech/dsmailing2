
// window.global_token = null;
// window.returned_data = null;
// var x;
// (function () {
//     function init_variables(){
//     global_token = Cookies.get("csrftoken");
// }
// init_variables();
//
// })();
//
// function get_request(url, data){
// data.csrfmiddlewaretoken = global_token;
// $.post(
//     url,
//     data,
//     function(data, status){
//             if (status === 'success'){
//                 window.returned_data = JSON.parse(JSON.stringify(data));
//                 // console.log(returned_data);
//             }
//         }
//     );
// }
// x = get_request('/operator/get-clients', {}, global_token);
// console.log(x);
