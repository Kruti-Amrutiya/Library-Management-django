var tableOutput = document.querySelector('.table-output');
var appTable = document.querySelector('.app-table');
var paginationContainer = document.querySelector('.pagination-container');
tableOutput.style.display = 'none';
var tbody = document.querySelector('.table-body')

$("#searchField").on('keyup', function(e){
    e.preventDefault();
    var searchText = $(this).val()
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val() 
    var searchValue = e.target.value;
    if(searchValue.trim().length > 0){
        $.ajax({  
            url: '/searchbox/',  
            method: 'POST',            
            data: {
                searchText: searchText,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function(data){   
                console.log(data)
                paginationContainer.style.display = 'none';
                appTable.style.display = 'none';
                tableOutput.style.display = 'block';
                tbody.innerHTML = '';
                if(data.length === 0){
                    tableOutput.innerHTML = 'No results founds';
                }
                else{
                    data.forEach((item) => {
                    tbody.innerHTML += `
                    <tr>
                        <td><a href="/bookdetail/${ item.id }">${ item.title }</a></td>
                        <td>${ item.author }</td>
                        <td>${ item.category}</td>
                        <td><img style="width: 90px; height: 90px;" src="${ item.book_img }" alt="${ item.title }"></td>
                        <td>${ item.total_copies_of_books }</td>
                        <td>${ item.available_copies_of_books }</td>
                    </tr>`;
                    });
                }
            },
        });
    }
    else{
        tableOutput.style.display = 'none';
        appTable.style.display = 'block';
        paginationContainer.style.display = 'block';
    }
});
