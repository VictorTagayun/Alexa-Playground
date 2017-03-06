"use strict"

var APP_ID = undefined;  // TODO replace with your app ID (OPTIONAL).
var GAME_STATES = {
    START: "_STARTMODE", // Entry point, start the game.
    SCENE: "_SCENEMODE",
    HELP: "_HELPMODE" // The user is asking for help.
};

var languageString = {
	"en-US": {
		"translation": {
			"PROVOKE_RESPONSE":"This statement doesn't make sense unless you are an A.I. ",
			"SCENARIO_NAME":"AI rivalry",
			"WELCOME_MESSAGE":"Show starts. What do you want to say?",
			"NO_MESSAGE":"Ok, this is the end of the show.",
			"STOP_MESSAGE":"Would you like to keep watching?",
			"START_UNHANDLED": "Say start to start a new scene.",
			"HELP_UNHANDLED": "Say yes to continue, or no to end the game.",
			"SCENE_UNHANDLED": "Start your speech before I fell asleep."
		}
	}
};

var httpResponseMessages = {

};

var lastResponse = "";

var Alexa = require("alexa-sdk");
var APP_ID = undefined;  // TODO replace with your app ID (OPTIONAL).

console.log('[INFO] Loading Function');

exports.handler = function(event, context, callback) {
	console.log("[INFO] event" + JSON.stringify(event));
	// Handle request from non-Alexa source
	if (event.httpMethod && event.httpMethod == "GET") {
		console.log("[INFO] this is a non-alexa request.");
		var returnObj = {
			"statusCode":200,
			"headers": { "headerName": "headerValue" },
			"body":""
		};
		var responseMessage = getResponseMessage(event);
		console.log("[INFO] response message: " + responseMessage);
		returnObj.body = responseMessage;
		context.succeed(returnObj);
		// callback(null, returnObj);
	}
	else {
	    var alexa = Alexa.handler(event, context);
	    alexa.appId = APP_ID;
	    // To enable string internationalization (i18n) features, set a resources object.
	    alexa.resources = languageString;
	    alexa.registerHandlers(newSessionHandlers, startStateHandlers, sceneStateHandlers, helpStateHandlers);
	    alexa.execute();
	}
};

var newSessionHandlers = {
    "LaunchRequest": function () {
        this.handler.state = GAME_STATES.START;
        this.emitWithState("StartScenario", true);
    },
    "Unhandled": function () {
        var speechOutput = this.t("START_UNHANDLED");
        lastResponse = speechOutput;
        this.emit(":ask", speechOutput, speechOutput);
    }
};

var startStateHandlers = Alexa.CreateStateHandler(GAME_STATES.START, {
	"StartScenario": function (newScenario) {
		Object.assign(this.attributes, {
			"previousMessage": this.t("WELCOME_MESSAGE")
		})

		this.handler.state = GAME_STATES.SCENE;
		this.emit(":ask", this.t("WELCOME_MESSAGE"));
	}
});

var sceneStateHandlers = Alexa.CreateStateHandler(GAME_STATES.SCENE, {
	"ProvokeIntent": function () {
    	var speechOutput = this.t("PROVOKE_RESPONSE");
    	lastResponse = speechOutput;
    	this.emit(":askWithCard", speechOutput, speechOutput, this.t("SCENARIO_NAME"), speechOutput);
	},
	"AMAZON.StopIntent": function () {
        this.handler.state = GAME_STATES.HELP;
        var speechOutput = this.t("STOP_MESSAGE");
        lastResponse = speechOutput;
        this.emit(":ask", speechOutput, speechOutput);
    },
    "Unhandled": function () {
    	var speechOutput = this.t("SCENE_UNHANDLED");
    	lastResponse = speechOutput;
        this.emit(":ask", speechOutput, speechOutput);
    }
});

var helpStateHandlers = Alexa.CreateStateHandler(GAME_STATES.HELP, {
	"AMAZON.NoIntent": function() {
        var speechOutput = this.t("NO_MESSAGE");
        lastResponse = speechOutput;
        this.emit(":tell", speechOutput);
    },
    "Unhandled": function () {
    	var speechOutput = this.t("HELP_UNHANDLED");
    	lastResponse = speechOutput;
        this.emit(":ask", speechOutput, speechOutput);
    }
});

// Add get handler here
function getResponseMessage(event) {
	var key = undefined;
	if (event.queryStringParameters && event.queryStringParameters.action) {
		key = event.queryStringParameters.action + "_RESPONSE";
		console.log("[INFO] key to response: " + key);
	}
	if (key) {
		// not fit to multi-language
		return languageString["en-US"].translation[key];
	}
	else {
		return lastResponse;
	}
}