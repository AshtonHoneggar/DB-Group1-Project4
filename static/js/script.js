$(document).ready(function(){
    // $('#homeComponent').hide();
    $('#itHome').hide();
    $('#userHome').hide();
    $('#logoutComponent').hide();
    $('#Login').on('click', function() {
        $.ajax({
            url: '/login',
            data: $('#formLogin').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.auth === true){
                    localStorage.setItem('userdata', JSON.stringify(response.user));
                    $('#loginComponent').hide();
                    let user = JSON.parse(localStorage.getItem('userdata'));
                    console.log(user);
                    if (user.role.toUpperCase() === 'IT') {
                        $('#itHome').show();
                        getUnassignedTable();
                    }
                    else
                        $('#userHome').show();
                    populateUser();
                    getAssignedTable();
                }else{
                    $('#errorMessageLogin').text('Incorrect email and/or password.')
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('#Register').on('click', function() {
        $.ajax({
            url: '/register',
            data: $('#formRegister').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.registered === true){
                    $('#formRegister').trigger("reset");
                    $('#errorMessageReg').text('Registration successful!')
                }else{
                    $('#errorMessageReg').text('Registration failed. Try again.')
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('.CloseTicket').on('click', function() {
        $.ajax({
            url: '/closeTicket',
            data: $('#formClose').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if (response.closed === true) {
                     $('#formClose').trigger("reset");
                     $('#errorMessageClose').text('Ticket closed successfully!');
                      getAssignedTable();
                      getUnassignedTable();
                } else {
                    $('#errorMessageClose').text('Ticket closure failed. Try again.');
                } 
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    
    //For itHome
    $('#EventSubmit').on('click', function() {
        let user3 = JSON.parse(localStorage.getItem('userdata'));
        let tempForm1 = {
            username: user3.username,
            eventName: $('#eventName').val(),
            eventTime: $('#eventTime').val(),
            eventUrl: $('#eventUrl').val()
        };
    });
    //For userHome
    $('#submitTicket').on('click', function() {
          $.ajax({
            url: '/newTicket',
           data: $('#formSubmitTicket').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.newticket === true){
                    $('#formSubmitTicket').trigger("reset");
                    $('#errorMessageReg').text('Ticket submission successful!');
                    getAssignedTable();
                }else{
                    $('#errorMessageReg').text('Ticket submission failed. Try again.');
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }); 

    $('#AssignTicket').on('click', function() {
        $.ajax({
            url: '/assignTicket',
            data: $('#form-assign-ticket').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if (response.assign_it === true){
                    $('#form-assign-ticket').trigger("reset");
                    $('#errorMessageAssign').text('Ticket assign successful!');
                    getAssignedTable();
                    getUnassignedTable();
                }else{
                    $('#errorMessageAssign').text('Ticket assignment failed. Try again.');
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    
    $('#UnassignTicket').on('click', function() {
        $.ajax({
            url: '/unassignTicket',
            data: $('#formUnassign').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if (response.unassign_it === true){
                    $('#formUnassign').trigger("reset");
                    $('#errorMessageUnassign').text('Ticket unassign successful!');
                    getAssignedTable();
                    getUnassignedTable();
                }else{
                    $('#errorMessageUnassign').text('Ticket unassign failed. Try again.');
                }
            },
            error: function(error) {
                console.log(error);
            }
        })
    })


    function populateUser(){
        let user = JSON.parse(localStorage.getItem('userdata'));
        console.log(user);
        $('.greeting').append(user.firstName);
    }

    function getAssignedTable(){
        tempuser = localStorage.getItem('userdata');
        let parseduser;
        if (tempuser) {
            parseduser = JSON.parse(tempuser);
            let user = parseduser.username;
            $.ajax({
                url: '/getAssigned',
                data: {
                    temp: user
                },
                contentType: 'application/json',
                dataType: 'json',
                type: 'POST',
                success: function(response) {
                    // $('#PopulateTable').hide();
                    $('.eventTableBody').empty();
                    localStorage.setItem('userevents', JSON.stringify(response.assignedtickets));
                    response.assignedtickets.forEach(function(val){
                        $('.eventTableBody').append("<tr><td>" + val.id + "</td><td>" + val.date_opened + "</td><td>" + val.date_closed + "</td><td>" + val.status + "</td><td>" + val.reported_by + "</td><td>" + val.assigned_to + "</td><td>" + val.issue + "</td><td>" + val.user_comment + "</td><td>" + val.IT_comment + "</td></tr>");
                    });
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    }

    function getUnassignedTable(){
        tempuser = localStorage.getItem('userdata');
        let parseduser;
        if (tempuser) {
            parseduser = JSON.parse(tempuser);
            $.ajax({
                url: '/getUnassigned',
                type: 'POST',
                success: function(response) {
                    $('#unassignedTableBody').empty();
                    localStorage.setItem('userevents', JSON.stringify(response.unassignedtickets));
                    response.unassignedtickets.forEach(function(val){
                        $('#unassignedTableBody').append("<tr><td>" + val.id + "</td><td>" + val.date_opened + "</td><td>" + val.status + "</td><td>" + val.reported_by + "</td><td>" + val.issue + "</td><td>" + val.user_comment + "</td></tr>");
                    });
                },
                error: function(error){
                    console.log(error);
                }
            });
        }
    }
    
   $('#itLogoutButton').on('click', function() {
        $.ajax({
            url: '/logoutIT',
            data: $('#formITLogout').serialize(),
            type: 'POST',
            success: function(response) {
               console.log(response);
                if (response.isIT === true){
                    $('#logoutComponent').show(); 
                    $('#itLogout').show();
                    $('#userLogout').hide();
                     $('#itHome').hide();
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });     

    $('#userLogoutButton').on('click', function() {
        $.ajax({
            url: '/logoutUser',
            data: $('#formUserLogout').serialize(),
            type: 'POST',
            success: function(response) {
               console.log(response);
                 if (response.isUser === true){
                     $('#logoutComponent').show();
                     $('#userLogout').show();
                     $('#itLogout').hide();
                     $('#userHome').hide();
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }); 
    
    $('#SubmitLogout').on('click', function() {
        //redirect user to login page
        location.reload()
    }); 
       $('#Logout').on('click', function() {
        //redirect user to login page
        location.reload()
    });    

    
});