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
page_id = getUrlParameter('id');
if (!page_id) {
  page_id = 1;
}
url = '/odes/ode_id'.replaceAll('ode_id', page_id);

$.get(url, function(data) {
  console.log(data);
  $('#random_ode').attr('href', 'index.html?id=ode_id'.replaceAll('ode_id', getRandomInt(305)));
  $('#title').text(data.title);
  $('#fulltext').text(data.full_text);
  $('#category').append('<li><a href=\'' + '#' + '\' class=\'btn-lg\'>' + data.p_class + '</a></li>')
  $('#category').append('<li><a href=\'' + '#' + '\' class=\'btn-lg\'>' + data.p_group + '</a></li>')
  if (data.p_subgroup) {
    $('#category').append('<li><a href=\'' + '#' + '\' class=\'btn-lg\'>' + data.p_subgroup + '</a></li>')
  }
  if (data.pre_title) {
    $('#left_ode').text('上一篇：' + data.pre_title).attr('href', 'index.html?id=ode_id'.replaceAll('ode_id', data.id - 1));
  }
  if (data.next_title) {
    $('#right_ode').text('下一篇：' + data.next_title).attr('href', 'index.html?id=ode_id'.replaceAll('ode_id', data.id + 1));
  }
})
