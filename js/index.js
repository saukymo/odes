String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

url="/odes-api/ode_id".replaceAll("ode_id", getUrlParameter('id'));

$.get(url, function(data){
	console.log(data);
	$('#title').text(data[0].title);
	$('#fulltext').text(data[0].full_text);
	$('#category').append("<li><a href=" + "#" + ">" + data[0].p_class + "</a></li>")
})