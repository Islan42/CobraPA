jQuery( function(){
    /*$.ajax({
        url: '/api/',
        method: 'GET',
        dataType: 'json'
    }).done(function(data){
        $('#carrossel-home').empty();

        $.each(data, function(i, cidade){
            $('#carrossel-home').append(
                `<li>${cidade.nome} - <a href="/cidade/${cidade.id}">Comprar</a></li>`
            )
        });
    });
    */

    const carrosselLista = $('#carrossel-home-lista li').toArray()
    const carrosselControle = $('#carrossel-home-controle span').toArray()

    $.each(carrosselControle, function(i, controle){
        $(controle).on('click', function(event){
            $.each(carrosselLista, function(i, item){
                $(item).addClass('hidden')
            })

            $(carrosselLista[i]).removeClass('hidden')
        })
    });
})
