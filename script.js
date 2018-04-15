$(document).ready(function(){
    // $('#homeComponent').hide();
    $('#itHome').hide();
    $('#userHome').hide();
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
                    if (user.role.toUpperCase() === 'IT')
                        $('#itHome').show();
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
                    $('#myForm').trigger("reset");
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
    $('#EventSubmit').on('click', function() {
        $.ajax({
            url: '/newEvent',
            data: $('#newEventForm').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    // Repurpose as Update Table?
    $('#PopulateTable').on('click', function() {
        getTable();
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
                    $('#myForm').trigger("reset");
                    $('#errorMessageReg').text('Ticket submission successful!')
                }else{
                    $('#errorMessageReg').text('Ticket submission failed. Try again.')
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }); 

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
            console.log(user);
            $.ajax({
                url: '/getAssigned',
                data: {
                    temp: user
                },
                contentType: 'application/json',
                dataType: 'json',
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    // $('#PopulateTable').hide();
                    $('#eventTableBody').empty();
                    localStorage.setItem('userevents', JSON.stringify(response.events));
                    response.events.forEach(function(val){
                        $('#eventTableBody').append("<tr><td>" + val.eventName + "</td><td>" + val.eventTime + "</td><td>" + val.eventUrl + "</td></tr>");
                    })
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    }
});