var $myForm = $(".my-ajax-form");
      $myForm.submit(function(event){
        event.preventDefault();
        event.stopImmediatePropagation();
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr("data-url") || window.location.href
  
        console.log($formData)
        console.log($thisURL)
        $.ajax({
          method: "POST",
          url: $thisURL,
          data: $formData,
          success: handleFormSuccess,
              error: handleFormError,
        })
        function handleFormSuccess(data, textStatus, jqXHR){
         console.log(data)
         console.log(textStatus)
         console.log(jqXHR)
         $myForm[0].reset(); // reset form data
         $('.alert-success'). addClass('alert'). html('submitted successfully!'). fadeIn().delay(4000).fadeOut()
     }
  
     function handleFormError(jqXHR, textStatus, errorThrown){
         console.log(jqXHR)
         console.log(textStatus)
         console.log(errorThrown)
          $('.alert-danger'). addClass('alert'). html('submitted successfully!'). fadeIn().delay(4000).fadeOut()
     }
      })