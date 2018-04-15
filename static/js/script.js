$(document).ready(function(){
    $('#homeComponent').hide();
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
                    // getTable();
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

    $('#PopulateTable').on('click', function() {
        getTable();
    });
    //For itHome
    $('#EventSubmit').on('click', function() {
        let user3 = JSON.parse(localStorage.getItem('userdata'));
        let tempForm1 = {
            email: user3.email,
            eventName: $('#eventName').val(),
            eventTime: $('#eventTime').val(),
            eventUrl: $('#eventUrl').val()
        };
    });
    //For userHome
    $('#EventSubmit2').on('click', function() {
        let user4 = JSON.parse(localStorage.getItem('userdata'));
        let tempForm2 = {
            email: user4.email,
            eventName: $('#eventName2').val(),
            eventTime: $('#eventTime2').val(),
            eventUrl: $('#eventUrl2').val()
        };
        console.log(tempForm1);
        console.log(tempForm2);
        $.ajax({
            url: '/newEvent',
            data: tempForm1,
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(response.newEventStatus === true){
                    console.log('Event submit successful');
                    $('#eventName').val("");
                    $('#eventTime').val("");
                    $('#eventUrl').val("");
                    $('#errorMessageNewEvent').text('Success!');
                    $('#eventTableBody').append("<tr><td>" + tempForm.eventName + "</td><td>" + tempForm.eventTime + "</td><td>" + tempForm.eventUrl + "</td></tr>");
                }else{
                    $('#errorMessageNewEvent').text('Event submittal failed. Try again.');
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


    function getTable(){
        tempuser = localStorage.getItem('userdata');
        let parseduser;
        if (tempuser) {
            parseduser = JSON.parse(tempuser);
            let email = parseduser.email;
            console.log(email);
            $.ajax({
                url: '/getTickets',
                data: {
                    temp: email
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