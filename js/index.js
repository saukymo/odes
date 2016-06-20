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

function getRandomInt(x) {
  return Math.floor(Math.random() * x) + 1;
}

url="/odes-api/ode_id".replaceAll("ode_id", getUrlParameter('id'));

$.get(url, function(data){
	console.log(data);
	$('#random_ode').attr("href", "/odes/index.html?id=ode_id".replaceAll("ode_id", getRandomInt(305)));
	$('#title').text(data[1].title);
	$('#fulltext').text(data[1].full_text);
	$('#category').append("<li><a href=\"" + "#" + "\" class=\"btn-lg\">" + data[1].p_class + "</a></li>")
	$('#category').append("<li><a href=\"" + "#" + "\" class=\"btn-lg\">" + data[1].p_group + "</a></li>")
	if (data[1].p_subgroup)
	{
		$('#category').append("<li><a href=\"" + "#" + "\" class=\"btn-lg\">" + data[1].p_subgroup + "</a></li>")
	}
	$('#left_ode').text("上一篇：" + data[0].title).attr("href", "/odes/index.html?id=ode_id".replaceAll("ode_id", data[0].id));
	$('#right_ode').text("下一篇：" + data[2].title).attr("href", "/odes/index.html?id=ode_id".replaceAll("ode_id", data[2].id));
})