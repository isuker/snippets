
function test() {
	var o = new ActiveXObject("WScript.Shell"); 
	o.exec("open_ra.py"); 
}

function exec (command) { 
	window.oldOnError = window.onerror; 
	window._command = command; 
	window.onerror = function (err) { 
		if (err.indexOf('utomation') != -1) { 
			alert('命令' + window._command + ' 已经被用户禁止！'); 
			return true; 
		} 
		else return false; 
	}; 
	var wsh = new ActiveXObject('WScript.Shell'); 
	if (wsh) 
		wsh.Run(command); 
	window.onerror = window.oldOnError; 
} 

function host_check(hostname){
	$("div[id='" + hostname + "'] .services").html("Updating ...");
	$.ajax({
		  url: $SCRIPT_ROOT + "/_check_port",
		  data: {hostname: hostname},
		  dataType:"html"
		}).done(function(data){
		  $("div[id='" + hostname + "'] .services").html(data);
		});
}

function show_access(hostname){
	var val = $("div[id='" + hostname + "'] .show").text();
	if(val == "Show Access"){
		 $("div[id='" + hostname + "'] .show").text("Hide Access");
	}else{
		$("div[id='" + hostname + "'] .show").text("Show Access");
	}
	$("div[id='" + hostname + "'] .pwd_info").toggle();
}

function addlink(){
	apprise("Add your link with format Name:Url", 
			{'input':true}, 
			function(data){
				var str = $.trim(data); 
				alert(data);
			});
}


$(function(){
	$.ajax({
		  url: $SCRIPT_ROOT + "/message",
		  data: {},
		  dataType:"html"
		}).done(function(data){
			if($.trim(data)){
				$('#messages').sticky(data);
			}
		});
	
	$.ajax({
		  url: $SCRIPT_ROOT + "/admin/listssh",
		  data: {},
		  dataType:"html"
		}).done(function(data){
			$("#toolbox").html(data);
		});
	
	$.ajax({
		  url: $SCRIPT_ROOT + "/admin/listlink",
		  data: {},
		  dataType:"html"
		}).done(function(data){
			$("#linkbox").html(data);
		});
	$("div.ringheader:odd").css("background-color", "#D7E6F0");
	//$("div.ring:even").css("background-color","#F6FAFC");
});



