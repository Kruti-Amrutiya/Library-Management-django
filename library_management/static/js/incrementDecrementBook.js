$("#increment").click(function(e){
    e.preventDefault();
    $.ajax({  
        url: '/copies_of_books/',  
        method: 'POST',            
        data: {
            action: 'increment',
            book_id: template.book_id,
            csrfmiddlewaretoken: template.csrf_token,
        },
        success: function(data){   
            $("#id_total_copies_of_books").html(data.copies_of_books);
            $("#id_available_copies_of_books").html(data.available_copies);
        },
    });
});
$("#decrement").click(function(e){
    e.preventDefault();
    $.ajax({  
        url: '/copies_of_books/',
        method: 'POST',            
        data: {
            action: 'decrement',
            book_id: template.book_id,
            csrfmiddlewaretoken: template.csrf_token,
        },
        success: function(data){
            $("#id_total_copies_of_books").html(data.copies_of_books);
            $("#id_available_copies_of_books").html(data.available_copies);
        },
        
    });
});