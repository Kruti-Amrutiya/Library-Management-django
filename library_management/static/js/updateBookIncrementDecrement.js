$("#increment").click(function(e){
    e.preventDefault();
    $.ajax({  
        url: '/increment_copies_of_books/',  
        method: 'POST',            
        data: {
            book_id: template.book_id,
            csrfmiddlewaretoken: template.csrf_token,
        },
        success: function(data){   
            $("#id_total_copies_of_books").val(data.copies_of_book);
            $("#id_available_copies_of_books").val(data.available_copies);
        },
        error: function(data){
            alert("Error occured");
        }
    });
});
$("#decrement").click(function(e){
    e.preventDefault();
    $.ajax({  
        url: '/decrement_copies_of_books/',
        method: 'POST',            
        data: {
            book_id: template.book_id,
            csrfmiddlewaretoken: template.csrf_token,
        },
        success: function(data){
            $("#id_total_copies_of_books").val(data.copies_of_book);
            $("#id_available_copies_of_books").val(data.available_copies);
        },
        error: function(data){
            alert("Error occured");
        }
    });
});