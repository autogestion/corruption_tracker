

$(document).ready(function () {

    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#claim_form").submit(function(event){
        add_claim(event);
    });

    $("#org_form").submit(function(event){
        add_organization(event)
    });


    $("#about").on('click', function() { 
        $("#claims_list").html(' <span id="close_claims_list">x</span><div id="legend"><h3>Подолати корупцію в один клік.</h3>' +
        '<p>Кожен громадянин України має важелі впливу на корупційну діяльність. Це - особиста відповідальність та публічність.</p>' +
        '<p>Відповідальність спонукає зробити вибір підтримувати чи не підтримувати корупцію. А публічність нівелює прояви корупції, якщо вибір було зроблено на користь її подолання.</p>' +
        '<p>Питання стоїть лише за інструментом, який поєднає особисте прагнення здолати корупцію в Україні з максимальним розголосом актів корупційної діяльності.</p>' +
        '<p>Система є таким інструментом. Основний акцент у ній зроблено на можливості зафіксувати корупційну діяльність на місці її вчинення. Далі акцент зміщується у публічну сферу. Розголос набуває форми структурованої мапи корупції.</p>' +
        '<p>Так, Система є найпростішим способом вести облік корупційної активності. А універсальність її даних відкриває можливість боротьби з корупцією на всіх рівнях: від рівня особистого невдоволення до рівня громадянського суспільства чи законодавчих ініціатив.</p>' +
        '<p>А потрібно лише зробити один клік "Повідомити".</p>' +       
        '<h3>Проекту потрібні</h3><ul><li>Javascript UI Developer</li><li>Mobile Developer (iOS, Android)</li><li>Та інші.</li></ul>' +
        '<h3>Долучится до розробки можна</h3><ul>' +
            '<li>на GitHup => <a href="https://github.com/autogestion/corruption_tracker" target="_blank">Corruption tracker</a></li>' +
            '<li>у Facebook спільноті => <a href="https://www.facebook.com/activecorruptiontracking/" target="_blank">Система учёта коррупционной активности</a></li>' +
           '</ul></div>')
    });

    $('#close_claims_list').on('click', function() { 
        $("#claims_list").html('')
    });


});