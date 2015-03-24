var global_username = '';


/*** After successful authentication, show user interface ***/

var showUI = function() {
	$('div#call').show();
	$('form#userForm').css('display', 'none');
	$('div#userInfo').css('display', 'inline');
	$('h3#login').css('display', 'none');
	$('span#username').text(global_username);
}


/*** If no valid session could be started, show the login interface ***/

var showLoginUI = function() {
	$('form#userForm').css('display', 'inline');
}

/*** Set up sinchClient ***/

sinchClient = new SinchClient({
	applicationKey: '7ecce9b0-b11d-48ef-9792-67a0467942d7',
	capabilities: {calling: true,video: true},
	startActiveConnection: true, /* NOTE: This is required if application is to receive calls / instant messages. */ 
	//Note: For additional loging, please uncomment the three rows below
	onLogMessage: function(message) {
		console.log(message);
	},
});


/*** Name of session, can be anything. ***/

var sessionName = 'sinchSessionWEB-' + sinchClient.applicationKey;


$.ajax({
		url: 'http://localhost:8000/live/login/',
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
		$('audio#ringback').prop("currentTime", 0);
		$('audio#ringback').trigger("play");

		//Report call stats
		$('div#callLog').append('<div id="stats">Ringing...</div>');
	},
	onCallEstablished: function(call) {
		$('audio#incoming').attr('src', call.incomingStreamURL);
		$('audio#ringback').trigger("pause");
		$('audio#ringtone').trigger("pause");

		clock.start(function() {
		// this (optional) callback will fire each time the clock flips
		});
		//Report call stats
		var callDetails = call.getDetails();
		$('div#callLog').append('<div id="stats">Answered at: '+(callDetails.establishedTime)+'</div>');
	},
	onCallEnded: function(call) {
		$('audio#ringback').trigger("pause");
		$('audio#ringtone').trigger("pause");
		$('audio#incoming').attr('src', '');

		$('button').removeClass('incall');
		$('button').removeClass('callwaiting');

		clock.stop();
		
		//Report call stats
		var callDetails = call.getDetails();
		$('div#callLog').append('<div id="stats">Ended: '+callDetails.endedTime+'</div>');
		$('div#callLog').append('<div id="stats">Duration (s): '+callDetails.duration+'</div>');
		$('div#callLog').append('<div id="stats">End cause: '+call.getEndCause()+'</div>');
		if(call.error) {
			$('div#callLog').append('<div id="stats">Failure message: '+call.error.message+'</div>');
		}
	}
}

/*** Set up callClient and define how to handle incoming calls ***/

var callClient = sinchClient.getCallClient();
callClient.initStream().then(function() { // Directly init streams, in order to force user to accept use of media sources at a time we choose
	$('div.frame').not('#chromeFileWarning').show();
}); 
var call;

callClient.addEventListener({
  onIncomingCall: function(incomingCall) {
	//Play some groovy tunes 
	$('audio#ringtone').prop("currentTime", 0);
	$('audio#ringtone').trigger("play");

	//Print statistics
	$('div#callLog').append('<div id="title">Incoming call from ' + incomingCall.fromId + '</div>');
	$('div#callLog').append('<div id="stats">Ringing...</div>');
	$('button').addClass('incall');

	//Manage the call object
    call = incomingCall;
    call.addEventListener(callListeners);
	$('button').addClass('callwaiting');
  }
});

$('button#answer').click(function(event) {
	event.preventDefault();

	if($(this).hasClass("callwaiting")) {
		clearError();

		try {
			call.answer();
			$('button').removeClass('callwaiting');
		}
		catch(error) {
			handleError(error);
		}
	}
});

/*** Make a new data call ***/

$('button#call').click(function(event) {
	event.preventDefault();

	if(!$(this).hasClass("incall") && !$(this).hasClass("callwaiting")) {
		clearError();

		$('button').addClass('incall');

		$('div#callLog').append('<div id="title">Calling ' + $('input#callUserName').val()+'</div>');

		console.log('Placing call to: ' + $('input#callUserName').val());
		call = callClient.callUser($('#calleeId').val());

		call.addEventListener(callListeners);
	}
});

/*** Hang up a call ***/

$('button#hangup').click(function(event) {
	event.preventDefault();

	if($(this).hasClass("incall")) {
		clearError();
		
		console.info('Will request hangup..');

		call && call.hangup();
	}
});




/*** Handle errors, report them and re-enable UI ***/

var handleError = function(error) {
	//Enable buttons
	$('button#createUser').prop('disabled', false);
	$('button#loginUser').prop('disabled', false);

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
	$('div#chromeFileWarning').show();
}

$('button').prop('disabled', false); //Solve Firefox issue, ensure buttons always clickable after load



