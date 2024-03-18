$(function() { // после загрузки страницы

    init();

});

function init() // тут привяжем обработчики и иное
{
     $('#resultbutton').on('click', function() { // к какому элементу привязывать отправку
       var formData =  new FormData($('#form-data')[0]);
       var url = '/doctoranalyzer/send_data';   // куда отправлять

       sendAjax(url, formData);
       return false;
    });
}

// выводим идентификатор


function sendAjax(url, data)
{
    $.ajax({ //  сам запрос
    type: 'POST',
    url: url,
    data: data, // данные которые передаём  серверу
    contentType: false,
    cache: false,
    processData: false,
    success: function(answer) {
          $('#result').after($('<h3>',{
          text: answer
          })
          );
        },

    });
}
