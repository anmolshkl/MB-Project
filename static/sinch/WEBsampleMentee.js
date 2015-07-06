
var global_username = '';
var callType = 1;
var owner;
var callEstablished = false;
/*** After successful authentication, show user interface ***/

var showUI = function() {
	$('div.call').show();

}

/*** Set up sinchClient ***/

sinchClient = new SinchClient({
	applicationKey: '7ecce9b0-b11d-48ef-9792-67a0467942d7',
	capabilities: {calling: true, video: false},
	startActiveConnection: true, /* NOTE: This is required if application is to receive calls / instant messages. */
	//Note: For additional logging, please uncomment the three rows below
	onLogMessage: function(message) {
		console.log(message);
	}
});

/***  PERIODIC AJAX CALLS TO GET LAST SEEN ***/
    setInterval(function() {
        // Update last seen only when not in a call -> saves from unnecessary requests to server
        if(callEstablished === false && $(".calleeId").first().val() !== '') {
            $.ajax({
                url: '/mentor/check-mentor-status/',
                type: 'get',
                data: {'id': $(".calleeId").val().slice(4)}, //ASSUMPTION!!!! ONLY ONE REQUEST CAN BE SEEN BY MENTEE AT A TIME
                success: function(data) {
                    if(data.status == "online") {
                        $(".btn-danger").hide();
                        $("button.call").removeClass('hidden');
                        $(".status").html("online");
                        $(".unavailableMsg").hide();
                    } else if(data.status == "offline"){
                        $(".status").html("offline");
                        $(".btn-danger").show();
                        $("button.call").hide();
                    }
                },
                failure: function() {
                    alert("Updating last seen failed");
                }
        });
    }
    },1000*10);


/*** Name of session, can be anything. ***/

var sessionName = 'sinchSessionWEB-' + sinchClient.applicationKey;


$.ajax({
		url: '/live/login/',
		type: 'get',
		dataType: 'json',
		success: function(ticket) {
			sinchClient.start(ticket, function() {
				//On success, show the UI
				showUI();
				//Store session & manage in some way (optional)
				localStorage[sessionName] = JSON.stringify(sinchClient.getSession());
			}).fail(handleError);
		}
	});

/*** Define listener for managing calls ***/

var callListeners = {
	onCallProgressing: function(call) {
		$('audio.ringback').prop("currentTime", 0);
		$('audio.ringback').trigger("play");

		//Report call
		$('.callLog').append('<div class="stats">Ringing...</div>');
	},
	onCallEstablished: function(call) {
        callEstablished = true;

		$('audio.incoming').attr('src', call.incomingStreamURL);
		$('audio.ringback').trigger("pause");
		$('audio.ringtone').trigger("pause");
        if(callType == 3) {
            owner.find('#incomingVideo').show();
            owner.find('#incomingVideo').attr('src', call.incomingStreamURL);
        }
		clock.start(function() {
		// this (optional) callback will fire each time the clock flips
		})
		//Report call stats
		var callDetails = call.getDetails();
		owner.find('.callLog').append('<div class="stats">Answered at: '+(callDetails.establishedTime)+'</div>');
	},
	onCallEnded: function(call) {
        callEstablished = false;
        if(callType == 3) {
            //owner.find('#outgoingVideo').attr('src', '');
		    owner.find('#incomingVideo').attr('src', '');
        }
		$('audio.ringback').trigger("pause");
		$('audio.ringtone').trigger("pause");
		$('audio.incoming').attr('src', '');

		$('button').removeClass('incall');
		$('button').removeClass('callwaiting');

		clock.stop();

		//Report call stats
		var callDetails = call.getDetails();
        var est_time = callDetails.establishedTime + "";
        var end_time = callDetails.endedTime + "";
        alert("End cause="+call.getEndCause());
        $.ajax({
            url: "/user/submit-callLog/",
            type: "post",
            data: {'csrfmiddlewaretoken': csrf, 'request_id': owner.parent().find('.request_id').val(),
                    'est_time': est_time.split(" ")[4], 'end_time': end_time.split(" ")[4],
                    'end_cause': call.getEndCause(), 'duration': callDetails.duration},
            dataType: "json",
            success: function(data) {
                owner.fadeOut();
                owner.parent().find(".clock").fadeOut();
                owner.parent().find(".callLog").fadeOut();
                owner.parent().find(".hangup").fadeOut();
                owner.parent().find(".call-title").fadeOut();
                if(callType == 3) {
                    owner.parent().find('#incomingVideo').remove();
                    //owner.parent().find('#outgoingVideo').remove();
                }
                if(call.getEndCause() == "HUNG_UP") {
                    owner.parent().find(".call-title").html("Your feedback is valuable to us!");
                    setInterval(function() {
                        owner.parent().find(".call-title").fadeIn();
                        owner.parent().find(".form-feedback").animate({
                            left: $(".form-feedback").parent().width() / 2 - $(".form-feedback").width() / 2 + 20
                        }, 200);
                    }, 1000);
                    owner.parent().find('.form-feedback').append('<input type="hidden" class="request_id" value=" '+ data.request_id + ' " > ');
                } else {
                    //give a gap of 1sec to let the call log, timer etc fade out
                    setInterval(function() {
                        owner.parent().find(".call-title").html("Well, this is embarrassing...");
                        owner.parent().find(".call-title").fadeIn();
                        owner.parent().find(".call-title").append("<br><br><button class='btn btn-primary btn-large' onClick='window.location.reload()'><i class='fa fa-rotate-right'></i> Refresh</button>");
                    },1000);
                }
            },
            failure: function() {
                alert("failed to submit call log details");
            }
        });

		$('div.callLog').append('<div class="stats">Ended: '+callDetails.endedTime+'</div>');
		$('div.callLog').append('<div class="stats">Duration (s): '+callDetails.duration+'</div>');
		$('div.callLog').append('<div class="stats">End cause: '+call.getEndCause()+'</div>');
		if(call.error) {
			$('div.callLog').append('<div id="stats">Failure message: '+call.error.message+'</div>');
		}



	}
}

/*** Set up callClient and define how to handle incoming calls ***/

var callClient = sinchClient.getCallClient();
callClient.initStream().then(function() { // Directly init streams, in order to force user to accept use of media sources at a time we choose
	$('div.frame').not('.chromeFileWarning').show();
});
var call;




/*** Make a new data call ***/

$('.morph-button').on('click','button.call',function(event) {
	event.preventDefault();

	if(!$(this).hasClass("incall") && !$(this).hasClass("callwaiting")) {
		clearError();

		$(this).parent().find('button').addClass('incall');
        clock = new FlipClock($(this).parent().find('.clock'), {
            autoStart: false,
            clockFace: 'MinuteCounter'
        });
        owner = $(this);
        $.ajax({
            url: '/user/call-valid/', //Returns weather call is valid or not
            type: 'GET',
            data: {'request_id': owner.parent().find('.request_id').val()},
            success: function(data) {
                if(data == "True") {
                    owner.parent().find(".callLog").show();
                    owner.parent().find(".call-title").html("Relax while we place your call...");
                    owner.parent().find(".clock").show();
                    owner.parent().find('.form-feedback').css({'left': '-500px' });
                    owner.parent().find('.hangup').show();
                    owner.parent().find(".callLog").html("");
                    owner.parent().find('.icon-close').addClass('close-alert');
                    /*** Prevent Closing of overlay when in call ***/
                    $('.close-alert').click(function(e) {
                        e.preventDefault();
                    });
                    owner.parent().find('.callLog').append('<div class="title">Calling <b>' + owner.parent().find('.callUserName').val()+'</b></div>');

                    console.log('Placing call to: ' + owner.parent().find('.callUserName').val());
                    callType = parseInt(owner.parent().find(".callType").val());
                    if(callType == 1 || callType == 3) {
                        // Video or web call
                        call = callClient.callUser(owner.parent().find(".calleeId").val());
                    }
                    else if(callType == 2) {
                        // phone call
                        call = callClient.callPhoneNumber($(this).parent().find('.number'));
                    }

                    //Remove video element if call Type is not 3
                    if(callType != 3) {
                        //owner.parent().find('#outgoingVideo').hide();
                        owner.parent().find('#incomingVideo').hide();

                    }
                    call.addEventListener(callListeners);
                }
                else {
                    owner.parent().find('.call-overlay-content').html("<h2>Sorry but you have completed this call!</h2>");
                    setInterval(function(){ location.reload(); },2000);
                }
            }
        });

	}
});

/*** Hang up a call ***/

$('button.hangup').click(function(event) {
	event.preventDefault();

	if($(this).hasClass("incall")) {
		clearError();

		console.info('Will request hangup..');

		call && call.hangup();

        //remove close-alert class from close icon
        $(this).parent().find('.icon-close').removeClass('close-alert');
	}
});




/*** Handle errors, report them and re-enable UI ***/

var handleError = function(error) {
	//Show error
	$('div.error').text(error.message);
	$('div.error').show();
}

/** Always clear errors **/
var clearError = function() {
	$('div.error').hide();
}

/** Chrome check for file - This will warn developers of using file: protocol when testing WebRTC **/
if(location.protocol == 'file:' && navigator.userAgent.toLowerCase().indexOf('chrome') > -1) {
	$('div.chromeFileWarning').show();
}

$('button').prop('disabled', false); //Solve Firefox issue, ensure buttons always clickable after load


$('.refresh').click(function() {
    location.reload();
});