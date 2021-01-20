    var ShowForm = function(){
      var btn = $(this);
      $.ajax({
        url: btn.attr('data-url'),
        type: 'get',
        dataType: 'json',
        beforeSend: function(){
          $('#modal-user').modal('show');
        },
        success: function(data){
          $('#modal-user .modal-content').html(data.html_form);
        }
      });
    }
    var SaveForm = function(e){
        var form = $(this);
          e.preventDefault();
          e.stopImmediatePropagation();
          $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data, textStatus, jqXHR){
              console.log(data)
              console.log(textStatus)
              console.log(jqXHR)
              var mainObj = data
              if(isEmpty(mainObj)) {
                $('#modal-user').modal('hide');
                ShowTable();
                $myForm[0].reset(); // reset form data
                $('.alert-success'). addClass('alert'). html('submitted successfully!'). fadeIn().delay(4000).fadeOut();
                ShowTable();
              } else {
                $.each(mainObj, function(index, value){
                $("#result").append(index + ": " + value + '<br>').addClass('alert').fadeIn().delay(4000).fadeOut();
                });
              }
            },
            error: function(data){
              console.log('not working');
            }
          });
        return false;
      }
  
  //update
  $("#tableData").unbind().on("click",".show-form-update",ShowForm);
  $("#modal-user").on("submit",".update-form",SaveForm)
 //delete
 $("#tableData").on("click",".show-form-delete",ShowForm);
 $("#modal-user").on("submit",".delete-form",SaveForm)
  
//Fetch Table
function ShowTable(){
  $.ajax({
    url: '/designation-table',
    dataType: 'json',
    type: 'GET',
    success: function(response){
      tableFromResponse(response);
      console.log("Data got successfully")
    },
    error: function(response){
      console.log("Enable to get data");
    }
  });
  function tableFromResponse(responseData) {
    var mainObj = JSON.parse(responseData.data);
    var count = 1;
    var urlu = "{% url 'dashboard-designation-update' 0 %}"
    var urld = "{% url 'dashboard-designation-delete' 0 %}"     
    var k = '<thead>';
          k+= '<tr>';                            
              k+= '<th>#</th>';                        
              k+= '<th>Designation</th>';                        
              k+= '<th colspan="2">Action</th>'                        
          k+= '</tr>';                        
      k+= '</thead>';
      k+= '<tfoot>';
          k+= '<tr>';                            
              k+= '<th>#</th>';                        
              k+= '<th>Designation</th>';                        
              k+= '<th colspan="2">Action</th>'                        
          k+= '</tr>';                        
      k+= '</tfoot>';
      k += '<tbody id="user-table">';                        
      for(i = 0;i < mainObj.length; i++){
          
          k+= '<tr>';
            k+= '<td>' + count + '</td>';
            k+= '<td>' + mainObj[i]["fields"]["designation"] + '</td>';
            k+='<td>';
              k+= '<button type="button" class="btn btn-warning show-form-update"   data-target="#modal-user" data-url=' + urlu.replace('0', mainObj[i]["pk"]) + '>';
                  k+= 'Edit';
              k+= '</button>';    
            k+= '</td>'; 
            k+='<td>';
              k+= '<button type="button" class="btn btn-danger show-form-delete"   data-target="#modal-user" data-url=' + urld.replace('0', mainObj[i]["pk"]) + '>';
                  k+= 'Delete';
              k+= '</button>';    
            k+= '</td>';     
            k+= '</tr>';
            count++;
        }
        k+='</tbody>';
        $('#tableData').html(k);
  }
}  
